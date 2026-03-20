# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import bstack1ll11llllll_opy_, bstack111ll1lll1_opy_, bstack11lllll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1lll111_opy_ import bstack1l1ll111111_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111l1111_opy_, TestHookState, bstack1l1ll1111ll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack11l1111l1l_opy_, bstack11lllll1lll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack11lllllll11_opy_ = [bstack11lll1_opy_ (u"ࠥࡲࡦࡳࡥࠣᕬ"), bstack11lll1_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᕭ"), bstack11lll1_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧᕮ"), bstack11lll1_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࠢᕯ"), bstack11lll1_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᕰ")]
bstack1l1111l1lll_opy_ = bstack11lllll1lll_opy_()
bstack1l1111l11ll_opy_ = bstack11lll1_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᕱ")
bstack1l111111lll_opy_ = {
    bstack11lll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢᕲ"): bstack11lllllll11_opy_,
    bstack11lll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦᕳ"): bstack11lllllll11_opy_,
    bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦᕴ"): bstack11lllllll11_opy_,
    bstack11lll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦᕵ"): bstack11lllllll11_opy_,
    bstack11lll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣᕶ"): bstack11lllllll11_opy_
    + [
        bstack11lll1_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨᕷ"),
        bstack11lll1_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᕸ"),
        bstack11lll1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢᕹ"),
        bstack11lll1_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᕺ"),
        bstack11lll1_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨᕻ"),
        bstack11lll1_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨᕼ"),
        bstack11lll1_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᕽ"),
        bstack11lll1_opy_ (u"ࠢࡴࡶࡲࡴࠧᕾ"),
        bstack11lll1_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥᕿ"),
        bstack11lll1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᖀ"),
    ],
    bstack11lll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤᖁ"): [bstack11lll1_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢᖂ"), bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥᖃ"), bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᖄ"), bstack11lll1_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨᖅ")],
    bstack11lll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣᖆ"): [bstack11lll1_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨᖇ"), bstack11lll1_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᖈ")],
    bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥᖉ"): [bstack11lll1_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᖊ"), bstack11lll1_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᖋ"), bstack11lll1_opy_ (u"ࠢࡧࡷࡱࡧࠧᖌ"), bstack11lll1_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᖍ"), bstack11lll1_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᖎ"), bstack11lll1_opy_ (u"ࠥ࡭ࡩࡹࠢᖏ")],
    bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥᖐ"): [bstack11lll1_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᖑ"), bstack11lll1_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧᖒ"), bstack11lll1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧᖓ")],
    bstack11lll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥᖔ"): [bstack11lll1_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᖕ"), bstack11lll1_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥᖖ")],
    bstack11lll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧᖗ"): [bstack11lll1_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᖘ"), bstack11lll1_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᖙ")],
    bstack11lll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢᖚ"): [bstack11lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨᖛ"), bstack11lll1_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᖜ"), bstack11lll1_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥᖝ")],
}
_1l11111l1ll_opy_ = set()
class bstack11lll11ll_opy_(bstack1l1lllllll1_opy_):
    bstack1l111l1l111_opy_ = bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦᖞ")
    bstack1l111llll11_opy_ = bstack11lll1_opy_ (u"ࠧࡏࡎࡇࡑࠥᖟ")
    bstack1l1111l1ll1_opy_ = bstack11lll1_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧᖠ")
    bstack1l11111ll1l_opy_: Callable
    bstack1l111l11111_opy_: Callable
    def __init__(self, bstack1l1llll1lll_opy_, bstack1l1l1l1l11l_opy_):
        super().__init__()
        self.bstack1l1l1111111_opy_ = bstack1l1l1l1l11l_opy_
        if os.getenv(bstack11lll1_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦᖡ"), bstack11lll1_opy_ (u"ࠣ࠳ࠥᖢ")) != bstack11lll1_opy_ (u"ࠤ࠴ࠦᖣ") or not self.is_enabled():
            return
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l111111l_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l1111_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1l111lll1_opy_((event, state), self.bstack1l111lll111_opy_)
        bstack1l1llll1lll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.POST), self.bstack1l111ll1lll_opy_)
        self.bstack1l11111ll1l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l111l11ll1_opy_(bstack11lll11ll_opy_.bstack1l111llll11_opy_, self.bstack1l11111ll1l_opy_)
        self.bstack1l111l11111_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l111l11ll1_opy_(bstack11lll11ll_opy_.bstack1l1111l1ll1_opy_, self.bstack1l111l11111_opy_)
        self.bstack1l111ll11l1_opy_ = builtins.print
        builtins.print = self.bstack1l11111llll_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l111lll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l111ll1l11_opy_() or f.bstack11lllll1l1l_opy_()) and instance:
            bstack11llllll1l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1l111111_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack111ll1l1_opy_ = datetime.now()
                entries = f.bstack1l1111111l1_opy_(instance, bstack1ll1l111111_opy_)
                if entries:
                    self.bstack11lllll1ll1_opy_(instance, entries)
                    instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥᖤ"), datetime.now() - bstack111ll1l1_opy_)
                    f.bstack1l1111llll1_opy_(instance, bstack1ll1l111111_opy_)
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᖥ"), datetime.now() - bstack11llllll1l1_opy_)
                return # bstack11lllllll1l_opy_ not send this event with the bstack1l111ll1l1l_opy_ bstack1l11111ll11_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1ll11_opy_)
            ):
                f.bstack1ll1ll1l1l_opy_(instance, bstack11lll11ll_opy_.bstack1l111l1l111_opy_, True)
                return # bstack11lllllll1l_opy_ not send this event bstack1l11111l11l_opy_ bstack11llllllll1_opy_
            elif (
                f.bstack1ll1l1l1111_opy_(instance, bstack11lll11ll_opy_.bstack1l111l1l111_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l111l1ll11_opy_)
            ):
                self.bstack1l111lll111_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack111ll1l1_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l111ll1l11_opy_():
                bstack11lllllllll_opy_ = sorted(
                    filter(lambda x: x.get(bstack11lll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᖦ"), None), data.pop(bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᖧ"), {}).values()),
                    key=lambda x: x[bstack11lll1_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᖨ")],
                )
                data.update({bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᖩ"): bstack11lllllllll_opy_})
            elif f.bstack11lllll1l1l_opy_():
                bstack1l111l1l1ll_opy_ = sorted(
                    filter(lambda x: x.get(bstack11lll1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᖪ"), None), data.pop(bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᖫ"), {}).values()),
                    key=lambda x: x[bstack11lll1_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᖬ")],
                )
                data.update({bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᖭ"): bstack1l111l1l1ll_opy_})
            if bstack1l1ll111111_opy_.bstack11llllll11l_opy_ in data:
                data.pop(bstack1l1ll111111_opy_.bstack11llllll11l_opy_)
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᖮ"), datetime.now() - bstack111ll1l1_opy_)
            bstack111ll1l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l111l1ll1l_opy_)
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᖯ"), datetime.now() - bstack111ll1l1_opy_)
            if TestFramework.bstack1l11llll11l_opy_ in data:
                self.bstack1l11111ll11_opy_(instance, bstack1ll1l111111_opy_, event_json=event_json)
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᖰ"), datetime.now() - bstack11llllll1l1_opy_)
    def bstack1l1l111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
        bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l1llll1_opy_.value)
        self.bstack1l1l1111111_opy_.bstack1l111lll11l_opy_(instance, f, bstack1ll1l111111_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1l1111111_opy_.bstack1l111lll1ll_opy_(instance, f, bstack1ll1l111111_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶࠣ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡠࢁࡽ࡞ࠢࡾࢁࡡࡴࡻࡾࠤᖱ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l1111lll11_opy_ data not ready for robot-playwright at the time of bstack1l1l111111l_opy_, so bstack1l1111l1l11_opy_ will send bstack1l1111lll11_opy_ event in bstack1l1l11l1111_opy_ for robot-playwright
            self.bstack1l11111lll1_opy_(f, instance, req)
        bstack1llll11l_opy_.end(EVENTS.bstack11l1llll1_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᖲ"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᖳ"), status=True, failure=None, test_name=None)
    def bstack1l1l11l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1l1l1111_opy_(instance, self.bstack1l1l1111111_opy_.bstack1l1111111ll_opy_, False):
            try:
                req = self.bstack1l1l1111111_opy_.bstack1l111lll1ll_opy_(instance, f, bstack1ll1l111111_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack11lll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸࠥ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿࡛ࠦࡼࡿࡠࠤࢀࢃ࡜࡯ࡽࢀࠦᖴ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l11111lll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l111111l11_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲ࠺ࠡࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠤᖵ"))
            return
        bstack111ll1l1_opy_ = datetime.now()
        try:
            r = self.bstack1l1lll11l11_opy_.TestSessionEvent(req)
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡨࡺࡪࡴࡴࠣᖶ"), datetime.now() - bstack111ll1l1_opy_)
            f.bstack1ll1ll1l1l_opy_(instance, self.bstack1l1l1111111_opy_.bstack1l1111111ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11lll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᖷ") + str(r) + bstack11lll1_opy_ (u"ࠤࠥᖸ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᖹ") + str(e) + bstack11lll1_opy_ (u"ࠦࠧᖺ"))
            traceback.print_exc()
            raise e
    def bstack1l111ll1lll_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        _driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        _1l1111ll1l1_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll111l11ll_opy_.bstack1l11ll1ll11_opy_(method_name):
            return
        if f.bstack1l11l1lll11_opy_(*args) == bstack1ll111l11ll_opy_.bstack1l111l1lll1_opy_:
            bstack11llllll1l1_opy_ = datetime.now()
            screenshot = result.get(bstack11lll1_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᖻ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11lll1_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡮ࡳࡡࡨࡧࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡹࡸࠢᖼ"))
                return
            bstack1l1111lllll_opy_ = self.bstack11llllll111_opy_(instance)
            if bstack1l1111lllll_opy_:
                entry = bstack1l1ll1111ll_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack11lllll1ll1_opy_(bstack1l1111lllll_opy_, [entry])
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡦࡺࡨࡧࡺࡺࡥࠣᖽ"), datetime.now() - bstack11llllll1l1_opy_)
            else:
                self.logger.warning(bstack11lll1_opy_ (u"ࠣࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡧࡶࡸࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶ࡫࡭ࡸࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡻࡦࡹࠠࡵࡣ࡮ࡩࡳࠦࡢࡺࠢࡧࡶ࡮ࡼࡥࡳ࠿ࠣࡿࢂࠨᖾ").format(instance.ref()))
        event = {}
        bstack1l1111lllll_opy_ = self.bstack11llllll111_opy_(instance)
        if bstack1l1111lllll_opy_:
            self.bstack1l111lll1l1_opy_(event, bstack1l1111lllll_opy_)
            if event.get(bstack11lll1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᖿ")):
                self.bstack11lllll1ll1_opy_(bstack1l1111lllll_opy_, event[bstack11lll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᗀ")])
            else:
                self.logger.debug(bstack11lll1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡰࡴ࡭ࡳࠡࡨࡲࡶࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡨࡺࡪࡴࡴࠣᗁ"))
    @measure(event_name=EVENTS.bstack1l111l11l11_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack11lllll1ll1_opy_(
        self,
        bstack1l1111lllll_opy_: bstack1ll111l1111_opy_,
        entries: List[bstack1l1ll1111ll_opy_],
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll1ll1_opy_)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᗂ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1111lllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1111lllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1111lllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11lll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l111l11lll_opy_)
            log_entry.uuid = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack1l11llll11l_opy_)
            log_entry.test_framework_state = bstack1l1111lllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᗃ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11lll1_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᗄ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11111111l_opy_
                log_entry.file_path = entry.bstack11111l1_opy_
        def bstack1l111111ll1_opy_():
            bstack111ll1l1_opy_ = datetime.now()
            try:
                self.bstack1l1lll11l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l1111lllll_opy_.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᗅ"), datetime.now() - bstack111ll1l1_opy_)
                elif entry.kind == TestFramework.bstack1l111ll1ll1_opy_:
                    bstack1l1111lllll_opy_.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᗆ"), datetime.now() - bstack111ll1l1_opy_)
                else:
                    bstack1l1111lllll_opy_.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡰࡴ࡭ࠢᗇ"), datetime.now() - bstack111ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lll1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᗈ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l111111ll1_opy_)
    @measure(event_name=EVENTS.bstack1l111l111l1_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11111ll11_opy_(
        self,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll1ll1_opy_)
        req.client_worker_id = bstack11lll1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᗉ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll111l_opy_)
        req.test_framework_version = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l111l11lll_opy_)
        req.test_framework_state = bstack1ll1l111111_opy_[0].name
        req.test_hook_state = bstack1ll1l111111_opy_[1].name
        started_at = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l111l1llll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l111l1111l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l111l1ll1l_opy_)).encode(bstack11lll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᗊ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l111111ll1_opy_():
            bstack111ll1l1_opy_ = datetime.now()
            try:
                self.bstack1l1lll11l11_opy_.TestFrameworkEvent(req)
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡪࡼࡥ࡯ࡶࠥᗋ"), datetime.now() - bstack111ll1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lll1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᗌ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1l11l1l1_opy_.enqueue(bstack1l111111ll1_opy_)
    def bstack11llllll111_opy_(self, instance: bstack1ll11llllll_opy_):
        bstack1l111111111_opy_ = TestFramework.bstack1ll11lllll1_opy_(instance.context)
        for t in bstack1l111111111_opy_:
            bstack1l111llll1l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(t, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
            if not bstack11l1111l1l_opy_() and len(bstack1l111llll1l_opy_) == 0:
                bstack1l111llll1l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(t, bstack1l1ll111111_opy_.bstack1l1111ll11l_opy_, [])
            if any(instance is d[1] for d in bstack1l111llll1l_opy_):
                return t
    def bstack1l1111l11l1_opy_(self, message):
        self.bstack1l11111ll1l_opy_(message + bstack11lll1_opy_ (u"ࠤ࡟ࡲࠧᗍ"))
    def log_error(self, message):
        self.bstack1l111l11111_opy_(message + bstack11lll1_opy_ (u"ࠥࡠࡳࠨᗎ"))
    def bstack1l111l11ll1_opy_(self, level, original_func):
        def bstack1l111ll111l_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack11lll1_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧᗏ") in message or bstack11lll1_opy_ (u"ࠧࡡࡓࡅࡍࡆࡐࡎࡣࠢᗐ") in message or bstack11lll1_opy_ (u"ࠨ࡛ࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠥᗑ") in message:
                        return return_value
                    bstack1l111111111_opy_ = TestFramework.bstack1l111l1l11l_opy_()
                    if not bstack1l111111111_opy_:
                        return return_value
                    bstack1l1111lllll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l111111111_opy_
                            if TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
                        ),
                        None,
                    )
                    if not bstack1l1111lllll_opy_:
                        return return_value
                    entry = bstack1l1ll1111ll_opy_(TestFramework.bstack11lllll1l11_opy_, message, level)
                    self.bstack11lllll1ll1_opy_(bstack1l1111lllll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l111ll111l_opy_
    def bstack1l11111llll_opy_(self):
        def bstack1l111l1l1l1_opy_(*args, **kwargs):
            try:
                self.bstack1l111ll11l1_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack11lll1_opy_ (u"ࠧࠡࠩᗒ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack11lll1_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤᗓ") in message:
                    return
                bstack1l111111111_opy_ = TestFramework.bstack1l111l1l11l_opy_()
                if not bstack1l111111111_opy_:
                    return
                bstack1l1111lllll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l111111111_opy_
                        if TestFramework.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
                    ),
                    None,
                )
                if not bstack1l1111lllll_opy_:
                    return
                entry = bstack1l1ll1111ll_opy_(TestFramework.bstack11lllll1l11_opy_, message, bstack11lll11ll_opy_.bstack1l111llll11_opy_)
                self.bstack11lllll1ll1_opy_(bstack1l1111lllll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111ll11l1_opy_(bstack1ll11ll1ll1_opy_ (u"ࠤ࡞ࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠥࡒ࡯ࡨࠢࡦࡥࡵࡺࡵࡳࡧࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢᗔ"))
                except:
                    pass
        return bstack1l111l1l1l1_opy_
    def bstack1l111lll1l1_opy_(self, event: dict, instance=None) -> None:
        global _1l11111l1ll_opy_
        levels = [bstack11lll1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᗕ"), bstack11lll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᗖ")]
        bstack1l11111l1l1_opy_ = bstack11lll1_opy_ (u"ࠧࠨᗗ")
        if instance is not None:
            try:
                bstack1l11111l1l1_opy_ = TestFramework.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
            except Exception as e:
                self.logger.warning(bstack11lll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᗘ").format(e))
        bstack1l111l11l1l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᗙ")]
                bstack1l1111l111l_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l1111l11ll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1111l111l_opy_):
                    self.logger.debug(bstack11lll1_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᗚ").format(bstack1l1111l111l_opy_))
                    continue
                file_names = os.listdir(bstack1l1111l111l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1111l111l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11111l1ll_opy_:
                        self.logger.info(bstack11lll1_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᗛ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1111l1l1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1111l1l1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11lll1_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᗜ"):
                                entry = bstack1l1ll1111ll_opy_(
                                    kind=bstack11lll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᗝ"),
                                    message=bstack11lll1_opy_ (u"ࠧࠨᗞ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11111111l_opy_=file_size,
                                    bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᗟ"),
                                    bstack11111l1_opy_=os.path.abspath(file_path),
                                    bstack1l11l1lll_opy_=bstack1l11111l1l1_opy_
                                )
                            elif level == bstack11lll1_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᗠ"):
                                entry = bstack1l1ll1111ll_opy_(
                                    kind=bstack11lll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᗡ"),
                                    message=bstack11lll1_opy_ (u"ࠤࠥᗢ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11111111l_opy_=file_size,
                                    bstack1l1111l1111_opy_=bstack11lll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᗣ"),
                                    bstack11111l1_opy_=os.path.abspath(file_path),
                                    bstack1l111l111ll_opy_=bstack1l11111l1l1_opy_
                                )
                            bstack1l111l11l1l_opy_.append(entry)
                            _1l11111l1ll_opy_.add(abs_path)
                        except Exception as bstack1l1111ll1ll_opy_:
                            self.logger.error(bstack11lll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᗤ").format(bstack1l1111ll1ll_opy_))
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᗥ").format(e))
        event[bstack11lll1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᗦ")] = bstack1l111l11l1l_opy_
class bstack1l111l1ll1l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack11llllll1ll_opy_ = set()
        kwargs[bstack11lll1_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤᗧ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l111111l1l_opy_(obj, self.bstack11llllll1ll_opy_)
def bstack1l111ll1111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l111111l1l_opy_(obj, bstack11llllll1ll_opy_=None, max_depth=3):
    if bstack11llllll1ll_opy_ is None:
        bstack11llllll1ll_opy_ = set()
    if id(obj) in bstack11llllll1ll_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack11llllll1ll_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111ll11ll_opy_ = TestFramework.bstack1l1111lll1l_opy_(obj)
    bstack1l11111l111_opy_ = next((k.lower() in bstack1l111ll11ll_opy_.lower() for k in bstack1l111111lll_opy_.keys()), None)
    if bstack1l11111l111_opy_:
        obj = TestFramework.bstack1l1111ll111_opy_(obj, bstack1l111111lll_opy_[bstack1l11111l111_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11lll1_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦᗨ")):
            keys = getattr(obj, bstack11lll1_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᗩ"), [])
        elif hasattr(obj, bstack11lll1_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧᗪ")):
            keys = getattr(obj, bstack11lll1_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᗫ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11lll1_opy_ (u"ࠧࡥࠢᗬ"))}
        if not obj and bstack1l111ll11ll_opy_ == bstack11lll1_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥᗭ"):
            obj = {bstack11lll1_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᗮ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111ll1111_opy_(key) or str(key).startswith(bstack11lll1_opy_ (u"ࠣࡡࠥᗯ")):
            continue
        if value is not None and bstack1l111ll1111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l111111l1l_opy_(value, bstack11llllll1ll_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l111111l1l_opy_(o, bstack11llllll1ll_opy_, max_depth) for o in value]))
    return result or None