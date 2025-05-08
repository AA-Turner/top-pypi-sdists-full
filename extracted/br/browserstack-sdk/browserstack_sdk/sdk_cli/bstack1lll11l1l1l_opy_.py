# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import bstack11111ll111_opy_, bstack1llllllllll_opy_, bstack11111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1ll_opy_ import bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1ll1lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11111_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1ll1l1_opy_, bstack1llllll11ll_opy_, bstack1llll1lll1l_opy_, bstack1lll1l111l1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1ll1111lll1_opy_, bstack1l1lll1111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1lll1l111_opy_ = [bstack1l1lll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᆳ"), bstack1l1lll_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᆴ"), bstack1l1lll_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦᆵ"), bstack1l1lll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࠨᆶ"), bstack1l1lll_opy_ (u"ࠨࡰࡢࡶ࡫ࠦᆷ")]
bstack1ll111l1l1l_opy_ = bstack1l1lll1111l_opy_()
bstack1l1ll1lll1l_opy_ = bstack1l1lll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢᆸ")
bstack1ll111l11ll_opy_ = {
    bstack1l1lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡋࡷࡩࡲࠨᆹ"): bstack1l1lll1l111_opy_,
    bstack1l1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡓࡥࡨࡱࡡࡨࡧࠥᆺ"): bstack1l1lll1l111_opy_,
    bstack1l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡑࡴࡪࡵ࡭ࡧࠥᆻ"): bstack1l1lll1l111_opy_,
    bstack1l1lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡈࡲࡡࡴࡵࠥᆼ"): bstack1l1lll1l111_opy_,
    bstack1l1lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠢᆽ"): bstack1l1lll1l111_opy_
    + [
        bstack1l1lll_opy_ (u"ࠨ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬࡯ࡣࡰࡩࠧᆾ"),
        bstack1l1lll_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᆿ"),
        bstack1l1lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦ࡫ࡱࡪࡴࠨᇀ"),
        bstack1l1lll_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᇁ"),
        bstack1l1lll_opy_ (u"ࠥࡧࡦࡲ࡬ࡴࡲࡨࡧࠧᇂ"),
        bstack1l1lll_opy_ (u"ࠦࡨࡧ࡬࡭ࡱࡥ࡮ࠧᇃ"),
        bstack1l1lll_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦᇄ"),
        bstack1l1lll_opy_ (u"ࠨࡳࡵࡱࡳࠦᇅ"),
        bstack1l1lll_opy_ (u"ࠢࡥࡷࡵࡥࡹ࡯࡯࡯ࠤᇆ"),
        bstack1l1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᇇ"),
    ],
    bstack1l1lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥ࡮ࡴ࠮ࡔࡧࡶࡷ࡮ࡵ࡮ࠣᇈ"): [bstack1l1lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡲࡤࡸ࡭ࠨᇉ"), bstack1l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡩࡥ࡮ࡲࡥࡥࠤᇊ"), bstack1l1lll_opy_ (u"ࠧࡺࡥࡴࡶࡶࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨᇋ"), bstack1l1lll_opy_ (u"ࠨࡩࡵࡧࡰࡷࠧᇌ")],
    bstack1l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡤࡱࡱࡪ࡮࡭࠮ࡄࡱࡱࡪ࡮࡭ࠢᇍ"): [bstack1l1lll_opy_ (u"ࠣ࡫ࡱࡺࡴࡩࡡࡵ࡫ࡲࡲࡤࡶࡡࡳࡣࡰࡷࠧᇎ"), bstack1l1lll_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᇏ")],
    bstack1l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳ࡌࡩࡹࡶࡸࡶࡪࡊࡥࡧࠤᇐ"): [bstack1l1lll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᇑ"), bstack1l1lll_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᇒ"), bstack1l1lll_opy_ (u"ࠨࡦࡶࡰࡦࠦᇓ"), bstack1l1lll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᇔ"), bstack1l1lll_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᇕ"), bstack1l1lll_opy_ (u"ࠤ࡬ࡨࡸࠨᇖ")],
    bstack1l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳࡙ࡵࡣࡔࡨࡵࡺ࡫ࡳࡵࠤᇗ"): [bstack1l1lll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᇘ"), bstack1l1lll_opy_ (u"ࠧࡶࡡࡳࡣࡰࠦᇙ"), bstack1l1lll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡤ࡯࡮ࡥࡧࡻࠦᇚ")],
    bstack1l1lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡳࡷࡱࡲࡪࡸ࠮ࡄࡣ࡯ࡰࡎࡴࡦࡰࠤᇛ"): [bstack1l1lll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᇜ"), bstack1l1lll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࠤᇝ")],
    bstack1l1lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡔ࡯ࡥࡧࡎࡩࡾࡽ࡯ࡳࡦࡶࠦᇞ"): [bstack1l1lll_opy_ (u"ࠦࡳࡵࡤࡦࠤᇟ"), bstack1l1lll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᇠ")],
    bstack1l1lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡏࡤࡶࡰࠨᇡ"): [bstack1l1lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇢ"), bstack1l1lll_opy_ (u"ࠣࡣࡵ࡫ࡸࠨᇣ"), bstack1l1lll_opy_ (u"ࠤ࡮ࡻࡦࡸࡧࡴࠤᇤ")],
}
_1ll111ll11l_opy_ = set()
class bstack1lll1ll11l1_opy_(bstack1ll1llll1ll_opy_):
    bstack1ll1111l1ll_opy_ = bstack1l1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡨࡪࡪࡸࡲࡦࡦࠥᇥ")
    bstack1l1lll11l11_opy_ = bstack1l1lll_opy_ (u"ࠦࡎࡔࡆࡐࠤᇦ")
    bstack1l1llll11l1_opy_ = bstack1l1lll_opy_ (u"ࠧࡋࡒࡓࡑࡕࠦᇧ")
    bstack1ll1111l111_opy_: Callable
    bstack1ll1111111l_opy_: Callable
    def __init__(self, bstack1llll1ll11l_opy_, bstack1llll1ll1ll_opy_):
        super().__init__()
        self.bstack1ll1l1l11ll_opy_ = bstack1llll1ll1ll_opy_
        if os.getenv(bstack1l1lll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡕ࠱࠲࡛ࠥᇨ"), bstack1l1lll_opy_ (u"ࠢ࠲ࠤᇩ")) != bstack1l1lll_opy_ (u"ࠣ࠳ࠥᇪ") or not self.is_enabled():
            self.logger.warning(bstack1l1lll_opy_ (u"ࠤࠥᇫ") + str(self.__class__.__name__) + bstack1l1lll_opy_ (u"ࠥࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠨᇬ"))
            return
        TestFramework.bstack1ll1ll1l111_opy_((bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.PRE), self.bstack1ll1l11ll1l_opy_)
        TestFramework.bstack1ll1ll1l111_opy_((bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1l1lll_opy_)
        for event in bstack1llll1ll1l1_opy_:
            for state in bstack1llll1lll1l_opy_:
                TestFramework.bstack1ll1ll1l111_opy_((event, state), self.bstack1l1lll1lll1_opy_)
        bstack1llll1ll11l_opy_.bstack1ll1ll1l111_opy_((bstack1llllllllll_opy_.bstack1111l11111_opy_, bstack11111lll1l_opy_.POST), self.bstack1l1lll111ll_opy_)
        self.bstack1ll1111l111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1ll111l11l1_opy_(bstack1lll1ll11l1_opy_.bstack1l1lll11l11_opy_, self.bstack1ll1111l111_opy_)
        self.bstack1ll1111111l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1ll111l11l1_opy_(bstack1lll1ll11l1_opy_.bstack1l1llll11l1_opy_, self.bstack1ll1111111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lllll1ll_opy_() and instance:
            bstack1l1llll11ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lllllll1l1_opy_
            if test_framework_state == bstack1llll1ll1l1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1llll1ll1l1_opy_.LOG:
                bstack1ll1l11l_opy_ = datetime.now()
                entries = f.bstack1l1lll11l1l_opy_(instance, bstack1lllllll1l1_opy_)
                if entries:
                    self.bstack1ll111lll11_opy_(instance, entries)
                    instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦᇭ"), datetime.now() - bstack1ll1l11l_opy_)
                    f.bstack1ll111llll1_opy_(instance, bstack1lllllll1l1_opy_)
                instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣᇮ"), datetime.now() - bstack1l1llll11ll_opy_)
                return # bstack1l1lll11111_opy_ not send this event with the bstack1ll111l1l11_opy_ bstack1l1lll11ll1_opy_
            elif (
                test_framework_state == bstack1llll1ll1l1_opy_.TEST
                and test_hook_state == bstack1llll1lll1l_opy_.POST
                and not f.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
            ):
                self.logger.warning(bstack1l1lll_opy_ (u"ࠨࡤࡳࡱࡳࡴ࡮ࡴࡧࠡࡦࡸࡩࠥࡺ࡯ࠡ࡮ࡤࡧࡰࠦ࡯ࡧࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࠦᇯ") + str(TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111111l1_opy_)) + bstack1l1lll_opy_ (u"ࠢࠣᇰ"))
                f.bstack1111l11l1l_opy_(instance, bstack1lll1ll11l1_opy_.bstack1ll1111l1ll_opy_, True)
                return # bstack1l1lll11111_opy_ not send this event bstack1ll111l1ll1_opy_ bstack1l1llllllll_opy_
            elif (
                f.bstack11111l11l1_opy_(instance, bstack1lll1ll11l1_opy_.bstack1ll1111l1ll_opy_, False)
                and test_framework_state == bstack1llll1ll1l1_opy_.LOG_REPORT
                and test_hook_state == bstack1llll1lll1l_opy_.POST
                and f.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111111l1_opy_)
            ):
                self.logger.warning(bstack1l1lll_opy_ (u"ࠣ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡗࡉࡘ࡚ࠬࠡࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡒࡒࡗ࡙ࠦࠢᇱ") + str(TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll111111l1_opy_)) + bstack1l1lll_opy_ (u"ࠤࠥᇲ"))
                self.bstack1l1lll1lll1_opy_(f, instance, (bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.POST), *args, **kwargs)
            bstack1ll1l11l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll1111ll1l_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1lll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᇳ"), None), data.pop(bstack1l1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᇴ"), {}).values()),
                key=lambda x: x[bstack1l1lll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᇵ")],
            )
            if bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_ in data:
                data.pop(bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_)
            data.update({bstack1l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᇶ"): bstack1ll1111ll1l_opy_})
            instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᇷ"), datetime.now() - bstack1ll1l11l_opy_)
            bstack1ll1l11l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1ll11111111_opy_)
            instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᇸ"), datetime.now() - bstack1ll1l11l_opy_)
            self.bstack1l1lll11ll1_opy_(instance, bstack1lllllll1l1_opy_, event_json=event_json)
            instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᇹ"), datetime.now() - bstack1l1llll11ll_opy_)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
        bstack1ll1l11lll1_opy_ = bstack1lll1lll111_opy_.bstack1ll1l1ll1l1_opy_(EVENTS.bstack1l1111lll_opy_.value)
        self.bstack1ll1l1l11ll_opy_.bstack1ll11111lll_opy_(instance, f, bstack1lllllll1l1_opy_, *args, **kwargs)
        bstack1lll1lll111_opy_.end(EVENTS.bstack1l1111lll_opy_.value, bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᇺ"), bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᇻ"), status=True, failure=None, test_name=None)
    def bstack1ll1l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l1l11ll_opy_.bstack1l1lll1ll11_opy_(instance, f, bstack1lllllll1l1_opy_, *args, **kwargs)
        self.bstack1ll111l111l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll1l11l_opy_, stage=STAGE.bstack1111lll1_opy_)
    def bstack1ll111l111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1lll_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠣ࡫ࡗࡖࡃࠡࡥࡤࡰࡱࡀࠠࡏࡱࠣࡺࡦࡲࡩࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠣᇼ"))
            return
        bstack1ll1l11l_opy_ = datetime.now()
        try:
            r = self.bstack1lll1ll1l11_opy_.TestSessionEvent(req)
            instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡧࡹࡩࡳࡺࠢᇽ"), datetime.now() - bstack1ll1l11l_opy_)
            f.bstack1111l11l1l_opy_(instance, self.bstack1ll1l1l11ll_opy_.bstack1ll11l11111_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇾ") + str(r) + bstack1l1lll_opy_ (u"ࠣࠤᇿ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሀ") + str(e) + bstack1l1lll_opy_ (u"ࠥࠦሁ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll111ll_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        _driver: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        _1l1llllll1l_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll11lllll_opy_.bstack1ll1ll11111_opy_(method_name):
            return
        if f.bstack1ll1l111lll_opy_(*args) == bstack1lll11lllll_opy_.bstack1l1llll1ll1_opy_:
            bstack1l1llll11ll_opy_ = datetime.now()
            screenshot = result.get(bstack1l1lll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥሂ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1lll_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣ࡭ࡲࡧࡧࡦࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡸࡷࠨሃ"))
                return
            bstack1l1llllll11_opy_ = self.bstack1l1lllll11l_opy_(instance)
            if bstack1l1llllll11_opy_:
                entry = bstack1lll1l111l1_opy_(TestFramework.bstack1l1lllll111_opy_, screenshot)
                self.bstack1ll111lll11_opy_(bstack1l1llllll11_opy_, [entry])
                instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡥࡹࡧࡦࡹࡹ࡫ࠢሄ"), datetime.now() - bstack1l1llll11ll_opy_)
            else:
                self.logger.warning(bstack1l1lll_opy_ (u"ࠢࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡦࡵࡷࠤ࡫ࡵࡲࠡࡹ࡫࡭ࡨ࡮ࠠࡵࡪ࡬ࡷࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡺࡥࡸࠦࡴࡢ࡭ࡨࡲࠥࡨࡹࠡࡦࡵ࡭ࡻ࡫ࡲ࠾ࠢࡾࢁࠧህ").format(instance.ref()))
        event = {}
        bstack1l1llllll11_opy_ = self.bstack1l1lllll11l_opy_(instance)
        if bstack1l1llllll11_opy_:
            self.bstack1ll1111l1l1_opy_(event, bstack1l1llllll11_opy_)
            if event.get(bstack1l1lll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨሆ")):
                self.bstack1ll111lll11_opy_(bstack1l1llllll11_opy_, event[bstack1l1lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢሇ")])
            else:
                self.logger.info(bstack1l1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡯ࡳ࡬ࡹࠠࡧࡱࡵࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡧࡹࡩࡳࡺࠢለ"))
    @measure(event_name=EVENTS.bstack1ll111111ll_opy_, stage=STAGE.bstack1111lll1_opy_)
    def bstack1ll111lll11_opy_(
        self,
        bstack1l1llllll11_opy_: bstack1llllll11ll_opy_,
        entries: List[bstack1lll1l111l1_opy_],
    ):
        self.bstack1ll1ll1l1l1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll1l1lllll_opy_)
        req.execution_context.hash = str(bstack1l1llllll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1llllll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1llllll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll1l1ll11l_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll111ll111_opy_)
            log_entry.uuid = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1ll1l1l11l1_opy_)
            log_entry.test_framework_state = bstack1l1llllll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1lll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥሉ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢሊ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1ll111l1111_opy_
                log_entry.file_path = entry.bstack11l1lll_opy_
        def bstack1l1llll1111_opy_():
            bstack1ll1l11l_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1lllll111_opy_:
                    bstack1l1llllll11_opy_.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥላ"), datetime.now() - bstack1ll1l11l_opy_)
                elif entry.kind == TestFramework.bstack1l1lll1l1ll_opy_:
                    bstack1l1llllll11_opy_.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦሌ"), datetime.now() - bstack1ll1l11l_opy_)
                else:
                    bstack1l1llllll11_opy_.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧል"), datetime.now() - bstack1ll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢሎ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1l1l1_opy_.enqueue(bstack1l1llll1111_opy_)
    @measure(event_name=EVENTS.bstack1ll11111ll1_opy_, stage=STAGE.bstack1111lll1_opy_)
    def bstack1l1lll11ll1_opy_(
        self,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        event_json=None,
    ):
        self.bstack1ll1ll1l1l1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1lllll_opy_)
        req.test_framework_name = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1ll11l_opy_)
        req.test_framework_version = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll111ll111_opy_)
        req.test_framework_state = bstack1lllllll1l1_opy_[0].name
        req.test_hook_state = bstack1lllllll1l1_opy_[1].name
        started_at = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll111l1lll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1ll11111111_opy_)).encode(bstack1l1lll_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤሏ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1llll1111_opy_():
            bstack1ll1l11l_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.TestFrameworkEvent(req)
                instance.bstack1lllll11l1_opy_(bstack1l1lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡧࡹࡩࡳࡺࠢሐ"), datetime.now() - bstack1ll1l11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥሑ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111l1l1l1_opy_.enqueue(bstack1l1llll1111_opy_)
    def bstack1l1lllll11l_opy_(self, instance: bstack11111ll111_opy_):
        bstack1ll111ll1l1_opy_ = TestFramework.bstack111111111l_opy_(instance.context)
        for t in bstack1ll111ll1l1_opy_:
            bstack1l1lll11lll_opy_ = TestFramework.bstack11111l11l1_opy_(t, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11lll_opy_):
                return t
    def bstack1l1lll1ll1l_opy_(self, message):
        self.bstack1ll1111l111_opy_(message + bstack1l1lll_opy_ (u"ࠨ࡜࡯ࠤሒ"))
    def log_error(self, message):
        self.bstack1ll1111111l_opy_(message + bstack1l1lll_opy_ (u"ࠢ࡝ࡰࠥሓ"))
    def bstack1ll111l11l1_opy_(self, level, original_func):
        def bstack1ll1111llll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1ll111ll1l1_opy_ = TestFramework.bstack1l1llll111l_opy_()
            if not bstack1ll111ll1l1_opy_:
                return return_value
            bstack1l1llllll11_opy_ = next(
                (
                    instance
                    for instance in bstack1ll111ll1l1_opy_
                    if TestFramework.bstack11111l11ll_opy_(instance, TestFramework.bstack1ll1l1l11l1_opy_)
                ),
                None,
            )
            if not bstack1l1llllll11_opy_:
                return
            entry = bstack1lll1l111l1_opy_(TestFramework.bstack1l1ll1llll1_opy_, message, level)
            self.bstack1ll111lll11_opy_(bstack1l1llllll11_opy_, [entry])
            return return_value
        return bstack1ll1111llll_opy_
    def bstack1ll1111l1l1_opy_(self, event: dict, instance=None) -> None:
        global _1ll111ll11l_opy_
        levels = [bstack1l1lll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦሔ"), bstack1l1lll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨሕ")]
        bstack1l1ll1lllll_opy_ = bstack1l1lll_opy_ (u"ࠥࠦሖ")
        if instance is not None:
            try:
                bstack1l1ll1lllll_opy_ = TestFramework.bstack11111l11l1_opy_(instance, TestFramework.bstack1ll1l1l11l1_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡻࡩࡥࠢࡩࡶࡴࡳࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤሗ").format(e))
        bstack1l1lll1llll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬመ")]
                bstack1l1llll1lll_opy_ = os.path.join(bstack1ll111l1l1l_opy_, (bstack1l1ll1lll1l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1llll1lll_opy_):
                    self.logger.info(bstack1l1lll_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡱࡳࡹࠦࡰࡳࡧࡶࡩࡳࡺࠠࡧࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡖࡨࡷࡹࠦࡡ࡯ࡦࠣࡆࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠨሙ").format(bstack1l1llll1lll_opy_))
                file_names = os.listdir(bstack1l1llll1lll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1llll1lll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1ll111ll11l_opy_:
                        self.logger.info(bstack1l1lll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧሚ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1ll111lll1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1ll111lll1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1lll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦማ"):
                                entry = bstack1lll1l111l1_opy_(
                                    kind=bstack1l1lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦሜ"),
                                    message=bstack1l1lll_opy_ (u"ࠥࠦም"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1ll111l1111_opy_=file_size,
                                    bstack1l1lllllll1_opy_=bstack1l1lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦሞ"),
                                    bstack11l1lll_opy_=os.path.abspath(file_path),
                                    bstack1111ll1l1_opy_=bstack1l1ll1lllll_opy_
                                )
                            elif level == bstack1l1lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤሟ"):
                                entry = bstack1lll1l111l1_opy_(
                                    kind=bstack1l1lll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣሠ"),
                                    message=bstack1l1lll_opy_ (u"ࠢࠣሡ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1ll111l1111_opy_=file_size,
                                    bstack1l1lllllll1_opy_=bstack1l1lll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣሢ"),
                                    bstack11l1lll_opy_=os.path.abspath(file_path),
                                    bstack1ll1111l11l_opy_=bstack1l1ll1lllll_opy_
                                )
                            bstack1l1lll1llll_opy_.append(entry)
                            _1ll111ll11l_opy_.add(abs_path)
                        except Exception as bstack1l1lll111l1_opy_:
                            self.logger.error(bstack1l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠧሣ").format(bstack1l1lll111l1_opy_))
        except Exception as e:
            self.logger.error(bstack1l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠨሤ").format(e))
        event[bstack1l1lll_opy_ (u"ࠦࡱࡵࡧࡴࠤሥ")] = bstack1l1lll1llll_opy_
class bstack1ll11111111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1llll1l1l_opy_ = set()
        kwargs[bstack1l1lll_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢሦ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1ll111ll1ll_opy_(obj, self.bstack1l1llll1l1l_opy_)
def bstack1ll1111ll11_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1ll111ll1ll_opy_(obj, bstack1l1llll1l1l_opy_=None, max_depth=3):
    if bstack1l1llll1l1l_opy_ is None:
        bstack1l1llll1l1l_opy_ = set()
    if id(obj) in bstack1l1llll1l1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1llll1l1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llll1l11_opy_ = TestFramework.bstack1ll11111l11_opy_(obj)
    bstack1l1lllll1l1_opy_ = next((k.lower() in bstack1l1llll1l11_opy_.lower() for k in bstack1ll111l11ll_opy_.keys()), None)
    if bstack1l1lllll1l1_opy_:
        obj = TestFramework.bstack1ll11111l1l_opy_(obj, bstack1ll111l11ll_opy_[bstack1l1lllll1l1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1lll_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤሧ")):
            keys = getattr(obj, bstack1l1lll_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥረ"), [])
        elif hasattr(obj, bstack1l1lll_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥሩ")):
            keys = getattr(obj, bstack1l1lll_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦሪ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1lll_opy_ (u"ࠥࡣࠧራ"))}
        if not obj and bstack1l1llll1l11_opy_ == bstack1l1lll_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣሬ"):
            obj = {bstack1l1lll_opy_ (u"ࠧࡶࡡࡵࡪࠥር"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1ll1111ll11_opy_(key) or str(key).startswith(bstack1l1lll_opy_ (u"ࠨ࡟ࠣሮ")):
            continue
        if value is not None and bstack1ll1111ll11_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1ll111ll1ll_opy_(value, bstack1l1llll1l1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1ll111ll1ll_opy_(o, bstack1l1llll1l1l_opy_, max_depth) for o in value]))
    return result or None