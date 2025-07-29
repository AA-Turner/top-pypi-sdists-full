# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import bstack11111111l1_opy_, bstack1llllllllll_opy_, bstack1llllllll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1l1lll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l11l1l_opy_, bstack1ll1ll11l1l_opy_, bstack1lll111l111_opy_, bstack1ll1l1ll11l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll11l11l_opy_, bstack1l1l1llllll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll1ll1ll_opy_ = [bstackl_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቒ"), bstackl_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣቓ"), bstackl_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤቔ"), bstackl_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦቕ"), bstackl_opy_ (u"ࠦࡵࡧࡴࡩࠤቖ")]
bstack1l1ll1lllll_opy_ = bstack1l1l1llllll_opy_()
bstack1l1llll111l_opy_ = bstackl_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ቗")
bstack1l1lll11l1l_opy_ = {
    bstackl_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦቘ"): bstack1l1ll1ll1ll_opy_,
    bstackl_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣ቙"): bstack1l1ll1ll1ll_opy_,
    bstackl_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣቚ"): bstack1l1ll1ll1ll_opy_,
    bstackl_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣቛ"): bstack1l1ll1ll1ll_opy_,
    bstackl_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧቜ"): bstack1l1ll1ll1ll_opy_
    + [
        bstackl_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥቝ"),
        bstackl_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢ቞"),
        bstackl_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦ቟"),
        bstackl_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤበ"),
        bstackl_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥቡ"),
        bstackl_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥቢ"),
        bstackl_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤባ"),
        bstackl_opy_ (u"ࠦࡸࡺ࡯ࡱࠤቤ"),
        bstackl_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢብ"),
        bstackl_opy_ (u"ࠨࡷࡩࡧࡱࠦቦ"),
    ],
    bstackl_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨቧ"): [bstackl_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦቨ"), bstackl_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢቩ"), bstackl_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦቪ"), bstackl_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥቫ")],
    bstackl_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧቬ"): [bstackl_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥቭ"), bstackl_opy_ (u"ࠢࡢࡴࡪࡷࠧቮ")],
    bstackl_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢቯ"): [bstackl_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣተ"), bstackl_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦቱ"), bstackl_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤቲ"), bstackl_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧታ"), bstackl_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣቴ"), bstackl_opy_ (u"ࠢࡪࡦࡶࠦት")],
    bstackl_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢቶ"): [bstackl_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢቷ"), bstackl_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤቸ"), bstackl_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤቹ")],
    bstackl_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢቺ"): [bstackl_opy_ (u"ࠨࡷࡩࡧࡱࠦቻ"), bstackl_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢቼ")],
    bstackl_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤች"): [bstackl_opy_ (u"ࠤࡱࡳࡩ࡫ࠢቾ"), bstackl_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥቿ")],
    bstackl_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦኀ"): [bstackl_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኁ"), bstackl_opy_ (u"ࠨࡡࡳࡩࡶࠦኂ"), bstackl_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢኃ")],
}
_1l1ll1l111l_opy_ = set()
class bstack1lll11l111l_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1l1lll1l111_opy_ = bstackl_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣኄ")
    bstack1l1ll11llll_opy_ = bstackl_opy_ (u"ࠤࡌࡒࡋࡕࠢኅ")
    bstack1l1l1ll1l11_opy_ = bstackl_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤኆ")
    bstack1l1ll11lll1_opy_: Callable
    bstack1l1ll1ll1l1_opy_: Callable
    def __init__(self, bstack1lll1l11ll1_opy_, bstack1lll1ll11ll_opy_):
        super().__init__()
        self.bstack1ll11l1l1ll_opy_ = bstack1lll1ll11ll_opy_
        if os.getenv(bstackl_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣኇ"), bstackl_opy_ (u"ࠧ࠷ࠢኈ")) != bstackl_opy_ (u"ࠨ࠱ࠣ኉") or not self.is_enabled():
            self.logger.warning(bstackl_opy_ (u"ࠢࠣኊ") + str(self.__class__.__name__) + bstackl_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦኋ"))
            return
        TestFramework.bstack1ll1l11ll1l_opy_((bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.PRE), self.bstack1ll11l1111l_opy_)
        TestFramework.bstack1ll1l11ll1l_opy_((bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.POST), self.bstack1ll11ll111l_opy_)
        for event in bstack1lll1l11l1l_opy_:
            for state in bstack1lll111l111_opy_:
                TestFramework.bstack1ll1l11ll1l_opy_((event, state), self.bstack1l1l1ll1lll_opy_)
        bstack1lll1l11ll1_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.POST), self.bstack1l1lll11lll_opy_)
        self.bstack1l1ll11lll1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1llll1111_opy_(bstack1lll11l111l_opy_.bstack1l1ll11llll_opy_, self.bstack1l1ll11lll1_opy_)
        self.bstack1l1ll1ll1l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1llll1111_opy_(bstack1lll11l111l_opy_.bstack1l1l1ll1l11_opy_, self.bstack1l1ll1ll1l1_opy_)
        self.bstack1l1l1ll111l_opy_ = builtins.print
        builtins.print = self.bstack1l1ll1111l1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1ll11111l_opy_() and instance:
            bstack1l1ll1l1ll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lllll1l1ll_opy_
            if test_framework_state == bstack1lll1l11l1l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1l11l1l_opy_.LOG:
                bstack1l1ll11l1_opy_ = datetime.now()
                entries = f.bstack1l1l1lll1l1_opy_(instance, bstack1lllll1l1ll_opy_)
                if entries:
                    self.bstack1l1ll1l1111_opy_(instance, entries)
                    instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤኌ"), datetime.now() - bstack1l1ll11l1_opy_)
                    f.bstack1l1ll1ll111_opy_(instance, bstack1lllll1l1ll_opy_)
                instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨኍ"), datetime.now() - bstack1l1ll1l1ll1_opy_)
                return # bstack1l1lll111l1_opy_ not send this event with the bstack1l1ll1l11l1_opy_ bstack1l1lll11ll1_opy_
            elif (
                test_framework_state == bstack1lll1l11l1l_opy_.TEST
                and test_hook_state == bstack1lll111l111_opy_.POST
                and not f.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_)
            ):
                self.logger.warning(bstackl_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤ኎") + str(TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_)) + bstackl_opy_ (u"ࠧࠨ኏"))
                f.bstack1lllllllll1_opy_(instance, bstack1lll11l111l_opy_.bstack1l1lll1l111_opy_, True)
                return # bstack1l1lll111l1_opy_ not send this event bstack1l1l1l1ll1l_opy_ bstack1l1lll1llll_opy_
            elif (
                f.bstack1llllll1l1l_opy_(instance, bstack1lll11l111l_opy_.bstack1l1lll1l111_opy_, False)
                and test_framework_state == bstack1lll1l11l1l_opy_.LOG_REPORT
                and test_hook_state == bstack1lll111l111_opy_.POST
                and f.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_)
            ):
                self.logger.warning(bstackl_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧነ") + str(TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1l1l1llll1l_opy_)) + bstackl_opy_ (u"ࠢࠣኑ"))
                self.bstack1l1l1ll1lll_opy_(f, instance, (bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.POST), *args, **kwargs)
            bstack1l1ll11l1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll11ll11_opy_ = sorted(
                filter(lambda x: x.get(bstackl_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦኒ"), None), data.pop(bstackl_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤና"), {}).values()),
                key=lambda x: x[bstackl_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨኔ")],
            )
            if bstack1lll11l1ll1_opy_.bstack1l1lll11l11_opy_ in data:
                data.pop(bstack1lll11l1ll1_opy_.bstack1l1lll11l11_opy_)
            data.update({bstackl_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦን"): bstack1l1ll11ll11_opy_})
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥኖ"), datetime.now() - bstack1l1ll11l1_opy_)
            bstack1l1ll11l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1lll1lll1_opy_)
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤኗ"), datetime.now() - bstack1l1ll11l1_opy_)
            self.bstack1l1lll11ll1_opy_(instance, bstack1lllll1l1ll_opy_, event_json=event_json)
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥኘ"), datetime.now() - bstack1l1ll1l1ll1_opy_)
    def bstack1ll11l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
        bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack11lll111ll_opy_.value)
        self.bstack1ll11l1l1ll_opy_.bstack1l1ll11l1ll_opy_(instance, f, bstack1lllll1l1ll_opy_, *args, **kwargs)
        bstack1lll11lll1l_opy_.end(EVENTS.bstack11lll111ll_opy_.value, bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኙ"), bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠤ࠽ࡩࡳࡪࠢኚ"), status=True, failure=None, test_name=None)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11l1l1ll_opy_.bstack1l1ll1l1l1l_opy_(instance, f, bstack1lllll1l1ll_opy_, *args, **kwargs)
        self.bstack1l1ll111lll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1l1lll111_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l1ll111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstackl_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨኛ"))
            return
        bstack1l1ll11l1_opy_ = datetime.now()
        try:
            r = self.bstack1lll1l1l1ll_opy_.TestSessionEvent(req)
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧኜ"), datetime.now() - bstack1l1ll11l1_opy_)
            f.bstack1lllllllll1_opy_(instance, self.bstack1ll11l1l1ll_opy_.bstack1l1lll1111l_opy_, r.success)
            if not r.success:
                self.logger.info(bstackl_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢኝ") + str(r) + bstackl_opy_ (u"ࠨࠢኞ"))
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧኟ") + str(e) + bstackl_opy_ (u"ࠣࠤአ"))
            traceback.print_exc()
            raise e
    def bstack1l1lll11lll_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        _driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        _1l1lll1l11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1l1lll11_opy_.bstack1ll111l1111_opy_(method_name):
            return
        if f.bstack1ll11l1ll1l_opy_(*args) == bstack1ll1l1lll11_opy_.bstack1l1l1ll11l1_opy_:
            bstack1l1ll1l1ll1_opy_ = datetime.now()
            screenshot = result.get(bstackl_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣኡ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstackl_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦኢ"))
                return
            bstack1l1l1l1llll_opy_ = self.bstack1l1l1llll11_opy_(instance)
            if bstack1l1l1l1llll_opy_:
                entry = bstack1ll1l1ll11l_opy_(TestFramework.bstack1l1ll111l11_opy_, screenshot)
                self.bstack1l1ll1l1111_opy_(bstack1l1l1l1llll_opy_, [entry])
                instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧኣ"), datetime.now() - bstack1l1ll1l1ll1_opy_)
            else:
                self.logger.warning(bstackl_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥኤ").format(instance.ref()))
        event = {}
        bstack1l1l1l1llll_opy_ = self.bstack1l1l1llll11_opy_(instance)
        if bstack1l1l1l1llll_opy_:
            self.bstack1l1lll1ll11_opy_(event, bstack1l1l1l1llll_opy_)
            if event.get(bstackl_opy_ (u"ࠨ࡬ࡰࡩࡶࠦእ")):
                self.bstack1l1ll1l1111_opy_(bstack1l1l1l1llll_opy_, event[bstackl_opy_ (u"ࠢ࡭ࡱࡪࡷࠧኦ")])
            else:
                self.logger.debug(bstackl_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧኧ"))
    @measure(event_name=EVENTS.bstack1l1ll111ll1_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l1ll1l1111_opy_(
        self,
        bstack1l1l1l1llll_opy_: bstack1ll1ll11l1l_opy_,
        entries: List[bstack1ll1l1ll11l_opy_],
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll111ll1l1_opy_)
        req.execution_context.hash = str(bstack1l1l1l1llll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1llll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1llll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll1l1111l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1l1lll1l1l1_opy_)
            log_entry.uuid = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1ll11l11lll_opy_)
            log_entry.test_framework_state = bstack1l1l1l1llll_opy_.state.name
            log_entry.message = entry.message.encode(bstackl_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣከ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstackl_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧኩ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1llll11l1_opy_
                log_entry.file_path = entry.bstack11llll_opy_
        def bstack1l1ll11l1l1_opy_():
            bstack1l1ll11l1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1l1ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll111l11_opy_:
                    bstack1l1l1l1llll_opy_.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣኪ"), datetime.now() - bstack1l1ll11l1_opy_)
                elif entry.kind == TestFramework.bstack1l1ll1l1lll_opy_:
                    bstack1l1l1l1llll_opy_.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤካ"), datetime.now() - bstack1l1ll11l1_opy_)
                else:
                    bstack1l1l1l1llll_opy_.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥኬ"), datetime.now() - bstack1l1ll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstackl_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧክ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l1l1_opy_.enqueue(bstack1l1ll11l1l1_opy_)
    @measure(event_name=EVENTS.bstack1l1ll11ll1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1l1lll11ll1_opy_(
        self,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        event_json=None,
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll111ll1l1_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1lll1l1l1_opy_)
        req.test_framework_state = bstack1lllll1l1ll_opy_[0].name
        req.test_hook_state = bstack1lllll1l1ll_opy_[1].name
        started_at = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1lll111ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1lll11111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1lll1lll1_opy_)).encode(bstackl_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኮ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1ll11l1l1_opy_():
            bstack1l1ll11l1_opy_ = datetime.now()
            try:
                self.bstack1lll1l1l1ll_opy_.TestFrameworkEvent(req)
                instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧኯ"), datetime.now() - bstack1l1ll11l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstackl_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣኰ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l1l1_opy_.enqueue(bstack1l1ll11l1l1_opy_)
    def bstack1l1l1llll11_opy_(self, instance: bstack11111111l1_opy_):
        bstack1l1ll1lll11_opy_ = TestFramework.bstack1llllll1111_opy_(instance.context)
        for t in bstack1l1ll1lll11_opy_:
            bstack1l1l1lll1ll_opy_ = TestFramework.bstack1llllll1l1l_opy_(t, bstack1lll11l1ll1_opy_.bstack1l1lll11l11_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1lll1ll_opy_):
                return t
    def bstack1l1ll1111ll_opy_(self, message):
        self.bstack1l1ll11lll1_opy_(message + bstackl_opy_ (u"ࠦࡡࡴࠢ኱"))
    def log_error(self, message):
        self.bstack1l1ll1ll1l1_opy_(message + bstackl_opy_ (u"ࠧࡢ࡮ࠣኲ"))
    def bstack1l1llll1111_opy_(self, level, original_func):
        def bstack1l1ll1ll11l_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstackl_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢኳ") in message or bstackl_opy_ (u"ࠢ࡜ࡕࡇࡏࡈࡒࡉ࡞ࠤኴ") in message or bstackl_opy_ (u"ࠣ࡝࡚ࡩࡧࡊࡲࡪࡸࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠧኵ") in message:
                return return_value
            bstack1l1ll1lll11_opy_ = TestFramework.bstack1l1l1ll11ll_opy_()
            if not bstack1l1ll1lll11_opy_:
                return return_value
            bstack1l1l1l1llll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1lll11_opy_
                    if TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
                ),
                None,
            )
            if not bstack1l1l1l1llll_opy_:
                return return_value
            entry = bstack1ll1l1ll11l_opy_(TestFramework.bstack1l1lll1l1ll_opy_, message, level)
            self.bstack1l1ll1l1111_opy_(bstack1l1l1l1llll_opy_, [entry])
            return return_value
        return bstack1l1ll1ll11l_opy_
    def bstack1l1ll1111l1_opy_(self):
        def bstack1l1l1lll11l_opy_(*args, **kwargs):
            self.bstack1l1l1ll111l_opy_(*args, **kwargs)
            message = bstackl_opy_ (u"ࠩࠣࠫ኶").join(str(arg) for arg in args)
            if not message.strip():
                return
            if bstackl_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦ኷") in message:
                return
            bstack1l1ll1lll11_opy_ = TestFramework.bstack1l1l1ll11ll_opy_()
            if not bstack1l1ll1lll11_opy_:
                return
            bstack1l1l1l1llll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1lll11_opy_
                    if TestFramework.bstack1lllll11111_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
                ),
                None,
            )
            if not bstack1l1l1l1llll_opy_:
                return
            entry = bstack1ll1l1ll11l_opy_(TestFramework.bstack1l1lll1l1ll_opy_, message, bstack1lll11l111l_opy_.bstack1l1ll11llll_opy_)
            self.bstack1l1ll1l1111_opy_(bstack1l1l1l1llll_opy_, [entry])
        return bstack1l1l1lll11l_opy_
    def bstack1l1lll1ll11_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1l111l_opy_
        levels = [bstackl_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢኸ"), bstackl_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤኹ")]
        bstack1l1l1ll1111_opy_ = bstackl_opy_ (u"ࠨࠢኺ")
        if instance is not None:
            try:
                bstack1l1l1ll1111_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
            except Exception as e:
                self.logger.warning(bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧኻ").format(e))
        bstack1l1ll11l111_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstackl_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨኼ")]
                bstack1l1lll1ll1l_opy_ = os.path.join(bstack1l1ll1lllll_opy_, (bstack1l1llll111l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1lll1ll1l_opy_):
                    self.logger.debug(bstackl_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧኽ").format(bstack1l1lll1ll1l_opy_))
                    continue
                file_names = os.listdir(bstack1l1lll1ll1l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1lll1ll1l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1l111l_opy_:
                        self.logger.info(bstackl_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣኾ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll111l1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll111l1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstackl_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ኿"):
                                entry = bstack1ll1l1ll11l_opy_(
                                    kind=bstackl_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢዀ"),
                                    message=bstackl_opy_ (u"ࠨࠢ዁"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1llll11l1_opy_=file_size,
                                    bstack1l1ll1lll1l_opy_=bstackl_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢዂ"),
                                    bstack11llll_opy_=os.path.abspath(file_path),
                                    bstack1ll1l1ll1_opy_=bstack1l1l1ll1111_opy_
                                )
                            elif level == bstackl_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧዃ"):
                                entry = bstack1ll1l1ll11l_opy_(
                                    kind=bstackl_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦዄ"),
                                    message=bstackl_opy_ (u"ࠥࠦዅ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1llll11l1_opy_=file_size,
                                    bstack1l1ll1lll1l_opy_=bstackl_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ዆"),
                                    bstack11llll_opy_=os.path.abspath(file_path),
                                    bstack1l1l1l1lll1_opy_=bstack1l1l1ll1111_opy_
                                )
                            bstack1l1ll11l111_opy_.append(entry)
                            _1l1ll1l111l_opy_.add(abs_path)
                        except Exception as bstack1l1ll111111_opy_:
                            self.logger.error(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦ዇").format(bstack1l1ll111111_opy_))
        except Exception as e:
            self.logger.error(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧወ").format(e))
        event[bstackl_opy_ (u"ࠢ࡭ࡱࡪࡷࠧዉ")] = bstack1l1ll11l111_opy_
class bstack1l1lll1lll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1l1lllll1_opy_ = set()
        kwargs[bstackl_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥዊ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l1ll1l1l_opy_(obj, self.bstack1l1l1lllll1_opy_)
def bstack1l1ll1llll1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l1ll1l1l_opy_(obj, bstack1l1l1lllll1_opy_=None, max_depth=3):
    if bstack1l1l1lllll1_opy_ is None:
        bstack1l1l1lllll1_opy_ = set()
    if id(obj) in bstack1l1l1lllll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1l1lllll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1l1ll1ll1_opy_ = TestFramework.bstack1l1ll1l11ll_opy_(obj)
    bstack1l1ll1l1l11_opy_ = next((k.lower() in bstack1l1l1ll1ll1_opy_.lower() for k in bstack1l1lll11l1l_opy_.keys()), None)
    if bstack1l1ll1l1l11_opy_:
        obj = TestFramework.bstack1l1l1l1ll11_opy_(obj, bstack1l1lll11l1l_opy_[bstack1l1ll1l1l11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstackl_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧዋ")):
            keys = getattr(obj, bstackl_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨዌ"), [])
        elif hasattr(obj, bstackl_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨው")):
            keys = getattr(obj, bstackl_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢዎ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstackl_opy_ (u"ࠨ࡟ࠣዏ"))}
        if not obj and bstack1l1l1ll1ll1_opy_ == bstackl_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦዐ"):
            obj = {bstackl_opy_ (u"ࠣࡲࡤࡸ࡭ࠨዑ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll1llll1_opy_(key) or str(key).startswith(bstackl_opy_ (u"ࠤࡢࠦዒ")):
            continue
        if value is not None and bstack1l1ll1llll1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l1ll1l1l_opy_(value, bstack1l1l1lllll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l1ll1l1l_opy_(o, bstack1l1l1lllll1_opy_, max_depth) for o in value]))
    return result or None