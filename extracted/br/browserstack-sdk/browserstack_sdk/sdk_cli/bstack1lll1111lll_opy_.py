# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import bstack1111111l1l_opy_, bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1ll111l_opy_, bstack1ll1l1lll1l_opy_, bstack1lll1111l1l_opy_, bstack1lll111ll1l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lll11111_opy_, bstack1l1ll1l11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1llll11l1_opy_ = [bstack11ll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥመ"), bstack11ll1l1_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨሙ"), bstack11ll1l1_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢሚ"), bstack11ll1l1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࠤማ"), bstack11ll1l1_opy_ (u"ࠤࡳࡥࡹ࡮ࠢሜ")]
bstack1l1l1llll11_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l1l1ll1ll1_opy_ = bstack11ll1l1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥም")
bstack1l1llll1ll1_opy_ = {
    bstack11ll1l1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡎࡺࡥ࡮ࠤሞ"): bstack1l1llll11l1_opy_,
    bstack11ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡖࡡࡤ࡭ࡤ࡫ࡪࠨሟ"): bstack1l1llll11l1_opy_,
    bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡍࡰࡦࡸࡰࡪࠨሠ"): bstack1l1llll11l1_opy_,
    bstack11ll1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡄ࡮ࡤࡷࡸࠨሡ"): bstack1l1llll11l1_opy_,
    bstack11ll1l1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡈࡸࡲࡨࡺࡩࡰࡰࠥሢ"): bstack1l1llll11l1_opy_
    + [
        bstack11ll1l1_opy_ (u"ࠤࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡲࡦࡳࡥࠣሣ"),
        bstack11ll1l1_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧሤ"),
        bstack11ll1l1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩ࡮ࡴࡦࡰࠤሥ"),
        bstack11ll1l1_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢሦ"),
        bstack11ll1l1_opy_ (u"ࠨࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠣሧ"),
        bstack11ll1l1_opy_ (u"ࠢࡤࡣ࡯ࡰࡴࡨࡪࠣረ"),
        bstack11ll1l1_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢሩ"),
        bstack11ll1l1_opy_ (u"ࠤࡶࡸࡴࡶࠢሪ"),
        bstack11ll1l1_opy_ (u"ࠥࡨࡺࡸࡡࡵ࡫ࡲࡲࠧራ"),
        bstack11ll1l1_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤሬ"),
    ],
    bstack11ll1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡪࡰ࠱ࡗࡪࡹࡳࡪࡱࡱࠦር"): [bstack11ll1l1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡵࡧࡴࡩࠤሮ"), bstack11ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡸ࡬ࡡࡪ࡮ࡨࡨࠧሯ"), bstack11ll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡹࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤሰ"), bstack11ll1l1_opy_ (u"ࠤ࡬ࡸࡪࡳࡳࠣሱ")],
    bstack11ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡧࡴࡴࡦࡪࡩ࠱ࡇࡴࡴࡦࡪࡩࠥሲ"): [bstack11ll1l1_opy_ (u"ࠦ࡮ࡴࡶࡰࡥࡤࡸ࡮ࡵ࡮ࡠࡲࡤࡶࡦࡳࡳࠣሳ"), bstack11ll1l1_opy_ (u"ࠧࡧࡲࡨࡵࠥሴ")],
    bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡈ࡬ࡼࡹࡻࡲࡦࡆࡨࡪࠧስ"): [bstack11ll1l1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨሶ"), bstack11ll1l1_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤሷ"), bstack11ll1l1_opy_ (u"ࠤࡩࡹࡳࡩࠢሸ"), bstack11ll1l1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥሹ"), bstack11ll1l1_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨሺ"), bstack11ll1l1_opy_ (u"ࠧ࡯ࡤࡴࠤሻ")],
    bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡕࡸࡦࡗ࡫ࡱࡶࡧࡶࡸࠧሼ"): [bstack11ll1l1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧሽ"), bstack11ll1l1_opy_ (u"ࠣࡲࡤࡶࡦࡳࠢሾ"), bstack11ll1l1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡠ࡫ࡱࡨࡪࡾࠢሿ")],
    bstack11ll1l1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡶࡺࡴ࡮ࡦࡴ࠱ࡇࡦࡲ࡬ࡊࡰࡩࡳࠧቀ"): [bstack11ll1l1_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤቁ"), bstack11ll1l1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࠧቂ")],
    bstack11ll1l1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡐࡲࡨࡪࡑࡥࡺࡹࡲࡶࡩࡹࠢቃ"): [bstack11ll1l1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧቄ"), bstack11ll1l1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣቅ")],
    bstack11ll1l1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡒࡧࡲ࡬ࠤቆ"): [bstack11ll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣቇ"), bstack11ll1l1_opy_ (u"ࠦࡦࡸࡧࡴࠤቈ"), bstack11ll1l1_opy_ (u"ࠧࡱࡷࡢࡴࡪࡷࠧ቉")],
}
_1l1ll11l1l1_opy_ = set()
class bstack1lll11lllll_opy_(bstack1lll1ll1l1l_opy_):
    bstack1l1ll1l1lll_opy_ = bstack11ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࠨቊ")
    bstack1l1l1ll1l11_opy_ = bstack11ll1l1_opy_ (u"ࠢࡊࡐࡉࡓࠧቋ")
    bstack1l1ll11ll11_opy_ = bstack11ll1l1_opy_ (u"ࠣࡇࡕࡖࡔࡘࠢቌ")
    bstack1l1l1llllll_opy_: Callable
    bstack1l1lll1lll1_opy_: Callable
    def __init__(self, bstack1ll1l1ll1l1_opy_, bstack1ll1ll1ll1l_opy_):
        super().__init__()
        self.bstack1ll11lll11l_opy_ = bstack1ll1ll1ll1l_opy_
        if os.getenv(bstack11ll1l1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡑ࠴࠵࡞ࠨቍ"), bstack11ll1l1_opy_ (u"ࠥ࠵ࠧ቎")) != bstack11ll1l1_opy_ (u"ࠦ࠶ࠨ቏") or not self.is_enabled():
            self.logger.warning(bstack11ll1l1_opy_ (u"ࠧࠨቐ") + str(self.__class__.__name__) + bstack11ll1l1_opy_ (u"ࠨࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠤቑ"))
            return
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.PRE), self.bstack1ll111l11ll_opy_)
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST), self.bstack1ll11lllll1_opy_)
        for event in bstack1lll1ll111l_opy_:
            for state in bstack1lll1111l1l_opy_:
                TestFramework.bstack1ll11l11lll_opy_((event, state), self.bstack1l1lll1ll1l_opy_)
        bstack1ll1l1ll1l1_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.POST), self.bstack1l1l1llll1l_opy_)
        self.bstack1l1l1llllll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1llll1l11_opy_(bstack1lll11lllll_opy_.bstack1l1l1ll1l11_opy_, self.bstack1l1l1llllll_opy_)
        self.bstack1l1lll1lll1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1llll1l11_opy_(bstack1lll11lllll_opy_.bstack1l1ll11ll11_opy_, self.bstack1l1lll1lll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1l1lll1l1_opy_() and instance:
            bstack1l1ll11llll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llllllllll_opy_
            if test_framework_state == bstack1lll1ll111l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1ll111l_opy_.LOG:
                bstack11ll11ll1_opy_ = datetime.now()
                entries = f.bstack1l1ll1l111l_opy_(instance, bstack1llllllllll_opy_)
                if entries:
                    self.bstack1l1ll11l11l_opy_(instance, entries)
                    instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺࠢቒ"), datetime.now() - bstack11ll11ll1_opy_)
                    f.bstack1l1ll11l111_opy_(instance, bstack1llllllllll_opy_)
                instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦቓ"), datetime.now() - bstack1l1ll11llll_opy_)
                return # bstack1l1lll11l11_opy_ not send this event with the bstack1l1ll11111l_opy_ bstack1l1ll1lll1l_opy_
            elif (
                test_framework_state == bstack1lll1ll111l_opy_.TEST
                and test_hook_state == bstack1lll1111l1l_opy_.POST
                and not f.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_)
            ):
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠤࡧࡶࡴࡶࡰࡪࡰࡪࠤࡩࡻࡥࠡࡶࡲࠤࡱࡧࡣ࡬ࠢࡲࡪࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࠢቔ") + str(TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_)) + bstack11ll1l1_opy_ (u"ࠥࠦቕ"))
                f.bstack1lllll1ll1l_opy_(instance, bstack1lll11lllll_opy_.bstack1l1ll1l1lll_opy_, True)
                return # bstack1l1lll11l11_opy_ not send this event bstack1l1l1lll11l_opy_ bstack1l1ll1l11ll_opy_
            elif (
                f.bstack11111111ll_opy_(instance, bstack1lll11lllll_opy_.bstack1l1ll1l1lll_opy_, False)
                and test_framework_state == bstack1lll1ll111l_opy_.LOG_REPORT
                and test_hook_state == bstack1lll1111l1l_opy_.POST
                and f.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_)
            ):
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠦ࡮ࡴࡪࡦࡥࡷ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳࡚ࡅࡔࡖ࠯ࠤ࡙࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࡕࡕࡓࡕࠢࠥቖ") + str(TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1lll11l1l_opy_)) + bstack11ll1l1_opy_ (u"ࠧࠨ቗"))
                self.bstack1l1lll1ll1l_opy_(f, instance, (bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST), *args, **kwargs)
            bstack11ll11ll1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1llll1l1l_opy_ = sorted(
                filter(lambda x: x.get(bstack11ll1l1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤቘ"), None), data.pop(bstack11ll1l1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ቙"), {}).values()),
                key=lambda x: x[bstack11ll1l1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦቚ")],
            )
            if bstack1lll111l1l1_opy_.bstack1l1l1ll1lll_opy_ in data:
                data.pop(bstack1lll111l1l1_opy_.bstack1l1l1ll1lll_opy_)
            data.update({bstack11ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤቛ"): bstack1l1llll1l1l_opy_})
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣቜ"), datetime.now() - bstack11ll11ll1_opy_)
            bstack11ll11ll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1llll1111_opy_)
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢቝ"), datetime.now() - bstack11ll11ll1_opy_)
            self.bstack1l1ll1lll1l_opy_(instance, bstack1llllllllll_opy_, event_json=event_json)
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣ቞"), datetime.now() - bstack1l1ll11llll_opy_)
    def bstack1ll111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
        bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack1l11l11l1_opy_.value)
        self.bstack1ll11lll11l_opy_.bstack1l1ll1l1ll1_opy_(instance, f, bstack1llllllllll_opy_, *args, **kwargs)
        bstack1llll11lll1_opy_.end(EVENTS.bstack1l11l11l1_opy_.value, bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ቟"), bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧበ"), status=True, failure=None, test_name=None)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11lll11l_opy_.bstack1l1ll1lll11_opy_(instance, f, bstack1llllllllll_opy_, *args, **kwargs)
        self.bstack1l1l1ll1l1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll1l1ll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l1l1ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹࠦࡧࡓࡒࡆࠤࡨࡧ࡬࡭࠼ࠣࡒࡴࠦࡶࡢ࡮࡬ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠦቡ"))
            return
        bstack11ll11ll1_opy_ = datetime.now()
        try:
            r = self.bstack1lll1l1ll1l_opy_.TestSessionEvent(req)
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡪࡼࡥ࡯ࡶࠥቢ"), datetime.now() - bstack11ll11ll1_opy_)
            f.bstack1lllll1ll1l_opy_(instance, self.bstack1ll11lll11l_opy_.bstack1l1ll1l1111_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11ll1l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧባ") + str(r) + bstack11ll1l1_opy_ (u"ࠦࠧቤ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥብ") + str(e) + bstack11ll1l1_opy_ (u"ࠨࠢቦ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1llll1l_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        _driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        _1l1lll1111l_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1lllllll_opy_.bstack1ll11l1lll1_opy_(method_name):
            return
        if f.bstack1ll1l111ll1_opy_(*args) == bstack1ll1lllllll_opy_.bstack1l1lll111ll_opy_:
            bstack1l1ll11llll_opy_ = datetime.now()
            screenshot = result.get(bstack11ll1l1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨቧ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡩ࡮ࡣࡪࡩࠥࡨࡡࡴࡧ࠹࠸ࠥࡹࡴࡳࠤቨ"))
                return
            bstack1l1lll1l1l1_opy_ = self.bstack1l1ll111l1l_opy_(instance)
            if bstack1l1lll1l1l1_opy_:
                entry = bstack1lll111ll1l_opy_(TestFramework.bstack1l1lll11lll_opy_, screenshot)
                self.bstack1l1ll11l11l_opy_(bstack1l1lll1l1l1_opy_, [entry])
                instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡨࡼࡪࡩࡵࡵࡧࠥቩ"), datetime.now() - bstack1l1ll11llll_opy_)
            else:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠥࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷࡩࡸࡺࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸ࡭࡯ࡳࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡽࡡࡴࠢࡷࡥࡰ࡫࡮ࠡࡤࡼࠤࡩࡸࡩࡷࡧࡵࡁࠥࢁࡽࠣቪ").format(instance.ref()))
        event = {}
        bstack1l1lll1l1l1_opy_ = self.bstack1l1ll111l1l_opy_(instance)
        if bstack1l1lll1l1l1_opy_:
            self.bstack1l1lll1l111_opy_(event, bstack1l1lll1l1l1_opy_)
            if event.get(bstack11ll1l1_opy_ (u"ࠦࡱࡵࡧࡴࠤቫ")):
                self.bstack1l1ll11l11l_opy_(bstack1l1lll1l1l1_opy_, event[bstack11ll1l1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥቬ")])
            else:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡲ࡯ࡨࡵࠣࡪࡴࡸࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡪࡼࡥ࡯ࡶࠥቭ"))
    @measure(event_name=EVENTS.bstack1l1ll111ll1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l1ll11l11l_opy_(
        self,
        bstack1l1lll1l1l1_opy_: bstack1ll1l1lll1l_opy_,
        entries: List[bstack1lll111ll1l_opy_],
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll111ll11l_opy_)
        req.execution_context.hash = str(bstack1l1lll1l1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll1l1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll1l1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11lll111_opy_)
            log_entry.test_framework_version = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1ll1111l1_opy_)
            log_entry.uuid = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1ll11l11l11_opy_)
            log_entry.test_framework_state = bstack1l1lll1l1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll1l1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨቮ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11ll1l1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥቯ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1lll1llll_opy_
                log_entry.file_path = entry.bstack11111ll_opy_
        def bstack1l1ll1l1l11_opy_():
            bstack11ll11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1ll1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1lll11lll_opy_:
                    bstack1l1lll1l1l1_opy_.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨተ"), datetime.now() - bstack11ll11ll1_opy_)
                elif entry.kind == TestFramework.bstack1l1ll111l11_opy_:
                    bstack1l1lll1l1l1_opy_.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢቱ"), datetime.now() - bstack11ll11ll1_opy_)
                else:
                    bstack1l1lll1l1l1_opy_.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣቲ"), datetime.now() - bstack11ll11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll1l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥታ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111lll1_opy_.enqueue(bstack1l1ll1l1l11_opy_)
    @measure(event_name=EVENTS.bstack1l1l1lll1ll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l1ll1lll1l_opy_(
        self,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        event_json=None,
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111ll11l_opy_)
        req.test_framework_name = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11lll111_opy_)
        req.test_framework_version = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1ll1111l1_opy_)
        req.test_framework_state = bstack1llllllllll_opy_[0].name
        req.test_hook_state = bstack1llllllllll_opy_[1].name
        started_at = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1lll11ll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1l1lll111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1llll1111_opy_)).encode(bstack11ll1l1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧቴ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1ll1l1l11_opy_():
            bstack11ll11ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1ll1l_opy_.TestFrameworkEvent(req)
                instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡪࡼࡥ࡯ࡶࠥት"), datetime.now() - bstack11ll11ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቶ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111lll1_opy_.enqueue(bstack1l1ll1l1l11_opy_)
    def bstack1l1ll111l1l_opy_(self, instance: bstack1111111l1l_opy_):
        bstack1l1ll1111ll_opy_ = TestFramework.bstack1lllll1llll_opy_(instance.context)
        for t in bstack1l1ll1111ll_opy_:
            bstack1l1lll1ll11_opy_ = TestFramework.bstack11111111ll_opy_(t, bstack1lll111l1l1_opy_.bstack1l1l1ll1lll_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1ll11_opy_):
                return t
    def bstack1l1ll11lll1_opy_(self, message):
        self.bstack1l1l1llllll_opy_(message + bstack11ll1l1_opy_ (u"ࠤ࡟ࡲࠧቷ"))
    def log_error(self, message):
        self.bstack1l1lll1lll1_opy_(message + bstack11ll1l1_opy_ (u"ࠥࡠࡳࠨቸ"))
    def bstack1l1llll1l11_opy_(self, level, original_func):
        def bstack1l1lll111l1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1ll1111ll_opy_ = TestFramework.bstack1l1ll1ll11l_opy_()
            if not bstack1l1ll1111ll_opy_:
                return return_value
            bstack1l1lll1l1l1_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1111ll_opy_
                    if TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1ll11l11l11_opy_)
                ),
                None,
            )
            if not bstack1l1lll1l1l1_opy_:
                return
            entry = bstack1lll111ll1l_opy_(TestFramework.bstack1l1ll11ll1l_opy_, message, level)
            self.bstack1l1ll11l11l_opy_(bstack1l1lll1l1l1_opy_, [entry])
            return return_value
        return bstack1l1lll111l1_opy_
    def bstack1l1lll1l111_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll11l1l1_opy_
        levels = [bstack11ll1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢቹ"), bstack11ll1l1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤቺ")]
        bstack1l1ll111111_opy_ = bstack11ll1l1_opy_ (u"ࠨࠢቻ")
        if instance is not None:
            try:
                bstack1l1ll111111_opy_ = TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11l11l11_opy_)
            except Exception as e:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧቼ").format(e))
        bstack1l1ll11l1ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨች")]
                bstack1l1lll1l11l_opy_ = os.path.join(bstack1l1l1llll11_opy_, (bstack1l1l1ll1ll1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1lll1l11l_opy_):
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧቾ").format(bstack1l1lll1l11l_opy_))
                    continue
                file_names = os.listdir(bstack1l1lll1l11l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1lll1l11l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll11l1l1_opy_:
                        self.logger.info(bstack11ll1l1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣቿ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1llll11ll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1llll11ll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11ll1l1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢኀ"):
                                entry = bstack1lll111ll1l_opy_(
                                    kind=bstack11ll1l1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢኁ"),
                                    message=bstack11ll1l1_opy_ (u"ࠨࠢኂ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll1llll_opy_=file_size,
                                    bstack1l1ll1lllll_opy_=bstack11ll1l1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢኃ"),
                                    bstack11111ll_opy_=os.path.abspath(file_path),
                                    bstack1llll11ll1_opy_=bstack1l1ll111111_opy_
                                )
                            elif level == bstack11ll1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧኄ"):
                                entry = bstack1lll111ll1l_opy_(
                                    kind=bstack11ll1l1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦኅ"),
                                    message=bstack11ll1l1_opy_ (u"ࠥࠦኆ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1lll1llll_opy_=file_size,
                                    bstack1l1ll1lllll_opy_=bstack11ll1l1_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦኇ"),
                                    bstack11111ll_opy_=os.path.abspath(file_path),
                                    bstack1l1llll111l_opy_=bstack1l1ll111111_opy_
                                )
                            bstack1l1ll11l1ll_opy_.append(entry)
                            _1l1ll11l1l1_opy_.add(abs_path)
                        except Exception as bstack1l1ll1ll1ll_opy_:
                            self.logger.error(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦኈ").format(bstack1l1ll1ll1ll_opy_))
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧ኉").format(e))
        event[bstack11ll1l1_opy_ (u"ࠢ࡭ࡱࡪࡷࠧኊ")] = bstack1l1ll11l1ll_opy_
class bstack1l1llll1111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1ll111_opy_ = set()
        kwargs[bstack11ll1l1_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥኋ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l1lllll1_opy_(obj, self.bstack1l1ll1ll111_opy_)
def bstack1l1ll1llll1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l1lllll1_opy_(obj, bstack1l1ll1ll111_opy_=None, max_depth=3):
    if bstack1l1ll1ll111_opy_ is None:
        bstack1l1ll1ll111_opy_ = set()
    if id(obj) in bstack1l1ll1ll111_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1ll111_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1ll111lll_opy_ = TestFramework.bstack1l1ll1ll1l1_opy_(obj)
    bstack1l1l1ll11ll_opy_ = next((k.lower() in bstack1l1ll111lll_opy_.lower() for k in bstack1l1llll1ll1_opy_.keys()), None)
    if bstack1l1l1ll11ll_opy_:
        obj = TestFramework.bstack1l1ll1l1l1l_opy_(obj, bstack1l1llll1ll1_opy_[bstack1l1l1ll11ll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11ll1l1_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧኌ")):
            keys = getattr(obj, bstack11ll1l1_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨኍ"), [])
        elif hasattr(obj, bstack11ll1l1_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨ኎")):
            keys = getattr(obj, bstack11ll1l1_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢ኏"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11ll1l1_opy_ (u"ࠨ࡟ࠣነ"))}
        if not obj and bstack1l1ll111lll_opy_ == bstack11ll1l1_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦኑ"):
            obj = {bstack11ll1l1_opy_ (u"ࠣࡲࡤࡸ࡭ࠨኒ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll1llll1_opy_(key) or str(key).startswith(bstack11ll1l1_opy_ (u"ࠤࡢࠦና")):
            continue
        if value is not None and bstack1l1ll1llll1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l1lllll1_opy_(value, bstack1l1ll1ll111_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l1lllll1_opy_(o, bstack1l1ll1ll111_opy_, max_depth) for o in value]))
    return result or None