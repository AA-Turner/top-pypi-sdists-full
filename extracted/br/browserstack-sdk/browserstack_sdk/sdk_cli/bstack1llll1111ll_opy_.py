# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import bstack1llll1ll1ll_opy_, bstack1111111l11_opy_, bstack1llllll1111_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll11111l_opy_, bstack1llll111l11_opy_, bstack1ll1l1lll11_opy_, bstack1lll11lll11_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll111ll1_opy_, bstack1l1lllll111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1lll1ll11_opy_ = [bstack11ll11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇷ"), bstack11ll11_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᇸ"), bstack11ll11_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤᇹ"), bstack11ll11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦᇺ"), bstack11ll11_opy_ (u"ࠦࡵࡧࡴࡩࠤᇻ")]
bstack1l1ll11ll1l_opy_ = bstack1l1lllll111_opy_()
bstack1l1lllllll1_opy_ = bstack11ll11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᇼ")
bstack1l1l1llll11_opy_ = {
    bstack11ll11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦᇽ"): bstack1l1lll1ll11_opy_,
    bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣᇾ"): bstack1l1lll1ll11_opy_,
    bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣᇿ"): bstack1l1lll1ll11_opy_,
    bstack11ll11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣሀ"): bstack1l1lll1ll11_opy_,
    bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧሁ"): bstack1l1lll1ll11_opy_
    + [
        bstack11ll11_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥሂ"),
        bstack11ll11_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢሃ"),
        bstack11ll11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦሄ"),
        bstack11ll11_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤህ"),
        bstack11ll11_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥሆ"),
        bstack11ll11_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥሇ"),
        bstack11ll11_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤለ"),
        bstack11ll11_opy_ (u"ࠦࡸࡺ࡯ࡱࠤሉ"),
        bstack11ll11_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢሊ"),
        bstack11ll11_opy_ (u"ࠨࡷࡩࡧࡱࠦላ"),
    ],
    bstack11ll11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨሌ"): [bstack11ll11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦል"), bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢሎ"), bstack11ll11_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦሏ"), bstack11ll11_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥሐ")],
    bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧሑ"): [bstack11ll11_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥሒ"), bstack11ll11_opy_ (u"ࠢࡢࡴࡪࡷࠧሓ")],
    bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢሔ"): [bstack11ll11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣሕ"), bstack11ll11_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦሖ"), bstack11ll11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤሗ"), bstack11ll11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧመ"), bstack11ll11_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣሙ"), bstack11ll11_opy_ (u"ࠢࡪࡦࡶࠦሚ")],
    bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢማ"): [bstack11ll11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢሜ"), bstack11ll11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤም"), bstack11ll11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤሞ")],
    bstack11ll11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢሟ"): [bstack11ll11_opy_ (u"ࠨࡷࡩࡧࡱࠦሠ"), bstack11ll11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢሡ")],
    bstack11ll11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤሢ"): [bstack11ll11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢሣ"), bstack11ll11_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥሤ")],
    bstack11ll11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦሥ"): [bstack11ll11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሦ"), bstack11ll11_opy_ (u"ࠨࡡࡳࡩࡶࠦሧ"), bstack11ll11_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢረ")],
}
_1l1ll1lll11_opy_ = set()
class bstack1llll11l11l_opy_(bstack1ll1ll1llll_opy_):
    bstack1l1ll111l1l_opy_ = bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣሩ")
    bstack1l1lll11111_opy_ = bstack11ll11_opy_ (u"ࠤࡌࡒࡋࡕࠢሪ")
    bstack1l1lll1l1ll_opy_ = bstack11ll11_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤራ")
    bstack1l1lll111ll_opy_: Callable
    bstack1l1ll1l1l1l_opy_: Callable
    def __init__(self, bstack1ll1lllll11_opy_, bstack1lll1l111ll_opy_):
        super().__init__()
        self.bstack1ll111ll11l_opy_ = bstack1lll1l111ll_opy_
        if os.getenv(bstack11ll11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣሬ"), bstack11ll11_opy_ (u"ࠧ࠷ࠢር")) != bstack11ll11_opy_ (u"ࠨ࠱ࠣሮ") or not self.is_enabled():
            self.logger.warning(bstack11ll11_opy_ (u"ࠢࠣሯ") + str(self.__class__.__name__) + bstack11ll11_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦሰ"))
            return
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.PRE), self.bstack1ll11ll1l1l_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), self.bstack1ll1l111ll1_opy_)
        for event in bstack1llll11111l_opy_:
            for state in bstack1ll1l1lll11_opy_:
                TestFramework.bstack1ll1l11l1l1_opy_((event, state), self.bstack1l1lll11l11_opy_)
        bstack1ll1lllll11_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.POST), self.bstack1l1llll1lll_opy_)
        self.bstack1l1lll111ll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1lll11lll_opy_(bstack1llll11l11l_opy_.bstack1l1lll11111_opy_, self.bstack1l1lll111ll_opy_)
        self.bstack1l1ll1l1l1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1lll11lll_opy_(bstack1llll11l11l_opy_.bstack1l1lll1l1ll_opy_, self.bstack1l1ll1l1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll11l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1llllllll_opy_() and instance:
            bstack1l1ll111111_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack111111111l_opy_
            if test_framework_state == bstack1llll11111l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1llll11111l_opy_.LOG:
                bstack1ll1lll1ll_opy_ = datetime.now()
                entries = f.bstack1l1ll1l11l1_opy_(instance, bstack111111111l_opy_)
                if entries:
                    self.bstack1l1ll11l1ll_opy_(instance, entries)
                    instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤሱ"), datetime.now() - bstack1ll1lll1ll_opy_)
                    f.bstack1l1ll1l1l11_opy_(instance, bstack111111111l_opy_)
                instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨሲ"), datetime.now() - bstack1l1ll111111_opy_)
                return # bstack1l1llll11l1_opy_ not send this event with the bstack1l1ll1l111l_opy_ bstack1l1ll111lll_opy_
            elif (
                test_framework_state == bstack1llll11111l_opy_.TEST
                and test_hook_state == bstack1ll1l1lll11_opy_.POST
                and not f.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)
            ):
                self.logger.warning(bstack11ll11_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤሳ") + str(TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)) + bstack11ll11_opy_ (u"ࠧࠨሴ"))
                f.bstack1llllllllll_opy_(instance, bstack1llll11l11l_opy_.bstack1l1ll111l1l_opy_, True)
                return # bstack1l1llll11l1_opy_ not send this event bstack1l1llllll1l_opy_ bstack1l1ll1ll1l1_opy_
            elif (
                f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l11l_opy_.bstack1l1ll111l1l_opy_, False)
                and test_framework_state == bstack1llll11111l_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1l1lll11_opy_.POST
                and f.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)
            ):
                self.logger.warning(bstack11ll11_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧስ") + str(TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1llll11ll_opy_)) + bstack11ll11_opy_ (u"ࠢࠣሶ"))
                self.bstack1l1lll11l11_opy_(f, instance, (bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), *args, **kwargs)
            bstack1ll1lll1ll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1llll1l11_opy_ = sorted(
                filter(lambda x: x.get(bstack11ll11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦሷ"), None), data.pop(bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤሸ"), {}).values()),
                key=lambda x: x[bstack11ll11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨሹ")],
            )
            if bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_ in data:
                data.pop(bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_)
            data.update({bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦሺ"): bstack1l1llll1l11_opy_})
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥሻ"), datetime.now() - bstack1ll1lll1ll_opy_)
            bstack1ll1lll1ll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll11111l_opy_)
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤሼ"), datetime.now() - bstack1ll1lll1ll_opy_)
            self.bstack1l1ll111lll_opy_(instance, bstack111111111l_opy_, event_json=event_json)
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥሽ"), datetime.now() - bstack1l1ll111111_opy_)
    def bstack1ll11ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
        bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l1lll1ll1_opy_.value)
        self.bstack1ll111ll11l_opy_.bstack1l1ll11llll_opy_(instance, f, bstack111111111l_opy_, *args, **kwargs)
        bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1l1lll1ll1_opy_.value, bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሾ"), bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሿ"), status=True, failure=None, test_name=None)
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll111ll11l_opy_.bstack1l1ll11l11l_opy_(instance, f, bstack111111111l_opy_, *args, **kwargs)
        self.bstack1l1llll1111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1ll1111ll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l1llll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨቀ"))
            return
        bstack1ll1lll1ll_opy_ = datetime.now()
        try:
            r = self.bstack1llll1l1l11_opy_.TestSessionEvent(req)
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧቁ"), datetime.now() - bstack1ll1lll1ll_opy_)
            f.bstack1llllllllll_opy_(instance, self.bstack1ll111ll11l_opy_.bstack1l1llllll11_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11ll11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢቂ") + str(r) + bstack11ll11_opy_ (u"ࠨࠢቃ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧቄ") + str(e) + bstack11ll11_opy_ (u"ࠣࠤቅ"))
            traceback.print_exc()
            raise e
    def bstack1l1llll1lll_opy_(
        self,
        f: bstack1llll11l111_opy_,
        _driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        _1l1llll1l1l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1llll11l111_opy_.bstack1ll1l11ll1l_opy_(method_name):
            return
        if f.bstack1ll11l1ll1l_opy_(*args) == bstack1llll11l111_opy_.bstack1l1ll1llll1_opy_:
            bstack1l1ll111111_opy_ = datetime.now()
            screenshot = result.get(bstack11ll11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣቆ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11ll11_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦቇ"))
                return
            bstack1l1lll1l1l1_opy_ = self.bstack1l1ll1ll11l_opy_(instance)
            if bstack1l1lll1l1l1_opy_:
                entry = bstack1lll11lll11_opy_(TestFramework.bstack1l1lll1111l_opy_, screenshot)
                self.bstack1l1ll11l1ll_opy_(bstack1l1lll1l1l1_opy_, [entry])
                instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧቈ"), datetime.now() - bstack1l1ll111111_opy_)
            else:
                self.logger.warning(bstack11ll11_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥ቉").format(instance.ref()))
        event = {}
        bstack1l1lll1l1l1_opy_ = self.bstack1l1ll1ll11l_opy_(instance)
        if bstack1l1lll1l1l1_opy_:
            self.bstack1l1lllll1ll_opy_(event, bstack1l1lll1l1l1_opy_)
            if event.get(bstack11ll11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦቊ")):
                self.bstack1l1ll11l1ll_opy_(bstack1l1lll1l1l1_opy_, event[bstack11ll11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧቋ")])
            else:
                self.logger.debug(bstack11ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧቌ"))
    @measure(event_name=EVENTS.bstack1l1lll1l11l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l1ll11l1ll_opy_(
        self,
        bstack1l1lll1l1l1_opy_: bstack1llll111l11_opy_,
        entries: List[bstack1lll11lll11_opy_],
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll1l11111l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11l11lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1ll1l11ll_opy_)
            log_entry.uuid = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll1l11ll11_opy_)
            log_entry.test_framework_state = bstack1l1lll1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣቍ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11ll11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧ቎"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1ll1l_opy_
                log_entry.file_path = entry.bstack1llll11_opy_
        def bstack1l1lll111l1_opy_():
            bstack1ll1lll1ll_opy_ = datetime.now()
            try:
                self.bstack1llll1l1l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1lll1111l_opy_:
                    bstack1l1lll1l1l1_opy_.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣ቏"), datetime.now() - bstack1ll1lll1ll_opy_)
                elif entry.kind == TestFramework.bstack1l1llll111l_opy_:
                    bstack1l1lll1l1l1_opy_.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤቐ"), datetime.now() - bstack1ll1lll1ll_opy_)
                else:
                    bstack1l1lll1l1l1_opy_.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥቑ"), datetime.now() - bstack1ll1lll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧቒ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l1ll_opy_.enqueue(bstack1l1lll111l1_opy_)
    @measure(event_name=EVENTS.bstack1l1ll1l1111_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1l1ll111lll_opy_(
        self,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        event_json=None,
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11111l_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1ll1l11ll_opy_)
        req.test_framework_state = bstack111111111l_opy_[0].name
        req.test_hook_state = bstack111111111l_opy_[1].name
        started_at = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1lll1lll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1l1lll1l111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll11111l_opy_)).encode(bstack11ll11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቓ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1lll111l1_opy_():
            bstack1ll1lll1ll_opy_ = datetime.now()
            try:
                self.bstack1llll1l1l11_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧቔ"), datetime.now() - bstack1ll1lll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቕ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l1ll_opy_.enqueue(bstack1l1lll111l1_opy_)
    def bstack1l1ll1ll11l_opy_(self, instance: bstack1llll1ll1ll_opy_):
        bstack1l1lllll11l_opy_ = TestFramework.bstack1llllll111l_opy_(instance.context)
        for t in bstack1l1lllll11l_opy_:
            bstack1l1lll11l1l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(t, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11l1l_opy_):
                return t
    def bstack1l1ll1ll1ll_opy_(self, message):
        self.bstack1l1lll111ll_opy_(message + bstack11ll11_opy_ (u"ࠦࡡࡴࠢቖ"))
    def log_error(self, message):
        self.bstack1l1ll1l1l1l_opy_(message + bstack11ll11_opy_ (u"ࠧࡢ࡮ࠣ቗"))
    def bstack1l1lll11lll_opy_(self, level, original_func):
        def bstack1l1lll1llll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1lllll11l_opy_ = TestFramework.bstack1l1ll1ll111_opy_()
            if not bstack1l1lllll11l_opy_:
                return return_value
            bstack1l1lll1l1l1_opy_ = next(
                (
                    instance
                    for instance in bstack1l1lllll11l_opy_
                    if TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1ll1l11ll11_opy_)
                ),
                None,
            )
            if not bstack1l1lll1l1l1_opy_:
                return
            entry = bstack1lll11lll11_opy_(TestFramework.bstack1l1ll1111l1_opy_, message, level)
            self.bstack1l1ll11l1ll_opy_(bstack1l1lll1l1l1_opy_, [entry])
            return return_value
        return bstack1l1lll1llll_opy_
    def bstack1l1lllll1ll_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1lll11_opy_
        levels = [bstack11ll11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤቘ"), bstack11ll11_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦ቙")]
        bstack1l1llll1ll1_opy_ = bstack11ll11_opy_ (u"ࠣࠤቚ")
        if instance is not None:
            try:
                bstack1l1llll1ll1_opy_ = TestFramework.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11ll11_opy_)
            except Exception as e:
                self.logger.warning(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡹ࡮ࡪࠠࡧࡴࡲࡱࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢቛ").format(e))
        bstack1l1l1llll1l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪቜ")]
                bstack1l1ll111l11_opy_ = os.path.join(bstack1l1ll11ll1l_opy_, (bstack1l1lllllll1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll111l11_opy_):
                    self.logger.debug(bstack11ll11_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡯ࡱࡷࠤࡵࡸࡥࡴࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡔࡦࡵࡷࠤࡦࡴࡤࠡࡄࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢቝ").format(bstack1l1ll111l11_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll111l11_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll111l11_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1lll11_opy_:
                        self.logger.info(bstack11ll11_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥ቞").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1lllll1l1_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1lllll1l1_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11ll11_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤ቟"):
                                entry = bstack1lll11lll11_opy_(
                                    kind=bstack11ll11_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤበ"),
                                    message=bstack11ll11_opy_ (u"ࠣࠤቡ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll1ll1l_opy_=file_size,
                                    bstack1l1ll1l1lll_opy_=bstack11ll11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤቢ"),
                                    bstack1llll11_opy_=os.path.abspath(file_path),
                                    bstack1l1llll1l_opy_=bstack1l1llll1ll1_opy_
                                )
                            elif level == bstack11ll11_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢባ"):
                                entry = bstack1lll11lll11_opy_(
                                    kind=bstack11ll11_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨቤ"),
                                    message=bstack11ll11_opy_ (u"ࠧࠨብ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll1ll1l_opy_=file_size,
                                    bstack1l1ll1l1lll_opy_=bstack11ll11_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨቦ"),
                                    bstack1llll11_opy_=os.path.abspath(file_path),
                                    bstack1l1l1lllll1_opy_=bstack1l1llll1ll1_opy_
                                )
                            bstack1l1l1llll1l_opy_.append(entry)
                            _1l1ll1lll11_opy_.add(abs_path)
                        except Exception as bstack1l1ll1lllll_opy_:
                            self.logger.error(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨቧ").format(bstack1l1ll1lllll_opy_))
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢቨ").format(e))
        event[bstack11ll11_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢቩ")] = bstack1l1l1llll1l_opy_
class bstack1l1ll11111l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1l1ll1_opy_ = set()
        kwargs[bstack11ll11_opy_ (u"ࠥࡷࡰ࡯ࡰ࡬ࡧࡼࡷࠧቪ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll11lll1_opy_(obj, self.bstack1l1ll1l1ll1_opy_)
def bstack1l1ll11l1l1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll11lll1_opy_(obj, bstack1l1ll1l1ll1_opy_=None, max_depth=3):
    if bstack1l1ll1l1ll1_opy_ is None:
        bstack1l1ll1l1ll1_opy_ = set()
    if id(obj) in bstack1l1ll1l1ll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1l1ll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1l1llllll_opy_ = TestFramework.bstack1l1ll11l111_opy_(obj)
    bstack1l1lll11ll1_opy_ = next((k.lower() in bstack1l1l1llllll_opy_.lower() for k in bstack1l1l1llll11_opy_.keys()), None)
    if bstack1l1lll11ll1_opy_:
        obj = TestFramework.bstack1l1ll1lll1l_opy_(obj, bstack1l1l1llll11_opy_[bstack1l1lll11ll1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11ll11_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢቫ")):
            keys = getattr(obj, bstack11ll11_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣቬ"), [])
        elif hasattr(obj, bstack11ll11_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣቭ")):
            keys = getattr(obj, bstack11ll11_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤቮ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11ll11_opy_ (u"ࠣࡡࠥቯ"))}
        if not obj and bstack1l1l1llllll_opy_ == bstack11ll11_opy_ (u"ࠤࡳࡥࡹ࡮࡬ࡪࡤ࠱ࡔࡴࡹࡩࡹࡒࡤࡸ࡭ࠨተ"):
            obj = {bstack11ll11_opy_ (u"ࠥࡴࡦࡺࡨࠣቱ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll11l1l1_opy_(key) or str(key).startswith(bstack11ll11_opy_ (u"ࠦࡤࠨቲ")):
            continue
        if value is not None and bstack1l1ll11l1l1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll11lll1_opy_(value, bstack1l1ll1l1ll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll11lll1_opy_(o, bstack1l1ll1l1ll1_opy_, max_depth) for o in value]))
    return result or None