# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import bstack1lllll1ll11_opy_, bstack1lllll1lll1_opy_, bstack1llllll1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll111l_opy_, bstack1ll1ll1l1l1_opy_, bstack1lll111111l_opy_, bstack1ll1ll111ll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lll11l1l_opy_, bstack1l1ll1lll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll111l1l_opy_ = [bstack1111lll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቘ"), bstack1111lll_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢ቙"), bstack1111lll_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣቚ"), bstack1111lll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥቛ"), bstack1111lll_opy_ (u"ࠥࡴࡦࡺࡨࠣቜ")]
bstack1l1ll1l1l11_opy_ = bstack1l1ll1lll11_opy_()
bstack1l1lll1l1l1_opy_ = bstack1111lll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦቝ")
bstack1l1l1llll1l_opy_ = {
    bstack1111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥ቞"): bstack1l1ll111l1l_opy_,
    bstack1111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢ቟"): bstack1l1ll111l1l_opy_,
    bstack1111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢበ"): bstack1l1ll111l1l_opy_,
    bstack1111lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢቡ"): bstack1l1ll111l1l_opy_,
    bstack1111lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦቢ"): bstack1l1ll111l1l_opy_
    + [
        bstack1111lll_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤባ"),
        bstack1111lll_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨቤ"),
        bstack1111lll_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥብ"),
        bstack1111lll_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣቦ"),
        bstack1111lll_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤቧ"),
        bstack1111lll_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤቨ"),
        bstack1111lll_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣቩ"),
        bstack1111lll_opy_ (u"ࠥࡷࡹࡵࡰࠣቪ"),
        bstack1111lll_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨቫ"),
        bstack1111lll_opy_ (u"ࠧࡽࡨࡦࡰࠥቬ"),
    ],
    bstack1111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧቭ"): [bstack1111lll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥቮ"), bstack1111lll_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨቯ"), bstack1111lll_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥተ"), bstack1111lll_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤቱ")],
    bstack1111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦቲ"): [bstack1111lll_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤታ"), bstack1111lll_opy_ (u"ࠨࡡࡳࡩࡶࠦቴ")],
    bstack1111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨት"): [bstack1111lll_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢቶ"), bstack1111lll_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥቷ"), bstack1111lll_opy_ (u"ࠥࡪࡺࡴࡣࠣቸ"), bstack1111lll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦቹ"), bstack1111lll_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢቺ"), bstack1111lll_opy_ (u"ࠨࡩࡥࡵࠥቻ")],
    bstack1111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨቼ"): [bstack1111lll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨች"), bstack1111lll_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣቾ"), bstack1111lll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣቿ")],
    bstack1111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨኀ"): [bstack1111lll_opy_ (u"ࠧࡽࡨࡦࡰࠥኁ"), bstack1111lll_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨኂ")],
    bstack1111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣኃ"): [bstack1111lll_opy_ (u"ࠣࡰࡲࡨࡪࠨኄ"), bstack1111lll_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤኅ")],
    bstack1111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥኆ"): [bstack1111lll_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኇ"), bstack1111lll_opy_ (u"ࠧࡧࡲࡨࡵࠥኈ"), bstack1111lll_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨ኉")],
}
_1l1ll111ll1_opy_ = set()
class bstack1lll1111l1l_opy_(bstack1llll11l111_opy_):
    bstack1l1ll1l11l1_opy_ = bstack1111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢኊ")
    bstack1l1lll11l11_opy_ = bstack1111lll_opy_ (u"ࠣࡋࡑࡊࡔࠨኋ")
    bstack1l1lll11ll1_opy_ = bstack1111lll_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣኌ")
    bstack1l1ll1l1ll1_opy_: Callable
    bstack1l1l1ll1ll1_opy_: Callable
    def __init__(self, bstack1lll11l1lll_opy_, bstack1llll1l1l1l_opy_):
        super().__init__()
        self.bstack1ll11ll111l_opy_ = bstack1llll1l1l1l_opy_
        if os.getenv(bstack1111lll_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢኍ"), bstack1111lll_opy_ (u"ࠦ࠶ࠨ኎")) != bstack1111lll_opy_ (u"ࠧ࠷ࠢ኏") or not self.is_enabled():
            self.logger.warning(bstack1111lll_opy_ (u"ࠨࠢነ") + str(self.__class__.__name__) + bstack1111lll_opy_ (u"ࠢࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠥኑ"))
            return
        TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.PRE), self.bstack1ll1l11l111_opy_)
        TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.POST), self.bstack1ll1l11ll11_opy_)
        for event in bstack1ll1lll111l_opy_:
            for state in bstack1lll111111l_opy_:
                TestFramework.bstack1ll11l111l1_opy_((event, state), self.bstack1l1ll11l1l1_opy_)
        bstack1lll11l1lll_opy_.bstack1ll11l111l1_opy_((bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_, bstack1llllll1111_opy_.POST), self.bstack1l1ll1111l1_opy_)
        self.bstack1l1ll1l1ll1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1ll111lll_opy_(bstack1lll1111l1l_opy_.bstack1l1lll11l11_opy_, self.bstack1l1ll1l1ll1_opy_)
        self.bstack1l1l1ll1ll1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1ll111lll_opy_(bstack1lll1111l1l_opy_.bstack1l1lll11ll1_opy_, self.bstack1l1l1ll1ll1_opy_)
        self.bstack1l1ll1l1lll_opy_ = builtins.print
        builtins.print = self.bstack1l1lll1111l_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1llll1111_opy_() and instance:
            bstack1l1lll1l11l_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llllll11ll_opy_
            if test_framework_state == bstack1ll1lll111l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1lll111l_opy_.LOG:
                bstack11l1l1ll1l_opy_ = datetime.now()
                entries = f.bstack1l1l1lll1ll_opy_(instance, bstack1llllll11ll_opy_)
                if entries:
                    self.bstack1l1ll1llll1_opy_(instance, entries)
                    instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࠣኒ"), datetime.now() - bstack11l1l1ll1l_opy_)
                    f.bstack1l1lll11lll_opy_(instance, bstack1llllll11ll_opy_)
                instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧና"), datetime.now() - bstack1l1lll1l11l_opy_)
                return # bstack1l1lll1lll1_opy_ not send this event with the bstack1l1l1ll111l_opy_ bstack1l1l1l1lll1_opy_
            elif (
                test_framework_state == bstack1ll1lll111l_opy_.TEST
                and test_hook_state == bstack1lll111111l_opy_.POST
                and not f.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_)
            ):
                self.logger.warning(bstack1111lll_opy_ (u"ࠥࡨࡷࡵࡰࡱ࡫ࡱ࡫ࠥࡪࡵࡦࠢࡷࡳࠥࡲࡡࡤ࡭ࠣࡳ࡫ࠦࡲࡦࡵࡸࡰࡹࡹࠠࠣኔ") + str(TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_)) + bstack1111lll_opy_ (u"ࠦࠧን"))
                f.bstack1llllll1l1l_opy_(instance, bstack1lll1111l1l_opy_.bstack1l1ll1l11l1_opy_, True)
                return # bstack1l1lll1lll1_opy_ not send this event bstack1l1l1llllll_opy_ bstack1l1llll11l1_opy_
            elif (
                f.bstack1llllll1l11_opy_(instance, bstack1lll1111l1l_opy_.bstack1l1ll1l11l1_opy_, False)
                and test_framework_state == bstack1ll1lll111l_opy_.LOG_REPORT
                and test_hook_state == bstack1lll111111l_opy_.POST
                and f.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_)
            ):
                self.logger.warning(bstack1111lll_opy_ (u"ࠧ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡔࡆࡕࡗ࠰࡚ࠥࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࡖࡏࡔࡖࠣࠦኖ") + str(TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_)) + bstack1111lll_opy_ (u"ࠨࠢኗ"))
                self.bstack1l1ll11l1l1_opy_(f, instance, (bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.POST), *args, **kwargs)
            bstack11l1l1ll1l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll1ll1l1_opy_ = sorted(
                filter(lambda x: x.get(bstack1111lll_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥኘ"), None), data.pop(bstack1111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣኙ"), {}).values()),
                key=lambda x: x[bstack1111lll_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧኚ")],
            )
            if bstack1lll11l1ll1_opy_.bstack1l1ll1lll1l_opy_ in data:
                data.pop(bstack1lll11l1ll1_opy_.bstack1l1ll1lll1l_opy_)
            data.update({bstack1111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥኛ"): bstack1l1ll1ll1l1_opy_})
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤኜ"), datetime.now() - bstack11l1l1ll1l_opy_)
            bstack11l1l1ll1l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll1l1111_opy_)
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣኝ"), datetime.now() - bstack11l1l1ll1l_opy_)
            self.bstack1l1l1l1lll1_opy_(instance, bstack1llllll11ll_opy_, event_json=event_json)
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤኞ"), datetime.now() - bstack1l1lll1l11l_opy_)
    def bstack1ll1l11l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
        bstack1ll11l1l11l_opy_ = bstack1ll1llll11l_opy_.bstack1ll111llll1_opy_(EVENTS.bstack11lll11l1_opy_.value)
        self.bstack1ll11ll111l_opy_.bstack1l1ll1l1l1l_opy_(instance, f, bstack1llllll11ll_opy_, *args, **kwargs)
        bstack1ll1llll11l_opy_.end(EVENTS.bstack11lll11l1_opy_.value, bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢኟ"), bstack1ll11l1l11l_opy_ + bstack1111lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨአ"), status=True, failure=None, test_name=None)
    def bstack1ll1l11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11ll111l_opy_.bstack1l1l1ll1lll_opy_(instance, f, bstack1llllll11ll_opy_, *args, **kwargs)
        self.bstack1l1l1ll1111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll1ll1l_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1l1l1ll1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧኡ"))
            return
        bstack11l1l1ll1l_opy_ = datetime.now()
        try:
            r = self.bstack1lll1llll11_opy_.TestSessionEvent(req)
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦኢ"), datetime.now() - bstack11l1l1ll1l_opy_)
            f.bstack1llllll1l1l_opy_(instance, self.bstack1ll11ll111l_opy_.bstack1l1llll11ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1111lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨኣ") + str(r) + bstack1111lll_opy_ (u"ࠧࠨኤ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦእ") + str(e) + bstack1111lll_opy_ (u"ࠢࠣኦ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1111l1_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        _driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        _1l1lll11111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1lll11l_opy_.bstack1ll11llllll_opy_(method_name):
            return
        if f.bstack1ll11lll11l_opy_(*args) == bstack1lll1lll11l_opy_.bstack1l1ll1111ll_opy_:
            bstack1l1lll1l11l_opy_ = datetime.now()
            screenshot = result.get(bstack1111lll_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢኧ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1111lll_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥከ"))
                return
            bstack1l1ll11l11l_opy_ = self.bstack1l1ll11l1ll_opy_(instance)
            if bstack1l1ll11l11l_opy_:
                entry = bstack1ll1ll111ll_opy_(TestFramework.bstack1l1llll111l_opy_, screenshot)
                self.bstack1l1ll1llll1_opy_(bstack1l1ll11l11l_opy_, [entry])
                instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦኩ"), datetime.now() - bstack1l1lll1l11l_opy_)
            else:
                self.logger.warning(bstack1111lll_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤኪ").format(instance.ref()))
        event = {}
        bstack1l1ll11l11l_opy_ = self.bstack1l1ll11l1ll_opy_(instance)
        if bstack1l1ll11l11l_opy_:
            self.bstack1l1ll1ll1ll_opy_(event, bstack1l1ll11l11l_opy_)
            if event.get(bstack1111lll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥካ")):
                self.bstack1l1ll1llll1_opy_(bstack1l1ll11l11l_opy_, event[bstack1111lll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦኬ")])
            else:
                self.logger.debug(bstack1111lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦክ"))
    @measure(event_name=EVENTS.bstack1l1ll11l111_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1l1ll1llll1_opy_(
        self,
        bstack1l1ll11l11l_opy_: bstack1ll1ll1l1l1_opy_,
        entries: List[bstack1ll1ll111ll_opy_],
    ):
        self.bstack1ll1l111lll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1ll11l1ll11_opy_)
        req.execution_context.hash = str(bstack1l1ll11l11l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1ll11l11l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1ll11l11l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1ll11l1l1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1l1lll1l111_opy_)
            log_entry.uuid = TestFramework.bstack1llllll1l11_opy_(bstack1l1ll11l11l_opy_, TestFramework.bstack1ll111lllll_opy_)
            log_entry.test_framework_state = bstack1l1ll11l11l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኮ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦኯ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll111l11_opy_
                log_entry.file_path = entry.bstack1l1111_opy_
        def bstack1l1ll11111l_opy_():
            bstack11l1l1ll1l_opy_ = datetime.now()
            try:
                self.bstack1lll1llll11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1llll111l_opy_:
                    bstack1l1ll11l11l_opy_.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢኰ"), datetime.now() - bstack11l1l1ll1l_opy_)
                elif entry.kind == TestFramework.bstack1l1l1l1llll_opy_:
                    bstack1l1ll11l11l_opy_.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣ኱"), datetime.now() - bstack11l1l1ll1l_opy_)
                else:
                    bstack1l1ll11l11l_opy_.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤኲ"), datetime.now() - bstack11l1l1ll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦኳ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l111_opy_.enqueue(bstack1l1ll11111l_opy_)
    @measure(event_name=EVENTS.bstack1l1lll1l1ll_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1l1l1l1lll1_opy_(
        self,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        event_json=None,
    ):
        self.bstack1ll1l111lll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll11l1ll11_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll11l1l1l1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
        req.test_framework_state = bstack1llllll11ll_opy_[0].name
        req.test_hook_state = bstack1llllll11ll_opy_[1].name
        started_at = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll1l1111_opy_)).encode(bstack1111lll_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨኴ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1ll11111l_opy_():
            bstack11l1l1ll1l_opy_ = datetime.now()
            try:
                self.bstack1lll1llll11_opy_.TestFrameworkEvent(req)
                instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦኵ"), datetime.now() - bstack11l1l1ll1l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ኶") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l111_opy_.enqueue(bstack1l1ll11111l_opy_)
    def bstack1l1ll11l1ll_opy_(self, instance: bstack1lllll1ll11_opy_):
        bstack1l1ll111111_opy_ = TestFramework.bstack1lllll11111_opy_(instance.context)
        for t in bstack1l1ll111111_opy_:
            bstack1l1ll1ll111_opy_ = TestFramework.bstack1llllll1l11_opy_(t, bstack1lll11l1ll1_opy_.bstack1l1ll1lll1l_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll1ll111_opy_):
                return t
    def bstack1l1l1ll11l1_opy_(self, message):
        self.bstack1l1ll1l1ll1_opy_(message + bstack1111lll_opy_ (u"ࠥࡠࡳࠨ኷"))
    def log_error(self, message):
        self.bstack1l1l1ll1ll1_opy_(message + bstack1111lll_opy_ (u"ࠦࡡࡴࠢኸ"))
    def bstack1l1ll111lll_opy_(self, level, original_func):
        def bstack1l1lll111ll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstack1111lll_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨኹ") in message or bstack1111lll_opy_ (u"ࠨ࡛ࡔࡆࡎࡇࡑࡏ࡝ࠣኺ") in message or bstack1111lll_opy_ (u"ࠢ࡜࡙ࡨࡦࡉࡸࡩࡷࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠦኻ") in message:
                return return_value
            bstack1l1ll111111_opy_ = TestFramework.bstack1l1l1lll111_opy_()
            if not bstack1l1ll111111_opy_:
                return return_value
            bstack1l1ll11l11l_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll111111_opy_
                    if TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1ll111lllll_opy_)
                ),
                None,
            )
            if not bstack1l1ll11l11l_opy_:
                return return_value
            entry = bstack1ll1ll111ll_opy_(TestFramework.bstack1l1l1ll1l1l_opy_, message, level)
            self.bstack1l1ll1llll1_opy_(bstack1l1ll11l11l_opy_, [entry])
            return return_value
        return bstack1l1lll111ll_opy_
    def bstack1l1lll1111l_opy_(self):
        def bstack1l1ll11llll_opy_(*args, **kwargs):
            try:
                self.bstack1l1ll1l1lll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1111lll_opy_ (u"ࠨࠢࠪኼ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1111lll_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥኽ") in message:
                    return
                bstack1l1ll111111_opy_ = TestFramework.bstack1l1l1lll111_opy_()
                if not bstack1l1ll111111_opy_:
                    return
                bstack1l1ll11l11l_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1ll111111_opy_
                        if TestFramework.bstack1lllll11ll1_opy_(instance, TestFramework.bstack1ll111lllll_opy_)
                    ),
                    None,
                )
                if not bstack1l1ll11l11l_opy_:
                    return
                entry = bstack1ll1ll111ll_opy_(TestFramework.bstack1l1l1ll1l1l_opy_, message, bstack1lll1111l1l_opy_.bstack1l1lll11l11_opy_)
                self.bstack1l1ll1llll1_opy_(bstack1l1ll11l11l_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1ll1l1lll_opy_(bstack1llll1l1ll1_opy_ (u"ࠥ࡟ࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠦࡌࡰࡩࠣࡧࡦࡶࡴࡶࡴࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣኾ"))
                except:
                    pass
        return bstack1l1ll11llll_opy_
    def bstack1l1ll1ll1ll_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll111ll1_opy_
        levels = [bstack1111lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ኿"), bstack1111lll_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤዀ")]
        bstack1l1l1ll1l11_opy_ = bstack1111lll_opy_ (u"ࠨࠢ዁")
        if instance is not None:
            try:
                bstack1l1l1ll1l11_opy_ = TestFramework.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll111lllll_opy_)
            except Exception as e:
                self.logger.warning(bstack1111lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧዂ").format(e))
        bstack1l1l1lllll1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨዃ")]
                bstack1l1ll1l11ll_opy_ = os.path.join(bstack1l1ll1l1l11_opy_, (bstack1l1lll1l1l1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll1l11ll_opy_):
                    self.logger.debug(bstack1111lll_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧዄ").format(bstack1l1ll1l11ll_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll1l11ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll1l11ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll111ll1_opy_:
                        self.logger.info(bstack1111lll_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣዅ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1lll1llll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1lll1llll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1111lll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ዆"):
                                entry = bstack1ll1ll111ll_opy_(
                                    kind=bstack1111lll_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢ዇"),
                                    message=bstack1111lll_opy_ (u"ࠨࠢወ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll111l11_opy_=file_size,
                                    bstack1l1lll1ll11_opy_=bstack1111lll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢዉ"),
                                    bstack1l1111_opy_=os.path.abspath(file_path),
                                    bstack11ll1111_opy_=bstack1l1l1ll1l11_opy_
                                )
                            elif level == bstack1111lll_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧዊ"):
                                entry = bstack1ll1ll111ll_opy_(
                                    kind=bstack1111lll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦዋ"),
                                    message=bstack1111lll_opy_ (u"ࠥࠦዌ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll111l11_opy_=file_size,
                                    bstack1l1lll1ll11_opy_=bstack1111lll_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦው"),
                                    bstack1l1111_opy_=os.path.abspath(file_path),
                                    bstack1l1ll1lllll_opy_=bstack1l1l1ll1l11_opy_
                                )
                            bstack1l1l1lllll1_opy_.append(entry)
                            _1l1ll111ll1_opy_.add(abs_path)
                        except Exception as bstack1l1ll1l111l_opy_:
                            self.logger.error(bstack1111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦዎ").format(bstack1l1ll1l111l_opy_))
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧዏ").format(e))
        event[bstack1111lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧዐ")] = bstack1l1l1lllll1_opy_
class bstack1l1ll1l1111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1lll111l1_opy_ = set()
        kwargs[bstack1111lll_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥዑ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l1llll11_opy_(obj, self.bstack1l1lll111l1_opy_)
def bstack1l1l1lll1l1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l1llll11_opy_(obj, bstack1l1lll111l1_opy_=None, max_depth=3):
    if bstack1l1lll111l1_opy_ is None:
        bstack1l1lll111l1_opy_ = set()
    if id(obj) in bstack1l1lll111l1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1lll111l1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llll1l11_opy_ = TestFramework.bstack1l1ll11lll1_opy_(obj)
    bstack1l1ll11ll1l_opy_ = next((k.lower() in bstack1l1llll1l11_opy_.lower() for k in bstack1l1l1llll1l_opy_.keys()), None)
    if bstack1l1ll11ll1l_opy_:
        obj = TestFramework.bstack1l1ll11ll11_opy_(obj, bstack1l1l1llll1l_opy_[bstack1l1ll11ll1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1111lll_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧዒ")):
            keys = getattr(obj, bstack1111lll_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨዓ"), [])
        elif hasattr(obj, bstack1111lll_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨዔ")):
            keys = getattr(obj, bstack1111lll_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢዕ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1111lll_opy_ (u"ࠨ࡟ࠣዖ"))}
        if not obj and bstack1l1llll1l11_opy_ == bstack1111lll_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦ዗"):
            obj = {bstack1111lll_opy_ (u"ࠣࡲࡤࡸ࡭ࠨዘ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1l1lll1l1_opy_(key) or str(key).startswith(bstack1111lll_opy_ (u"ࠤࡢࠦዙ")):
            continue
        if value is not None and bstack1l1l1lll1l1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l1llll11_opy_(value, bstack1l1lll111l1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l1llll11_opy_(o, bstack1l1lll111l1_opy_, max_depth) for o in value]))
    return result or None