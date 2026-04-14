# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import bstack1l1ll1lllll_opy_, bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11l1l_opy_ import bstack1l11ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11l1l1_opy_ import bstack1l11l1ll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l11l11111l_opy_, TestHookState, bstack1llll11ll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack11ll1l1l1l_opy_, bstack11ll111ll11_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11ll11lll11_opy_ = [bstack1l111l_opy_ (u"ࠥࡲࡦࡳࡥࠣᛘ"), bstack1l111l_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᛙ"), bstack1l111l_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧᛚ"), bstack1l111l_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࠢᛛ"), bstack1l111l_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᛜ")]
bstack11lll1l1111_opy_ = bstack11ll111ll11_opy_()
bstack11ll111l1l1_opy_ = bstack1l111l_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᛝ")
bstack11ll1llll11_opy_ = {
    bstack1l111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢᛞ"): bstack11ll11lll11_opy_,
    bstack1l111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦᛟ"): bstack11ll11lll11_opy_,
    bstack1l111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦᛠ"): bstack11ll11lll11_opy_,
    bstack1l111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦᛡ"): bstack11ll11lll11_opy_,
    bstack1l111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣᛢ"): bstack11ll11lll11_opy_
    + [
        bstack1l111l_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨᛣ"),
        bstack1l111l_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᛤ"),
        bstack1l111l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢᛥ"),
        bstack1l111l_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᛦ"),
        bstack1l111l_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨᛧ"),
        bstack1l111l_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨᛨ"),
        bstack1l111l_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᛩ"),
        bstack1l111l_opy_ (u"ࠢࡴࡶࡲࡴࠧᛪ"),
        bstack1l111l_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥ᛫"),
        bstack1l111l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢ᛬"),
    ],
    bstack1l111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤ᛭"): [bstack1l111l_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢᛮ"), bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥᛯ"), bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᛰ"), bstack1l111l_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨᛱ")],
    bstack1l111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣᛲ"): [bstack1l111l_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨᛳ"), bstack1l111l_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᛴ")],
    bstack1l111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥᛵ"): [bstack1l111l_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᛶ"), bstack1l111l_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᛷ"), bstack1l111l_opy_ (u"ࠢࡧࡷࡱࡧࠧᛸ"), bstack1l111l_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣ᛹"), bstack1l111l_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦ᛺"), bstack1l111l_opy_ (u"ࠥ࡭ࡩࡹࠢ᛻")],
    bstack1l111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥ᛼"): [bstack1l111l_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥ᛽"), bstack1l111l_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧ᛾"), bstack1l111l_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧ᛿")],
    bstack1l111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥᜀ"): [bstack1l111l_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᜁ"), bstack1l111l_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥᜂ")],
    bstack1l111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧᜃ"): [bstack1l111l_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᜄ"), bstack1l111l_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᜅ")],
    bstack1l111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢᜆ"): [bstack1l111l_opy_ (u"ࠣࡰࡤࡱࡪࠨᜇ"), bstack1l111l_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᜈ"), bstack1l111l_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥᜉ")],
}
_11ll1ll11l1_opy_ = set()
class bstack1l11111l1_opy_(bstack1l11ll1l11l_opy_):
    bstack11ll1ll1111_opy_ = bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦᜊ")
    bstack11ll1l11l1l_opy_ = bstack1l111l_opy_ (u"ࠧࡏࡎࡇࡑࠥᜋ")
    bstack11lll111l11_opy_ = bstack1l111l_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧᜌ")
    bstack11ll11lll1l_opy_: Callable
    bstack11ll11ll111_opy_: Callable
    def __init__(self, bstack1l1l11lllll_opy_, bstack1l11l1lllll_opy_):
        super().__init__()
        self.bstack11lllllll11_opy_ = bstack1l11l1lllll_opy_
        if os.getenv(bstack1l111l_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦᜍ"), bstack1l111l_opy_ (u"ࠣ࠳ࠥᜎ")) != bstack1l111l_opy_ (u"ࠤ࠴ࠦᜏ") or not self.is_enabled():
            return
        TestFramework.bstack1l11111ll11_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111ll1ll_opy_)
        TestFramework.bstack1l11111ll11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11111lll1_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l11111ll11_opy_((event, state), self.bstack11lll111ll1_opy_)
        bstack1l1l11lllll_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.POST), self.bstack11ll1l11l11_opy_)
        self.bstack11ll11lll1l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack11lll1l1ll1_opy_(bstack1l11111l1_opy_.bstack11ll1l11l1l_opy_, self.bstack11ll11lll1l_opy_)
        self.bstack11ll11ll111_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack11lll1l1ll1_opy_(bstack1l11111l1_opy_.bstack11lll111l11_opy_, self.bstack11ll11ll111_opy_)
        self.bstack11ll11l11l1_opy_ = builtins.print
        builtins.print = self.bstack11lll111lll_opy_()
        self._11ll1lll111_opy_()
    def _11ll1lll111_opy_(self):
        bstack1l111l_opy_ (u"ࠥࠦࠧࡖࡡࡵࡥ࡫ࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴ࠯ࡵࡼࡲࡨࡥࡡࡱ࡫࠱ࡔࡦ࡭ࡥ࠯ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡺ࡯ࠡࡥࡤࡴࡹࡻࡲࡦࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠠࡧࡱࡵࠎࠥࠦࠠࠡࠢࠣࠤ࡚ࠥࡥࡴࡶࠣࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠣࡻ࡭࡫࡮ࠡࡶࡨࡷࡹࡹࠠࡳࡷࡱࠤࡴࡴࠠ࡯ࡱࡱ࠱ࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣ࡭ࡳ࡬ࡲࡢࡵࡷࡶࡺࡩࡴࡶࡴࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥ࠮ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡩࡥࡱࡹࡥࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡎࡴࡴࡦࡴࡦࡩࡵࡺࡳࠡࡤࡼࡸࡪࡹࠠࡳࡧࡷࡹࡷࡴࡥࡥࠢࡥࡽࠥࡶࡡࡨࡧ࠱ࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠨࠪ࠮ࠣࡦࡦࡹࡥ࠷࠶࠰ࡩࡳࡩ࡯ࡥࡧࡶࠤࡹ࡮ࡥ࡮࠮ࠣࡥࡳࡪࠊࠡࠢࠣࠤࠥࠦࠠࠡࡵࡨࡲࡩࡹࠠࡵࡪࡨࡱࠥࡼࡩࡢࠢࡪࡖࡕࡉࠠࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࡉࡻ࡫࡮ࡵࠢࠫ࡯࡮ࡴࡤ࠾ࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠬ࠰ࠥࡩ࡯࡯ࡵ࡬ࡷࡹ࡫࡮ࡵࠢࡺ࡭ࡹ࡮ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡪࡲࡻ࡙ࠥࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡨࡵ࡭࡮ࡣࡱࡨࡸࠦࡡࡳࡧࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤ࡮ࡴࠠࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡨࡼࡪࡩࡵࡵࡧࠫ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᜐ")
        try:
            from playwright.sync_api import Page as bstack11lll11lll1_opy_
        except ImportError:
            return
        if getattr(bstack11lll11lll1_opy_.screenshot, bstack1l111l_opy_ (u"ࠫࡤࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡥ࡫ࡩࡩ࠭ᜑ"), False):
            return
        bstack11ll11l111l_opy_ = bstack11lll11lll1_opy_.screenshot
        dispatcher = self
        def bstack_page_screenshot(bstack1l11l11l1_opy_, **kwargs):
            bstack11ll11l1111_opy_ = bstack11ll11l111l_opy_(bstack1l11l11l1_opy_, **kwargs)
            try:
                if not bstack11ll1l1l1l_opy_():
                    import base64
                    bstack11ll11ll1ll_opy_ = base64.b64encode(bstack11ll11l1111_opy_).decode(bstack1l111l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᜒ"))
                    bstack11lll1l11l1_opy_ = TestFramework.bstack11ll11l1lll_opy_()
                    if bstack11lll1l11l1_opy_:
                        bstack11l1l11111_opy_ = next(
                            (t for t in bstack11lll1l11l1_opy_ if TestFramework.bstack1l1lll1l1l1_opy_(t, TestFramework.bstack1l11111llll_opy_)),
                            None,
                        )
                        if bstack11l1l11111_opy_:
                            entry = bstack1llll11ll_opy_(TestFramework.KIND_SCREENSHOT, bstack11ll11ll1ll_opy_)
                            dispatcher.bstack111ll1llll_opy_(bstack11l1l11111_opy_, [entry])
            except Exception:
                pass
            return bstack11ll11l1111_opy_
        bstack_page_screenshot._bstack_patched = True
        bstack11lll11lll1_opy_.screenshot = bstack_page_screenshot
    def is_enabled(self) -> bool:
        return True
    def _11ll1l1111l_opy_(self, f: TestFramework) -> bool:
        bstack1l111l_opy_ (u"ࠨࠢࠣࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡸࠦࡖࡢࡰ࡬ࡰࡱࡧࡐࡺࡶ࡫ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࠪࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠬ࠲ࠧࠨࠢᜓ")
        return (hasattr(f, bstack1l111l_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢࡒࡆࡓࡅࠨ᜔")) and f.FRAMEWORK_NAME == bstack1l111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤ᜕ࠩ")) or \
               (hasattr(f, bstack1l111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶࠫ᜖")) and bstack1l111l_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ᜗") in f.bstack1l11llllll1_opy_)
    def bstack11lll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l11111l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_supported = f.bstack11lll1l111l_opy_() or f.bstack11ll1llllll_opy_() or self._11ll1l1111l_opy_(f)
        if is_supported and instance:
            bstack11ll11l1l11_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1l1l1lllll1_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1ll111l111_opy_ = datetime.now()
                entries = f.bstack11ll1l1lll1_opy_(instance, bstack1l1l1lllll1_opy_)
                if entries:
                    self.bstack111ll1llll_opy_(instance, entries)
                    instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦ᜘"), datetime.now() - bstack1ll111l111_opy_)
                    f.bstack11ll1l111ll_opy_(instance, bstack1l1l1lllll1_opy_)
                instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣ᜙"), datetime.now() - bstack11ll11l1l11_opy_)
                return # bstack11ll1l1l11l_opy_ not send this event with the bstack11lll11l1ll_opy_ bstack11lll11ll1l_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack11ll11llll1_opy_)
            ):
                f.bstack11111ll11l_opy_(instance, bstack1l11111l1_opy_.bstack11ll1ll1111_opy_, True)
                return # bstack11ll1l1l11l_opy_ not send this event bstack11lll1l1l1l_opy_ bstack11ll1l1ll11_opy_
            elif (
                f.bstack1ll111111ll_opy_(instance, bstack1l11111l1_opy_.bstack11ll1ll1111_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack11ll11llll1_opy_)
            ):
                self.bstack11lll111ll1_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1ll111l111_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack11lll1l111l_opy_():
                bstack11ll1llll1l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1l111l_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤ᜚"), None), data.pop(bstack1l111l_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ᜛"), {}).values()),
                    key=lambda x: x[bstack1l111l_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦ᜜")],
                )
                data.update({bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ᜝"): bstack11ll1llll1l_opy_})
            elif f.bstack11ll1llllll_opy_():
                bstack11ll11l1l1l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1l111l_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨ᜞"), None), data.pop(bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᜟ"), {}).values()),
                    key=lambda x: x[bstack1l111l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᜠ")],
                )
                data.update({bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᜡ"): bstack11ll11l1l1l_opy_})
            if bstack1l11ll111l1_opy_.bstack11ll1l11111_opy_ in data:
                data.pop(bstack1l11ll111l1_opy_.bstack11ll1l11111_opy_)
            instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᜢ"), datetime.now() - bstack1ll111l111_opy_)
            bstack1ll111l111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack11ll1l1l1l1_opy_)
            instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᜣ"), datetime.now() - bstack1ll111l111_opy_)
            if TestFramework.bstack1l11111llll_opy_ in data:
                self.bstack11lll11ll1l_opy_(instance, bstack1l1l1lllll1_opy_, event_json=event_json)
            instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᜤ"), datetime.now() - bstack11ll11l1l11_opy_)
    def bstack1l1111ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l11111l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
        bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack1l1l11lll_opy_.value)
        self.bstack11lllllll11_opy_.bstack11ll111l1ll_opy_(instance, f, bstack1l1l1lllll1_opy_, *args, **kwargs)
        try:
            req = self.bstack11lllllll11_opy_.bstack11lll11l11l_opy_(instance, f, bstack1l1l1lllll1_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷࠤ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡡࡻࡾ࡟ࠣࡿࢂࡢ࡮ࡼࡿࠥᜥ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack11ll1lll1ll_opy_ data not ready for robot-playwright at the time of bstack1l1111ll1ll_opy_, so bstack11lll1111l1_opy_ will send bstack11ll1lll1ll_opy_ event in bstack1l11111lll1_opy_ for robot-playwright
            self.bstack11lll1l1l11_opy_(f, instance, req)
        bstack111ll11l1_opy_.end(EVENTS.bstack1l1l11lll_opy_.value, bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᜦ"), bstack1l11l11l_opy_ + bstack1l111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᜧ"), status=True, failure=None, test_name=None)
    def bstack1l11111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l11111l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll111111ll_opy_(instance, self.bstack11lllllll11_opy_.bstack11ll1ll1ll1_opy_, False):
            try:
                req = self.bstack11lllllll11_opy_.bstack11lll11l11l_opy_(instance, f, bstack1l1l1lllll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1l111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࠦࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡜ࡽࢀࡡࠥࢁࡽ࡝ࡰࡾࢁࠧᜨ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack11lll1l1l11_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack11lll1111ll_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11lll1l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l11111l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥᜩ"))
            return
        bstack1ll111l111_opy_ = datetime.now()
        try:
            r = self.bstack1l1l1111l1_opy_.TestSessionEvent(req)
            instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤᜪ"), datetime.now() - bstack1ll111l111_opy_)
            f.bstack11111ll11l_opy_(instance, self.bstack11lllllll11_opy_.bstack11ll1ll1ll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᜫ") + str(r) + bstack1l111l_opy_ (u"ࠥࠦᜬ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᜭ") + str(e) + bstack1l111l_opy_ (u"ࠧࠨᜮ"))
            traceback.print_exc()
            raise e
    def bstack11ll1l11l11_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        _driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        _11ll11ll11l_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l11l1ll1l1_opy_.bstack11lllll1ll1_opy_(method_name):
            return
        if f.bstack1l111111l11_opy_(*args) == bstack1l11l1ll1l1_opy_.bstack11lll111l1l_opy_:
            bstack11ll11l1l11_opy_ = datetime.now()
            screenshot = result.get(bstack1l111l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᜯ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l111l_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲࠣᜰ"))
                return
            bstack11l1l11111_opy_ = self.bstack11ll1l11ll1_opy_(instance)
            if bstack11l1l11111_opy_:
                entry = bstack1llll11ll_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack111ll1llll_opy_(bstack11l1l11111_opy_, [entry])
                instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤᜱ"), datetime.now() - bstack11ll11l1l11_opy_)
            else:
                self.logger.warning(bstack1l111l_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢᜲ").format(instance.ref()))
        event = {}
        bstack11l1l11111_opy_ = self.bstack11ll1l11ll1_opy_(instance)
        if bstack11l1l11111_opy_:
            self.bstack11lll11111l_opy_(event, bstack11l1l11111_opy_)
            if event.get(bstack1l111l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᜳ")):
                self.bstack111ll1llll_opy_(bstack11l1l11111_opy_, event[bstack1l111l_opy_ (u"ࠦࡱࡵࡧࡴࠤ᜴")])
            else:
                self.logger.debug(bstack1l111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤ᜵"))
    @measure(event_name=EVENTS.bstack11ll111lll1_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack111ll1llll_opy_(
        self,
        bstack11l1l11111_opy_: bstack1l11l11111l_opy_,
        entries: List[bstack1llll11ll_opy_],
    ):
        self.bstack1l1111llll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack1l111l1111l_opy_)
        req.client_worker_id = bstack1l111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᜶").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack11l1l11111_opy_.context.hash)
        req.execution_context.thread_id = str(bstack11l1l11111_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack11l1l11111_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack11lllllll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack11ll11l11ll_opy_)
            log_entry.uuid = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack1l11111llll_opy_)
            log_entry.test_framework_state = bstack11l1l11111_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᜷"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᜸"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lll11llll_opy_
                log_entry.file_path = entry.bstack111l11l_opy_
        def bstack11ll1lllll1_opy_():
            bstack1ll111l111_opy_ = datetime.now()
            try:
                self.bstack1l1l1111l1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack11l1l11111_opy_.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᜹"), datetime.now() - bstack1ll111l111_opy_)
                elif entry.kind == TestFramework.bstack11ll111llll_opy_:
                    bstack11l1l11111_opy_.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ᜺"), datetime.now() - bstack1ll111l111_opy_)
                else:
                    bstack11l1l11111_opy_.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣ᜻"), datetime.now() - bstack1ll111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ᜼") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1lll111ll_opy_.enqueue(bstack11ll1lllll1_opy_)
    @measure(event_name=EVENTS.bstack11ll1l1ll1l_opy_, stage=STAGE.bstack1l11llll1_opy_)
    def bstack11lll11ll1l_opy_(
        self,
        instance: bstack1l11l11111l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1111llll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l111l1111l_opy_)
        req.client_worker_id = bstack1l111l_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᜽").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack11lllllll1l_opy_)
        req.test_framework_version = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack11ll11l11ll_opy_)
        req.test_framework_state = bstack1l1l1lllll1_opy_[0].name
        req.test_hook_state = bstack1l1l1lllll1_opy_[1].name
        started_at = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack11ll1ll1l1l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack11lll11ll11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack11ll1l1l1l1_opy_)).encode(bstack1l111l_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᜾"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack11ll1lllll1_opy_():
            bstack1ll111l111_opy_ = datetime.now()
            try:
                self.bstack1l1l1111l1_opy_.TestFrameworkEvent(req)
                instance.bstack1lllll1l11l_opy_(bstack1l111l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦ᜿"), datetime.now() - bstack1ll111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l111l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᝀ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1lll111ll_opy_.enqueue(bstack11ll1lllll1_opy_)
    def bstack11ll1l11ll1_opy_(self, instance: bstack1l1ll1lllll_opy_):
        bstack11lll1l11l1_opy_ = TestFramework.bstack1l1ll11111l_opy_(instance.context)
        for t in bstack11lll1l11l1_opy_:
            bstack11ll11ll1l1_opy_ = TestFramework.bstack1ll111111ll_opy_(t, bstack1l11ll111l1_opy_.bstack11ll1l11111_opy_, [])
            if not bstack11ll1l1l1l_opy_() and len(bstack11ll11ll1l1_opy_) == 0:
                bstack11ll11ll1l1_opy_ = TestFramework.bstack1ll111111ll_opy_(t, bstack1l11ll111l1_opy_.bstack11ll11l1ll1_opy_, [])
            if any(instance is d[1] for d in bstack11ll11ll1l1_opy_):
                return t
    def bstack11ll1lll1l1_opy_(self, message):
        self.bstack11ll11lll1l_opy_(message + bstack1l111l_opy_ (u"ࠥࡠࡳࠨᝁ"))
    def log_error(self, message):
        self.bstack11ll11ll111_opy_(message + bstack1l111l_opy_ (u"ࠦࡡࡴࠢᝂ"))
    def bstack11lll1l1ll1_opy_(self, level, original_func):
        def bstack11lll11l1l1_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1l111l_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨᝃ") in message or bstack1l111l_opy_ (u"ࠨ࡛ࡔࡆࡎࡇࡑࡏ࡝ࠣᝄ") in message or bstack1l111l_opy_ (u"ࠢ࡜࡙ࡨࡦࡉࡸࡩࡷࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠦᝅ") in message:
                        return return_value
                    bstack11lll1l11l1_opy_ = TestFramework.bstack11ll11l1lll_opy_()
                    if not bstack11lll1l11l1_opy_:
                        return return_value
                    bstack11l1l11111_opy_ = next(
                        (
                            instance
                            for instance in bstack11lll1l11l1_opy_
                            if TestFramework.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack1l11111llll_opy_)
                        ),
                        None,
                    )
                    if not bstack11l1l11111_opy_:
                        return return_value
                    entry = bstack1llll11ll_opy_(TestFramework.bstack11ll1lll11l_opy_, message, level)
                    self.bstack111ll1llll_opy_(bstack11l1l11111_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack11lll11l1l1_opy_
    def bstack11lll111lll_opy_(self):
        def bstack11lll11l111_opy_(*args, **kwargs):
            try:
                self.bstack11ll11l11l1_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l111l_opy_ (u"ࠨࠢࠪᝆ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l111l_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᝇ") in message:
                    return
                bstack11lll1l11l1_opy_ = TestFramework.bstack11ll11l1lll_opy_()
                if not bstack11lll1l11l1_opy_:
                    return
                bstack11l1l11111_opy_ = next(
                    (
                        instance
                        for instance in bstack11lll1l11l1_opy_
                        if TestFramework.bstack1l1lll1l1l1_opy_(instance, TestFramework.bstack1l11111llll_opy_)
                    ),
                    None,
                )
                if not bstack11l1l11111_opy_:
                    return
                entry = bstack1llll11ll_opy_(TestFramework.bstack11ll1lll11l_opy_, message, bstack1l11111l1_opy_.bstack11ll1l11l1l_opy_)
                self.bstack111ll1llll_opy_(bstack11l1l11111_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack11ll11l11l1_opy_(bstack1l1l1llll11_opy_ (u"ࠥ࡟ࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠦࡌࡰࡩࠣࡧࡦࡶࡴࡶࡴࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣᝈ"))
                except:
                    pass
        return bstack11lll11l111_opy_
    def bstack11lll11111l_opy_(self, event: dict, instance=None) -> None:
        global _11ll1ll11l1_opy_
        levels = [bstack1l111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᝉ"), bstack1l111l_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᝊ")]
        bstack11ll1l111l1_opy_ = bstack1l111l_opy_ (u"ࠨࠢᝋ")
        if instance is not None:
            try:
                bstack11ll1l111l1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l11111llll_opy_)
            except Exception as e:
                self.logger.warning(bstack1l111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᝌ").format(e))
        bstack11ll1l1l1ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᝍ")]
                bstack11lll1l1lll_opy_ = os.path.join(bstack11lll1l1111_opy_, (bstack11ll111l1l1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack11lll1l1lll_opy_):
                    self.logger.debug(bstack1l111l_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᝎ").format(bstack11lll1l1lll_opy_))
                    continue
                file_names = os.listdir(bstack11lll1l1lll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack11lll1l1lll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _11ll1ll11l1_opy_:
                        self.logger.info(bstack1l111l_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᝏ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack11ll11lllll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack11ll11lllll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᝐ"):
                                entry = bstack1llll11ll_opy_(
                                    kind=bstack1l111l_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᝑ"),
                                    message=bstack1l111l_opy_ (u"ࠨࠢᝒ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11lll11llll_opy_=file_size,
                                    bstack11ll1l1l111_opy_=bstack1l111l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᝓ"),
                                    bstack111l11l_opy_=os.path.abspath(file_path),
                                    bstack111l1ll11_opy_=bstack11ll1l111l1_opy_
                                )
                            elif level == bstack1l111l_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᝔"):
                                entry = bstack1llll11ll_opy_(
                                    kind=bstack1l111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᝕"),
                                    message=bstack1l111l_opy_ (u"ࠥࠦ᝖"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11lll11llll_opy_=file_size,
                                    bstack11ll1l1l111_opy_=bstack1l111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᝗"),
                                    bstack111l11l_opy_=os.path.abspath(file_path),
                                    bstack11ll1ll11ll_opy_=bstack11ll1l111l1_opy_
                                )
                            bstack11ll1l1l1ll_opy_.append(entry)
                            _11ll1ll11l1_opy_.add(abs_path)
                        except Exception as bstack11ll1ll111l_opy_:
                            self.logger.error(bstack1l111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦ᝘").format(bstack11ll1ll111l_opy_))
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧ᝙").format(e))
        event[bstack1l111l_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ᝚")] = bstack11ll1l1l1ll_opy_
class bstack11ll1l1l1l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11ll1l1llll_opy_ = set()
        kwargs[bstack1l111l_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥ᝛")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack11lll111111_opy_(obj, self.bstack11ll1l1llll_opy_)
def bstack11ll1ll1lll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack11lll111111_opy_(obj, bstack11ll1l1llll_opy_=None, max_depth=3):
    if bstack11ll1l1llll_opy_ is None:
        bstack11ll1l1llll_opy_ = set()
    if id(obj) in bstack11ll1l1llll_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11ll1l1llll_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack11ll1l11lll_opy_ = TestFramework.bstack11ll111ll1l_opy_(obj)
    bstack11ll1ll1l11_opy_ = next((k.lower() in bstack11ll1l11lll_opy_.lower() for k in bstack11ll1llll11_opy_.keys()), None)
    if bstack11ll1ll1l11_opy_:
        obj = TestFramework.bstack11lll1l11ll_opy_(obj, bstack11ll1llll11_opy_[bstack11ll1ll1l11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l111l_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧ᝜")):
            keys = getattr(obj, bstack1l111l_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨ᝝"), [])
        elif hasattr(obj, bstack1l111l_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨ᝞")):
            keys = getattr(obj, bstack1l111l_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢ᝟"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l111l_opy_ (u"ࠨ࡟ࠣᝠ"))}
        if not obj and bstack11ll1l11lll_opy_ == bstack1l111l_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦᝡ"):
            obj = {bstack1l111l_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᝢ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack11ll1ll1lll_opy_(key) or str(key).startswith(bstack1l111l_opy_ (u"ࠤࡢࠦᝣ")):
            continue
        if value is not None and bstack11ll1ll1lll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack11lll111111_opy_(value, bstack11ll1l1llll_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack11lll111111_opy_(o, bstack11ll1l1llll_opy_, max_depth) for o in value]))
    return result or None