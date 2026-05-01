# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import bstack1l1ll111lll_opy_, bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l111l1l_opy_ import bstack1l1l1111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1ll11l1_opy_, TestHookState, bstack11l1l1l1ll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l1l11_opy_, bstack11ll11l1lll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11ll1l1l11l_opy_ = [bstack111ll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᛩ"), bstack111ll_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᛪ"), bstack111ll_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣ᛫"), bstack111ll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥ᛬"), bstack111ll_opy_ (u"ࠥࡴࡦࡺࡨࠣ᛭")]
bstack11ll11l1ll1_opy_ = bstack11ll11l1lll_opy_()
bstack11ll1ll1l11_opy_ = bstack111ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᛮ")
bstack11ll1ll11l1_opy_ = {
    bstack111ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᛯ"): bstack11ll1l1l11l_opy_,
    bstack111ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᛰ"): bstack11ll1l1l11l_opy_,
    bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᛱ"): bstack11ll1l1l11l_opy_,
    bstack111ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᛲ"): bstack11ll1l1l11l_opy_,
    bstack111ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᛳ"): bstack11ll1l1l11l_opy_
    + [
        bstack111ll_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᛴ"),
        bstack111ll_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᛵ"),
        bstack111ll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᛶ"),
        bstack111ll_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᛷ"),
        bstack111ll_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᛸ"),
        bstack111ll_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤ᛹"),
        bstack111ll_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣ᛺"),
        bstack111ll_opy_ (u"ࠥࡷࡹࡵࡰࠣ᛻"),
        bstack111ll_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨ᛼"),
        bstack111ll_opy_ (u"ࠧࡽࡨࡦࡰࠥ᛽"),
    ],
    bstack111ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧ᛾"): [bstack111ll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥ᛿"), bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᜀ"), bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᜁ"), bstack111ll_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᜂ")],
    bstack111ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᜃ"): [bstack111ll_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᜄ"), bstack111ll_opy_ (u"ࠨࡡࡳࡩࡶࠦᜅ")],
    bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᜆ"): [bstack111ll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᜇ"), bstack111ll_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᜈ"), bstack111ll_opy_ (u"ࠥࡪࡺࡴࡣࠣᜉ"), bstack111ll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᜊ"), bstack111ll_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᜋ"), bstack111ll_opy_ (u"ࠨࡩࡥࡵࠥᜌ")],
    bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᜍ"): [bstack111ll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᜎ"), bstack111ll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣᜏ"), bstack111ll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᜐ")],
    bstack111ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨᜑ"): [bstack111ll_opy_ (u"ࠧࡽࡨࡦࡰࠥᜒ"), bstack111ll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨᜓ")],
    bstack111ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳ᜔ࠣ"): [bstack111ll_opy_ (u"ࠣࡰࡲࡨࡪࠨ᜕"), bstack111ll_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤ᜖")],
    bstack111ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥ᜗"): [bstack111ll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᜘"), bstack111ll_opy_ (u"ࠧࡧࡲࡨࡵࠥ᜙"), bstack111ll_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨ᜚")],
}
_11ll111lll1_opy_ = set()
class bstack1l111l11_opy_(bstack1l11l1l11ll_opy_):
    bstack11lll1111l1_opy_ = bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢ᜛")
    bstack11lll111ll1_opy_ = bstack111ll_opy_ (u"ࠣࡋࡑࡊࡔࠨ᜜")
    bstack11lll111111_opy_ = bstack111ll_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣ᜝")
    bstack11ll1llll11_opy_: Callable
    bstack11ll111l1l1_opy_: Callable
    def __init__(self, bstack1l11l1111ll_opy_, bstack1l11l1l1l1l_opy_):
        super().__init__()
        self.bstack11llll1lll1_opy_ = bstack1l11l1l1l1l_opy_
        if os.getenv(bstack111ll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢ᜞"), bstack111ll_opy_ (u"ࠦ࠶ࠨᜟ")) != bstack111ll_opy_ (u"ࠧ࠷ࠢᜠ") or not self.is_enabled():
            return
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111l11ll_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l111l1_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l111l1111l_opy_((event, state), self.bstack11lll1l11l1_opy_)
        bstack1l11l1111ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.POST), self.bstack11ll1ll1ll1_opy_)
        self.bstack11ll1llll11_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack11lll11l1l1_opy_(bstack1l111l11_opy_.bstack11lll111ll1_opy_, self.bstack11ll1llll11_opy_)
        self.bstack11ll111l1l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack11lll11l1l1_opy_(bstack1l111l11_opy_.bstack11lll111111_opy_, self.bstack11ll111l1l1_opy_)
        self.bstack11ll111ll1l_opy_ = builtins.print
        builtins.print = self.bstack11ll1l1llll_opy_()
        self._11ll11ll1l1_opy_()
    def _11ll11ll1l1_opy_(self):
        bstack111ll_opy_ (u"ࠨࠢࠣࡒࡤࡸࡨ࡮ࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠲ࡸࡿ࡮ࡤࡡࡤࡴ࡮࠴ࡐࡢࡩࡨ࠲ࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡶࡲࠤࡨࡧࡰࡵࡷࡵࡩࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠣࡪࡴࡸࠊࠡࠢࠣࠤࠥࠦࠠࠡࡖࡨࡷࡹࠦࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࠦࡷࡩࡧࡱࠤࡹ࡫ࡳࡵࡵࠣࡶࡺࡴࠠࡰࡰࠣࡲࡴࡴ࠭ࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡩ࡯ࡨࡵࡥࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠪࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࡬ࡡ࡭ࡵࡨ࠭࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰࡷࡩࡷࡩࡥࡱࡶࡶࠤࡧࡿࡴࡦࡵࠣࡶࡪࡺࡵࡳࡰࡨࡨࠥࡨࡹࠡࡲࡤ࡫ࡪ࠴ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠫ࠭࠱ࠦࡢࡢࡵࡨ࠺࠹࠳ࡥ࡯ࡥࡲࡨࡪࡹࠠࡵࡪࡨࡱ࠱ࠦࡡ࡯ࡦࠍࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡫࡮ࡥࡵࠣࡸ࡭࡫࡭ࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠣࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࡅࡷࡧࡱࡸࠥ࠮࡫ࡪࡰࡧࡁ࡙ࡋࡓࡕࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࠯ࠬࠡࡥࡲࡲࡸ࡯ࡳࡵࡧࡱࡸࠥࡽࡩࡵࡪࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡭ࡵࡷࠡࡕࡨࡰࡪࡴࡩࡶ࡯ࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡤࡱࡰࡱࡦࡴࡤࡴࠢࡤࡶࡪࠦࡨࡢࡰࡧࡰࡪࡪࠠࡪࡰࠣࡳࡳࡥࡡࡧࡶࡨࡶࡤ࡫ࡸࡦࡥࡸࡸࡪ࠮ࠩ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᜡ")
        try:
            from playwright.sync_api import Page as bstack11ll11l1l11_opy_
        except ImportError:
            return
        if getattr(bstack11ll11l1l11_opy_.screenshot, bstack111ll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸࡨ࡮ࡥࡥࠩᜢ"), False):
            return
        bstack11ll11lll11_opy_ = bstack11ll11l1l11_opy_.screenshot
        dispatcher = self
        def bstack_page_screenshot(bstack111l1llll_opy_, **kwargs):
            bstack11ll11ll11l_opy_ = bstack11ll11lll11_opy_(bstack111l1llll_opy_, **kwargs)
            try:
                if not bstack1l1l1l11_opy_():
                    import base64
                    bstack11ll1l1l111_opy_ = base64.b64encode(bstack11ll11ll11l_opy_).decode(bstack111ll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᜣ"))
                    bstack11lll11l11l_opy_ = TestFramework.bstack11ll1l1111l_opy_()
                    if bstack11lll11l11l_opy_:
                        bstack1llllllll_opy_ = next(
                            (t for t in bstack11lll11l11l_opy_ if TestFramework.bstack1l1lllll1l1_opy_(t, TestFramework.bstack1l11111111l_opy_)),
                            None,
                        )
                        if bstack1llllllll_opy_:
                            entry = bstack11l1l1l1ll_opy_(TestFramework.KIND_SCREENSHOT, bstack11ll1l1l111_opy_)
                            dispatcher.bstack1l1111ll1l_opy_(bstack1llllllll_opy_, [entry])
            except Exception:
                pass
            return bstack11ll11ll11l_opy_
        bstack_page_screenshot._bstack_patched = True
        bstack11ll11l1l11_opy_.screenshot = bstack_page_screenshot
    def is_enabled(self) -> bool:
        return True
    def _11ll11l111l_opy_(self, f: TestFramework) -> bool:
        bstack111ll_opy_ (u"ࠤࠥࠦࡈ࡮ࡥࡤ࡭ࠣ࡭࡫ࠦࡴࡩࡧࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩࡴ࡙ࠢࡥࡳ࡯࡬࡭ࡣࡓࡽࡹ࡮࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠭ࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠯࠮ࠣࠤࠥᜤ")
        return (hasattr(f, bstack111ll_opy_ (u"ࠪࡊࡗࡇࡍࡆ࡙ࡒࡖࡐࡥࡎࡂࡏࡈࠫᜥ")) and f.FRAMEWORK_NAME == bstack111ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬᜦ")) or \
               (hasattr(f, bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹࠧᜧ")) and bstack111ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧᜨ") in f.bstack1l1l11l1111_opy_)
    def bstack11lll1l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_supported = f.bstack11ll1l111ll_opy_() or f.bstack11ll1ll1l1l_opy_() or self._11ll11l111l_opy_(f)
        if is_supported and instance:
            bstack11ll111l11l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1l1l1lll11l_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1l11111lll_opy_ = datetime.now()
                entries = f.bstack11lll111l1l_opy_(instance, bstack1l1l1lll11l_opy_)
                if entries:
                    self.bstack1l1111ll1l_opy_(instance, entries)
                    instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺࠢᜩ"), datetime.now() - bstack1l11111lll_opy_)
                    f.bstack11lll11l1ll_opy_(instance, bstack1l1l1lll11l_opy_)
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᜪ"), datetime.now() - bstack11ll111l11l_opy_)
                return # bstack11ll1l111l1_opy_ not send this event with the bstack11ll1lll11l_opy_ bstack11lll1l1111_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11111l_opy_)
            ):
                f.bstack11ll11l1_opy_(instance, bstack1l111l11_opy_.bstack11lll1111l1_opy_, True)
                return # bstack11ll1l111l1_opy_ not send this event bstack11ll111ll11_opy_ bstack11lll1l111l_opy_
            elif (
                f.bstack1l1llll1111_opy_(instance, bstack1l111l11_opy_.bstack11lll1111l1_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11111l_opy_)
            ):
                self.bstack11lll1l11l1_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1l11111lll_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack11ll1l111ll_opy_():
                bstack11ll1lll1l1_opy_ = sorted(
                    filter(lambda x: x.get(bstack111ll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᜫ"), None), data.pop(bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᜬ"), {}).values()),
                    key=lambda x: x[bstack111ll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᜭ")],
                )
                data.update({bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᜮ"): bstack11ll1lll1l1_opy_})
            elif f.bstack11ll1ll1l1l_opy_():
                bstack11ll1llllll_opy_ = sorted(
                    filter(lambda x: x.get(bstack111ll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤᜯ"), None), data.pop(bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡱࡥࡺࡹࡲࡶࡩࡹࠢᜰ"), {}).values()),
                    key=lambda x: x[bstack111ll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᜱ")],
                )
                data.update({bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺ࡟࡬ࡧࡼࡻࡴࡸࡤࡴࠤᜲ"): bstack11ll1llllll_opy_})
            if bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_ in data:
                data.pop(bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_)
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᜳ"), datetime.now() - bstack1l11111lll_opy_)
            bstack1l11111lll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack11ll1l11111_opy_)
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹ᜴ࠢ"), datetime.now() - bstack1l11111lll_opy_)
            if TestFramework.bstack1l11111111l_opy_ in data:
                self.bstack11lll1l1111_opy_(instance, bstack1l1l1lll11l_opy_, event_json=event_json)
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣ᜵"), datetime.now() - bstack11ll111l11l_opy_)
    def bstack1l1111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
        bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack111llllll1_opy_.value)
        self.bstack11llll1lll1_opy_.bstack11ll11lll1l_opy_(instance, f, bstack1l1l1lll11l_opy_, *args, **kwargs)
        try:
            req = self.bstack11llll1lll1_opy_.bstack11ll111llll_opy_(instance, f, bstack1l1l1lll11l_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺࠠࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡝ࡾࢁࡢࠦࡻࡾ࡞ࡱࡿࢂࠨ᜶").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack11ll11l1111_opy_ data not ready for robot-playwright at the time of bstack1l1111l11ll_opy_, so bstack11ll1111l1l_opy_ will send bstack11ll11l1111_opy_ event in bstack1l111l111l1_opy_ for robot-playwright
            self.bstack11ll11l11l1_opy_(f, instance, req)
        bstack111l1l1l_opy_.end(EVENTS.bstack111llllll1_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᜷"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᜸"), status=True, failure=None, test_name=None)
    def bstack1l111l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1l1llll1111_opy_(instance, self.bstack11llll1lll1_opy_.bstack11ll11l11ll_opy_, False):
            try:
                req = self.bstack11llll1lll1_opy_.bstack11ll111llll_opy_(instance, f, bstack1l1l1lll11l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵࠢࡪࡩࡹࡥࡣࡣࡶࡢࡩࡻ࡫࡮ࡵࠢࡩࡥ࡮ࡲࡥࡥ࠼ࠣ࡟ࢀࢃ࡝ࠡࡽࢀࡠࡳࢁࡽࠣ᜹").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack11ll11l11l1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack11lll11ll11_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11ll11l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨ᜺"))
            return
        bstack1l11111lll_opy_ = datetime.now()
        try:
            r = self.bstack111111ll1l_opy_.TestSessionEvent(req)
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧ᜻"), datetime.now() - bstack1l11111lll_opy_)
            f.bstack11ll11l1_opy_(instance, self.bstack11llll1lll1_opy_.bstack11ll11l11ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack111ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢ᜼") + str(r) + bstack111ll_opy_ (u"ࠨࠢ᜽"))
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ᜾") + str(e) + bstack111ll_opy_ (u"ࠣࠤ᜿"))
            traceback.print_exc()
            raise e
    def bstack11ll1ll1ll1_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        _driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        _11ll11l1l1l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l11lll111l_opy_.bstack1l1111llll1_opy_(method_name):
            return
        if f.bstack1l111l1l1l1_opy_(*args) == bstack1l11lll111l_opy_.bstack11ll111l111_opy_:
            bstack11ll111l11l_opy_ = datetime.now()
            screenshot = result.get(bstack111ll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᝀ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack111ll_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦᝁ"))
                return
            bstack1llllllll_opy_ = self.bstack11ll1l1l1l1_opy_(instance)
            if bstack1llllllll_opy_:
                entry = bstack11l1l1l1ll_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l1111ll1l_opy_(bstack1llllllll_opy_, [entry])
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧᝂ"), datetime.now() - bstack11ll111l11l_opy_)
            else:
                self.logger.warning(bstack111ll_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥᝃ").format(instance.ref()))
        event = {}
        bstack1llllllll_opy_ = self.bstack11ll1l1l1l1_opy_(instance)
        if bstack1llllllll_opy_:
            self.bstack11ll1ll11ll_opy_(event, bstack1llllllll_opy_)
            if event.get(bstack111ll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᝄ")):
                self.bstack1l1111ll1l_opy_(bstack1llllllll_opy_, event[bstack111ll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᝅ")])
            else:
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧᝆ"))
    @measure(event_name=EVENTS.bstack11ll1l11ll1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack1l1111ll1l_opy_(
        self,
        bstack1llllllll_opy_: bstack1l1l1ll11l1_opy_,
        entries: List[bstack11l1l1l1ll_opy_],
    ):
        self.bstack11llllll111_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l111111111_opy_)
        req.client_worker_id = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᝇ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1llllllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1llllllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1llllllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l1111l111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack11ll1l11l1l_opy_)
            log_entry.uuid = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack1l11111111l_opy_)
            log_entry.test_framework_state = bstack1llllllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᝈ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111ll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᝉ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11ll1lll111_opy_
                log_entry.file_path = entry.bstack111l1_opy_
        def bstack11lll111lll_opy_():
            bstack1l11111lll_opy_ = datetime.now()
            try:
                self.bstack111111ll1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1llllllll_opy_.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᝊ"), datetime.now() - bstack1l11111lll_opy_)
                elif entry.kind == TestFramework.bstack11ll111l1ll_opy_:
                    bstack1llllllll_opy_.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᝋ"), datetime.now() - bstack1l11111lll_opy_)
                else:
                    bstack1llllllll_opy_.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟࡭ࡱࡪࠦᝌ"), datetime.now() - bstack1l11111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᝍ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1ll1llll1_opy_.enqueue(bstack11lll111lll_opy_)
    @measure(event_name=EVENTS.bstack11ll1l11lll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack11lll1l1111_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack11llllll111_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111111111_opy_)
        req.client_worker_id = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᝎ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l1111l111l_opy_)
        req.test_framework_version = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l11l1l_opy_)
        req.test_framework_state = bstack1l1l1lll11l_opy_[0].name
        req.test_hook_state = bstack1l1l1lll11l_opy_[1].name
        started_at = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11lll11llll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack11ll1l11111_opy_)).encode(bstack111ll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᝏ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack11lll111lll_opy_():
            bstack1l11111lll_opy_ = datetime.now()
            try:
                self.bstack111111ll1l_opy_.TestFrameworkEvent(req)
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡧࡹࡩࡳࡺࠢᝐ"), datetime.now() - bstack1l11111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111ll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᝑ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1ll1llll1_opy_.enqueue(bstack11lll111lll_opy_)
    def bstack11ll1l1l1l1_opy_(self, instance: bstack1l1ll111lll_opy_):
        bstack11lll11l11l_opy_ = TestFramework.bstack1l1ll11llll_opy_(instance.context)
        for t in bstack11lll11l11l_opy_:
            bstack11ll1111ll1_opy_ = TestFramework.bstack1l1llll1111_opy_(t, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
            if not bstack1l1l1l11_opy_() and len(bstack11ll1111ll1_opy_) == 0:
                bstack11ll1111ll1_opy_ = TestFramework.bstack1l1llll1111_opy_(t, bstack1l1l1111ll1_opy_.bstack11ll1l1ll11_opy_, [])
            if any(instance is d[1] for d in bstack11ll1111ll1_opy_):
                return t
    def bstack11ll1l1ll1l_opy_(self, message):
        self.bstack11ll1llll11_opy_(message + bstack111ll_opy_ (u"ࠨ࡜࡯ࠤᝒ"))
    def log_error(self, message):
        self.bstack11ll111l1l1_opy_(message + bstack111ll_opy_ (u"ࠢ࡝ࡰࠥᝓ"))
    def bstack11lll11l1l1_opy_(self, level, original_func):
        def bstack11lll111l11_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack111ll_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤ᝔") in message or bstack111ll_opy_ (u"ࠤ࡞ࡗࡉࡑࡃࡍࡋࡠࠦ᝕") in message or bstack111ll_opy_ (u"ࠥ࡟࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࡍࡰࡦࡸࡰࡪࡣࠢ᝖") in message:
                        return return_value
                    bstack11lll11l11l_opy_ = TestFramework.bstack11ll1l1111l_opy_()
                    if not bstack11lll11l11l_opy_:
                        return return_value
                    bstack1llllllll_opy_ = next(
                        (
                            instance
                            for instance in bstack11lll11l11l_opy_
                            if TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l11111111l_opy_)
                        ),
                        None,
                    )
                    if not bstack1llllllll_opy_:
                        return return_value
                    entry = bstack11l1l1l1ll_opy_(TestFramework.bstack11ll1l1l1ll_opy_, message, level)
                    self.bstack1l1111ll1l_opy_(bstack1llllllll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack11lll111l11_opy_
    def bstack11ll1l1llll_opy_(self):
        def bstack11ll11ll1ll_opy_(*args, **kwargs):
            try:
                self.bstack11ll111ll1l_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack111ll_opy_ (u"ࠫࠥ࠭᝗").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack111ll_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨ᝘") in message:
                    return
                bstack11lll11l11l_opy_ = TestFramework.bstack11ll1l1111l_opy_()
                if not bstack11lll11l11l_opy_:
                    return
                bstack1llllllll_opy_ = next(
                    (
                        instance
                        for instance in bstack11lll11l11l_opy_
                        if TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l11111111l_opy_)
                    ),
                    None,
                )
                if not bstack1llllllll_opy_:
                    return
                entry = bstack11l1l1l1ll_opy_(TestFramework.bstack11ll1l1l1ll_opy_, message, bstack1l111l11_opy_.bstack11lll111ll1_opy_)
                self.bstack1l1111ll1l_opy_(bstack1llllllll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack11ll111ll1l_opy_(bstack1l1ll1l1111_opy_ (u"ࠨ࡛ࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠢࡏࡳ࡬ࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦ᝙"))
                except:
                    pass
        return bstack11ll11ll1ll_opy_
    def bstack11ll1ll11ll_opy_(self, event: dict, instance=None) -> None:
        global _11ll111lll1_opy_
        levels = [bstack111ll_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥ᝚"), bstack111ll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᝛")]
        bstack11ll1ll1lll_opy_ = bstack111ll_opy_ (u"ࠤࠥ᝜")
        if instance is not None:
            try:
                bstack11ll1ll1lll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_)
            except Exception as e:
                self.logger.warning(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡺ࡯ࡤࠡࡨࡵࡳࡲࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣ᝝").format(e))
        bstack11ll1ll111l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᝞")]
                bstack11ll11lllll_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11ll1ll1l11_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack11ll11lllll_opy_):
                    self.logger.debug(bstack111ll_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡰࡲࡸࠥࡶࡲࡦࡵࡨࡲࡹࠦࡦࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡕࡧࡶࡸࠥࡧ࡮ࡥࠢࡅࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣ᝟").format(bstack11ll11lllll_opy_))
                    continue
                file_names = os.listdir(bstack11ll11lllll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack11ll11lllll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _11ll111lll1_opy_:
                        self.logger.info(bstack111ll_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᝠ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack11ll1ll1111_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack11ll1ll1111_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack111ll_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᝡ"):
                                entry = bstack11l1l1l1ll_opy_(
                                    kind=bstack111ll_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᝢ"),
                                    message=bstack111ll_opy_ (u"ࠤࠥᝣ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11ll1lll111_opy_=file_size,
                                    bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᝤ"),
                                    bstack111l1_opy_=os.path.abspath(file_path),
                                    bstack1lllllllll_opy_=bstack11ll1ll1lll_opy_
                                )
                            elif level == bstack111ll_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᝥ"):
                                entry = bstack11l1l1l1ll_opy_(
                                    kind=bstack111ll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᝦ"),
                                    message=bstack111ll_opy_ (u"ࠨࠢᝧ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11ll1lll111_opy_=file_size,
                                    bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᝨ"),
                                    bstack111l1_opy_=os.path.abspath(file_path),
                                    bstack11lll11ll1l_opy_=bstack11ll1ll1lll_opy_
                                )
                            bstack11ll1ll111l_opy_.append(entry)
                            _11ll111lll1_opy_.add(abs_path)
                        except Exception as bstack11ll11llll1_opy_:
                            self.logger.error(bstack111ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᝩ").format(bstack11ll11llll1_opy_))
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣᝪ").format(e))
        event[bstack111ll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᝫ")] = bstack11ll1ll111l_opy_
class bstack11ll1l11111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11ll1llll1l_opy_ = set()
        kwargs[bstack111ll_opy_ (u"ࠦࡸࡱࡩࡱ࡭ࡨࡽࡸࠨᝬ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack11ll1111lll_opy_(obj, self.bstack11ll1llll1l_opy_)
def bstack11lll11l111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack11ll1111lll_opy_(obj, bstack11ll1llll1l_opy_=None, max_depth=3):
    if bstack11ll1llll1l_opy_ is None:
        bstack11ll1llll1l_opy_ = set()
    if id(obj) in bstack11ll1llll1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11ll1llll1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack11ll1lllll1_opy_ = TestFramework.bstack11ll1l11l11_opy_(obj)
    bstack11lll11lll1_opy_ = next((k.lower() in bstack11ll1lllll1_opy_.lower() for k in bstack11ll1ll11l1_opy_.keys()), None)
    if bstack11lll11lll1_opy_:
        obj = TestFramework.bstack11lll1111ll_opy_(obj, bstack11ll1ll11l1_opy_[bstack11lll11lll1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack111ll_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣ᝭")):
            keys = getattr(obj, bstack111ll_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤᝮ"), [])
        elif hasattr(obj, bstack111ll_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤᝯ")):
            keys = getattr(obj, bstack111ll_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥᝰ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack111ll_opy_ (u"ࠤࡢࠦ᝱"))}
        if not obj and bstack11ll1lllll1_opy_ == bstack111ll_opy_ (u"ࠥࡴࡦࡺࡨ࡭࡫ࡥ࠲ࡕࡵࡳࡪࡺࡓࡥࡹ࡮ࠢᝲ"):
            obj = {bstack111ll_opy_ (u"ࠦࡵࡧࡴࡩࠤᝳ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack11lll11l111_opy_(key) or str(key).startswith(bstack111ll_opy_ (u"ࠧࡥࠢ᝴")):
            continue
        if value is not None and bstack11lll11l111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack11ll1111lll_opy_(value, bstack11ll1llll1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack11ll1111lll_opy_(o, bstack11ll1llll1l_opy_, max_depth) for o in value]))
    return result or None