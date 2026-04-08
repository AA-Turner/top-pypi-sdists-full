# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import bstack1l1l111l1l1_opy_, bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11111111l_opy_ import bstack1l1111l111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l11ll11l_opy_, TestHookState, bstack11lllllll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll1ll111_opy_, bstack1l1ll1lllll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11ll11l111l_opy_ = [bstack111l_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᝓ"), bstack111l_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣ᝔"), bstack111l_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤ᝕"), bstack111l_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦ᝖"), bstack111l_opy_ (u"ࠦࡵࡧࡴࡩࠤ᝗")]
bstack11l1llll1l1_opy_ = bstack1l1ll1lllll_opy_()
bstack11ll111llll_opy_ = bstack111l_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ᝘")
bstack11ll11l1lll_opy_ = {
    bstack111l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦ᝙"): bstack11ll11l111l_opy_,
    bstack111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣ᝚"): bstack11ll11l111l_opy_,
    bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣ᝛"): bstack11ll11l111l_opy_,
    bstack111l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣ᝜"): bstack11ll11l111l_opy_,
    bstack111l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧ᝝"): bstack11ll11l111l_opy_
    + [
        bstack111l_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥ᝞"),
        bstack111l_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢ᝟"),
        bstack111l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦᝠ"),
        bstack111l_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᝡ"),
        bstack111l_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥᝢ"),
        bstack111l_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥᝣ"),
        bstack111l_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤᝤ"),
        bstack111l_opy_ (u"ࠦࡸࡺ࡯ࡱࠤᝥ"),
        bstack111l_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢᝦ"),
        bstack111l_opy_ (u"ࠨࡷࡩࡧࡱࠦᝧ"),
    ],
    bstack111l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨᝨ"): [bstack111l_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦᝩ"), bstack111l_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢᝪ"), bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦᝫ"), bstack111l_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥᝬ")],
    bstack111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧ᝭"): [bstack111l_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥᝮ"), bstack111l_opy_ (u"ࠢࡢࡴࡪࡷࠧᝯ")],
    bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢᝰ"): [bstack111l_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ᝱"), bstack111l_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦᝲ"), bstack111l_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤᝳ"), bstack111l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ᝴"), bstack111l_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣ᝵"), bstack111l_opy_ (u"ࠢࡪࡦࡶࠦ᝶")],
    bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢ᝷"): [bstack111l_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢ᝸"), bstack111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤ᝹"), bstack111l_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤ᝺")],
    bstack111l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢ᝻"): [bstack111l_opy_ (u"ࠨࡷࡩࡧࡱࠦ᝼"), bstack111l_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢ᝽")],
    bstack111l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤ᝾"): [bstack111l_opy_ (u"ࠤࡱࡳࡩ࡫ࠢ᝿"), bstack111l_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥក")],
    bstack111l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦខ"): [bstack111l_opy_ (u"ࠧࡴࡡ࡮ࡧࠥគ"), bstack111l_opy_ (u"ࠨࡡࡳࡩࡶࠦឃ"), bstack111l_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢង")],
}
_11ll1111l1l_opy_ = set()
class bstack1l1ll111ll_opy_(bstack1l111111l1l_opy_):
    bstack11l1llllll1_opy_ = bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣច")
    bstack11ll111l11l_opy_ = bstack111l_opy_ (u"ࠤࡌࡒࡋࡕࠢឆ")
    bstack11ll111lll1_opy_ = bstack111l_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤជ")
    bstack11l1ll11l1l_opy_: Callable
    bstack11l1llll111_opy_: Callable
    def __init__(self, bstack1l111l1l1ll_opy_, bstack1l11ll1ll1l_opy_):
        super().__init__()
        self.bstack11ll1llll11_opy_ = bstack1l11ll1ll1l_opy_
        if os.getenv(bstack111l_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣឈ"), bstack111l_opy_ (u"ࠧ࠷ࠢញ")) != bstack111l_opy_ (u"ࠨ࠱ࠣដ") or not self.is_enabled():
            return
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11lll1ll1ll_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11lll1ll111_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack11llll1l1l1_opy_((event, state), self.bstack11ll11ll11l_opy_)
        bstack1l111l1l1ll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.POST), self.bstack11ll11l1l1l_opy_)
        self.bstack11l1ll11l1l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack11l1ll11111_opy_(bstack1l1ll111ll_opy_.bstack11ll111l11l_opy_, self.bstack11l1ll11l1l_opy_)
        self.bstack11l1llll111_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack11l1ll11111_opy_(bstack1l1ll111ll_opy_.bstack11ll111lll1_opy_, self.bstack11l1llll111_opy_)
        self.bstack11ll111l1l1_opy_ = builtins.print
        builtins.print = self.bstack11ll111111l_opy_()
    def is_enabled(self) -> bool:
        return True
    def _11l1lll111l_opy_(self, f: TestFramework) -> bool:
        bstack111l_opy_ (u"ࠢࠣࠤࡆ࡬ࡪࡩ࡫ࠡ࡫ࡩࠤࡹ࡮ࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡹࠠࡗࡣࡱ࡭ࡱࡲࡡࡑࡻࡷ࡬ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࠫࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦ࠭࠳ࠨࠢࠣឋ")
        return (hasattr(f, bstack111l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣࡓࡇࡍࡆࠩឌ")) and f.FRAMEWORK_NAME == bstack111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪឍ")) or \
               (hasattr(f, bstack111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷࠬណ")) and bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬត") in f.bstack1l1ll1ll11l_opy_)
    def bstack11ll11ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        is_supported = f.bstack1l1l1llll1l_opy_() or f.bstack1l1lll11111_opy_() or self._11l1lll111l_opy_(f)
        if is_supported and instance:
            bstack11l1ll1lll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1l1l1lllll1_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1lllllll1ll_opy_ = datetime.now()
                entries = f.bstack1l1lll1111l_opy_(instance, bstack1l1l1lllll1_opy_)
                if entries:
                    self.bstack11l1lll11_opy_(instance, entries)
                    instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࠧថ"), datetime.now() - bstack1lllllll1ll_opy_)
                    f.bstack1l1l1l11111_opy_(instance, bstack1l1l1lllll1_opy_)
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤទ"), datetime.now() - bstack11l1ll1lll1_opy_)
                return # bstack11l1ll11ll1_opy_ not send this event with the bstack11l1lll1lll_opy_ bstack11l1lll1l1l_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_)
            ):
                f.bstack1l11l1ll11_opy_(instance, bstack1l1ll111ll_opy_.bstack11l1llllll1_opy_, True)
                return # bstack11l1ll11ll1_opy_ not send this event bstack11ll11l11l1_opy_ bstack11ll1111l11_opy_
            elif (
                f.bstack1ll111111ll_opy_(instance, bstack1l1ll111ll_opy_.bstack11l1llllll1_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1111_opy_)
            ):
                self.bstack11ll11ll11l_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1lllllll1ll_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l1l1llll1l_opy_():
                bstack11l1ll111ll_opy_ = sorted(
                    filter(lambda x: x.get(bstack111l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥធ"), None), data.pop(bstack111l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣន"), {}).values()),
                    key=lambda x: x[bstack111l_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧប")],
                )
                data.update({bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥផ"): bstack11l1ll111ll_opy_})
            elif f.bstack1l1lll11111_opy_():
                bstack11l1lll1111_opy_ = sorted(
                    filter(lambda x: x.get(bstack111l_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢព"), None), data.pop(bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧភ"), {}).values()),
                    key=lambda x: x[bstack111l_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤម")],
                )
                data.update({bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡱࡥࡺࡹࡲࡶࡩࡹࠢយ"): bstack11l1lll1111_opy_})
            if bstack1l1111l111l_opy_.bstack11ll11ll111_opy_ in data:
                data.pop(bstack1l1111l111l_opy_.bstack11ll11ll111_opy_)
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠣ࡬ࡶࡳࡳࡀࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨរ"), datetime.now() - bstack1lllllll1ll_opy_)
            bstack1lllllll1ll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack11l1ll1l111_opy_)
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧល"), datetime.now() - bstack1lllllll1ll_opy_)
            if TestFramework.bstack1l1l1lll11l_opy_ in data:
                self.bstack11l1lll1l1l_opy_(instance, bstack1l1l1lllll1_opy_, event_json=event_json)
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨវ"), datetime.now() - bstack11l1ll1lll1_opy_)
    def bstack11lll1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
        bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack1ll1ll111l_opy_.value)
        self.bstack11ll1llll11_opy_.bstack11ll111l1ll_opy_(instance, f, bstack1l1l1lllll1_opy_, *args, **kwargs)
        try:
            req = self.bstack11ll1llll11_opy_.bstack11l1lll11ll_opy_(instance, f, bstack1l1l1lllll1_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸࠥ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿࡛ࠦࡼࡿࡠࠤࢀࢃ࡜࡯ࡽࢀࠦឝ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack11ll1111lll_opy_ data not ready for robot-playwright at the time of bstack11lll1ll1ll_opy_, so bstack11l1ll111l1_opy_ will send bstack11ll1111lll_opy_ event in bstack11lll1ll111_opy_ for robot-playwright
            self.bstack11ll11l1l11_opy_(f, instance, req)
        bstack11lll11111_opy_.end(EVENTS.bstack1ll1ll111l_opy_.value, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧឞ"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦស"), status=True, failure=None, test_name=None)
    def bstack11lll1ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll111111ll_opy_(instance, self.bstack11ll1llll11_opy_.bstack11ll11111ll_opy_, False):
            try:
                req = self.bstack11ll1llll11_opy_.bstack11l1lll11ll_opy_(instance, f, bstack1l1l1lllll1_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺࠠࡨࡧࡷࡣࡨࡨࡴࡠࡧࡹࡩࡳࡺࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡ࡝ࡾࢁࡢࠦࡻࡾ࡞ࡱࡿࢂࠨហ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack11ll11l1l11_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack11l1ll1llll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11ll11l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹࠦࡧࡓࡒࡆࠤࡨࡧ࡬࡭࠼ࠣࡒࡴࠦࡶࡢ࡮࡬ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠦឡ"))
            return
        bstack1lllllll1ll_opy_ = datetime.now()
        try:
            r = self.bstack11l11lll11_opy_.TestSessionEvent(req)
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡪࡼࡥ࡯ࡶࠥអ"), datetime.now() - bstack1lllllll1ll_opy_)
            f.bstack1l11l1ll11_opy_(instance, self.bstack11ll1llll11_opy_.bstack11ll11111ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack111l_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧឣ") + str(r) + bstack111l_opy_ (u"ࠦࠧឤ"))
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥឥ") + str(e) + bstack111l_opy_ (u"ࠨࠢឦ"))
            traceback.print_exc()
            raise e
    def bstack11ll11l1l1l_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        _driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        _11l1ll1l1l1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l11l11l11l_opy_.bstack11llll111l1_opy_(method_name):
            return
        if f.bstack11lll1ll11l_opy_(*args) == bstack1l11l11l11l_opy_.bstack11l1llll11l_opy_:
            bstack11l1ll1lll1_opy_ = datetime.now()
            screenshot = result.get(bstack111l_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨឧ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack111l_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡩ࡮ࡣࡪࡩࠥࡨࡡࡴࡧ࠹࠸ࠥࡹࡴࡳࠤឨ"))
                return
            bstack1lll1l1lll_opy_ = self.bstack11l1lllllll_opy_(instance)
            if bstack1lll1l1lll_opy_:
                entry = bstack11lllllll1_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack11l1lll11_opy_(bstack1lll1l1lll_opy_, [entry])
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡨࡼࡪࡩࡵࡵࡧࠥឩ"), datetime.now() - bstack11l1ll1lll1_opy_)
            else:
                self.logger.warning(bstack111l_opy_ (u"ࠥࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷࡩࡸࡺࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸ࡭࡯ࡳࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡽࡡࡴࠢࡷࡥࡰ࡫࡮ࠡࡤࡼࠤࡩࡸࡩࡷࡧࡵࡁࠥࢁࡽࠣឪ").format(instance.ref()))
        event = {}
        bstack1lll1l1lll_opy_ = self.bstack11l1lllllll_opy_(instance)
        if bstack1lll1l1lll_opy_:
            self.bstack11ll1111ll1_opy_(event, bstack1lll1l1lll_opy_)
            if event.get(bstack111l_opy_ (u"ࠦࡱࡵࡧࡴࠤឫ")):
                self.bstack11l1lll11_opy_(bstack1lll1l1lll_opy_, event[bstack111l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥឬ")])
            else:
                self.logger.debug(bstack111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡲ࡯ࡨࡵࠣࡪࡴࡸࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡪࡼࡥ࡯ࡶࠥឭ"))
    @measure(event_name=EVENTS.bstack11ll111l111_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l1lll11_opy_(
        self,
        bstack1lll1l1lll_opy_: bstack1l1l11ll11l_opy_,
        entries: List[bstack11lllllll1_opy_],
    ):
        self.bstack11lllll1111_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1l11ll1_opy_)
        req.client_worker_id = bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨឮ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1lll1l1lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1lll1l1lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1lll1l1lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1ll1l1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1lll1l1_opy_)
            log_entry.uuid = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1l1lll11l_opy_)
            log_entry.test_framework_state = bstack1lll1l1lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢឯ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111l_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦឰ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                log_entry.file_path = entry.bstack1lllllll_opy_
        def bstack11ll11l1ll1_opy_():
            bstack1lllllll1ll_opy_ = datetime.now()
            try:
                self.bstack11l11lll11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1lll1l1lll_opy_.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢឱ"), datetime.now() - bstack1lllllll1ll_opy_)
                elif entry.kind == TestFramework.bstack11l1ll1l1ll_opy_:
                    bstack1lll1l1lll_opy_.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣឲ"), datetime.now() - bstack1lllllll1ll_opy_)
                else:
                    bstack1lll1l1lll_opy_.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤឳ"), datetime.now() - bstack1lllllll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦ឴") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1l1ll11l1_opy_.enqueue(bstack11ll11l1ll1_opy_)
    @measure(event_name=EVENTS.bstack11l1ll11lll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11l1lll1l1l_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack11lllll1111_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_)
        req.client_worker_id = bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨ឵").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l11_opy_)
        req.test_framework_version = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_)
        req.test_framework_state = bstack1l1l1lllll1_opy_[0].name
        req.test_hook_state = bstack1l1l1lllll1_opy_[1].name
        started_at = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack11l1ll1l111_opy_)).encode(bstack111l_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢា"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack11ll11l1ll1_opy_():
            bstack1lllllll1ll_opy_ = datetime.now()
            try:
                self.bstack11l11lll11_opy_.TestFrameworkEvent(req)
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧិ"), datetime.now() - bstack1lllllll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣី") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1l1l1ll11l1_opy_.enqueue(bstack11ll11l1ll1_opy_)
    def bstack11l1lllllll_opy_(self, instance: bstack1l1l111l1l1_opy_):
        bstack11l1lllll1l_opy_ = TestFramework.bstack1l1l111111l_opy_(instance.context)
        for t in bstack11l1lllll1l_opy_:
            bstack11l1ll1ll1l_opy_ = TestFramework.bstack1ll111111ll_opy_(t, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
            if not bstack1ll1ll111_opy_() and len(bstack11l1ll1ll1l_opy_) == 0:
                bstack11l1ll1ll1l_opy_ = TestFramework.bstack1ll111111ll_opy_(t, bstack1l1111l111l_opy_.bstack11l1lll11l1_opy_, [])
            if any(instance is d[1] for d in bstack11l1ll1ll1l_opy_):
                return t
    def bstack11l1ll1111l_opy_(self, message):
        self.bstack11l1ll11l1l_opy_(message + bstack111l_opy_ (u"ࠦࡡࡴࠢឹ"))
    def log_error(self, message):
        self.bstack11l1llll111_opy_(message + bstack111l_opy_ (u"ࠧࡢ࡮ࠣឺ"))
    def bstack11l1ll11111_opy_(self, level, original_func):
        def bstack11l1ll11l11_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack111l_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢុ") in message or bstack111l_opy_ (u"ࠢ࡜ࡕࡇࡏࡈࡒࡉ࡞ࠤូ") in message or bstack111l_opy_ (u"ࠣ࡝࡚ࡩࡧࡊࡲࡪࡸࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠧួ") in message:
                        return return_value
                    bstack11l1lllll1l_opy_ = TestFramework.bstack11ll111ll11_opy_()
                    if not bstack11l1lllll1l_opy_:
                        return return_value
                    bstack1lll1l1lll_opy_ = next(
                        (
                            instance
                            for instance in bstack11l1lllll1l_opy_
                            if TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
                        ),
                        None,
                    )
                    if not bstack1lll1l1lll_opy_:
                        return return_value
                    entry = bstack11lllllll1_opy_(TestFramework.bstack11l1lllll11_opy_, message, level)
                    self.bstack11l1lll11_opy_(bstack1lll1l1lll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack11l1ll11l11_opy_
    def bstack11ll111111l_opy_(self):
        def bstack11l1ll1l11l_opy_(*args, **kwargs):
            try:
                self.bstack11ll111l1l1_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack111l_opy_ (u"ࠩࠣࠫើ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack111l_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦឿ") in message:
                    return
                bstack11l1lllll1l_opy_ = TestFramework.bstack11ll111ll11_opy_()
                if not bstack11l1lllll1l_opy_:
                    return
                bstack1lll1l1lll_opy_ = next(
                    (
                        instance
                        for instance in bstack11l1lllll1l_opy_
                        if TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
                    ),
                    None,
                )
                if not bstack1lll1l1lll_opy_:
                    return
                entry = bstack11lllllll1_opy_(TestFramework.bstack11l1lllll11_opy_, message, bstack1l1ll111ll_opy_.bstack11ll111l11l_opy_)
                self.bstack11l1lll11_opy_(bstack1lll1l1lll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack11ll111l1l1_opy_(bstack1l11lll11ll_opy_ (u"ࠦࡠࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࡣࠠࡍࡱࡪࠤࡨࡧࡰࡵࡷࡵࡩࠥ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡥࡾࠤៀ"))
                except:
                    pass
        return bstack11l1ll1l11l_opy_
    def bstack11ll1111ll1_opy_(self, event: dict, instance=None) -> None:
        global _11ll1111l1l_opy_
        levels = [bstack111l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣេ"), bstack111l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥែ")]
        bstack1l1l1l1l1l1_opy_ = bstack111l_opy_ (u"ࠢࠣៃ")
        if instance is not None:
            try:
                bstack1l1l1l1l1l1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
            except Exception as e:
                self.logger.warning(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡷࡸ࡭ࡩࠦࡦࡳࡱࡰࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠨោ").format(e))
        bstack11l1llll1ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩៅ")]
                bstack1l1l1l1l1ll_opy_ = os.path.join(bstack11l1llll1l1_opy_, (bstack11ll111llll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1l1l1l1ll_opy_):
                    self.logger.debug(bstack111l_opy_ (u"ࠥࡈ࡮ࡸࡥࡤࡶࡲࡶࡾࠦ࡮ࡰࡶࠣࡴࡷ࡫ࡳࡦࡰࡷࠤ࡫ࡵࡲࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡚ࠥࡥࡴࡶࠣࡥࡳࡪࠠࡃࡷ࡬ࡰࡩࠦ࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨំ").format(bstack1l1l1l1l1ll_opy_))
                    continue
                file_names = os.listdir(bstack1l1l1l1l1ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1l1l1l1ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _11ll1111l1l_opy_:
                        self.logger.info(bstack111l_opy_ (u"ࠦࡕࡧࡴࡩࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡻࡾࠤះ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l1ll111l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l1ll111l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack111l_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣៈ"):
                                entry = bstack11lllllll1_opy_(
                                    kind=bstack111l_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ៉"),
                                    message=bstack111l_opy_ (u"ࠢࠣ៊"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l11ll1l1_opy_=file_size,
                                    bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣ់"),
                                    bstack1lllllll_opy_=os.path.abspath(file_path),
                                    bstack1ll1l1l11l_opy_=bstack1l1l1l1l1l1_opy_
                                )
                            elif level == bstack111l_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨ៌"):
                                entry = bstack11lllllll1_opy_(
                                    kind=bstack111l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ៍"),
                                    message=bstack111l_opy_ (u"ࠦࠧ៎"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l11ll1l1_opy_=file_size,
                                    bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧ៏"),
                                    bstack1lllllll_opy_=os.path.abspath(file_path),
                                    bstack11ll1111111_opy_=bstack1l1l1l1l1l1_opy_
                                )
                            bstack11l1llll1ll_opy_.append(entry)
                            _11ll1111l1l_opy_.add(abs_path)
                        except Exception as bstack1l1ll1ll111_opy_:
                            self.logger.error(bstack111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧ័").format(bstack1l1ll1ll111_opy_))
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨ៑").format(e))
        event[bstack111l_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨ្")] = bstack11l1llll1ll_opy_
class bstack11l1ll1l111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11ll11111l1_opy_ = set()
        kwargs[bstack111l_opy_ (u"ࠤࡶ࡯࡮ࡶ࡫ࡦࡻࡶࠦ៓")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack11ll11l1111_opy_(obj, self.bstack11ll11111l1_opy_)
def bstack11ll11l11ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack11ll11l1111_opy_(obj, bstack11ll11111l1_opy_=None, max_depth=3):
    if bstack11ll11111l1_opy_ is None:
        bstack11ll11111l1_opy_ = set()
    if id(obj) in bstack11ll11111l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11ll11111l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack11l1lll1ll1_opy_ = TestFramework.bstack11l1lll1l11_opy_(obj)
    bstack11ll111ll1l_opy_ = next((k.lower() in bstack11l1lll1ll1_opy_.lower() for k in bstack11ll11l1lll_opy_.keys()), None)
    if bstack11ll111ll1l_opy_:
        obj = TestFramework.bstack11l1ll1ll11_opy_(obj, bstack11ll11l1lll_opy_[bstack11ll111ll1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack111l_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨ។")):
            keys = getattr(obj, bstack111l_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢ៕"), [])
        elif hasattr(obj, bstack111l_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢ៖")):
            keys = getattr(obj, bstack111l_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣៗ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack111l_opy_ (u"ࠢࡠࠤ៘"))}
        if not obj and bstack11l1lll1ll1_opy_ == bstack111l_opy_ (u"ࠣࡲࡤࡸ࡭ࡲࡩࡣ࠰ࡓࡳࡸ࡯ࡸࡑࡣࡷ࡬ࠧ៙"):
            obj = {bstack111l_opy_ (u"ࠤࡳࡥࡹ࡮ࠢ៚"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack11ll11l11ll_opy_(key) or str(key).startswith(bstack111l_opy_ (u"ࠥࡣࠧ៛")):
            continue
        if value is not None and bstack11ll11l11ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack11ll11l1111_opy_(value, bstack11ll11111l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack11ll11l1111_opy_(o, bstack11ll11111l1_opy_, max_depth) for o in value]))
    return result or None