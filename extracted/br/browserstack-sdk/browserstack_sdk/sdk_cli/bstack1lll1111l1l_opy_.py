# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import bstack1111111l1l_opy_, bstack1lllll1lll1_opy_, bstack1111111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1llll1l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1lll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1llll111_opy_, bstack1ll1llllll1_opy_, bstack1ll1lllll1l_opy_, bstack1lll11ll111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lll11111_opy_, bstack1l1l1lll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1lll1111l_opy_ = [bstack1l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥመ"), bstack1l1ll1_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨሙ"), bstack1l1ll1_opy_ (u"ࠢࡤࡱࡱࡪ࡮࡭ࠢሚ"), bstack1l1ll1_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࠤማ"), bstack1l1ll1_opy_ (u"ࠤࡳࡥࡹ࡮ࠢሜ")]
bstack1l1l1llllll_opy_ = bstack1l1l1lll11l_opy_()
bstack1l1lll1ll1l_opy_ = bstack1l1ll1_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࠥም")
bstack1l1ll111ll1_opy_ = {
    bstack1l1ll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡎࡺࡥ࡮ࠤሞ"): bstack1l1lll1111l_opy_,
    bstack1l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡖࡡࡤ࡭ࡤ࡫ࡪࠨሟ"): bstack1l1lll1111l_opy_,
    bstack1l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡍࡰࡦࡸࡰࡪࠨሠ"): bstack1l1lll1111l_opy_,
    bstack1l1ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡄ࡮ࡤࡷࡸࠨሡ"): bstack1l1lll1111l_opy_,
    bstack1l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡈࡸࡲࡨࡺࡩࡰࡰࠥሢ"): bstack1l1lll1111l_opy_
    + [
        bstack1l1ll1_opy_ (u"ࠤࡲࡶ࡮࡭ࡩ࡯ࡣ࡯ࡲࡦࡳࡥࠣሣ"),
        bstack1l1ll1_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧሤ"),
        bstack1l1ll1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩ࡮ࡴࡦࡰࠤሥ"),
        bstack1l1ll1_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢሦ"),
        bstack1l1ll1_opy_ (u"ࠨࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠣሧ"),
        bstack1l1ll1_opy_ (u"ࠢࡤࡣ࡯ࡰࡴࡨࡪࠣረ"),
        bstack1l1ll1_opy_ (u"ࠣࡵࡷࡥࡷࡺࠢሩ"),
        bstack1l1ll1_opy_ (u"ࠤࡶࡸࡴࡶࠢሪ"),
        bstack1l1ll1_opy_ (u"ࠥࡨࡺࡸࡡࡵ࡫ࡲࡲࠧራ"),
        bstack1l1ll1_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤሬ"),
    ],
    bstack1l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡪࡰ࠱ࡗࡪࡹࡳࡪࡱࡱࠦር"): [bstack1l1ll1_opy_ (u"ࠨࡳࡵࡣࡵࡸࡵࡧࡴࡩࠤሮ"), bstack1l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡸ࡬ࡡࡪ࡮ࡨࡨࠧሯ"), bstack1l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡹࡣࡰ࡮࡯ࡩࡨࡺࡥࡥࠤሰ"), bstack1l1ll1_opy_ (u"ࠤ࡬ࡸࡪࡳࡳࠣሱ")],
    bstack1l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡧࡴࡴࡦࡪࡩ࠱ࡇࡴࡴࡦࡪࡩࠥሲ"): [bstack1l1ll1_opy_ (u"ࠦ࡮ࡴࡶࡰࡥࡤࡸ࡮ࡵ࡮ࡠࡲࡤࡶࡦࡳࡳࠣሳ"), bstack1l1ll1_opy_ (u"ࠧࡧࡲࡨࡵࠥሴ")],
    bstack1l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡈ࡬ࡼࡹࡻࡲࡦࡆࡨࡪࠧስ"): [bstack1l1ll1_opy_ (u"ࠢࡴࡥࡲࡴࡪࠨሶ"), bstack1l1ll1_opy_ (u"ࠣࡣࡵ࡫ࡳࡧ࡭ࡦࠤሷ"), bstack1l1ll1_opy_ (u"ࠤࡩࡹࡳࡩࠢሸ"), bstack1l1ll1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡵࠥሹ"), bstack1l1ll1_opy_ (u"ࠦࡺࡴࡩࡵࡶࡨࡷࡹࠨሺ"), bstack1l1ll1_opy_ (u"ࠧ࡯ࡤࡴࠤሻ")],
    bstack1l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡦࡪࡺࡷࡹࡷ࡫ࡳ࠯ࡕࡸࡦࡗ࡫ࡱࡶࡧࡶࡸࠧሼ"): [bstack1l1ll1_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥ࡯ࡣࡰࡩࠧሽ"), bstack1l1ll1_opy_ (u"ࠣࡲࡤࡶࡦࡳࠢሾ"), bstack1l1ll1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡠ࡫ࡱࡨࡪࡾࠢሿ")],
    bstack1l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡶࡺࡴ࡮ࡦࡴ࠱ࡇࡦࡲ࡬ࡊࡰࡩࡳࠧቀ"): [bstack1l1ll1_opy_ (u"ࠦࡼ࡮ࡥ࡯ࠤቁ"), bstack1l1ll1_opy_ (u"ࠧࡸࡥࡴࡷ࡯ࡸࠧቂ")],
    bstack1l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡐࡲࡨࡪࡑࡥࡺࡹࡲࡶࡩࡹࠢቃ"): [bstack1l1ll1_opy_ (u"ࠢ࡯ࡱࡧࡩࠧቄ"), bstack1l1ll1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣቅ")],
    bstack1l1ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡒࡧࡲ࡬ࠤቆ"): [bstack1l1ll1_opy_ (u"ࠥࡲࡦࡳࡥࠣቇ"), bstack1l1ll1_opy_ (u"ࠦࡦࡸࡧࡴࠤቈ"), bstack1l1ll1_opy_ (u"ࠧࡱࡷࡢࡴࡪࡷࠧ቉")],
}
_1l1ll1lll11_opy_ = set()
class bstack1llll1ll1ll_opy_(bstack1llll1111ll_opy_):
    bstack1l1llll111l_opy_ = bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩ࡫ࡦࡦࡴࡵࡩࡩࠨቊ")
    bstack1l1ll11l111_opy_ = bstack1l1ll1_opy_ (u"ࠢࡊࡐࡉࡓࠧቋ")
    bstack1l1ll11l1ll_opy_ = bstack1l1ll1_opy_ (u"ࠣࡇࡕࡖࡔࡘࠢቌ")
    bstack1l1ll11l1l1_opy_: Callable
    bstack1l1llll1lll_opy_: Callable
    def __init__(self, bstack1lll111l1l1_opy_, bstack1lll11l11l1_opy_):
        super().__init__()
        self.bstack1ll1l11l1l1_opy_ = bstack1lll11l11l1_opy_
        if os.getenv(bstack1l1ll1_opy_ (u"ࠤࡖࡈࡐࡥࡃࡍࡋࡢࡊࡑࡇࡇࡠࡑ࠴࠵࡞ࠨቍ"), bstack1l1ll1_opy_ (u"ࠥ࠵ࠧ቎")) != bstack1l1ll1_opy_ (u"ࠦ࠶ࠨ቏") or not self.is_enabled():
            self.logger.warning(bstack1l1ll1_opy_ (u"ࠧࠨቐ") + str(self.__class__.__name__) + bstack1l1ll1_opy_ (u"ࠨࠠࡥ࡫ࡶࡥࡧࡲࡥࡥࠤቑ"))
            return
        TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.PRE), self.bstack1ll11ll111l_opy_)
        TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.POST), self.bstack1ll11l1llll_opy_)
        for event in bstack1ll1llll111_opy_:
            for state in bstack1ll1lllll1l_opy_:
                TestFramework.bstack1ll11llll11_opy_((event, state), self.bstack1l1llll1111_opy_)
        bstack1lll111l1l1_opy_.bstack1ll11llll11_opy_((bstack1lllll1lll1_opy_.bstack1llllllll11_opy_, bstack1111111ll1_opy_.POST), self.bstack1l1ll1l1l11_opy_)
        self.bstack1l1ll11l1l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1ll1lll1l_opy_(bstack1llll1ll1ll_opy_.bstack1l1ll11l111_opy_, self.bstack1l1ll11l1l1_opy_)
        self.bstack1l1llll1lll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1ll1lll1l_opy_(bstack1llll1ll1ll_opy_.bstack1l1ll11l1ll_opy_, self.bstack1l1llll1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll1l111_opy_() and instance:
            bstack1l1ll1l1l1l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llllll1111_opy_
            if test_framework_state == bstack1ll1llll111_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1llll111_opy_.LOG:
                bstack1l1l1lll1_opy_ = datetime.now()
                entries = f.bstack1l1llll11l1_opy_(instance, bstack1llllll1111_opy_)
                if entries:
                    self.bstack1l1lll11l11_opy_(instance, entries)
                    instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺࠢቒ"), datetime.now() - bstack1l1l1lll1_opy_)
                    f.bstack1l1lll11ll1_opy_(instance, bstack1llllll1111_opy_)
                instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦቓ"), datetime.now() - bstack1l1ll1l1l1l_opy_)
                return # bstack1l1l1lllll1_opy_ not send this event with the bstack1l1lll1ll11_opy_ bstack1l1lll111ll_opy_
            elif (
                test_framework_state == bstack1ll1llll111_opy_.TEST
                and test_hook_state == bstack1ll1lllll1l_opy_.POST
                and not f.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)
            ):
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠤࡧࡶࡴࡶࡰࡪࡰࡪࠤࡩࡻࡥࠡࡶࡲࠤࡱࡧࡣ࡬ࠢࡲࡪࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࠢቔ") + str(TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)) + bstack1l1ll1_opy_ (u"ࠥࠦቕ"))
                f.bstack1lllllll1ll_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1llll111l_opy_, True)
                return # bstack1l1l1lllll1_opy_ not send this event bstack1l1ll111l1l_opy_ bstack1l1lll1lll1_opy_
            elif (
                f.bstack111111l111_opy_(instance, bstack1llll1ll1ll_opy_.bstack1l1llll111l_opy_, False)
                and test_framework_state == bstack1ll1llll111_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1lllll1l_opy_.POST
                and f.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)
            ):
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠦ࡮ࡴࡪࡦࡥࡷ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳࡚ࡅࡔࡖ࠯ࠤ࡙࡫ࡳࡵࡊࡲࡳࡰ࡙ࡴࡢࡶࡨ࠲ࡕࡕࡓࡕࠢࠥቖ") + str(TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)) + bstack1l1ll1_opy_ (u"ࠧࠨ቗"))
                self.bstack1l1llll1111_opy_(f, instance, (bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.POST), *args, **kwargs)
            bstack1l1l1lll1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll111l11_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1ll1_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤቘ"), None), data.pop(bstack1l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢ቙"), {}).values()),
                key=lambda x: x[bstack1l1ll1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦቚ")],
            )
            if bstack1llll1l1ll1_opy_.bstack1l1ll11ll11_opy_ in data:
                data.pop(bstack1llll1l1ll1_opy_.bstack1l1ll11ll11_opy_)
            data.update({bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤቛ"): bstack1l1ll111l11_opy_})
            instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣቜ"), datetime.now() - bstack1l1l1lll1_opy_)
            bstack1l1l1lll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1lll11lll_opy_)
            instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢቝ"), datetime.now() - bstack1l1l1lll1_opy_)
            self.bstack1l1lll111ll_opy_(instance, bstack1llllll1111_opy_, event_json=event_json)
            instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣ቞"), datetime.now() - bstack1l1ll1l1l1l_opy_)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l11l1llll_opy_ import bstack1lll11l1l11_opy_
        bstack1ll111l1lll_opy_ = bstack1lll11l1l11_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1lll1l111_opy_.value)
        self.bstack1ll1l11l1l1_opy_.bstack1l1llll1ll1_opy_(instance, f, bstack1llllll1111_opy_, *args, **kwargs)
        bstack1lll11l1l11_opy_.end(EVENTS.bstack1lll1l111_opy_.value, bstack1ll111l1lll_opy_ + bstack1l1ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ቟"), bstack1ll111l1lll_opy_ + bstack1l1ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧበ"), status=True, failure=None, test_name=None)
    def bstack1ll11l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l11l1l1_opy_.bstack1l1lll11l1l_opy_(instance, f, bstack1llllll1111_opy_, *args, **kwargs)
        self.bstack1l1llll1l1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1ll11llll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1l1llll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠣࡕ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡘࡪࡹࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡆࡸࡨࡲࡹࠦࡧࡓࡒࡆࠤࡨࡧ࡬࡭࠼ࠣࡒࡴࠦࡶࡢ࡮࡬ࡨࠥࡸࡥࡲࡷࡨࡷࡹࠦࡤࡢࡶࡤࠦቡ"))
            return
        bstack1l1l1lll1_opy_ = datetime.now()
        try:
            r = self.bstack1lll1l111l1_opy_.TestSessionEvent(req)
            instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡪࡼࡥ࡯ࡶࠥቢ"), datetime.now() - bstack1l1l1lll1_opy_)
            f.bstack1lllllll1ll_opy_(instance, self.bstack1ll1l11l1l1_opy_.bstack1l1l1ll1ll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1ll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧባ") + str(r) + bstack1l1ll1_opy_ (u"ࠦࠧቤ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥብ") + str(e) + bstack1l1ll1_opy_ (u"ࠨࠢቦ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1l1l11_opy_(
        self,
        f: bstack1lll1l1l1ll_opy_,
        _driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        _1l1ll1l11l1_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1l1l1ll_opy_.bstack1ll111lll1l_opy_(method_name):
            return
        if f.bstack1ll1l1l111l_opy_(*args) == bstack1lll1l1l1ll_opy_.bstack1l1ll1lllll_opy_:
            bstack1l1ll1l1l1l_opy_ = datetime.now()
            screenshot = result.get(bstack1l1ll1_opy_ (u"ࠢࡷࡣ࡯ࡹࡪࠨቧ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡩ࡮ࡣࡪࡩࠥࡨࡡࡴࡧ࠹࠸ࠥࡹࡴࡳࠤቨ"))
                return
            bstack1l1l1ll1l11_opy_ = self.bstack1l1ll111111_opy_(instance)
            if bstack1l1l1ll1l11_opy_:
                entry = bstack1lll11ll111_opy_(TestFramework.bstack1l1ll1ll11l_opy_, screenshot)
                self.bstack1l1lll11l11_opy_(bstack1l1l1ll1l11_opy_, [entry])
                instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡨࡼࡪࡩࡵࡵࡧࠥቩ"), datetime.now() - bstack1l1ll1l1l1l_opy_)
            else:
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠥࡹࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡷࡩࡸࡺࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸ࡭࡯ࡳࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥࡽࡡࡴࠢࡷࡥࡰ࡫࡮ࠡࡤࡼࠤࡩࡸࡩࡷࡧࡵࡁࠥࢁࡽࠣቪ").format(instance.ref()))
        event = {}
        bstack1l1l1ll1l11_opy_ = self.bstack1l1ll111111_opy_(instance)
        if bstack1l1l1ll1l11_opy_:
            self.bstack1l1ll1l111l_opy_(event, bstack1l1l1ll1l11_opy_)
            if event.get(bstack1l1ll1_opy_ (u"ࠦࡱࡵࡧࡴࠤቫ")):
                self.bstack1l1lll11l11_opy_(bstack1l1l1ll1l11_opy_, event[bstack1l1ll1_opy_ (u"ࠧࡲ࡯ࡨࡵࠥቬ")])
            else:
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡲ࡯ࡨࡵࠣࡪࡴࡸࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡪࡼࡥ࡯ࡶࠥቭ"))
    @measure(event_name=EVENTS.bstack1l1ll1ll1ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1l1lll11l11_opy_(
        self,
        bstack1l1l1ll1l11_opy_: bstack1ll1llllll1_opy_,
        entries: List[bstack1lll11ll111_opy_],
    ):
        self.bstack1ll111ll1ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111111l111_opy_(bstack1l1l1ll1l11_opy_, TestFramework.bstack1ll11l1l111_opy_)
        req.execution_context.hash = str(bstack1l1l1ll1l11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1ll1l11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1ll1l11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack111111l111_opy_(bstack1l1l1ll1l11_opy_, TestFramework.bstack1ll1l11l1ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack111111l111_opy_(bstack1l1l1ll1l11_opy_, TestFramework.bstack1l1ll1ll1l1_opy_)
            log_entry.uuid = TestFramework.bstack111111l111_opy_(bstack1l1l1ll1l11_opy_, TestFramework.bstack1ll11l1l1ll_opy_)
            log_entry.test_framework_state = bstack1l1l1ll1l11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1ll1_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨቮ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1ll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥቯ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1ll1l1l_opy_
                log_entry.file_path = entry.bstack1llllll1_opy_
        def bstack1l1ll11lll1_opy_():
            bstack1l1l1lll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l111l1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll1ll11l_opy_:
                    bstack1l1l1ll1l11_opy_.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨተ"), datetime.now() - bstack1l1l1lll1_opy_)
                elif entry.kind == TestFramework.bstack1l1ll1llll1_opy_:
                    bstack1l1l1ll1l11_opy_.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢቱ"), datetime.now() - bstack1l1l1lll1_opy_)
                else:
                    bstack1l1l1ll1l11_opy_.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣቲ"), datetime.now() - bstack1l1l1lll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥታ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111ll11_opy_.enqueue(bstack1l1ll11lll1_opy_)
    @measure(event_name=EVENTS.bstack1l1llll11ll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1l1lll111ll_opy_(
        self,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        event_json=None,
    ):
        self.bstack1ll111ll1ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll11l1l111_opy_)
        req.test_framework_name = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll1l11l1ll_opy_)
        req.test_framework_version = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_state = bstack1llllll1111_opy_[0].name
        req.test_hook_state = bstack1llllll1111_opy_[1].name
        started_at = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l1ll111lll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1l1ll1111ll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1lll11lll_opy_)).encode(bstack1l1ll1_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧቴ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1ll11lll1_opy_():
            bstack1l1l1lll1_opy_ = datetime.now()
            try:
                self.bstack1lll1l111l1_opy_.TestFrameworkEvent(req)
                instance.bstack11l1l1111l_opy_(bstack1l1ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡪࡼࡥ࡯ࡶࠥት"), datetime.now() - bstack1l1l1lll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1ll1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨቶ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111ll11_opy_.enqueue(bstack1l1ll11lll1_opy_)
    def bstack1l1ll111111_opy_(self, instance: bstack1111111l1l_opy_):
        bstack1l1lll1llll_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance.context)
        for t in bstack1l1lll1llll_opy_:
            bstack1l1ll11111l_opy_ = TestFramework.bstack111111l111_opy_(t, bstack1llll1l1ll1_opy_.bstack1l1ll11ll11_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll11111l_opy_):
                return t
    def bstack1l1l1llll1l_opy_(self, message):
        self.bstack1l1ll11l1l1_opy_(message + bstack1l1ll1_opy_ (u"ࠤ࡟ࡲࠧቷ"))
    def log_error(self, message):
        self.bstack1l1llll1lll_opy_(message + bstack1l1ll1_opy_ (u"ࠥࡠࡳࠨቸ"))
    def bstack1l1ll1lll1l_opy_(self, level, original_func):
        def bstack1l1ll11l11l_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1lll1llll_opy_ = TestFramework.bstack1l1ll1l11ll_opy_()
            if not bstack1l1lll1llll_opy_:
                return return_value
            bstack1l1l1ll1l11_opy_ = next(
                (
                    instance
                    for instance in bstack1l1lll1llll_opy_
                    if TestFramework.bstack1lllll1ll1l_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
                ),
                None,
            )
            if not bstack1l1l1ll1l11_opy_:
                return
            entry = bstack1lll11ll111_opy_(TestFramework.bstack1l1lll111l1_opy_, message, level)
            self.bstack1l1lll11l11_opy_(bstack1l1l1ll1l11_opy_, [entry])
            return return_value
        return bstack1l1ll11l11l_opy_
    def bstack1l1ll1l111l_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1lll11_opy_
        levels = [bstack1l1ll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢቹ"), bstack1l1ll1_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤቺ")]
        bstack1l1ll1l1ll1_opy_ = bstack1l1ll1_opy_ (u"ࠨࠢቻ")
        if instance is not None:
            try:
                bstack1l1ll1l1ll1_opy_ = TestFramework.bstack111111l111_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧቼ").format(e))
        bstack1l1lll1l1ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨች")]
                bstack1l1l1lll111_opy_ = os.path.join(bstack1l1l1llllll_opy_, (bstack1l1lll1ll1l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1l1lll111_opy_):
                    self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧቾ").format(bstack1l1l1lll111_opy_))
                    continue
                file_names = os.listdir(bstack1l1l1lll111_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1l1lll111_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1lll11_opy_:
                        self.logger.info(bstack1l1ll1_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣቿ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l1llll11_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l1llll11_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1ll1_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢኀ"):
                                entry = bstack1lll11ll111_opy_(
                                    kind=bstack1l1ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢኁ"),
                                    message=bstack1l1ll1_opy_ (u"ࠨࠢኂ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l1ll1l1l_opy_=file_size,
                                    bstack1l1l1ll1lll_opy_=bstack1l1ll1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢኃ"),
                                    bstack1llllll1_opy_=os.path.abspath(file_path),
                                    bstack1l11l11l1_opy_=bstack1l1ll1l1ll1_opy_
                                )
                            elif level == bstack1l1ll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧኄ"):
                                entry = bstack1lll11ll111_opy_(
                                    kind=bstack1l1ll1_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦኅ"),
                                    message=bstack1l1ll1_opy_ (u"ࠥࠦኆ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l1ll1l1l_opy_=file_size,
                                    bstack1l1l1ll1lll_opy_=bstack1l1ll1_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦኇ"),
                                    bstack1llllll1_opy_=os.path.abspath(file_path),
                                    bstack1l1ll1l1lll_opy_=bstack1l1ll1l1ll1_opy_
                                )
                            bstack1l1lll1l1ll_opy_.append(entry)
                            _1l1ll1lll11_opy_.add(abs_path)
                        except Exception as bstack1l1ll11ll1l_opy_:
                            self.logger.error(bstack1l1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦኈ").format(bstack1l1ll11ll1l_opy_))
        except Exception as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧ኉").format(e))
        event[bstack1l1ll1_opy_ (u"ࠢ࡭ࡱࡪࡷࠧኊ")] = bstack1l1lll1l1ll_opy_
class bstack1l1lll11lll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1111l1_opy_ = set()
        kwargs[bstack1l1ll1_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥኋ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1l1111_opy_(obj, self.bstack1l1ll1111l1_opy_)
def bstack1l1l1lll1l1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1l1111_opy_(obj, bstack1l1ll1111l1_opy_=None, max_depth=3):
    if bstack1l1ll1111l1_opy_ is None:
        bstack1l1ll1111l1_opy_ = set()
    if id(obj) in bstack1l1ll1111l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1111l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llll1l11_opy_ = TestFramework.bstack1l1l1lll1ll_opy_(obj)
    bstack1l1lll1l11l_opy_ = next((k.lower() in bstack1l1llll1l11_opy_.lower() for k in bstack1l1ll111ll1_opy_.keys()), None)
    if bstack1l1lll1l11l_opy_:
        obj = TestFramework.bstack1l1lll1l1l1_opy_(obj, bstack1l1ll111ll1_opy_[bstack1l1lll1l11l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1ll1_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧኌ")):
            keys = getattr(obj, bstack1l1ll1_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨኍ"), [])
        elif hasattr(obj, bstack1l1ll1_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨ኎")):
            keys = getattr(obj, bstack1l1ll1_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢ኏"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1ll1_opy_ (u"ࠨ࡟ࠣነ"))}
        if not obj and bstack1l1llll1l11_opy_ == bstack1l1ll1_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦኑ"):
            obj = {bstack1l1ll1_opy_ (u"ࠣࡲࡤࡸ࡭ࠨኒ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1l1lll1l1_opy_(key) or str(key).startswith(bstack1l1ll1_opy_ (u"ࠤࡢࠦና")):
            continue
        if value is not None and bstack1l1l1lll1l1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1l1111_opy_(value, bstack1l1ll1111l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1l1111_opy_(o, bstack1l1ll1111l1_opy_, max_depth) for o in value]))
    return result or None