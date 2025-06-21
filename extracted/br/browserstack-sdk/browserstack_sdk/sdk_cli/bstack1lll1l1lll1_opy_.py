# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import bstack1111111111_opy_, bstack1lllll1l111_opy_, bstack1lllll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l11_opy_, bstack1lll1l1l1l1_opy_, bstack1lll1lll111_opy_, bstack1lll111l1l1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lll11ll1_opy_, bstack1l1l1llllll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll1111ll_opy_ = [bstack1l1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᇸ"), bstack1l1l1l1_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᇹ"), bstack1l1l1l1_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥᇺ"), bstack1l1l1l1_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧᇻ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡵࡪࠥᇼ")]
bstack1l1lll11l1l_opy_ = bstack1l1l1llllll_opy_()
bstack1l1llllll1l_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᇽ")
bstack1l1ll1l1ll1_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡊࡶࡨࡱࠧᇾ"): bstack1l1ll1111ll_opy_,
    bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡒࡤࡧࡰࡧࡧࡦࠤᇿ"): bstack1l1ll1111ll_opy_,
    bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡐࡳࡩࡻ࡬ࡦࠤሀ"): bstack1l1ll1111ll_opy_,
    bstack1l1l1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡇࡱࡧࡳࡴࠤሁ"): bstack1l1ll1111ll_opy_,
    bstack1l1l1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡋࡻ࡮ࡤࡶ࡬ࡳࡳࠨሂ"): bstack1l1ll1111ll_opy_
    + [
        bstack1l1l1l1_opy_ (u"ࠧࡵࡲࡪࡩ࡬ࡲࡦࡲ࡮ࡢ࡯ࡨࠦሃ"),
        bstack1l1l1l1_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣሄ"),
        bstack1l1l1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࡪࡰࡩࡳࠧህ"),
        bstack1l1l1l1_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥሆ"),
        bstack1l1l1l1_opy_ (u"ࠤࡦࡥࡱࡲࡳࡱࡧࡦࠦሇ"),
        bstack1l1l1l1_opy_ (u"ࠥࡧࡦࡲ࡬ࡰࡤ࡭ࠦለ"),
        bstack1l1l1l1_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥሉ"),
        bstack1l1l1l1_opy_ (u"ࠧࡹࡴࡰࡲࠥሊ"),
        bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠣላ"),
        bstack1l1l1l1_opy_ (u"ࠢࡸࡪࡨࡲࠧሌ"),
    ],
    bstack1l1l1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤ࡭ࡳ࠴ࡓࡦࡵࡶ࡭ࡴࡴࠢል"): [bstack1l1l1l1_opy_ (u"ࠤࡶࡸࡦࡸࡴࡱࡣࡷ࡬ࠧሎ"), bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡴࡨࡤ࡭ࡱ࡫ࡤࠣሏ"), bstack1l1l1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧሐ"), bstack1l1l1l1_opy_ (u"ࠧ࡯ࡴࡦ࡯ࡶࠦሑ")],
    bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡣࡰࡰࡩ࡭࡬࠴ࡃࡰࡰࡩ࡭࡬ࠨሒ"): [bstack1l1l1l1_opy_ (u"ࠢࡪࡰࡹࡳࡨࡧࡴࡪࡱࡱࡣࡵࡧࡲࡢ࡯ࡶࠦሓ"), bstack1l1l1l1_opy_ (u"ࠣࡣࡵ࡫ࡸࠨሔ")],
    bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡋ࡯ࡸࡵࡷࡵࡩࡉ࡫ࡦࠣሕ"): [bstack1l1l1l1_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤሖ"), bstack1l1l1l1_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧሗ"), bstack1l1l1l1_opy_ (u"ࠧ࡬ࡵ࡯ࡥࠥመ"), bstack1l1l1l1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨሙ"), bstack1l1l1l1_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤሚ"), bstack1l1l1l1_opy_ (u"ࠣ࡫ࡧࡷࠧማ")],
    bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡘࡻࡢࡓࡧࡴࡹࡪࡹࡴࠣሜ"): [bstack1l1l1l1_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣም"), bstack1l1l1l1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࠥሞ"), bstack1l1l1l1_opy_ (u"ࠧࡶࡡࡳࡣࡰࡣ࡮ࡴࡤࡦࡺࠥሟ")],
    bstack1l1l1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡲࡶࡰࡱࡩࡷ࠴ࡃࡢ࡮࡯ࡍࡳ࡬࡯ࠣሠ"): [bstack1l1l1l1_opy_ (u"ࠢࡸࡪࡨࡲࠧሡ"), bstack1l1l1l1_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࠣሢ")],
    bstack1l1l1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡓࡵࡤࡦࡍࡨࡽࡼࡵࡲࡥࡵࠥሣ"): [bstack1l1l1l1_opy_ (u"ࠥࡲࡴࡪࡥࠣሤ"), bstack1l1l1l1_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦሥ")],
    bstack1l1l1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡎࡣࡵ࡯ࠧሦ"): [bstack1l1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦሧ"), bstack1l1l1l1_opy_ (u"ࠢࡢࡴࡪࡷࠧረ"), bstack1l1l1l1_opy_ (u"ࠣ࡭ࡺࡥࡷ࡭ࡳࠣሩ")],
}
_1l1lll111l1_opy_ = set()
class bstack1llll1l1111_opy_(bstack1llll11l1ll_opy_):
    bstack1l1llll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࠤሪ")
    bstack1l1llll11l1_opy_ = bstack1l1l1l1_opy_ (u"ࠥࡍࡓࡌࡏࠣራ")
    bstack1l1lll1l1ll_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡊࡘࡒࡐࡔࠥሬ")
    bstack1l1lllll111_opy_: Callable
    bstack1l1lll1ll11_opy_: Callable
    def __init__(self, bstack1ll1lll1ll1_opy_, bstack1lll1ll111l_opy_):
        super().__init__()
        self.bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_
        if os.getenv(bstack1l1l1l1_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡔ࠷࠱࡚ࠤር"), bstack1l1l1l1_opy_ (u"ࠨ࠱ࠣሮ")) != bstack1l1l1l1_opy_ (u"ࠢ࠲ࠤሯ") or not self.is_enabled():
            self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࠤሰ") + str(self.__class__.__name__) + bstack1l1l1l1_opy_ (u"ࠤࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠧሱ"))
            return
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.PRE), self.bstack1ll11l1l111_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), self.bstack1ll1l11ll1l_opy_)
        for event in bstack1ll1ll11l11_opy_:
            for state in bstack1lll1lll111_opy_:
                TestFramework.bstack1ll111lll1l_opy_((event, state), self.bstack1l1ll11l11l_opy_)
        bstack1ll1lll1ll1_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.POST), self.bstack1l1llll11ll_opy_)
        self.bstack1l1lllll111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1ll11111l_opy_(bstack1llll1l1111_opy_.bstack1l1llll11l1_opy_, self.bstack1l1lllll111_opy_)
        self.bstack1l1lll1ll11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1ll11111l_opy_(bstack1llll1l1111_opy_.bstack1l1lll1l1ll_opy_, self.bstack1l1lll1ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1ll1l1l11_opy_() and instance:
            bstack1l1ll11ll1l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lllll11ll1_opy_
            if test_framework_state == bstack1ll1ll11l11_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1ll11l11_opy_.LOG:
                bstack1l1ll1l1ll_opy_ = datetime.now()
                entries = f.bstack1l1lll1111l_opy_(instance, bstack1lllll11ll1_opy_)
                if entries:
                    self.bstack1l1lll11111_opy_(instance, entries)
                    instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥሲ"), datetime.now() - bstack1l1ll1l1ll_opy_)
                    f.bstack1l1lll11l11_opy_(instance, bstack1lllll11ll1_opy_)
                instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢሳ"), datetime.now() - bstack1l1ll11ll1l_opy_)
                return # bstack1l1l1lllll1_opy_ not send this event with the bstack1l1ll1l1111_opy_ bstack1l1ll111111_opy_
            elif (
                test_framework_state == bstack1ll1ll11l11_opy_.TEST
                and test_hook_state == bstack1lll1lll111_opy_.POST
                and not f.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_)
            ):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠧࡪࡲࡰࡲࡳ࡭ࡳ࡭ࠠࡥࡷࡨࠤࡹࡵࠠ࡭ࡣࡦ࡯ࠥࡵࡦࠡࡴࡨࡷࡺࡲࡴࡴࠢࠥሴ") + str(TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_)) + bstack1l1l1l1_opy_ (u"ࠨࠢስ"))
                f.bstack1lllll1111l_opy_(instance, bstack1llll1l1111_opy_.bstack1l1llll1l11_opy_, True)
                return # bstack1l1l1lllll1_opy_ not send this event bstack1l1lllllll1_opy_ bstack1l1llll111l_opy_
            elif (
                f.bstack1lllll1ll11_opy_(instance, bstack1llll1l1111_opy_.bstack1l1llll1l11_opy_, False)
                and test_framework_state == bstack1ll1ll11l11_opy_.LOG_REPORT
                and test_hook_state == bstack1lll1lll111_opy_.POST
                and f.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_)
            ):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡖࡈࡗ࡙࠲ࠠࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡑࡑࡖࡘࠥࠨሶ") + str(TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1l1lll1l11l_opy_)) + bstack1l1l1l1_opy_ (u"ࠣࠤሷ"))
                self.bstack1l1ll11l11l_opy_(f, instance, (bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), *args, **kwargs)
            bstack1l1ll1l1ll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll11l1ll_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1l1l1_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧሸ"), None), data.pop(bstack1l1l1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥሹ"), {}).values()),
                key=lambda x: x[bstack1l1l1l1_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢሺ")],
            )
            if bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_ in data:
                data.pop(bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_)
            data.update({bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧሻ"): bstack1l1ll11l1ll_opy_})
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦሼ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            bstack1l1ll1l1ll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1l1llll11_opy_)
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥሽ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            self.bstack1l1ll111111_opy_(instance, bstack1lllll11ll1_opy_, event_json=event_json)
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦሾ"), datetime.now() - bstack1l1ll11ll1l_opy_)
    def bstack1ll11l1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
        bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack111111111_opy_.value)
        self.bstack1ll11l1lll1_opy_.bstack1l1ll1l11l1_opy_(instance, f, bstack1lllll11ll1_opy_, *args, **kwargs)
        bstack1lll1ll11l1_opy_.end(EVENTS.bstack111111111_opy_.value, bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤሿ"), bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣቀ"), status=True, failure=None, test_name=None)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11l1lll1_opy_.bstack1l1lll1llll_opy_(instance, f, bstack1lllll11ll1_opy_, *args, **kwargs)
        self.bstack1l1lllll1l1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1ll11l111_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l1lllll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵࠢࡪࡖࡕࡉࠠࡤࡣ࡯ࡰ࠿ࠦࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠢቁ"))
            return
        bstack1l1ll1l1ll_opy_ = datetime.now()
        try:
            r = self.bstack1ll1ll111l1_opy_.TestSessionEvent(req)
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡦࡸࡨࡲࡹࠨቂ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            f.bstack1lllll1111l_opy_(instance, self.bstack1ll11l1lll1_opy_.bstack1l1ll1ll111_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣቃ") + str(r) + bstack1l1l1l1_opy_ (u"ࠢࠣቄ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቅ") + str(e) + bstack1l1l1l1_opy_ (u"ࠤࠥቆ"))
            traceback.print_exc()
            raise e
    def bstack1l1llll11ll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        _driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        _1l1llll1lll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1llll111lll_opy_.bstack1ll11l111ll_opy_(method_name):
            return
        if f.bstack1ll11l1ll11_opy_(*args) == bstack1llll111lll_opy_.bstack1l1ll1lll1l_opy_:
            bstack1l1ll11ll1l_opy_ = datetime.now()
            screenshot = result.get(bstack1l1l1l1_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤቇ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢ࡬ࡱࡦ࡭ࡥࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡷࡶࠧቈ"))
                return
            bstack1l1lll111ll_opy_ = self.bstack1l1llll1111_opy_(instance)
            if bstack1l1lll111ll_opy_:
                entry = bstack1lll111l1l1_opy_(TestFramework.bstack1l1ll1lllll_opy_, screenshot)
                self.bstack1l1lll11111_opy_(bstack1l1lll111ll_opy_, [entry])
                instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡࡧࡶࡨࡶࡤ࡫ࡸࡦࡥࡸࡸࡪࠨ቉"), datetime.now() - bstack1l1ll11ll1l_opy_)
            else:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡥࡴࡶࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡩ࡫ࡶࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡹࡤࡷࠥࡺࡡ࡬ࡧࡱࠤࡧࡿࠠࡥࡴ࡬ࡺࡪࡸ࠽ࠡࡽࢀࠦቊ").format(instance.ref()))
        event = {}
        bstack1l1lll111ll_opy_ = self.bstack1l1llll1111_opy_(instance)
        if bstack1l1lll111ll_opy_:
            self.bstack1l1ll11ll11_opy_(event, bstack1l1lll111ll_opy_)
            if event.get(bstack1l1l1l1_opy_ (u"ࠢ࡭ࡱࡪࡷࠧቋ")):
                self.bstack1l1lll11111_opy_(bstack1l1lll111ll_opy_, event[bstack1l1l1l1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨቌ")])
            else:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡ࡮ࡲ࡫ࡸࠦࡦࡰࡴࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡦࡸࡨࡲࡹࠨቍ"))
    @measure(event_name=EVENTS.bstack1l1ll111ll1_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l1lll11111_opy_(
        self,
        bstack1l1lll111ll_opy_: bstack1lll1l1l1l1_opy_,
        entries: List[bstack1lll111l1l1_opy_],
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll111ll1ll_opy_)
        req.execution_context.hash = str(bstack1l1lll111ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll1l11l1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1ll1111l1_opy_)
            log_entry.uuid = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll1l11lll1_opy_)
            log_entry.test_framework_state = bstack1l1lll111ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1l1l1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ቎"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1l1l1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ቏"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll11llll_opy_
                log_entry.file_path = entry.bstack111l1l1_opy_
        def bstack1l1lll11lll_opy_():
            bstack1l1ll1l1ll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll111l1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll1lllll_opy_:
                    bstack1l1lll111ll_opy_.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤቐ"), datetime.now() - bstack1l1ll1l1ll_opy_)
                elif entry.kind == TestFramework.bstack1l1ll1l1lll_opy_:
                    bstack1l1lll111ll_opy_.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥቑ"), datetime.now() - bstack1l1ll1l1ll_opy_)
                else:
                    bstack1l1lll111ll_opy_.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟࡭ࡱࡪࠦቒ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቓ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111lll1_opy_.enqueue(bstack1l1lll11lll_opy_)
    @measure(event_name=EVENTS.bstack1l1ll1llll1_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1l1ll111111_opy_(
        self,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        event_json=None,
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_)
        req.test_framework_state = bstack1lllll11ll1_opy_[0].name
        req.test_hook_state = bstack1lllll11ll1_opy_[1].name
        started_at = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1l1lll1l111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1l1llll11_opy_)).encode(bstack1l1l1l1_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቔ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1lll11lll_opy_():
            bstack1l1ll1l1ll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll111l1_opy_.TestFrameworkEvent(req)
                instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡦࡸࡨࡲࡹࠨቕ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1l1l1_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤቖ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111lll1_opy_.enqueue(bstack1l1lll11lll_opy_)
    def bstack1l1llll1111_opy_(self, instance: bstack1111111111_opy_):
        bstack1l1llllll11_opy_ = TestFramework.bstack1llll1lll11_opy_(instance.context)
        for t in bstack1l1llllll11_opy_:
            bstack1l1lllll1ll_opy_ = TestFramework.bstack1lllll1ll11_opy_(t, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1lllll1ll_opy_):
                return t
    def bstack1l1ll1ll1l1_opy_(self, message):
        self.bstack1l1lllll111_opy_(message + bstack1l1l1l1_opy_ (u"ࠧࡢ࡮ࠣ቗"))
    def log_error(self, message):
        self.bstack1l1lll1ll11_opy_(message + bstack1l1l1l1_opy_ (u"ࠨ࡜࡯ࠤቘ"))
    def bstack1l1ll11111l_opy_(self, level, original_func):
        def bstack1l1llll1ll1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1llllll11_opy_ = TestFramework.bstack1l1ll111l11_opy_()
            if not bstack1l1llllll11_opy_:
                return return_value
            bstack1l1lll111ll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1llllll11_opy_
                    if TestFramework.bstack1lllllll1ll_opy_(instance, TestFramework.bstack1ll1l11lll1_opy_)
                ),
                None,
            )
            if not bstack1l1lll111ll_opy_:
                return
            entry = bstack1lll111l1l1_opy_(TestFramework.bstack1l1ll111lll_opy_, message, level)
            self.bstack1l1lll11111_opy_(bstack1l1lll111ll_opy_, [entry])
            return return_value
        return bstack1l1llll1ll1_opy_
    def bstack1l1ll11ll11_opy_(self, event: dict, instance=None) -> None:
        global _1l1lll111l1_opy_
        levels = [bstack1l1l1l1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥ቙"), bstack1l1l1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧቚ")]
        bstack1l1lll1lll1_opy_ = bstack1l1l1l1_opy_ (u"ࠤࠥቛ")
        if instance is not None:
            try:
                bstack1l1lll1lll1_opy_ = TestFramework.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11lll1_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡺ࡯ࡤࠡࡨࡵࡳࡲࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣቜ").format(e))
        bstack1l1ll1l11ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫቝ")]
                bstack1l1ll111l1l_opy_ = os.path.join(bstack1l1lll11l1l_opy_, (bstack1l1llllll1l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll111l1l_opy_):
                    self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡰࡲࡸࠥࡶࡲࡦࡵࡨࡲࡹࠦࡦࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡕࡧࡶࡸࠥࡧ࡮ࡥࠢࡅࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣ቞").format(bstack1l1ll111l1l_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll111l1l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll111l1l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1lll111l1_opy_:
                        self.logger.info(bstack1l1l1l1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦ቟").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll11lll1_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll11lll1_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1l1l1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥበ"):
                                entry = bstack1lll111l1l1_opy_(
                                    kind=bstack1l1l1l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥቡ"),
                                    message=bstack1l1l1l1_opy_ (u"ࠤࠥቢ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll11llll_opy_=file_size,
                                    bstack1l1llll1l1l_opy_=bstack1l1l1l1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥባ"),
                                    bstack111l1l1_opy_=os.path.abspath(file_path),
                                    bstack1l1ll11ll_opy_=bstack1l1lll1lll1_opy_
                                )
                            elif level == bstack1l1l1l1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣቤ"):
                                entry = bstack1lll111l1l1_opy_(
                                    kind=bstack1l1l1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢብ"),
                                    message=bstack1l1l1l1_opy_ (u"ࠨࠢቦ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll11llll_opy_=file_size,
                                    bstack1l1llll1l1l_opy_=bstack1l1l1l1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢቧ"),
                                    bstack111l1l1_opy_=os.path.abspath(file_path),
                                    bstack1l1ll1ll11l_opy_=bstack1l1lll1lll1_opy_
                                )
                            bstack1l1ll1l11ll_opy_.append(entry)
                            _1l1lll111l1_opy_.add(abs_path)
                        except Exception as bstack1l1lll1ll1l_opy_:
                            self.logger.error(bstack1l1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢቨ").format(bstack1l1lll1ll1l_opy_))
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣቩ").format(e))
        event[bstack1l1l1l1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣቪ")] = bstack1l1ll1l11ll_opy_
class bstack1l1l1llll11_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1lllll11l_opy_ = set()
        kwargs[bstack1l1l1l1_opy_ (u"ࠦࡸࡱࡩࡱ࡭ࡨࡽࡸࠨቫ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1l1l1l_opy_(obj, self.bstack1l1lllll11l_opy_)
def bstack1l1ll1lll11_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1l1l1l_opy_(obj, bstack1l1lllll11l_opy_=None, max_depth=3):
    if bstack1l1lllll11l_opy_ is None:
        bstack1l1lllll11l_opy_ = set()
    if id(obj) in bstack1l1lllll11l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1lllll11l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1lll1l1l1_opy_ = TestFramework.bstack1l1llllllll_opy_(obj)
    bstack1l1ll11l1l1_opy_ = next((k.lower() in bstack1l1lll1l1l1_opy_.lower() for k in bstack1l1ll1l1ll1_opy_.keys()), None)
    if bstack1l1ll11l1l1_opy_:
        obj = TestFramework.bstack1l1ll1ll1ll_opy_(obj, bstack1l1ll1l1ll1_opy_[bstack1l1ll11l1l1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1l1l1_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣቬ")):
            keys = getattr(obj, bstack1l1l1l1_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤቭ"), [])
        elif hasattr(obj, bstack1l1l1l1_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤቮ")):
            keys = getattr(obj, bstack1l1l1l1_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥቯ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1l1l1_opy_ (u"ࠤࡢࠦተ"))}
        if not obj and bstack1l1lll1l1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠥࡴࡦࡺࡨ࡭࡫ࡥ࠲ࡕࡵࡳࡪࡺࡓࡥࡹ࡮ࠢቱ"):
            obj = {bstack1l1l1l1_opy_ (u"ࠦࡵࡧࡴࡩࠤቲ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll1lll11_opy_(key) or str(key).startswith(bstack1l1l1l1_opy_ (u"ࠧࡥࠢታ")):
            continue
        if value is not None and bstack1l1ll1lll11_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1l1l1l_opy_(value, bstack1l1lllll11l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1l1l1l_opy_(o, bstack1l1lllll11l_opy_, max_depth) for o in value]))
    return result or None