# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import bstack1llll1ll111_opy_, bstack1lllll1l111_opy_, bstack1lllll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1lll1111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1ll11_opy_, bstack1lll11ll1l1_opy_, bstack1ll1lllll11_opy_, bstack1ll1l1l1ll1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l1lll111_opy_, bstack1l1l1lll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll111l1l_opy_ = [bstack1ll11ll_opy_ (u"ࠥࡲࡦࡳࡥࠣቜ"), bstack1ll11ll_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦቝ"), bstack1ll11ll_opy_ (u"ࠧࡩ࡯࡯ࡨ࡬࡫ࠧ቞"), bstack1ll11ll_opy_ (u"ࠨࡳࡦࡵࡶ࡭ࡴࡴࠢ቟"), bstack1ll11ll_opy_ (u"ࠢࡱࡣࡷ࡬ࠧበ")]
bstack1l1ll1llll1_opy_ = bstack1l1l1lll1l1_opy_()
bstack1l1ll11111l_opy_ = bstack1ll11ll_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࠣቡ")
bstack1l1ll1111ll_opy_ = {
    bstack1ll11ll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡌࡸࡪࡳࠢቢ"): bstack1l1ll111l1l_opy_,
    bstack1ll11ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡔࡦࡩ࡫ࡢࡩࡨࠦባ"): bstack1l1ll111l1l_opy_,
    bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡒࡵࡤࡶ࡮ࡨࠦቤ"): bstack1l1ll111l1l_opy_,
    bstack1ll11ll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡉ࡬ࡢࡵࡶࠦብ"): bstack1l1ll111l1l_opy_,
    bstack1ll11ll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡆࡶࡰࡦࡸ࡮ࡵ࡮ࠣቦ"): bstack1l1ll111l1l_opy_
    + [
        bstack1ll11ll_opy_ (u"ࠢࡰࡴ࡬࡫࡮ࡴࡡ࡭ࡰࡤࡱࡪࠨቧ"),
        bstack1ll11ll_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥቨ"),
        bstack1ll11ll_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧ࡬ࡲ࡫ࡵࠢቩ"),
        bstack1ll11ll_opy_ (u"ࠥ࡯ࡪࡿࡷࡰࡴࡧࡷࠧቪ"),
        bstack1ll11ll_opy_ (u"ࠦࡨࡧ࡬࡭ࡵࡳࡩࡨࠨቫ"),
        bstack1ll11ll_opy_ (u"ࠧࡩࡡ࡭࡮ࡲࡦ࡯ࠨቬ"),
        bstack1ll11ll_opy_ (u"ࠨࡳࡵࡣࡵࡸࠧቭ"),
        bstack1ll11ll_opy_ (u"ࠢࡴࡶࡲࡴࠧቮ"),
        bstack1ll11ll_opy_ (u"ࠣࡦࡸࡶࡦࡺࡩࡰࡰࠥቯ"),
        bstack1ll11ll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢተ"),
    ],
    bstack1ll11ll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦ࡯࡮࠯ࡕࡨࡷࡸ࡯࡯࡯ࠤቱ"): [bstack1ll11ll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡳࡥࡹ࡮ࠢቲ"), bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡶࡪࡦ࡯࡬ࡦࡦࠥታ"), bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷࡷࡨࡵ࡬࡭ࡧࡦࡸࡪࡪࠢቴ"), bstack1ll11ll_opy_ (u"ࠢࡪࡶࡨࡱࡸࠨት")],
    bstack1ll11ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡥࡲࡲ࡫࡯ࡧ࠯ࡅࡲࡲ࡫࡯ࡧࠣቶ"): [bstack1ll11ll_opy_ (u"ࠤ࡬ࡲࡻࡵࡣࡢࡶ࡬ࡳࡳࡥࡰࡢࡴࡤࡱࡸࠨቷ"), bstack1ll11ll_opy_ (u"ࠥࡥࡷ࡭ࡳࠣቸ")],
    bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡆࡪࡺࡷࡹࡷ࡫ࡄࡦࡨࠥቹ"): [bstack1ll11ll_opy_ (u"ࠧࡹࡣࡰࡲࡨࠦቺ"), bstack1ll11ll_opy_ (u"ࠨࡡࡳࡩࡱࡥࡲ࡫ࠢቻ"), bstack1ll11ll_opy_ (u"ࠢࡧࡷࡱࡧࠧቼ"), bstack1ll11ll_opy_ (u"ࠣࡲࡤࡶࡦࡳࡳࠣች"), bstack1ll11ll_opy_ (u"ࠤࡸࡲ࡮ࡺࡴࡦࡵࡷࠦቾ"), bstack1ll11ll_opy_ (u"ࠥ࡭ࡩࡹࠢቿ")],
    bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲࡫࡯ࡸࡵࡷࡵࡩࡸ࠴ࡓࡶࡤࡕࡩࡶࡻࡥࡴࡶࠥኀ"): [bstack1ll11ll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪࡴࡡ࡮ࡧࠥኁ"), bstack1ll11ll_opy_ (u"ࠨࡰࡢࡴࡤࡱࠧኂ"), bstack1ll11ll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡥࡩ࡯ࡦࡨࡼࠧኃ")],
    bstack1ll11ll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡴࡸࡲࡳ࡫ࡲ࠯ࡅࡤࡰࡱࡏ࡮ࡧࡱࠥኄ"): [bstack1ll11ll_opy_ (u"ࠤࡺ࡬ࡪࡴࠢኅ"), bstack1ll11ll_opy_ (u"ࠥࡶࡪࡹࡵ࡭ࡶࠥኆ")],
    bstack1ll11ll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡎࡰࡦࡨࡏࡪࡿࡷࡰࡴࡧࡷࠧኇ"): [bstack1ll11ll_opy_ (u"ࠧࡴ࡯ࡥࡧࠥኈ"), bstack1ll11ll_opy_ (u"ࠨࡰࡢࡴࡨࡲࡹࠨ኉")],
    bstack1ll11ll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡐࡥࡷࡱࠢኊ"): [bstack1ll11ll_opy_ (u"ࠣࡰࡤࡱࡪࠨኋ"), bstack1ll11ll_opy_ (u"ࠤࡤࡶ࡬ࡹࠢኌ"), bstack1ll11ll_opy_ (u"ࠥ࡯ࡼࡧࡲࡨࡵࠥኍ")],
}
_1l1ll1l111l_opy_ = set()
class bstack1lll1lll1l1_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l1l1ll1l11_opy_ = bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡧࡩ࡫࡫ࡲࡳࡧࡧࠦ኎")
    bstack1l1lll11lll_opy_ = bstack1ll11ll_opy_ (u"ࠧࡏࡎࡇࡑࠥ኏")
    bstack1l1ll11ll11_opy_ = bstack1ll11ll_opy_ (u"ࠨࡅࡓࡔࡒࡖࠧነ")
    bstack1l1lll1ll1l_opy_: Callable
    bstack1l1ll11lll1_opy_: Callable
    def __init__(self, bstack1ll1lll1l1l_opy_, bstack1ll1ll1l1l1_opy_):
        super().__init__()
        self.bstack1ll11lll1l1_opy_ = bstack1ll1ll1l1l1_opy_
        if os.getenv(bstack1ll11ll_opy_ (u"ࠢࡔࡆࡎࡣࡈࡒࡉࡠࡈࡏࡅࡌࡥࡏ࠲࠳࡜ࠦኑ"), bstack1ll11ll_opy_ (u"ࠣ࠳ࠥኒ")) != bstack1ll11ll_opy_ (u"ࠤ࠴ࠦና") or not self.is_enabled():
            self.logger.warning(bstack1ll11ll_opy_ (u"ࠥࠦኔ") + str(self.__class__.__name__) + bstack1ll11ll_opy_ (u"ࠦࠥࡪࡩࡴࡣࡥࡰࡪࡪࠢን"))
            return
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.PRE), self.bstack1ll11ll1l11_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), self.bstack1ll1l1111ll_opy_)
        for event in bstack1lll1l1ll11_opy_:
            for state in bstack1ll1lllll11_opy_:
                TestFramework.bstack1ll111l11ll_opy_((event, state), self.bstack1l1l1l1llll_opy_)
        bstack1ll1lll1l1l_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.POST), self.bstack1l1lll11ll1_opy_)
        self.bstack1l1lll1ll1l_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1l1l1lll1_opy_(bstack1lll1lll1l1_opy_.bstack1l1lll11lll_opy_, self.bstack1l1lll1ll1l_opy_)
        self.bstack1l1ll11lll1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1l1l1lll1_opy_(bstack1lll1lll1l1_opy_.bstack1l1ll11ll11_opy_, self.bstack1l1ll11lll1_opy_)
        self.bstack1l1l1llllll_opy_ = builtins.print
        builtins.print = self.bstack1l1l1lllll1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1ll1l11l1_opy_() and instance:
            bstack1l1lll1ll11_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llll1ll1l1_opy_
            if test_framework_state == bstack1lll1l1ll11_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1l1ll11_opy_.LOG:
                bstack1ll111l11_opy_ = datetime.now()
                entries = f.bstack1l1ll1ll11l_opy_(instance, bstack1llll1ll1l1_opy_)
                if entries:
                    self.bstack1l1ll11l111_opy_(instance, entries)
                    instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࠧኖ"), datetime.now() - bstack1ll111l11_opy_)
                    f.bstack1l1l1ll11l1_opy_(instance, bstack1llll1ll1l1_opy_)
                instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤኗ"), datetime.now() - bstack1l1lll1ll11_opy_)
                return # bstack1l1l1l1l1l1_opy_ not send this event with the bstack1l1ll111l11_opy_ bstack1l1ll1ll1ll_opy_
            elif (
                test_framework_state == bstack1lll1l1ll11_opy_.TEST
                and test_hook_state == bstack1ll1lllll11_opy_.POST
                and not f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_)
            ):
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠢࡥࡴࡲࡴࡵ࡯࡮ࡨࠢࡧࡹࡪࠦࡴࡰࠢ࡯ࡥࡨࡱࠠࡰࡨࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࠧኘ") + str(TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_)) + bstack1ll11ll_opy_ (u"ࠣࠤኙ"))
                f.bstack1llll1l1lll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1ll1l11_opy_, True)
                return # bstack1l1l1l1l1l1_opy_ not send this event bstack1l1l1llll1l_opy_ bstack1l1l1ll1l1l_opy_
            elif (
                f.bstack1llll1lllll_opy_(instance, bstack1lll1lll1l1_opy_.bstack1l1l1ll1l11_opy_, False)
                and test_framework_state == bstack1lll1l1ll11_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1lllll11_opy_.POST
                and f.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_)
            ):
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠤ࡬ࡲ࡯࡫ࡣࡵ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡘࡊ࡙ࡔ࠭ࠢࡗࡩࡸࡺࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡓࡓࡘ࡚ࠠࠣኚ") + str(TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1l1ll11ll1l_opy_)) + bstack1ll11ll_opy_ (u"ࠥࠦኛ"))
                self.bstack1l1l1l1llll_opy_(f, instance, (bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), *args, **kwargs)
            bstack1ll111l11_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l1l1ll1l_opy_ = sorted(
                filter(lambda x: x.get(bstack1ll11ll_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢኜ"), None), data.pop(bstack1ll11ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧኝ"), {}).values()),
                key=lambda x: x[bstack1ll11ll_opy_ (u"ࠨࡥࡷࡧࡱࡸࡤࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠤኞ")],
            )
            if bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_ in data:
                data.pop(bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_)
            data.update({bstack1ll11ll_opy_ (u"ࠢࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢኟ"): bstack1l1l1l1ll1l_opy_})
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠣ࡬ࡶࡳࡳࡀࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨአ"), datetime.now() - bstack1ll111l11_opy_)
            bstack1ll111l11_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll1l1l1l_opy_)
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧኡ"), datetime.now() - bstack1ll111l11_opy_)
            self.bstack1l1ll1ll1ll_opy_(instance, bstack1llll1ll1l1_opy_, event_json=event_json)
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨኢ"), datetime.now() - bstack1l1lll1ll11_opy_)
    def bstack1ll11ll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
        bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack1ll1111l_opy_.value)
        self.bstack1ll11lll1l1_opy_.bstack1l1l1llll11_opy_(instance, f, bstack1llll1ll1l1_opy_, *args, **kwargs)
        bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1ll1111l_opy_.value, bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦኣ"), bstack1ll111ll1ll_opy_ + bstack1ll11ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥኤ"), status=True, failure=None, test_name=None)
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11lll1l1_opy_.bstack1l1l1ll111l_opy_(instance, f, bstack1llll1ll1l1_opy_, *args, **kwargs)
        self.bstack1l1lll1lll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll11l11_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l1lll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡓ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡖࡨࡷࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡋࡶࡦࡰࡷࠤ࡬ࡘࡐࡄࠢࡦࡥࡱࡲ࠺ࠡࡐࡲࠤࡻࡧ࡬ࡪࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡩࡧࡴࡢࠤእ"))
            return
        bstack1ll111l11_opy_ = datetime.now()
        try:
            r = self.bstack1ll1llllll1_opy_.TestSessionEvent(req)
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡸࡪࡹࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡨࡺࡪࡴࡴࠣኦ"), datetime.now() - bstack1ll111l11_opy_)
            f.bstack1llll1l1lll_opy_(instance, self.bstack1ll11lll1l1_opy_.bstack1l1lll1111l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1ll11ll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥኧ") + str(r) + bstack1ll11ll_opy_ (u"ࠤࠥከ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣኩ") + str(e) + bstack1ll11ll_opy_ (u"ࠦࠧኪ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll11ll1_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        _driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        _1l1ll1lll11_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1l1ll111_opy_.bstack1ll11ll1l1l_opy_(method_name):
            return
        if f.bstack1ll111ll1l1_opy_(*args) == bstack1ll1l1ll111_opy_.bstack1l1ll111ll1_opy_:
            bstack1l1lll1ll11_opy_ = datetime.now()
            screenshot = result.get(bstack1ll11ll_opy_ (u"ࠧࡼࡡ࡭ࡷࡨࠦካ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤ࡮ࡳࡡࡨࡧࠣࡦࡦࡹࡥ࠷࠶ࠣࡷࡹࡸࠢኬ"))
                return
            bstack1l1ll1ll1l1_opy_ = self.bstack1l1l1ll1lll_opy_(instance)
            if bstack1l1ll1ll1l1_opy_:
                entry = bstack1ll1l1l1ll1_opy_(TestFramework.bstack1l1l1l1l111_opy_, screenshot)
                self.bstack1l1ll11l111_opy_(bstack1l1ll1ll1l1_opy_, [entry])
                instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡦࡺࡨࡧࡺࡺࡥࠣክ"), datetime.now() - bstack1l1lll1ll11_opy_)
            else:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠣࡷࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡵࡧࡶࡸࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶ࡫࡭ࡸࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣࡻࡦࡹࠠࡵࡣ࡮ࡩࡳࠦࡢࡺࠢࡧࡶ࡮ࡼࡥࡳ࠿ࠣࡿࢂࠨኮ").format(instance.ref()))
        event = {}
        bstack1l1ll1ll1l1_opy_ = self.bstack1l1l1ll1lll_opy_(instance)
        if bstack1l1ll1ll1l1_opy_:
            self.bstack1l1lll11l1l_opy_(event, bstack1l1ll1ll1l1_opy_)
            if event.get(bstack1ll11ll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢኯ")):
                self.bstack1l1ll11l111_opy_(bstack1l1ll1ll1l1_opy_, event[bstack1ll11ll_opy_ (u"ࠥࡰࡴ࡭ࡳࠣኰ")])
            else:
                self.logger.debug(bstack1ll11ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡰࡴ࡭ࡳࠡࡨࡲࡶࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡨࡺࡪࡴࡴࠣ኱"))
    @measure(event_name=EVENTS.bstack1l1lll1l1ll_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l1ll11l111_opy_(
        self,
        bstack1l1ll1ll1l1_opy_: bstack1lll11ll1l1_opy_,
        entries: List[bstack1ll1l1l1ll1_opy_],
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll1111lll1_opy_)
        req.execution_context.hash = str(bstack1l1ll1ll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1ll1ll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1ll1ll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll11ll111l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1l1ll1l1111_opy_)
            log_entry.uuid = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1ll11l1111l_opy_)
            log_entry.test_framework_state = bstack1l1ll1ll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1ll11ll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦኲ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1ll11ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣኳ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1lll11l_opy_
                log_entry.file_path = entry.bstack11l111l_opy_
        def bstack1l1ll1l11ll_opy_():
            bstack1ll111l11_opy_ = datetime.now()
            try:
                self.bstack1ll1llllll1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1l1l1l111_opy_:
                    bstack1l1ll1ll1l1_opy_.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦኴ"), datetime.now() - bstack1ll111l11_opy_)
                elif entry.kind == TestFramework.bstack1l1ll111111_opy_:
                    bstack1l1ll1ll1l1_opy_.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧኵ"), datetime.now() - bstack1ll111l11_opy_)
                else:
                    bstack1l1ll1ll1l1_opy_.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨ኶"), datetime.now() - bstack1ll111l11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11ll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣ኷") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1l11ll_opy_)
    @measure(event_name=EVENTS.bstack1l1ll11l11l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1l1ll1ll1ll_opy_(
        self,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        event_json=None,
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll1111lll1_opy_)
        req.test_framework_name = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11ll111l_opy_)
        req.test_framework_version = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1ll1l1111_opy_)
        req.test_framework_state = bstack1llll1ll1l1_opy_[0].name
        req.test_hook_state = bstack1llll1ll1l1_opy_[1].name
        started_at = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1lll11111_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1l1ll111lll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll1l1l1l_opy_)).encode(bstack1ll11ll_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥኸ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1ll1l11ll_opy_():
            bstack1ll111l11_opy_ = datetime.now()
            try:
                self.bstack1ll1llllll1_opy_.TestFrameworkEvent(req)
                instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣኹ"), datetime.now() - bstack1ll111l11_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1ll11ll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦኺ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1l11ll_opy_)
    def bstack1l1l1ll1lll_opy_(self, instance: bstack1llll1ll111_opy_):
        bstack1l1lll1l1l1_opy_ = TestFramework.bstack1llllll1l11_opy_(instance.context)
        for t in bstack1l1lll1l1l1_opy_:
            bstack1l1lll111ll_opy_ = TestFramework.bstack1llll1lllll_opy_(t, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll111ll_opy_):
                return t
    def bstack1l1ll1l1ll1_opy_(self, message):
        self.bstack1l1lll1ll1l_opy_(message + bstack1ll11ll_opy_ (u"ࠢ࡝ࡰࠥኻ"))
    def log_error(self, message):
        self.bstack1l1ll11lll1_opy_(message + bstack1ll11ll_opy_ (u"ࠣ࡞ࡱࠦኼ"))
    def bstack1l1l1l1lll1_opy_(self, level, original_func):
        def bstack1l1l1lll1ll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstack1ll11ll_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥኽ") in message or bstack1ll11ll_opy_ (u"ࠥ࡟ࡘࡊࡋࡄࡎࡌࡡࠧኾ") in message or bstack1ll11ll_opy_ (u"ࠦࡠ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠣ኿") in message:
                return return_value
            bstack1l1lll1l1l1_opy_ = TestFramework.bstack1l1l1ll11ll_opy_()
            if not bstack1l1lll1l1l1_opy_:
                return return_value
            bstack1l1ll1ll1l1_opy_ = next(
                (
                    instance
                    for instance in bstack1l1lll1l1l1_opy_
                    if TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
                ),
                None,
            )
            if not bstack1l1ll1ll1l1_opy_:
                return return_value
            entry = bstack1ll1l1l1ll1_opy_(TestFramework.bstack1l1ll1l1lll_opy_, message, level)
            self.bstack1l1ll11l111_opy_(bstack1l1ll1ll1l1_opy_, [entry])
            return return_value
        return bstack1l1l1lll1ll_opy_
    def bstack1l1l1lllll1_opy_(self):
        def bstack1l1lll1l111_opy_(*args, **kwargs):
            try:
                self.bstack1l1l1llllll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1ll11ll_opy_ (u"ࠬࠦࠧዀ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1ll11ll_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢ዁") in message:
                    return
                bstack1l1lll1l1l1_opy_ = TestFramework.bstack1l1l1ll11ll_opy_()
                if not bstack1l1lll1l1l1_opy_:
                    return
                bstack1l1ll1ll1l1_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1lll1l1l1_opy_
                        if TestFramework.bstack1llllll1lll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
                    ),
                    None,
                )
                if not bstack1l1ll1ll1l1_opy_:
                    return
                entry = bstack1ll1l1l1ll1_opy_(TestFramework.bstack1l1ll1l1lll_opy_, message, bstack1lll1lll1l1_opy_.bstack1l1lll11lll_opy_)
                self.bstack1l1ll11l111_opy_(bstack1l1ll1ll1l1_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1l1llllll_opy_(bstack1lll111ll1l_opy_ (u"ࠢ࡜ࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠣࡐࡴ࡭ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧዂ"))
                except:
                    pass
        return bstack1l1lll1l111_opy_
    def bstack1l1lll11l1l_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1l111l_opy_
        levels = [bstack1ll11ll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦዃ"), bstack1ll11ll_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨዄ")]
        bstack1l1ll1111l1_opy_ = bstack1ll11ll_opy_ (u"ࠥࠦዅ")
        if instance is not None:
            try:
                bstack1l1ll1111l1_opy_ = TestFramework.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
            except Exception as e:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡻࡩࡥࠢࡩࡶࡴࡳࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤ዆").format(e))
        bstack1l1ll11llll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1ll11ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ዇")]
                bstack1l1ll1l1l11_opy_ = os.path.join(bstack1l1ll1llll1_opy_, (bstack1l1ll11111l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll1l1l11_opy_):
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡱࡳࡹࠦࡰࡳࡧࡶࡩࡳࡺࠠࡧࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡖࡨࡷࡹࠦࡡ࡯ࡦࠣࡆࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤወ").format(bstack1l1ll1l1l11_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll1l1l11_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll1l1l11_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1l111l_opy_:
                        self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧዉ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll1ll111_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll1ll111_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1ll11ll_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦዊ"):
                                entry = bstack1ll1l1l1ll1_opy_(
                                    kind=bstack1ll11ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦዋ"),
                                    message=bstack1ll11ll_opy_ (u"ࠥࠦዌ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l1lll11l_opy_=file_size,
                                    bstack1l1l1ll1ll1_opy_=bstack1ll11ll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦው"),
                                    bstack11l111l_opy_=os.path.abspath(file_path),
                                    bstack1lllllllll_opy_=bstack1l1ll1111l1_opy_
                                )
                            elif level == bstack1ll11ll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤዎ"):
                                entry = bstack1ll1l1l1ll1_opy_(
                                    kind=bstack1ll11ll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣዏ"),
                                    message=bstack1ll11ll_opy_ (u"ࠢࠣዐ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l1lll11l_opy_=file_size,
                                    bstack1l1l1ll1ll1_opy_=bstack1ll11ll_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣዑ"),
                                    bstack11l111l_opy_=os.path.abspath(file_path),
                                    bstack1l1ll11l1ll_opy_=bstack1l1ll1111l1_opy_
                                )
                            bstack1l1ll11llll_opy_.append(entry)
                            _1l1ll1l111l_opy_.add(abs_path)
                        except Exception as bstack1l1l1l1ll11_opy_:
                            self.logger.error(bstack1ll11ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣዒ").format(bstack1l1l1l1ll11_opy_))
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤዓ").format(e))
        event[bstack1ll11ll_opy_ (u"ࠦࡱࡵࡧࡴࠤዔ")] = bstack1l1ll11llll_opy_
class bstack1l1ll1l1l1l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1ll1lll1l_opy_ = set()
        kwargs[bstack1ll11ll_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢዕ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll11l1l1_opy_(obj, self.bstack1l1ll1lll1l_opy_)
def bstack1l1l1l1l11l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll11l1l1_opy_(obj, bstack1l1ll1lll1l_opy_=None, max_depth=3):
    if bstack1l1ll1lll1l_opy_ is None:
        bstack1l1ll1lll1l_opy_ = set()
    if id(obj) in bstack1l1ll1lll1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1ll1lll1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1l1l1l1ll_opy_ = TestFramework.bstack1l1ll1lllll_opy_(obj)
    bstack1l1lll1l11l_opy_ = next((k.lower() in bstack1l1l1l1l1ll_opy_.lower() for k in bstack1l1ll1111ll_opy_.keys()), None)
    if bstack1l1lll1l11l_opy_:
        obj = TestFramework.bstack1l1l1ll1111_opy_(obj, bstack1l1ll1111ll_opy_[bstack1l1lll1l11l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1ll11ll_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤዖ")):
            keys = getattr(obj, bstack1ll11ll_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥ዗"), [])
        elif hasattr(obj, bstack1ll11ll_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥዘ")):
            keys = getattr(obj, bstack1ll11ll_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦዙ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1ll11ll_opy_ (u"ࠥࡣࠧዚ"))}
        if not obj and bstack1l1l1l1l1ll_opy_ == bstack1ll11ll_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣዛ"):
            obj = {bstack1ll11ll_opy_ (u"ࠧࡶࡡࡵࡪࠥዜ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1l1l1l11l_opy_(key) or str(key).startswith(bstack1ll11ll_opy_ (u"ࠨ࡟ࠣዝ")):
            continue
        if value is not None and bstack1l1l1l1l11l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll11l1l1_opy_(value, bstack1l1ll1lll1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll11l1l1_opy_(o, bstack1l1ll1lll1l_opy_, max_depth) for o in value]))
    return result or None