# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import bstack1l1ll11l1ll_opy_, bstack1lll11l1l1_opy_, bstack1111llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l11l1ll111_opy_, TestHookState, bstack11lll1ll1l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1lllllll11l_opy_, bstack11lll11111l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11ll1l1111l_opy_ = [bstack1l1111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᛚ"), bstack1l1111l_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᛛ"), bstack1l1111l_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢᛜ"), bstack1l1111l_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࠤᛝ"), bstack1l1111l_opy_ (u"ࠤࡳࡥࡹ࡮ࠢᛞ")]
bstack11lll11l1ll_opy_ = bstack11lll11111l_opy_()
bstack11ll111ll11_opy_ = bstack1l1111l_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥᛟ")
bstack11lll1l11l1_opy_ = {
    bstack1l1111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡎࡺࡥ࡮ࠤᛠ"): bstack11ll1l1111l_opy_,
    bstack1l1111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡖࡡࡤ࡭ࡤ࡫ࡪࠨᛡ"): bstack11ll1l1111l_opy_,
    bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡍࡰࡦࡸࡰࡪࠨᛢ"): bstack11ll1l1111l_opy_,
    bstack1l1111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡄ࡮ࡤࡷࡸࠨᛣ"): bstack11ll1l1111l_opy_,
    bstack1l1111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡈࡸࡲࡨࡺࡩࡰࡰࠥᛤ"): bstack11ll1l1111l_opy_
    + [
        bstack1l1111l_opy_ (u"ࠤࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡲࡦࡳࡥࠣᛥ"),
        bstack1l1111l_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᛦ"),
        bstack1l1111l_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩ࡮ࡴࡦࡰࠤᛧ"),
        bstack1l1111l_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢᛨ"),
        bstack1l1111l_opy_ (u"ࠨࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠣᛩ"),
        bstack1l1111l_opy_ (u"ࠢࡤࡣ࡯ࡰࡴࡨࡪࠣᛪ"),
        bstack1l1111l_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢ᛫"),
        bstack1l1111l_opy_ (u"ࠤࡶࡸࡴࡶࠢ᛬"),
        bstack1l1111l_opy_ (u"ࠥࡨࡺࡸࡡࡵ࡫ࡲࡲࠧ᛭"),
        bstack1l1111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᛮ"),
    ],
    bstack1l1111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡪࡰ࠱ࡗࡪࡹࡳࡪࡱࡱࠦᛯ"): [bstack1l1111l_opy_ (u"ࠨࡳࡵࡣࡵࡸࡵࡧࡴࡩࠤᛰ"), bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࡸ࡬ࡡࡪ࡮ࡨࡨࠧᛱ"), bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡹࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤᛲ"), bstack1l1111l_opy_ (u"ࠤ࡬ࡸࡪࡳࡳࠣᛳ")],
    bstack1l1111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡧࡴࡴࡦࡪࡩ࠱ࡇࡴࡴࡦࡪࡩࠥᛴ"): [bstack1l1111l_opy_ (u"ࠦ࡮ࡴࡶࡰࡥࡤࡸ࡮ࡵ࡮ࡠࡲࡤࡶࡦࡳࡳࠣᛵ"), bstack1l1111l_opy_ (u"ࠧࡧࡲࡨࡵࠥᛶ")],
    bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡈ࡬ࡼࡹࡻࡲࡦࡆࡨࡪࠧᛷ"): [bstack1l1111l_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨᛸ"), bstack1l1111l_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤ᛹"), bstack1l1111l_opy_ (u"ࠤࡩࡹࡳࡩࠢ᛺"), bstack1l1111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥ᛻"), bstack1l1111l_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨ᛼"), bstack1l1111l_opy_ (u"ࠧ࡯ࡤࡴࠤ᛽")],
    bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡕࡸࡦࡗ࡫ࡱࡶࡧࡶࡸࠧ᛾"): [bstack1l1111l_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧ᛿"), bstack1l1111l_opy_ (u"ࠣࡲࡤࡶࡦࡳࠢᜀ"), bstack1l1111l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡠ࡫ࡱࡨࡪࡾࠢᜁ")],
    bstack1l1111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡶࡺࡴ࡮ࡦࡴ࠱ࡇࡦࡲ࡬ࡊࡰࡩࡳࠧᜂ"): [bstack1l1111l_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤᜃ"), bstack1l1111l_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࠧᜄ")],
    bstack1l1111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡐࡲࡨࡪࡑࡥࡺࡹࡲࡶࡩࡹࠢᜅ"): [bstack1l1111l_opy_ (u"ࠢ࡯ࡱࡧࡩࠧᜆ"), bstack1l1111l_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᜇ")],
    bstack1l1111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡒࡧࡲ࡬ࠤᜈ"): [bstack1l1111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᜉ"), bstack1l1111l_opy_ (u"ࠦࡦࡸࡧࡴࠤᜊ"), bstack1l1111l_opy_ (u"ࠧࡱࡷࡢࡴࡪࡷࠧᜋ")],
}
_11ll111llll_opy_ = set()
class bstack1l111l111l_opy_(bstack1l1l1111111_opy_):
    bstack11ll1l11ll1_opy_ = bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࠨᜌ")
    bstack11lll111l1l_opy_ = bstack1l1111l_opy_ (u"ࠢࡊࡐࡉࡓࠧᜍ")
    bstack11lll1l1l11_opy_ = bstack1l1111l_opy_ (u"ࠣࡇࡕࡖࡔࡘࠢᜎ")
    bstack11ll11lllll_opy_: Callable
    bstack11ll1llllll_opy_: Callable
    def __init__(self, bstack1l11lll1l1l_opy_, bstack1l1l11ll111_opy_):
        super().__init__()
        self.bstack1l1111ll1l1_opy_ = bstack1l1l11ll111_opy_
        if os.getenv(bstack1l1111l_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡑ࠴࠵࡞ࠨᜏ"), bstack1l1111l_opy_ (u"ࠥ࠵ࠧᜐ")) != bstack1l1111l_opy_ (u"ࠦ࠶ࠨᜑ") or not self.is_enabled():
            return
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111111ll_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111ll11l_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1111lllll_opy_((event, state), self.bstack11ll11l1l1l_opy_)
        bstack1l11lll1l1l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.POST), self.bstack11ll11l1l11_opy_)
        self.bstack11ll11lllll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack11ll111l1l1_opy_(bstack1l111l111l_opy_.bstack11lll111l1l_opy_, self.bstack11ll11lllll_opy_)
        self.bstack11ll1llllll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack11ll111l1l1_opy_(bstack1l111l111l_opy_.bstack11lll1l1l11_opy_, self.bstack11ll1llllll_opy_)
        self.bstack11ll1ll1111_opy_ = builtins.print
        builtins.print = self.bstack11ll1l1llll_opy_()
        self._11lll111l11_opy_()
    def _11lll111l11_opy_(self):
        bstack1l1111l_opy_ (u"ࠧࠨࠢࡑࡣࡷࡧ࡭ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠱ࡷࡾࡴࡣࡠࡣࡳ࡭࠳ࡖࡡࡨࡧ࠱ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡵࡱࠣࡧࡦࡶࡴࡶࡴࡨࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠢࡩࡳࡷࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡽࡨࡦࡰࠣࡸࡪࡹࡴࡴࠢࡵࡹࡳࠦ࡯࡯ࠢࡱࡳࡳ࠳ࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥ࡯࡮ࡧࡴࡤࡷࡹࡸࡵࡤࡶࡸࡶࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠩࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤ࡫ࡧ࡬ࡴࡧࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯ࡶࡨࡶࡨ࡫ࡰࡵࡵࠣࡦࡾࡺࡥࡴࠢࡵࡩࡹࡻࡲ࡯ࡧࡧࠤࡧࡿࠠࡱࡣࡪࡩ࠳ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠪࠬ࠰ࠥࡨࡡࡴࡧ࠹࠸࠲࡫࡮ࡤࡱࡧࡩࡸࠦࡴࡩࡧࡰ࠰ࠥࡧ࡮ࡥࠌࠣࠤࠥࠦࠠࠡࠢࠣࡷࡪࡴࡤࡴࠢࡷ࡬ࡪࡳࠠࡷ࡫ࡤࠤ࡬ࡘࡐࡄࠢࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩࡋࡶࡦࡰࡷࠤ࠭ࡱࡩ࡯ࡦࡀࡘࡊ࡙ࡔࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘ࠮࠲ࠠࡤࡱࡱࡷ࡮ࡹࡴࡦࡰࡷࠤࡼ࡯ࡴࡩࠌࠣࠤࠥࠦࠠࠡࠢࠣ࡬ࡴࡽࠠࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡣࡰ࡯ࡰࡥࡳࡪࡳࠡࡣࡵࡩࠥ࡮ࡡ࡯ࡦ࡯ࡩࡩࠦࡩ࡯ࠢࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩ࠭࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᜒ")
        try:
            from playwright.sync_api import Page as bstack11lll1111l1_opy_
        except ImportError:
            return
        if getattr(bstack11lll1111l1_opy_.screenshot, bstack1l1111l_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡱࡣࡷࡧ࡭࡫ࡤࠨᜓ"), False):
            return
        bstack11lll11lll1_opy_ = bstack11lll1111l1_opy_.screenshot
        dispatcher = self
        def bstack_page_screenshot(bstack11ll1ll1l_opy_, **kwargs):
            bstack11lll1l11ll_opy_ = bstack11lll11lll1_opy_(bstack11ll1ll1l_opy_, **kwargs)
            try:
                if not bstack1lllllll11l_opy_():
                    import base64
                    bstack11lll111lll_opy_ = base64.b64encode(bstack11lll1l11ll_opy_).decode(bstack1l1111l_opy_ (u"ࠧࡶࡶࡩ࠱࠽᜔࠭"))
                    bstack11ll1lll1ll_opy_ = TestFramework.bstack11ll1ll111l_opy_()
                    if bstack11ll1lll1ll_opy_:
                        bstack1l111ll1ll_opy_ = next(
                            (t for t in bstack11ll1lll1ll_opy_ if TestFramework.bstack1l1lll1l111_opy_(t, TestFramework.bstack11llllll111_opy_)),
                            None,
                        )
                        if bstack1l111ll1ll_opy_:
                            entry = bstack11lll1ll1l_opy_(TestFramework.KIND_SCREENSHOT, bstack11lll111lll_opy_)
                            dispatcher.bstack1llll111ll_opy_(bstack1l111ll1ll_opy_, [entry])
            except Exception:
                pass
            return bstack11lll1l11ll_opy_
        bstack_page_screenshot._bstack_patched = True
        bstack11lll1111l1_opy_.screenshot = bstack_page_screenshot
    def is_enabled(self) -> bool:
        return True
    def _11lll11l11l_opy_(self, f: TestFramework) -> bool:
        bstack1l1111l_opy_ (u"ࠣࠤࠥࡇ࡭࡫ࡣ࡬ࠢ࡬ࡪࠥࡺࡨࡦࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯ࡳࠡࡘࡤࡲ࡮ࡲ࡬ࡢࡒࡼࡸ࡭ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࠬࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧ࠮࠴ࠢࠣࠤ᜕")
        return (hasattr(f, bstack1l1111l_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤࡔࡁࡎࡇࠪ᜖")) and f.FRAMEWORK_NAME == bstack1l1111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ᜗")) or \
               (hasattr(f, bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸ࠭᜘")) and bstack1l1111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭᜙") in f.bstack1l1l1lll111_opy_)
    def bstack11ll11l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_supported = f.bstack11ll11l111l_opy_() or f.bstack11ll1l11l1l_opy_() or self._11lll11l11l_opy_(f)
        if is_supported and instance:
            bstack11ll11ll1l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1l1ll1ll111_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack11l11l1l_opy_ = datetime.now()
                entries = f.bstack11lll1l111l_opy_(instance, bstack1l1ll1ll111_opy_)
                if entries:
                    self.bstack1llll111ll_opy_(instance, entries)
                    instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨ᜚"), datetime.now() - bstack11l11l1l_opy_)
                    f.bstack11ll1llll1l_opy_(instance, bstack1l1ll1ll111_opy_)
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥ᜛"), datetime.now() - bstack11ll11ll1l1_opy_)
                return # bstack11ll11llll1_opy_ not send this event with the bstack11ll1l11l11_opy_ bstack11ll1l1ll11_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11ll111l11l_opy_)
            ):
                f.bstack111l1llll1_opy_(instance, bstack1l111l111l_opy_.bstack11ll1l11ll1_opy_, True)
                return # bstack11ll11llll1_opy_ not send this event bstack11ll1l1l1l1_opy_ bstack11ll1l111ll_opy_
            elif (
                f.bstack1ll1111l1l1_opy_(instance, bstack1l111l111l_opy_.bstack11ll1l11ll1_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11ll111l11l_opy_)
            ):
                self.bstack11ll11l1l1l_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack11l11l1l_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack11ll11l111l_opy_():
                bstack11ll1llll11_opy_ = sorted(
                    filter(lambda x: x.get(bstack1l1111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦ᜜"), None), data.pop(bstack1l1111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ᜝"), {}).values()),
                    key=lambda x: x[bstack1l1111l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨ᜞")],
                )
                data.update({bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᜟ"): bstack11ll1llll11_opy_})
            elif f.bstack11ll1l11l1l_opy_():
                bstack11lll11ll1l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1l1111l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᜠ"), None), data.pop(bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᜡ"), {}).values()),
                    key=lambda x: x[bstack1l1111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᜢ")],
                )
                data.update({bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࡥ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᜣ"): bstack11lll11ll1l_opy_})
            if bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_ in data:
                data.pop(bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_)
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᜤ"), datetime.now() - bstack11l11l1l_opy_)
            bstack11l11l1l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack11lll111111_opy_)
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᜥ"), datetime.now() - bstack11l11l1l_opy_)
            if TestFramework.bstack11llllll111_opy_ in data:
                self.bstack11ll1l1ll11_opy_(instance, bstack1l1ll1ll111_opy_, event_json=event_json)
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᜦ"), datetime.now() - bstack11ll11ll1l1_opy_)
    def bstack1l1111111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
        bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack1l11lll11l_opy_.value)
        self.bstack1l1111ll1l1_opy_.bstack11ll11l1ll1_opy_(instance, f, bstack1l1ll1ll111_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1111ll1l1_opy_.bstack11ll1l1l111_opy_(instance, f, bstack1l1ll1ll111_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࠦࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡜ࡽࢀࡡࠥࢁࡽ࡝ࡰࡾࢁࠧᜧ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack11ll1l11lll_opy_ data not ready for robot-playwright at the time of bstack1l1111111ll_opy_, so bstack11ll1l1l1ll_opy_ will send bstack11ll1l11lll_opy_ event in bstack1l1111ll11l_opy_ for robot-playwright
            self.bstack11ll1l1ll1l_opy_(f, instance, req)
        bstack11lll1111_opy_.end(EVENTS.bstack1l11lll11l_opy_.value, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᜨ"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᜩ"), status=True, failure=None, test_name=None)
    def bstack1l1111ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1111l1l1_opy_(instance, self.bstack1l1111ll1l1_opy_.bstack11ll1l1lll1_opy_, False):
            try:
                req = self.bstack1l1111ll1l1_opy_.bstack11ll1l1l111_opy_(instance, f, bstack1l1ll1ll111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l1111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴࠡࡩࡨࡸࡤࡩࡢࡵࡡࡨࡺࡪࡴࡴࠡࡨࡤ࡭ࡱ࡫ࡤ࠻ࠢ࡞ࡿࢂࡣࠠࡼࡿ࡟ࡲࢀࢃࠢᜪ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack11ll1l1ll1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack11ll1ll1l1l_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11ll1l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧᜫ"))
            return
        bstack11l11l1l_opy_ = datetime.now()
        try:
            r = self.bstack11l1ll1lll_opy_.TestSessionEvent(req)
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦᜬ"), datetime.now() - bstack11l11l1l_opy_)
            f.bstack111l1llll1_opy_(instance, self.bstack1l1111ll1l1_opy_.bstack11ll1l1lll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᜭ") + str(r) + bstack1l1111l_opy_ (u"ࠧࠨᜮ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᜯ") + str(e) + bstack1l1111l_opy_ (u"ࠢࠣᜰ"))
            traceback.print_exc()
            raise e
    def bstack11ll11l1l11_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        _driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        _11ll11l11l1_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l1l111l111_opy_.bstack1l1111l111l_opy_(method_name):
            return
        if f.bstack1l1111l11l1_opy_(*args) == bstack1l1l111l111_opy_.bstack11ll11lll1l_opy_:
            bstack11ll11ll1l1_opy_ = datetime.now()
            screenshot = result.get(bstack1l1111l_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢᜱ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥᜲ"))
                return
            bstack1l111ll1ll_opy_ = self.bstack11ll1ll11l1_opy_(instance)
            if bstack1l111ll1ll_opy_:
                entry = bstack11lll1ll1l_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1llll111ll_opy_(bstack1l111ll1ll_opy_, [entry])
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦᜳ"), datetime.now() - bstack11ll11ll1l1_opy_)
            else:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤ᜴").format(instance.ref()))
        event = {}
        bstack1l111ll1ll_opy_ = self.bstack11ll1ll11l1_opy_(instance)
        if bstack1l111ll1ll_opy_:
            self.bstack11ll1ll11ll_opy_(event, bstack1l111ll1ll_opy_)
            if event.get(bstack1l1111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥ᜵")):
                self.bstack1llll111ll_opy_(bstack1l111ll1ll_opy_, event[bstack1l1111l_opy_ (u"ࠨ࡬ࡰࡩࡶࠦ᜶")])
            else:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦ᜷"))
    @measure(event_name=EVENTS.bstack11ll111ll1l_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack1llll111ll_opy_(
        self,
        bstack1l111ll1ll_opy_: bstack1l11l1ll111_opy_,
        entries: List[bstack11lll1ll1l_opy_],
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l111l1l111_opy_)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᜸").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111ll1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111ll1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111ll1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack1l11111l11l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11ll11l1lll_opy_)
            log_entry.uuid = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11llllll111_opy_)
            log_entry.test_framework_state = bstack1l111ll1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᜹"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ᜺"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll11l1111_opy_
                log_entry.file_path = entry.bstack111111_opy_
        def bstack11ll11lll11_opy_():
            bstack11l11l1l_opy_ = datetime.now()
            try:
                self.bstack11l1ll1lll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l111ll1ll_opy_.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ᜻"), datetime.now() - bstack11l11l1l_opy_)
                elif entry.kind == TestFramework.bstack11ll1ll1ll1_opy_:
                    bstack1l111ll1ll_opy_.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤ᜼"), datetime.now() - bstack11l11l1l_opy_)
                else:
                    bstack1l111ll1ll_opy_.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥ᜽"), datetime.now() - bstack11l11l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ᜾") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11lll11_opy_)
    @measure(event_name=EVENTS.bstack11lll1l1l1l_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack11ll1l1ll11_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l1l111_opy_)
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᜿").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l11111l11l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11ll11l1lll_opy_)
        req.test_framework_state = bstack1l1ll1ll111_opy_[0].name
        req.test_hook_state = bstack1l1ll1ll111_opy_[1].name
        started_at = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11lll1111ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack11lll111111_opy_)).encode(bstack1l1111l_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᝀ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack11ll11lll11_opy_():
            bstack11l11l1l_opy_ = datetime.now()
            try:
                self.bstack11l1ll1lll_opy_.TestFrameworkEvent(req)
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡦࡸࡨࡲࡹࠨᝁ"), datetime.now() - bstack11l11l1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᝂ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1lll11l1l_opy_.enqueue(bstack11ll11lll11_opy_)
    def bstack11ll1ll11l1_opy_(self, instance: bstack1l1ll11l1ll_opy_):
        bstack11ll1lll1ll_opy_ = TestFramework.bstack1l1ll111111_opy_(instance.context)
        for t in bstack11ll1lll1ll_opy_:
            bstack11ll1l11111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(t, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
            if not bstack1lllllll11l_opy_() and len(bstack11ll1l11111_opy_) == 0:
                bstack11ll1l11111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(t, bstack1l11l11111l_opy_.bstack11ll1lll11l_opy_, [])
            if any(instance is d[1] for d in bstack11ll1l11111_opy_):
                return t
    def bstack11ll11ll11l_opy_(self, message):
        self.bstack11ll11lllll_opy_(message + bstack1l1111l_opy_ (u"ࠧࡢ࡮ࠣᝃ"))
    def log_error(self, message):
        self.bstack11ll1llllll_opy_(message + bstack1l1111l_opy_ (u"ࠨ࡜࡯ࠤᝄ"))
    def bstack11ll111l1l1_opy_(self, level, original_func):
        def bstack11ll111lll1_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1l1111l_opy_ (u"ࠢࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥࠣᝅ") in message or bstack1l1111l_opy_ (u"ࠣ࡝ࡖࡈࡐࡉࡌࡊ࡟ࠥᝆ") in message or bstack1l1111l_opy_ (u"ࠤ࡞࡛ࡪࡨࡄࡳ࡫ࡹࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠨᝇ") in message:
                        return return_value
                    bstack11ll1lll1ll_opy_ = TestFramework.bstack11ll1ll111l_opy_()
                    if not bstack11ll1lll1ll_opy_:
                        return return_value
                    bstack1l111ll1ll_opy_ = next(
                        (
                            instance
                            for instance in bstack11ll1lll1ll_opy_
                            if TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11llllll111_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111ll1ll_opy_:
                        return return_value
                    entry = bstack11lll1ll1l_opy_(TestFramework.bstack11lll11llll_opy_, message, level)
                    self.bstack1llll111ll_opy_(bstack1l111ll1ll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack11ll111lll1_opy_
    def bstack11ll1l1llll_opy_(self):
        def bstack11ll1lll111_opy_(*args, **kwargs):
            try:
                self.bstack11ll1ll1111_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l1111l_opy_ (u"ࠪࠤࠬᝈ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l1111l_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧᝉ") in message:
                    return
                bstack11ll1lll1ll_opy_ = TestFramework.bstack11ll1ll111l_opy_()
                if not bstack11ll1lll1ll_opy_:
                    return
                bstack1l111ll1ll_opy_ = next(
                    (
                        instance
                        for instance in bstack11ll1lll1ll_opy_
                        if TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11llllll111_opy_)
                    ),
                    None,
                )
                if not bstack1l111ll1ll_opy_:
                    return
                entry = bstack11lll1ll1l_opy_(TestFramework.bstack11lll11llll_opy_, message, bstack1l111l111l_opy_.bstack11lll111l1l_opy_)
                self.bstack1llll111ll_opy_(bstack1l111ll1ll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack11ll1ll1111_opy_(bstack1l1ll1l11l1_opy_ (u"ࠧࡡࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠡࡎࡲ࡫ࠥࡩࡡࡱࡶࡸࡶࡪࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡦࡿࠥᝊ"))
                except:
                    pass
        return bstack11ll1lll111_opy_
    def bstack11ll1ll11ll_opy_(self, event: dict, instance=None) -> None:
        global _11ll111llll_opy_
        levels = [bstack1l1111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᝋ"), bstack1l1111l_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᝌ")]
        bstack11lll11l1l1_opy_ = bstack1l1111l_opy_ (u"ࠣࠤᝍ")
        if instance is not None:
            try:
                bstack11lll11l1l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡹ࡮ࡪࠠࡧࡴࡲࡱࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢᝎ").format(e))
        bstack11lll111ll1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᝏ")]
                bstack11lll11l111_opy_ = os.path.join(bstack11lll11l1ll_opy_, (bstack11ll111ll11_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack11lll11l111_opy_):
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡯ࡱࡷࠤࡵࡸࡥࡴࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡔࡦࡵࡷࠤࡦࡴࡤࠡࡄࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᝐ").format(bstack11lll11l111_opy_))
                    continue
                file_names = os.listdir(bstack11lll11l111_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack11lll11l111_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _11ll111llll_opy_:
                        self.logger.info(bstack1l1111l_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥᝑ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack11ll1ll1lll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack11ll1ll1lll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᝒ"):
                                entry = bstack11lll1ll1l_opy_(
                                    kind=bstack1l1111l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᝓ"),
                                    message=bstack1l1111l_opy_ (u"ࠣࠤ᝔"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11ll11l1111_opy_=file_size,
                                    bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤ᝕"),
                                    bstack111111_opy_=os.path.abspath(file_path),
                                    bstack11l1l111ll_opy_=bstack11lll11l1l1_opy_
                                )
                            elif level == bstack1l1111l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢ᝖"):
                                entry = bstack11lll1ll1l_opy_(
                                    kind=bstack1l1111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ᝗"),
                                    message=bstack1l1111l_opy_ (u"ࠧࠨ᝘"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11ll11l1111_opy_=file_size,
                                    bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ᝙"),
                                    bstack111111_opy_=os.path.abspath(file_path),
                                    bstack11ll111l111_opy_=bstack11lll11l1l1_opy_
                                )
                            bstack11lll111ll1_opy_.append(entry)
                            _11ll111llll_opy_.add(abs_path)
                        except Exception as bstack11lll1l1111_opy_:
                            self.logger.error(bstack1l1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨ᝚").format(bstack11lll1l1111_opy_))
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢ᝛").format(e))
        event[bstack1l1111l_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢ᝜")] = bstack11lll111ll1_opy_
class bstack11lll111111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11ll1l111l1_opy_ = set()
        kwargs[bstack1l1111l_opy_ (u"ࠥࡷࡰ࡯ࡰ࡬ࡧࡼࡷࠧ᝝")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack11ll11ll111_opy_(obj, self.bstack11ll1l111l1_opy_)
def bstack11ll111l1ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack11ll11ll111_opy_(obj, bstack11ll1l111l1_opy_=None, max_depth=3):
    if bstack11ll1l111l1_opy_ is None:
        bstack11ll1l111l1_opy_ = set()
    if id(obj) in bstack11ll1l111l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11ll1l111l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack11ll11l11ll_opy_ = TestFramework.bstack11lll11ll11_opy_(obj)
    bstack11ll1l1l11l_opy_ = next((k.lower() in bstack11ll11l11ll_opy_.lower() for k in bstack11lll1l11l1_opy_.keys()), None)
    if bstack11ll1l1l11l_opy_:
        obj = TestFramework.bstack11ll1lll1l1_opy_(obj, bstack11lll1l11l1_opy_[bstack11ll1l1l11l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1111l_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢ᝞")):
            keys = getattr(obj, bstack1l1111l_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣ᝟"), [])
        elif hasattr(obj, bstack1l1111l_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣᝠ")):
            keys = getattr(obj, bstack1l1111l_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤᝡ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1111l_opy_ (u"ࠣࡡࠥᝢ"))}
        if not obj and bstack11ll11l11ll_opy_ == bstack1l1111l_opy_ (u"ࠤࡳࡥࡹ࡮࡬ࡪࡤ࠱ࡔࡴࡹࡩࡹࡒࡤࡸ࡭ࠨᝣ"):
            obj = {bstack1l1111l_opy_ (u"ࠥࡴࡦࡺࡨࠣᝤ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack11ll111l1ll_opy_(key) or str(key).startswith(bstack1l1111l_opy_ (u"ࠦࡤࠨᝥ")):
            continue
        if value is not None and bstack11ll111l1ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack11ll11ll111_opy_(value, bstack11ll1l111l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack11ll11ll111_opy_(o, bstack11ll1l111l1_opy_, max_depth) for o in value]))
    return result or None