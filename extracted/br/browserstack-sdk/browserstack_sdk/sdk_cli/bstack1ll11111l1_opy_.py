# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1l1l1ll1ll_opy_ import bstack1l1ll1111l1_opy_, bstack1l1111l1l1_opy_, bstack1ll111111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll111l_opy_ import bstack1l11lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1111ll_opy_ import bstack1l1l1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l1l111l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l11l1ll1ll_opy_, TestHookState, bstack111l1111l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lllllll_opy_, bstack11ll11ll11l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11ll1l11l1l_opy_ = [bstack1ll1l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᚿ"), bstack1ll1l11_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᛀ"), bstack1ll1l11_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣᛁ"), bstack1ll1l11_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥᛂ"), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡺࡨࠣᛃ")]
bstack11ll11l1ll1_opy_ = bstack11ll11ll11l_opy_()
bstack11lll11111l_opy_ = bstack1ll1l11_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦᛄ")
bstack11ll1ll11l1_opy_ = {
    bstack1ll1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥᛅ"): bstack11ll1l11l1l_opy_,
    bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢᛆ"): bstack11ll1l11l1l_opy_,
    bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢᛇ"): bstack11ll1l11l1l_opy_,
    bstack1ll1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢᛈ"): bstack11ll1l11l1l_opy_,
    bstack1ll1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦᛉ"): bstack11ll1l11l1l_opy_
    + [
        bstack1ll1l11_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤᛊ"),
        bstack1ll1l11_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᛋ"),
        bstack1ll1l11_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥᛌ"),
        bstack1ll1l11_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᛍ"),
        bstack1ll1l11_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤᛎ"),
        bstack1ll1l11_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤᛏ"),
        bstack1ll1l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣᛐ"),
        bstack1ll1l11_opy_ (u"ࠥࡷࡹࡵࡰࠣᛑ"),
        bstack1ll1l11_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨᛒ"),
        bstack1ll1l11_opy_ (u"ࠧࡽࡨࡦࡰࠥᛓ"),
    ],
    bstack1ll1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧᛔ"): [bstack1ll1l11_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥᛕ"), bstack1ll1l11_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨᛖ"), bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥᛗ"), bstack1ll1l11_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤᛘ")],
    bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦᛙ"): [bstack1ll1l11_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤᛚ"), bstack1ll1l11_opy_ (u"ࠨࡡࡳࡩࡶࠦᛛ")],
    bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨᛜ"): [bstack1ll1l11_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢᛝ"), bstack1ll1l11_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥᛞ"), bstack1ll1l11_opy_ (u"ࠥࡪࡺࡴࡣࠣᛟ"), bstack1ll1l11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦᛠ"), bstack1ll1l11_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢᛡ"), bstack1ll1l11_opy_ (u"ࠨࡩࡥࡵࠥᛢ")],
    bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨᛣ"): [bstack1ll1l11_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨᛤ"), bstack1ll1l11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣᛥ"), bstack1ll1l11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣᛦ")],
    bstack1ll1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨᛧ"): [bstack1ll1l11_opy_ (u"ࠧࡽࡨࡦࡰࠥᛨ"), bstack1ll1l11_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨᛩ")],
    bstack1ll1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣᛪ"): [bstack1ll1l11_opy_ (u"ࠣࡰࡲࡨࡪࠨ᛫"), bstack1ll1l11_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤ᛬")],
    bstack1ll1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥ᛭"): [bstack1ll1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᛮ"), bstack1ll1l11_opy_ (u"ࠧࡧࡲࡨࡵࠥᛯ"), bstack1ll1l11_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨᛰ")],
}
_11ll1llllll_opy_ = set()
class bstack1llll11l1l_opy_(bstack1l11lll1l1l_opy_):
    bstack11lll1l1lll_opy_ = bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢᛱ")
    bstack11lll1l1ll1_opy_ = bstack1ll1l11_opy_ (u"ࠣࡋࡑࡊࡔࠨᛲ")
    bstack11ll11lll11_opy_ = bstack1ll1l11_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣᛳ")
    bstack11ll11llll1_opy_: Callable
    bstack11ll11l1l1l_opy_: Callable
    def __init__(self, bstack1l11llll11l_opy_, bstack1l11llllll1_opy_):
        super().__init__()
        self.bstack1l1111l1111_opy_ = bstack1l11llllll1_opy_
        if os.getenv(bstack1ll1l11_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢᛴ"), bstack1ll1l11_opy_ (u"ࠦ࠶ࠨᛵ")) != bstack1ll1l11_opy_ (u"ࠧ࠷ࠢᛶ") or not self.is_enabled():
            return
        TestFramework.bstack1l1111ll11l_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111l11l1_opy_)
        TestFramework.bstack1l1111ll11l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11llllll111_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1111ll11l_opy_((event, state), self.bstack11lll1l1l1l_opy_)
        bstack1l11llll11l_opy_.bstack1l1111ll11l_opy_((bstack1l1111l1l1_opy_.bstack1l1llllll11_opy_, bstack1ll111111l_opy_.POST), self.bstack11ll11l1lll_opy_)
        self.bstack11ll11llll1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack11ll1ll1ll1_opy_(bstack1llll11l1l_opy_.bstack11lll1l1ll1_opy_, self.bstack11ll11llll1_opy_)
        self.bstack11ll11l1l1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack11ll1ll1ll1_opy_(bstack1llll11l1l_opy_.bstack11ll11lll11_opy_, self.bstack11ll11l1l1l_opy_)
        self.bstack11ll11lll1l_opy_ = builtins.print
        builtins.print = self.bstack11lll1111l1_opy_()
    def is_enabled(self) -> bool:
        return True
    def _11ll1l111l1_opy_(self, f: TestFramework) -> bool:
        bstack1ll1l11_opy_ (u"ࠨࠢࠣࡅ࡫ࡩࡨࡱࠠࡪࡨࠣࡸ࡭࡫ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡸࠦࡖࡢࡰ࡬ࡰࡱࡧࡐࡺࡶ࡫ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࠪࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠬ࠲ࠧࠨࠢᛷ")
        return (hasattr(f, bstack1ll1l11_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢࡒࡆࡓࡅࠨᛸ")) and f.FRAMEWORK_NAME == bstack1ll1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ᛹")) or \
               (hasattr(f, bstack1ll1l11_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶࠫ᛺")) and bstack1ll1l11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ᛻") in f.bstack1l111llllll_opy_)
    def bstack11lll1l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll1ll_opy_,
        bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_supported = f.bstack11ll1l11lll_opy_() or f.bstack11ll1lll1l1_opy_() or self._11ll1l111l1_opy_(f)
        if is_supported and instance:
            bstack11ll11ll1ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1l1ll1ll1ll_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1l1l11llll_opy_ = datetime.now()
                entries = f.bstack11ll1l1l1ll_opy_(instance, bstack1l1ll1ll1ll_opy_)
                if entries:
                    self.bstack1l1ll1lll_opy_(instance, entries)
                    instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦ᛼"), datetime.now() - bstack1l1l11llll_opy_)
                    f.bstack11lll11ll1l_opy_(instance, bstack1l1ll1ll1ll_opy_)
                instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣ᛽"), datetime.now() - bstack11ll11ll1ll_opy_)
                return # bstack11lll1l1l11_opy_ not send this event with the bstack11lll11lll1_opy_ bstack11ll11ll1l1_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1lll1ll_opy_)
            ):
                f.bstack1ll11l1ll_opy_(instance, bstack1llll11l1l_opy_.bstack11lll1l1lll_opy_, True)
                return # bstack11lll1l1l11_opy_ not send this event bstack11ll1l1ll1l_opy_ bstack11ll1ll1lll_opy_
            elif (
                f.bstack1l1lll1ll11_opy_(instance, bstack1llll11l1l_opy_.bstack11lll1l1lll_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1lll1ll_opy_)
            ):
                self.bstack11lll1l1l1l_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1l1l11llll_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack11ll1l11lll_opy_():
                bstack11ll11l11ll_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll1l11_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤ᛾"), None), data.pop(bstack1ll1l11_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ᛿"), {}).values()),
                    key=lambda x: x[bstack1ll1l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦᜀ")],
                )
                data.update({bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤᜁ"): bstack11ll11l11ll_opy_})
            elif f.bstack11ll1lll1l1_opy_():
                bstack11ll11lllll_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll1l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᜂ"), None), data.pop(bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᜃ"), {}).values()),
                    key=lambda x: x[bstack1ll1l11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᜄ")],
                )
                data.update({bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᜅ"): bstack11ll11lllll_opy_})
            if bstack1l1l1lll1l1_opy_.bstack11ll1l1l11l_opy_ in data:
                data.pop(bstack1l1l1lll1l1_opy_.bstack11ll1l1l11l_opy_)
            instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᜆ"), datetime.now() - bstack1l1l11llll_opy_)
            bstack1l1l11llll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack11lll11llll_opy_)
            instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᜇ"), datetime.now() - bstack1l1l11llll_opy_)
            if TestFramework.bstack1l111l1lll1_opy_ in data:
                self.bstack11ll11ll1l1_opy_(instance, bstack1l1ll1ll1ll_opy_, event_json=event_json)
            instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᜈ"), datetime.now() - bstack11ll11ll1ll_opy_)
    def bstack1l1111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll1ll_opy_,
        bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
        bstack1l111ll1ll_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack1l11ll1ll1_opy_.value)
        self.bstack1l1111l1111_opy_.bstack11lll1ll111_opy_(instance, f, bstack1l1ll1ll1ll_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1111l1111_opy_.bstack11ll1ll1111_opy_(instance, f, bstack1l1ll1ll1ll_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷࠤ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࡡࡻࡾ࡟ࠣࡿࢂࡢ࡮ࡼࡿࠥᜉ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack11ll1l1lll1_opy_ data not ready for robot-playwright at the time of bstack1l1111l11l1_opy_, so bstack11ll1lll111_opy_ will send bstack11ll1l1lll1_opy_ event in bstack11llllll111_opy_ for robot-playwright
            self.bstack11ll1l11ll1_opy_(f, instance, req)
        bstack11l1111l1l_opy_.end(EVENTS.bstack1l11ll1ll1_opy_.value, bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᜊ"), bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᜋ"), status=True, failure=None, test_name=None)
    def bstack11llllll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll1ll_opy_,
        bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1l1lll1ll11_opy_(instance, self.bstack1l1111l1111_opy_.bstack11lll11l1ll_opy_, False):
            try:
                req = self.bstack1l1111l1111_opy_.bstack11ll1ll1111_opy_(instance, f, bstack1l1ll1ll1ll_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࠦࡧࡦࡶࡢࡧࡧࡺ࡟ࡦࡸࡨࡲࡹࠦࡦࡢ࡫࡯ࡩࡩࡀࠠ࡜ࡽࢀࡡࠥࢁࡽ࡝ࡰࡾࢁࠧᜌ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack11ll1l11ll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack11lll111lll_opy_, stage=STAGE.bstack1ll11l11_opy_)
    def bstack11ll1l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll1ll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥᜍ"))
            return
        bstack1l1l11llll_opy_ = datetime.now()
        try:
            r = self.bstack1llll11l11_opy_.TestSessionEvent(req)
            instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤᜎ"), datetime.now() - bstack1l1l11llll_opy_)
            f.bstack1ll11l1ll_opy_(instance, self.bstack1l1111l1111_opy_.bstack11lll11l1ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll1l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᜏ") + str(r) + bstack1ll1l11_opy_ (u"ࠥࠦᜐ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᜑ") + str(e) + bstack1ll1l11_opy_ (u"ࠧࠨᜒ"))
            traceback.print_exc()
            raise e
    def bstack11ll11l1lll_opy_(
        self,
        f: bstack1l1l111l1ll_opy_,
        _driver: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        _11lll11l11l_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l1l111l1ll_opy_.bstack1l111l11l11_opy_(method_name):
            return
        if f.bstack1l111l1ll1l_opy_(*args) == bstack1l1l111l1ll_opy_.bstack11ll1l1llll_opy_:
            bstack11ll11ll1ll_opy_ = datetime.now()
            screenshot = result.get(bstack1ll1l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᜓ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲ᜔ࠣ"))
                return
            bstack1l11lll11l_opy_ = self.bstack11ll1l1l111_opy_(instance)
            if bstack1l11lll11l_opy_:
                entry = bstack111l1111l_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l1ll1lll_opy_(bstack1l11lll11l_opy_, [entry])
                instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤ᜕"), datetime.now() - bstack11ll11ll1ll_opy_)
            else:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢ᜖").format(instance.ref()))
        event = {}
        bstack1l11lll11l_opy_ = self.bstack11ll1l1l111_opy_(instance)
        if bstack1l11lll11l_opy_:
            self.bstack11ll1lllll1_opy_(event, bstack1l11lll11l_opy_)
            if event.get(bstack1ll1l11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣ᜗")):
                self.bstack1l1ll1lll_opy_(bstack1l11lll11l_opy_, event[bstack1ll1l11_opy_ (u"ࠦࡱࡵࡧࡴࠤ᜘")])
            else:
                self.logger.debug(bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤ᜙"))
    @measure(event_name=EVENTS.bstack11lll111111_opy_, stage=STAGE.bstack1ll11l11_opy_)
    def bstack1l1ll1lll_opy_(
        self,
        bstack1l11lll11l_opy_: bstack1l11l1ll1ll_opy_,
        entries: List[bstack111l1111l_opy_],
    ):
        self.bstack1l11111111l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack1l111ll1l1l_opy_)
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧ᜚").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11lll11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11lll11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11lll11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11llllll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11ll11l11l1_opy_)
            log_entry.uuid = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack1l111l1lll1_opy_)
            log_entry.test_framework_state = bstack1l11lll11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨ᜛"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll1l11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥ᜜"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack11lll1l111l_opy_
                log_entry.file_path = entry.bstack11ll_opy_
        def bstack11ll1lll11l_opy_():
            bstack1l1l11llll_opy_ = datetime.now()
            try:
                self.bstack1llll11l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l11lll11l_opy_.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨ᜝"), datetime.now() - bstack1l1l11llll_opy_)
                elif entry.kind == TestFramework.bstack11ll1l11l11_opy_:
                    bstack1l11lll11l_opy_.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢ᜞"), datetime.now() - bstack1l1l11llll_opy_)
                else:
                    bstack1l11lll11l_opy_.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣᜟ"), datetime.now() - bstack1l1l11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᜠ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1lll11l11_opy_.enqueue(bstack11ll1lll11l_opy_)
    @measure(event_name=EVENTS.bstack11lll11l1l1_opy_, stage=STAGE.bstack1ll11l11_opy_)
    def bstack11ll11ll1l1_opy_(
        self,
        instance: bstack1l11l1ll1ll_opy_,
        bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l11111111l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack1l111ll1l1l_opy_)
        req.client_worker_id = bstack1ll1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᜡ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack11llllll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack11ll11l11l1_opy_)
        req.test_framework_state = bstack1l1ll1ll1ll_opy_[0].name
        req.test_hook_state = bstack1l1ll1ll1ll_opy_[1].name
        started_at = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack11ll1l1ll11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack11lll1111ll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack11lll11llll_opy_)).encode(bstack1ll1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᜢ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack11ll1lll11l_opy_():
            bstack1l1l11llll_opy_ = datetime.now()
            try:
                self.bstack1llll11l11_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1lll1l_opy_(bstack1ll1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦᜣ"), datetime.now() - bstack1l1l11llll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᜤ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1lll11l11_opy_.enqueue(bstack11ll1lll11l_opy_)
    def bstack11ll1l1l111_opy_(self, instance: bstack1l1ll1111l1_opy_):
        bstack11lll1l1111_opy_ = TestFramework.bstack1l1ll11l1ll_opy_(instance.context)
        for t in bstack11lll1l1111_opy_:
            bstack11lll11ll11_opy_ = TestFramework.bstack1l1lll1ll11_opy_(t, bstack1l1l1lll1l1_opy_.bstack11ll1l1l11l_opy_, [])
            if not bstack1l1lllllll_opy_() and len(bstack11lll11ll11_opy_) == 0:
                bstack11lll11ll11_opy_ = TestFramework.bstack1l1lll1ll11_opy_(t, bstack1l1l1lll1l1_opy_.bstack11lll1l11ll_opy_, [])
            if any(instance is d[1] for d in bstack11lll11ll11_opy_):
                return t
    def bstack11ll1l11111_opy_(self, message):
        self.bstack11ll11llll1_opy_(message + bstack1ll1l11_opy_ (u"ࠥࡠࡳࠨᜥ"))
    def log_error(self, message):
        self.bstack11ll11l1l1l_opy_(message + bstack1ll1l11_opy_ (u"ࠦࡡࡴࠢᜦ"))
    def bstack11ll1ll1ll1_opy_(self, level, original_func):
        def bstack11ll1ll111l_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1ll1l11_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨᜧ") in message or bstack1ll1l11_opy_ (u"ࠨ࡛ࡔࡆࡎࡇࡑࡏ࡝ࠣᜨ") in message or bstack1ll1l11_opy_ (u"ࠢ࡜࡙ࡨࡦࡉࡸࡩࡷࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠦᜩ") in message:
                        return return_value
                    bstack11lll1l1111_opy_ = TestFramework.bstack11ll1l111ll_opy_()
                    if not bstack11lll1l1111_opy_:
                        return return_value
                    bstack1l11lll11l_opy_ = next(
                        (
                            instance
                            for instance in bstack11lll1l1111_opy_
                            if TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
                        ),
                        None,
                    )
                    if not bstack1l11lll11l_opy_:
                        return return_value
                    entry = bstack111l1111l_opy_(TestFramework.bstack11lll11l111_opy_, message, level)
                    self.bstack1l1ll1lll_opy_(bstack1l11lll11l_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack11ll1ll111l_opy_
    def bstack11lll1111l1_opy_(self):
        def bstack11ll11l111l_opy_(*args, **kwargs):
            try:
                self.bstack11ll11lll1l_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1ll1l11_opy_ (u"ࠨࠢࠪᜪ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1ll1l11_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᜫ") in message:
                    return
                bstack11lll1l1111_opy_ = TestFramework.bstack11ll1l111ll_opy_()
                if not bstack11lll1l1111_opy_:
                    return
                bstack1l11lll11l_opy_ = next(
                    (
                        instance
                        for instance in bstack11lll1l1111_opy_
                        if TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
                    ),
                    None,
                )
                if not bstack1l11lll11l_opy_:
                    return
                entry = bstack111l1111l_opy_(TestFramework.bstack11lll11l111_opy_, message, bstack1llll11l1l_opy_.bstack11lll1l1ll1_opy_)
                self.bstack1l1ll1lll_opy_(bstack1l11lll11l_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack11ll11lll1l_opy_(bstack1l1ll1ll11l_opy_ (u"ࠥ࡟ࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠦࡌࡰࡩࠣࡧࡦࡶࡴࡶࡴࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣᜬ"))
                except:
                    pass
        return bstack11ll11l111l_opy_
    def bstack11ll1lllll1_opy_(self, event: dict, instance=None) -> None:
        global _11ll1llllll_opy_
        levels = [bstack1ll1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᜭ"), bstack1ll1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᜮ")]
        bstack11lll111ll1_opy_ = bstack1ll1l11_opy_ (u"ࠨࠢᜯ")
        if instance is not None:
            try:
                bstack11lll111ll1_opy_ = TestFramework.bstack1l1lll1ll11_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᜰ").format(e))
        bstack11ll1llll1l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᜱ")]
                bstack11ll11l1l11_opy_ = os.path.join(bstack11ll11l1ll1_opy_, (bstack11lll11111l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack11ll11l1l11_opy_):
                    self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᜲ").format(bstack11ll11l1l11_opy_))
                    continue
                file_names = os.listdir(bstack11ll11l1l11_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack11ll11l1l11_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _11ll1llllll_opy_:
                        self.logger.info(bstack1ll1l11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᜳ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack11lll111l11_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack11lll111l11_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲ᜴ࠢ"):
                                entry = bstack111l1111l_opy_(
                                    kind=bstack1ll1l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢ᜵"),
                                    message=bstack1ll1l11_opy_ (u"ࠨࠢ᜶"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11lll1l111l_opy_=file_size,
                                    bstack11ll1l1l1l1_opy_=bstack1ll1l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ᜷"),
                                    bstack11ll_opy_=os.path.abspath(file_path),
                                    bstack1l1l1l1l_opy_=bstack11lll111ll1_opy_
                                )
                            elif level == bstack1ll1l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧ᜸"):
                                entry = bstack111l1111l_opy_(
                                    kind=bstack1ll1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦ᜹"),
                                    message=bstack1ll1l11_opy_ (u"ࠥࠦ᜺"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack11lll1l111l_opy_=file_size,
                                    bstack11ll1l1l1l1_opy_=bstack1ll1l11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ᜻"),
                                    bstack11ll_opy_=os.path.abspath(file_path),
                                    bstack11ll1ll1l1l_opy_=bstack11lll111ll1_opy_
                                )
                            bstack11ll1llll1l_opy_.append(entry)
                            _11ll1llllll_opy_.add(abs_path)
                        except Exception as bstack11ll1ll11ll_opy_:
                            self.logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦ᜼").format(bstack11ll1ll11ll_opy_))
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧ᜽").format(e))
        event[bstack1ll1l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧ᜾")] = bstack11ll1llll1l_opy_
class bstack11lll11llll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11lll1l11l1_opy_ = set()
        kwargs[bstack1ll1l11_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥ᜿")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack11lll111l1l_opy_(obj, self.bstack11lll1l11l1_opy_)
def bstack11lll1ll11l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack11lll111l1l_opy_(obj, bstack11lll1l11l1_opy_=None, max_depth=3):
    if bstack11lll1l11l1_opy_ is None:
        bstack11lll1l11l1_opy_ = set()
    if id(obj) in bstack11lll1l11l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11lll1l11l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack11ll11ll111_opy_ = TestFramework.bstack11ll1ll1l11_opy_(obj)
    bstack11ll1llll11_opy_ = next((k.lower() in bstack11ll11ll111_opy_.lower() for k in bstack11ll1ll11l1_opy_.keys()), None)
    if bstack11ll1llll11_opy_:
        obj = TestFramework.bstack11ll1l1111l_opy_(obj, bstack11ll1ll11l1_opy_[bstack11ll1llll11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll1l11_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᝀ")):
            keys = getattr(obj, bstack1ll1l11_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᝁ"), [])
        elif hasattr(obj, bstack1ll1l11_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᝂ")):
            keys = getattr(obj, bstack1ll1l11_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᝃ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll1l11_opy_ (u"ࠨ࡟ࠣᝄ"))}
        if not obj and bstack11ll11ll111_opy_ == bstack1ll1l11_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦᝅ"):
            obj = {bstack1ll1l11_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᝆ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack11lll1ll11l_opy_(key) or str(key).startswith(bstack1ll1l11_opy_ (u"ࠤࡢࠦᝇ")):
            continue
        if value is not None and bstack11lll1ll11l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack11lll111l1l_opy_(value, bstack11lll1l11l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack11lll111l1l_opy_(o, bstack11lll1l11l1_opy_, max_depth) for o in value]))
    return result or None