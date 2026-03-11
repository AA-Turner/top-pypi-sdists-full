# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1l1l111l_opy_, bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll111_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll11l1ll1l_opy_, TestHookState, bstack1l1ll11l111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1lll111l1_opy_, bstack1l1111ll1ll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l11l11l111_opy_ = [bstack1ll111_opy_ (u"ࠥࡲࡦࡳࡥࠣᓼ"), bstack1ll111_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᓽ"), bstack1ll111_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧᓾ"), bstack1ll111_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࠢᓿ"), bstack1ll111_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᔀ")]
bstack1l1111l1lll_opy_ = bstack1l1111ll1ll_opy_()
bstack1l111ll1111_opy_ = bstack1ll111_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣᔁ")
bstack1l111l1111l_opy_ = {
    bstack1ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢᔂ"): bstack1l11l11l111_opy_,
    bstack1ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦᔃ"): bstack1l11l11l111_opy_,
    bstack1ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦᔄ"): bstack1l11l11l111_opy_,
    bstack1ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦᔅ"): bstack1l11l11l111_opy_,
    bstack1ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣᔆ"): bstack1l11l11l111_opy_
    + [
        bstack1ll111_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨᔇ"),
        bstack1ll111_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᔈ"),
        bstack1ll111_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢᔉ"),
        bstack1ll111_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᔊ"),
        bstack1ll111_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨᔋ"),
        bstack1ll111_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨᔌ"),
        bstack1ll111_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧᔍ"),
        bstack1ll111_opy_ (u"ࠢࡴࡶࡲࡴࠧᔎ"),
        bstack1ll111_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥᔏ"),
        bstack1ll111_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᔐ"),
    ],
    bstack1ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤᔑ"): [bstack1ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢᔒ"), bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥᔓ"), bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢᔔ"), bstack1ll111_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨᔕ")],
    bstack1ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣᔖ"): [bstack1ll111_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨᔗ"), bstack1ll111_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᔘ")],
    bstack1ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥᔙ"): [bstack1ll111_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦᔚ"), bstack1ll111_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢᔛ"), bstack1ll111_opy_ (u"ࠢࡧࡷࡱࡧࠧᔜ"), bstack1ll111_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣᔝ"), bstack1ll111_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦᔞ"), bstack1ll111_opy_ (u"ࠥ࡭ࡩࡹࠢᔟ")],
    bstack1ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥᔠ"): [bstack1ll111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥᔡ"), bstack1ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧᔢ"), bstack1ll111_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧᔣ")],
    bstack1ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥᔤ"): [bstack1ll111_opy_ (u"ࠤࡺ࡬ࡪࡴࠢᔥ"), bstack1ll111_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥᔦ")],
    bstack1ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧᔧ"): [bstack1ll111_opy_ (u"ࠧࡴ࡯ࡥࡧࠥᔨ"), bstack1ll111_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨᔩ")],
    bstack1ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢᔪ"): [bstack1ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨᔫ"), bstack1ll111_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᔬ"), bstack1ll111_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥᔭ")],
}
_1l111ll1lll_opy_ = set()
class bstack1ll11l1lll_opy_(bstack1ll11111l11_opy_):
    bstack1l1111llll1_opy_ = bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦᔮ")
    bstack1l111l1lll1_opy_ = bstack1ll111_opy_ (u"ࠧࡏࡎࡇࡑࠥᔯ")
    bstack1l11l1l111l_opy_ = bstack1ll111_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧᔰ")
    bstack1l11l111l11_opy_: Callable
    bstack1l11l1111ll_opy_: Callable
    def __init__(self, bstack1l1ll1l1lll_opy_, bstack1l1lllllll1_opy_):
        super().__init__()
        self.bstack1l1l11l1111_opy_ = bstack1l1lllllll1_opy_
        if os.getenv(bstack1ll111_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦᔱ"), bstack1ll111_opy_ (u"ࠣ࠳ࠥᔲ")) != bstack1ll111_opy_ (u"ࠤ࠴ࠦᔳ") or not self.is_enabled():
            return
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11ll1ll_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll111l_opy_)
        for event in TestFrameworkState:
            for state in TestHookState:
                TestFramework.bstack1l1l1111111_opy_((event, state), self.bstack1l1111lll11_opy_)
        bstack1l1ll1l1lll_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.POST), self.bstack1l1111l11l1_opy_)
        self.bstack1l11l111l11_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11l1l1l11_opy_(bstack1ll11l1lll_opy_.bstack1l111l1lll1_opy_, self.bstack1l11l111l11_opy_)
        self.bstack1l11l1111ll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11l1l1l11_opy_(bstack1ll11l1lll_opy_.bstack1l11l1l111l_opy_, self.bstack1l11l1111ll_opy_)
        self.bstack1l11l11llll_opy_ = builtins.print
        builtins.print = self.bstack1l11l111111_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if (f.bstack1l111ll111l_opy_() or f.bstack1l1111lllll_opy_()) and instance:
            bstack1l11l111ll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1l1l1l1l_opy_
            if test_framework_state == TestFrameworkState.SETUP_FIXTURE:
                return
            elif test_framework_state == TestFrameworkState.LOG:
                bstack1ll1l1l111_opy_ = datetime.now()
                entries = f.bstack1l11111l1ll_opy_(instance, bstack1ll1l1l1l1l_opy_)
                if entries:
                    self.bstack1l11l11l11l_opy_(instance, entries)
                    instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥᔴ"), datetime.now() - bstack1ll1l1l111_opy_)
                    f.bstack1l11l11111l_opy_(instance, bstack1ll1l1l1l1l_opy_)
                instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᔵ"), datetime.now() - bstack1l11l111ll1_opy_)
                return # bstack1l111l11ll1_opy_ not send this event with the bstack1l111ll11ll_opy_ bstack1l111l111l1_opy_
            elif (
                test_framework_state == TestFrameworkState.TEST
                and test_hook_state == TestHookState.POST
                and not f.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l111llll11_opy_)
            ):
                f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11l1lll_opy_.bstack1l1111llll1_opy_, True)
                return # bstack1l111l11ll1_opy_ not send this event bstack1l111l11l11_opy_ bstack1l111ll11l1_opy_
            elif (
                f.bstack1lll111lll1_opy_(instance, bstack1ll11l1lll_opy_.bstack1l1111llll1_opy_, False)
                and test_framework_state == TestFrameworkState.LOG_REPORT
                and test_hook_state == TestHookState.POST
                and f.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l111llll11_opy_)
            ):
                self.bstack1l1111lll11_opy_(f, instance, (TestFrameworkState.TEST, TestHookState.POST), *args, **kwargs)
            bstack1ll1l1l111_opy_ = datetime.now()
            data = instance.data.copy()
            if f.bstack1l111ll111l_opy_():
                bstack1l111ll1l11_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll111_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᔶ"), None), data.pop(bstack1ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᔷ"), {}).values()),
                    key=lambda x: x[bstack1ll111_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᔸ")],
                )
                data.update({bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᔹ"): bstack1l111ll1l11_opy_})
            elif f.bstack1l1111lllll_opy_():
                bstack1l111ll1l1l_opy_ = sorted(
                    filter(lambda x: x.get(bstack1ll111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᔺ"), None), data.pop(bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᔻ"), {}).values()),
                    key=lambda x: x[bstack1ll111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᔼ")],
                )
                data.update({bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢ࡯ࡪࡿࡷࡰࡴࡧࡷࠧᔽ"): bstack1l111ll1l1l_opy_})
            if bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_ in data:
                data.pop(bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_)
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᔾ"), datetime.now() - bstack1ll1l1l111_opy_)
            bstack1ll1l1l111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1111l1ll1_opy_)
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᔿ"), datetime.now() - bstack1ll1l1l111_opy_)
            if TestFramework.bstack1l1l1ll11ll_opy_ in data:
                self.bstack1l111l111l1_opy_(instance, bstack1ll1l1l1l1l_opy_, event_json=event_json)
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᕀ"), datetime.now() - bstack1l11l111ll1_opy_)
    def bstack1l1l11ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
        bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1lllll11l1_opy_.value)
        self.bstack1l1l11l1111_opy_.bstack1l111lll1l1_opy_(instance, f, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        try:
            req = self.bstack1l1l11l1111_opy_.bstack1l111llll1l_opy_(instance, f, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶࠣ࡫ࡪࡺ࡟ࡤࡤࡷࡣࡪࡼࡥ࡯ࡶࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࡠࢁࡽ࡞ࠢࡾࢁࡡࡴࡻࡾࠤᕁ").format(type(e).__name__, e, traceback.format_exc()))
            req = None
        if not is_robot_playwright_installed(): # bstack1l111l1ll11_opy_ data not ready for robot-playwright at the time of bstack1l1l11ll1ll_opy_, so bstack1l11l1l1111_opy_ will send bstack1l111l1ll11_opy_ event in bstack1l11lll111l_opy_ for robot-playwright
            self.bstack1l11l11lll1_opy_(f, instance, req)
        bstack111ll11111_opy_.end(EVENTS.bstack1lllll11l1_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᕂ"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᕃ"), status=True, failure=None, test_name=None)
    def bstack1l11lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll111lll1_opy_(instance, self.bstack1l1l11l1111_opy_.bstack1l111l1l111_opy_, False):
            try:
                req = self.bstack1l1l11l1111_opy_.bstack1l111llll1l_opy_(instance, f, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
            except Exception as e:
                self.logger.error(bstack1ll111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸࠥ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸࠥ࡬ࡡࡪ࡮ࡨࡨ࠿࡛ࠦࡼࡿࡠࠤࢀࢃ࡜࡯ࡽࢀࠦᕄ").format(type(e).__name__, e, traceback.format_exc()))
                req = None
            self.bstack1l11l11lll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1111l11ll_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l11l11lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲ࠺ࠡࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠤᕅ"))
            return
        bstack1ll1l1l111_opy_ = datetime.now()
        try:
            r = self.bstack1ll1lll11ll_opy_.TestSessionEvent(req)
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡨࡺࡪࡴࡴࠣᕆ"), datetime.now() - bstack1ll1l1l111_opy_)
            f.bstack1ll1ll1lll1_opy_(instance, self.bstack1l1l11l1111_opy_.bstack1l111l1l111_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᕇ") + str(r) + bstack1ll111_opy_ (u"ࠤࠥᕈ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᕉ") + str(e) + bstack1ll111_opy_ (u"ࠦࠧᕊ"))
            traceback.print_exc()
            raise e
    def bstack1l1111l11l1_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        _1l1111l1111_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll11lll111_opy_.bstack1l1l111111l_opy_(method_name):
            return
        if f.bstack1l1l11l1l11_opy_(*args) == bstack1ll11lll111_opy_.bstack1l11l11ll11_opy_:
            bstack1l11l111ll1_opy_ = datetime.now()
            screenshot = result.get(bstack1ll111_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦᕋ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll111_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡮ࡳࡡࡨࡧࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡹࡸࠢᕌ"))
                return
            bstack1l111l11l1l_opy_ = self.bstack1l11111ll1l_opy_(instance)
            if bstack1l111l11l1l_opy_:
                entry = bstack1l1ll11l111_opy_(TestFramework.KIND_SCREENSHOT, screenshot)
                self.bstack1l11l11l11l_opy_(bstack1l111l11l1l_opy_, [entry])
                instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡦࡺࡨࡧࡺࡺࡥࠣᕍ"), datetime.now() - bstack1l11l111ll1_opy_)
            else:
                self.logger.warning(bstack1ll111_opy_ (u"ࠣࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡧࡶࡸࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶ࡫࡭ࡸࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡻࡦࡹࠠࡵࡣ࡮ࡩࡳࠦࡢࡺࠢࡧࡶ࡮ࡼࡥࡳ࠿ࠣࡿࢂࠨᕎ").format(instance.ref()))
        event = {}
        bstack1l111l11l1l_opy_ = self.bstack1l11111ll1l_opy_(instance)
        if bstack1l111l11l1l_opy_:
            self.bstack1l1111lll1l_opy_(event, bstack1l111l11l1l_opy_)
            if event.get(bstack1ll111_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᕏ")):
                self.bstack1l11l11l11l_opy_(bstack1l111l11l1l_opy_, event[bstack1ll111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᕐ")])
            else:
                self.logger.debug(bstack1ll111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡰࡴ࡭ࡳࠡࡨࡲࡶࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡨࡺࡪࡴࡴࠣᕑ"))
    @measure(event_name=EVENTS.bstack1l111lll11l_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l11l11l11l_opy_(
        self,
        bstack1l111l11l1l_opy_: bstack1ll11l1ll1l_opy_,
        entries: List[bstack1l1ll11l111_opy_],
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack1ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕒ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111l11l1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111l11l1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111l11l1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l11llllll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l111l111ll_opy_)
            log_entry.uuid = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l1l1ll11ll_opy_)
            log_entry.test_framework_state = bstack1l111l11l1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᕓ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll111_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᕔ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111lll111_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1111l1l11_opy_():
            bstack1ll1l1l111_opy_ = datetime.now()
            try:
                self.bstack1ll1lll11ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.KIND_SCREENSHOT:
                    bstack1l111l11l1l_opy_.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧᕕ"), datetime.now() - bstack1ll1l1l111_opy_)
                elif entry.kind == TestFramework.bstack1l11111ll11_opy_:
                    bstack1l111l11l1l_opy_.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨᕖ"), datetime.now() - bstack1ll1l1l111_opy_)
                else:
                    bstack1l111l11l1l_opy_.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡰࡴ࡭ࠢᕗ"), datetime.now() - bstack1ll1l1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᕘ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1ll1l111_opy_.enqueue(bstack1l1111l1l11_opy_)
    @measure(event_name=EVENTS.bstack1l111l1ll1l_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l111l111l1_opy_(
        self,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        event_json=None,
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack1ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᕙ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l11llllll1_opy_)
        req.test_framework_version = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l111l111ll_opy_)
        req.test_framework_state = bstack1ll1l1l1l1l_opy_[0].name
        req.test_hook_state = bstack1ll1l1l1l1l_opy_[1].name
        started_at = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1111ll111_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l111l1l1ll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1111l1ll1_opy_)).encode(bstack1ll111_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧᕚ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1111l1l11_opy_():
            bstack1ll1l1l111_opy_ = datetime.now()
            try:
                self.bstack1ll1lll11ll_opy_.TestFrameworkEvent(req)
                instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡪࡼࡥ࡯ࡶࠥᕛ"), datetime.now() - bstack1ll1l1l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᕜ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1ll1ll1l111_opy_.enqueue(bstack1l1111l1l11_opy_)
    def bstack1l11111ll1l_opy_(self, instance: bstack1ll1l1l111l_opy_):
        bstack1l11l11l1l1_opy_ = TestFramework.bstack1ll1l1111ll_opy_(instance.context)
        for t in bstack1l11l11l1l1_opy_:
            bstack1l11l111lll_opy_ = TestFramework.bstack1lll111lll1_opy_(t, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
            if not bstack1lll111l1_opy_() and len(bstack1l11l111lll_opy_) == 0:
                bstack1l11l111lll_opy_ = TestFramework.bstack1lll111lll1_opy_(t, bstack1ll111l1lll_opy_.bstack1l111l1l11l_opy_, [])
            if any(instance is d[1] for d in bstack1l11l111lll_opy_):
                return t
    def bstack1l1111ll1l1_opy_(self, message):
        self.bstack1l11l111l11_opy_(message + bstack1ll111_opy_ (u"ࠤ࡟ࡲࠧᕝ"))
    def log_error(self, message):
        self.bstack1l11l1111ll_opy_(message + bstack1ll111_opy_ (u"ࠥࡠࡳࠨᕞ"))
    def bstack1l11l1l1l11_opy_(self, level, original_func):
        def bstack1l1111ll11l_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1ll111_opy_ (u"ࠦࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࠧᕟ") in message or bstack1ll111_opy_ (u"ࠧࡡࡓࡅࡍࡆࡐࡎࡣࠢᕠ") in message or bstack1ll111_opy_ (u"ࠨ࡛ࡘࡧࡥࡈࡷ࡯ࡶࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠥᕡ") in message:
                        return return_value
                    bstack1l11l11l1l1_opy_ = TestFramework.bstack1l11111lll1_opy_()
                    if not bstack1l11l11l1l1_opy_:
                        return return_value
                    bstack1l111l11l1l_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11l11l1l1_opy_
                            if TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111l11l1l_opy_:
                        return return_value
                    entry = bstack1l1ll11l111_opy_(TestFramework.bstack1l11l11ll1l_opy_, message, level)
                    self.bstack1l11l11l11l_opy_(bstack1l111l11l1l_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l1111ll11l_opy_
    def bstack1l11l111111_opy_(self):
        def bstack1l111lll1ll_opy_(*args, **kwargs):
            try:
                self.bstack1l11l11llll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1ll111_opy_ (u"ࠧࠡࠩᕢ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1ll111_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤᕣ") in message:
                    return
                bstack1l11l11l1l1_opy_ = TestFramework.bstack1l11111lll1_opy_()
                if not bstack1l11l11l1l1_opy_:
                    return
                bstack1l111l11l1l_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11l11l1l1_opy_
                        if TestFramework.bstack1ll1l1lllll_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_)
                    ),
                    None,
                )
                if not bstack1l111l11l1l_opy_:
                    return
                entry = bstack1l1ll11l111_opy_(TestFramework.bstack1l11l11ll1l_opy_, message, bstack1ll11l1lll_opy_.bstack1l111l1lll1_opy_)
                self.bstack1l11l11l11l_opy_(bstack1l111l11l1l_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l11l11llll_opy_(bstack1ll1l11llll_opy_ (u"ࠤ࡞ࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠥࡒ࡯ࡨࠢࡦࡥࡵࡺࡵࡳࡧࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࡪࢃࠢᕤ"))
                except:
                    pass
        return bstack1l111lll1ll_opy_
    def bstack1l1111lll1l_opy_(self, event: dict, instance=None) -> None:
        global _1l111ll1lll_opy_
        levels = [bstack1ll111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᕥ"), bstack1ll111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᕦ")]
        bstack1l111l1llll_opy_ = bstack1ll111_opy_ (u"ࠧࠨᕧ")
        if instance is not None:
            try:
                bstack1l111l1llll_opy_ = TestFramework.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦᕨ").format(e))
        bstack1l111l11lll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᕩ")]
                bstack1l111l11111_opy_ = os.path.join(bstack1l1111l1lll_opy_, (bstack1l111ll1111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l111l11111_opy_):
                    self.logger.debug(bstack1ll111_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᕪ").format(bstack1l111l11111_opy_))
                    continue
                file_names = os.listdir(bstack1l111l11111_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l111l11111_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l111ll1lll_opy_:
                        self.logger.info(bstack1ll111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢᕫ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l11l1l11l1_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l11l1l11l1_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᕬ"):
                                entry = bstack1l1ll11l111_opy_(
                                    kind=bstack1ll111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᕭ"),
                                    message=bstack1ll111_opy_ (u"ࠧࠨᕮ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l111lll111_opy_=file_size,
                                    bstack1l111lllll1_opy_=bstack1ll111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨᕯ"),
                                    bstack11l111_opy_=os.path.abspath(file_path),
                                    bstack11ll11ll1_opy_=bstack1l111l1llll_opy_
                                )
                            elif level == bstack1ll111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦᕰ"):
                                entry = bstack1l1ll11l111_opy_(
                                    kind=bstack1ll111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᕱ"),
                                    message=bstack1ll111_opy_ (u"ࠤࠥᕲ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l111lll111_opy_=file_size,
                                    bstack1l111lllll1_opy_=bstack1ll111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᕳ"),
                                    bstack11l111_opy_=os.path.abspath(file_path),
                                    bstack1l11l1l11ll_opy_=bstack1l111l1llll_opy_
                                )
                            bstack1l111l11lll_opy_.append(entry)
                            _1l111ll1lll_opy_.add(abs_path)
                        except Exception as bstack1l1111l1l1l_opy_:
                            self.logger.error(bstack1ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᕴ").format(bstack1l1111l1l1l_opy_))
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᕵ").format(e))
        event[bstack1ll111_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᕶ")] = bstack1l111l11lll_opy_
class bstack1l1111l1ll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l111ll1ll1_opy_ = set()
        kwargs[bstack1ll111_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤᕷ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l11l11l1ll_opy_(obj, self.bstack1l111ll1ll1_opy_)
def bstack1l11111llll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l11l11l1ll_opy_(obj, bstack1l111ll1ll1_opy_=None, max_depth=3):
    if bstack1l111ll1ll1_opy_ is None:
        bstack1l111ll1ll1_opy_ = set()
    if id(obj) in bstack1l111ll1ll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l111ll1ll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1111l111l_opy_ = TestFramework.bstack1l111llllll_opy_(obj)
    bstack1l11l111l1l_opy_ = next((k.lower() in bstack1l1111l111l_opy_.lower() for k in bstack1l111l1111l_opy_.keys()), None)
    if bstack1l11l111l1l_opy_:
        obj = TestFramework.bstack1l11l1111l1_opy_(obj, bstack1l111l1111l_opy_[bstack1l11l111l1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll111_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦᕸ")):
            keys = getattr(obj, bstack1ll111_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᕹ"), [])
        elif hasattr(obj, bstack1ll111_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧᕺ")):
            keys = getattr(obj, bstack1ll111_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᕻ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll111_opy_ (u"ࠧࡥࠢᕼ"))}
        if not obj and bstack1l1111l111l_opy_ == bstack1ll111_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥᕽ"):
            obj = {bstack1ll111_opy_ (u"ࠢࡱࡣࡷ࡬ࠧᕾ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l11111llll_opy_(key) or str(key).startswith(bstack1ll111_opy_ (u"ࠣࡡࠥᕿ")):
            continue
        if value is not None and bstack1l11111llll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l11l11l1ll_opy_(value, bstack1l111ll1ll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l11l11l1ll_opy_(o, bstack1l111ll1ll1_opy_, max_depth) for o in value]))
    return result or None