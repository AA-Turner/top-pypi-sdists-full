# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack1lllll111ll_opy_, bstack1llll1l1lll_opy_, bstack1lllllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111ll_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1lll111llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll11l1l11_opy_, bstack1lll1llll11_opy_, bstack1ll1l1ll111_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l1lll111_opy_, bstack1l1l1ll11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll1l1l11_opy_ = [bstack1l11l11_opy_ (u"ࠢ࡯ࡣࡰࡩࠧቒ"), bstack1l11l11_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣቓ"), bstack1l11l11_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤቔ"), bstack1l11l11_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦቕ"), bstack1l11l11_opy_ (u"ࠦࡵࡧࡴࡩࠤቖ")]
bstack1l1ll1111ll_opy_ = bstack1l1l1ll11l1_opy_()
bstack1l1lll11l1l_opy_ = bstack1l11l11_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧ቗")
bstack1l1ll11l11l_opy_ = {
    bstack1l11l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦቘ"): bstack1l1ll1l1l11_opy_,
    bstack1l11l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣ቙"): bstack1l1ll1l1l11_opy_,
    bstack1l11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣቚ"): bstack1l1ll1l1l11_opy_,
    bstack1l11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣቛ"): bstack1l1ll1l1l11_opy_,
    bstack1l11l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧቜ"): bstack1l1ll1l1l11_opy_
    + [
        bstack1l11l11_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥቝ"),
        bstack1l11l11_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢ቞"),
        bstack1l11l11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦ቟"),
        bstack1l11l11_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤበ"),
        bstack1l11l11_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥቡ"),
        bstack1l11l11_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥቢ"),
        bstack1l11l11_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤባ"),
        bstack1l11l11_opy_ (u"ࠦࡸࡺ࡯ࡱࠤቤ"),
        bstack1l11l11_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢብ"),
        bstack1l11l11_opy_ (u"ࠨࡷࡩࡧࡱࠦቦ"),
    ],
    bstack1l11l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨቧ"): [bstack1l11l11_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦቨ"), bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢቩ"), bstack1l11l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦቪ"), bstack1l11l11_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥቫ")],
    bstack1l11l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧቬ"): [bstack1l11l11_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥቭ"), bstack1l11l11_opy_ (u"ࠢࡢࡴࡪࡷࠧቮ")],
    bstack1l11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢቯ"): [bstack1l11l11_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣተ"), bstack1l11l11_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦቱ"), bstack1l11l11_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤቲ"), bstack1l11l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧታ"), bstack1l11l11_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣቴ"), bstack1l11l11_opy_ (u"ࠢࡪࡦࡶࠦት")],
    bstack1l11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢቶ"): [bstack1l11l11_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢቷ"), bstack1l11l11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤቸ"), bstack1l11l11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤቹ")],
    bstack1l11l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢቺ"): [bstack1l11l11_opy_ (u"ࠨࡷࡩࡧࡱࠦቻ"), bstack1l11l11_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢቼ")],
    bstack1l11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤች"): [bstack1l11l11_opy_ (u"ࠤࡱࡳࡩ࡫ࠢቾ"), bstack1l11l11_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥቿ")],
    bstack1l11l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦኀ"): [bstack1l11l11_opy_ (u"ࠧࡴࡡ࡮ࡧࠥኁ"), bstack1l11l11_opy_ (u"ࠨࡡࡳࡩࡶࠦኂ"), bstack1l11l11_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢኃ")],
}
_1l1ll11lll1_opy_ = set()
class bstack1ll1l1ll11l_opy_(bstack1lll1l11lll_opy_):
    bstack1l1ll1l1lll_opy_ = bstack1l11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣኄ")
    bstack1l1ll111l11_opy_ = bstack1l11l11_opy_ (u"ࠤࡌࡒࡋࡕࠢኅ")
    bstack1l1lll1111l_opy_ = bstack1l11l11_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤኆ")
    bstack1l1ll1ll111_opy_: Callable
    bstack1l1l1lll1l1_opy_: Callable
    def __init__(self, bstack1lll1111l1l_opy_, bstack1lll11l1ll1_opy_):
        super().__init__()
        self.bstack1ll111llll1_opy_ = bstack1lll11l1ll1_opy_
        if os.getenv(bstack1l11l11_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣኇ"), bstack1l11l11_opy_ (u"ࠧ࠷ࠢኈ")) != bstack1l11l11_opy_ (u"ࠨ࠱ࠣ኉") or not self.is_enabled():
            self.logger.warning(bstack1l11l11_opy_ (u"ࠢࠣኊ") + str(self.__class__.__name__) + bstack1l11l11_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦኋ"))
            return
        TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.PRE), self.bstack1ll111l1l11_opy_)
        TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.POST), self.bstack1ll1111llll_opy_)
        for event in bstack1lll1l1lll1_opy_:
            for state in bstack1lll1llll11_opy_:
                TestFramework.bstack1ll1l111l11_opy_((event, state), self.bstack1l1ll1l1l1l_opy_)
        bstack1lll1111l1l_opy_.bstack1ll1l111l11_opy_((bstack1llll1l1lll_opy_.bstack1llll1ll111_opy_, bstack1lllllllll1_opy_.POST), self.bstack1l1ll11l1l1_opy_)
        self.bstack1l1ll1ll111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1ll111ll1_opy_(bstack1ll1l1ll11l_opy_.bstack1l1ll111l11_opy_, self.bstack1l1ll1ll111_opy_)
        self.bstack1l1l1lll1l1_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1ll111ll1_opy_(bstack1ll1l1ll11l_opy_.bstack1l1lll1111l_opy_, self.bstack1l1l1lll1l1_opy_)
        self.bstack1l1lll1ll1l_opy_ = builtins.print
        builtins.print = self.bstack1l1l1l1lll1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll1l1ll_opy_() and instance:
            bstack1l1ll111lll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llllll11l1_opy_
            if test_framework_state == bstack1lll1l1lll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1l1lll1_opy_.LOG:
                bstack1l11l11111_opy_ = datetime.now()
                entries = f.bstack1l1l1ll11ll_opy_(instance, bstack1llllll11l1_opy_)
                if entries:
                    self.bstack1l1ll1llll1_opy_(instance, entries)
                    instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤኌ"), datetime.now() - bstack1l11l11111_opy_)
                    f.bstack1l1ll11ll11_opy_(instance, bstack1llllll11l1_opy_)
                instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨኍ"), datetime.now() - bstack1l1ll111lll_opy_)
                return # bstack1l1l1lll1ll_opy_ not send this event with the bstack1l1lll11ll1_opy_ bstack1l1l1l1ll11_opy_
            elif (
                test_framework_state == bstack1lll1l1lll1_opy_.TEST
                and test_hook_state == bstack1lll1llll11_opy_.POST
                and not f.bstack1lllll1llll_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)
            ):
                self.logger.warning(bstack1l11l11_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤ኎") + str(TestFramework.bstack1lllll1llll_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)) + bstack1l11l11_opy_ (u"ࠧࠨ኏"))
                f.bstack1lllll1l11l_opy_(instance, bstack1ll1l1ll11l_opy_.bstack1l1ll1l1lll_opy_, True)
                return # bstack1l1l1lll1ll_opy_ not send this event bstack1l1l1llll11_opy_ bstack1l1ll11ll1l_opy_
            elif (
                f.bstack1lllllll11l_opy_(instance, bstack1ll1l1ll11l_opy_.bstack1l1ll1l1lll_opy_, False)
                and test_framework_state == bstack1lll1l1lll1_opy_.LOG_REPORT
                and test_hook_state == bstack1lll1llll11_opy_.POST
                and f.bstack1lllll1llll_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)
            ):
                self.logger.warning(bstack1l11l11_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧነ") + str(TestFramework.bstack1lllll1llll_opy_(instance, TestFramework.bstack1l1l1ll111l_opy_)) + bstack1l11l11_opy_ (u"ࠢࠣኑ"))
                self.bstack1l1ll1l1l1l_opy_(f, instance, (bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.POST), *args, **kwargs)
            bstack1l11l11111_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1ll1lllll_opy_ = sorted(
                filter(lambda x: x.get(bstack1l11l11_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦኒ"), None), data.pop(bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤና"), {}).values()),
                key=lambda x: x[bstack1l11l11_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨኔ")],
            )
            if bstack1lll111llll_opy_.bstack1l1lll11111_opy_ in data:
                data.pop(bstack1lll111llll_opy_.bstack1l1lll11111_opy_)
            data.update({bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦን"): bstack1l1ll1lllll_opy_})
            instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥኖ"), datetime.now() - bstack1l11l11111_opy_)
            bstack1l11l11111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1lll111l1_opy_)
            instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤኗ"), datetime.now() - bstack1l11l11111_opy_)
            self.bstack1l1l1l1ll11_opy_(instance, bstack1llllll11l1_opy_, event_json=event_json)
            instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥኘ"), datetime.now() - bstack1l1ll111lll_opy_)
    def bstack1ll111l1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1ll1l1lllll_opy_
        bstack1ll11l1l111_opy_ = bstack1ll1l1lllll_opy_.bstack1ll11llllll_opy_(EVENTS.bstack1l1111l1l_opy_.value)
        self.bstack1ll111llll1_opy_.bstack1l1lll1l1l1_opy_(instance, f, bstack1llllll11l1_opy_, *args, **kwargs)
        bstack1ll1l1lllll_opy_.end(EVENTS.bstack1l1111l1l_opy_.value, bstack1ll11l1l111_opy_ + bstack1l11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኙ"), bstack1ll11l1l111_opy_ + bstack1l11l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢኚ"), status=True, failure=None, test_name=None)
    def bstack1ll1111llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll111llll1_opy_.bstack1l1l1llllll_opy_(instance, f, bstack1llllll11l1_opy_, *args, **kwargs)
        self.bstack1l1l1l1ll1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1l1ll1ll1_opy_, stage=STAGE.bstack1lll11l1_opy_)
    def bstack1l1l1l1ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨኛ"))
            return
        bstack1l11l11111_opy_ = datetime.now()
        try:
            r = self.bstack1lll1lll111_opy_.TestSessionEvent(req)
            instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧኜ"), datetime.now() - bstack1l11l11111_opy_)
            f.bstack1lllll1l11l_opy_(instance, self.bstack1ll111llll1_opy_.bstack1l1lll1llll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l11l11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢኝ") + str(r) + bstack1l11l11_opy_ (u"ࠨࠢኞ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧኟ") + str(e) + bstack1l11l11_opy_ (u"ࠣࠤአ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll11l1l1_opy_(
        self,
        f: bstack1ll1llll111_opy_,
        _driver: object,
        exec: Tuple[bstack1lllll111ll_opy_, str],
        _1l1ll1l1111_opy_: Tuple[bstack1llll1l1lll_opy_, bstack1lllllllll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1llll111_opy_.bstack1ll11l1llll_opy_(method_name):
            return
        if f.bstack1ll11l1lll1_opy_(*args) == bstack1ll1llll111_opy_.bstack1l1l1ll1l11_opy_:
            bstack1l1ll111lll_opy_ = datetime.now()
            screenshot = result.get(bstack1l11l11_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣኡ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l11l11_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦኢ"))
                return
            bstack1l1ll1111l1_opy_ = self.bstack1l1lll11lll_opy_(instance)
            if bstack1l1ll1111l1_opy_:
                entry = bstack1ll1l1ll111_opy_(TestFramework.bstack1l1l1lll11l_opy_, screenshot)
                self.bstack1l1ll1llll1_opy_(bstack1l1ll1111l1_opy_, [entry])
                instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧኣ"), datetime.now() - bstack1l1ll111lll_opy_)
            else:
                self.logger.warning(bstack1l11l11_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥኤ").format(instance.ref()))
        event = {}
        bstack1l1ll1111l1_opy_ = self.bstack1l1lll11lll_opy_(instance)
        if bstack1l1ll1111l1_opy_:
            self.bstack1l1ll11l1ll_opy_(event, bstack1l1ll1111l1_opy_)
            if event.get(bstack1l11l11_opy_ (u"ࠨ࡬ࡰࡩࡶࠦእ")):
                self.bstack1l1ll1llll1_opy_(bstack1l1ll1111l1_opy_, event[bstack1l11l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧኦ")])
            else:
                self.logger.debug(bstack1l11l11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧኧ"))
    @measure(event_name=EVENTS.bstack1l1ll1ll11l_opy_, stage=STAGE.bstack1lll11l1_opy_)
    def bstack1l1ll1llll1_opy_(
        self,
        bstack1l1ll1111l1_opy_: bstack1lll11l1l11_opy_,
        entries: List[bstack1ll1l1ll111_opy_],
    ):
        self.bstack1ll1l111l1l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllllll11l_opy_(bstack1l1ll1111l1_opy_, TestFramework.bstack1ll11l1l11l_opy_)
        req.execution_context.hash = str(bstack1l1ll1111l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1ll1111l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1ll1111l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllllll11l_opy_(bstack1l1ll1111l1_opy_, TestFramework.bstack1ll11l11ll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllllll11l_opy_(bstack1l1ll1111l1_opy_, TestFramework.bstack1l1ll1ll1ll_opy_)
            log_entry.uuid = TestFramework.bstack1lllllll11l_opy_(bstack1l1ll1111l1_opy_, TestFramework.bstack1ll1l1111l1_opy_)
            log_entry.test_framework_state = bstack1l1ll1111l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l11l11_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣከ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l11l11_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧኩ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1l1_opy_
                log_entry.file_path = entry.bstack11ll111_opy_
        def bstack1l1l1ll1lll_opy_():
            bstack1l11l11111_opy_ = datetime.now()
            try:
                self.bstack1lll1lll111_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1l1lll11l_opy_:
                    bstack1l1ll1111l1_opy_.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣኪ"), datetime.now() - bstack1l11l11111_opy_)
                elif entry.kind == TestFramework.bstack1l1ll1lll11_opy_:
                    bstack1l1ll1111l1_opy_.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤካ"), datetime.now() - bstack1l11l11111_opy_)
                else:
                    bstack1l1ll1111l1_opy_.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥኬ"), datetime.now() - bstack1l11l11111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11l11_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧክ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l1l1_opy_.enqueue(bstack1l1l1ll1lll_opy_)
    @measure(event_name=EVENTS.bstack1l1lll111ll_opy_, stage=STAGE.bstack1lll11l1_opy_)
    def bstack1l1l1l1ll11_opy_(
        self,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        event_json=None,
    ):
        self.bstack1ll1l111l1l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1ll11l1l11l_opy_)
        req.test_framework_name = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1ll11l11ll1_opy_)
        req.test_framework_version = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1l1ll1ll1ll_opy_)
        req.test_framework_state = bstack1llllll11l1_opy_[0].name
        req.test_hook_state = bstack1llllll11l1_opy_[1].name
        started_at = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1l1lll1lll1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1lll111l1_opy_)).encode(bstack1l11l11_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኮ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1l1ll1lll_opy_():
            bstack1l11l11111_opy_ = datetime.now()
            try:
                self.bstack1lll1lll111_opy_.TestFrameworkEvent(req)
                instance.bstack1l1l1l1l1l_opy_(bstack1l11l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧኯ"), datetime.now() - bstack1l11l11111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11l11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣኰ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack111111l1l1_opy_.enqueue(bstack1l1l1ll1lll_opy_)
    def bstack1l1lll11lll_opy_(self, instance: bstack1lllll111ll_opy_):
        bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1lllll11l11_opy_(instance.context)
        for t in bstack1l1ll1l1ll1_opy_:
            bstack1l1lll1l111_opy_ = TestFramework.bstack1lllllll11l_opy_(t, bstack1lll111llll_opy_.bstack1l1lll11111_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1l111_opy_):
                return t
    def bstack1l1ll1l11ll_opy_(self, message):
        self.bstack1l1ll1ll111_opy_(message + bstack1l11l11_opy_ (u"ࠦࡡࡴࠢ኱"))
    def log_error(self, message):
        self.bstack1l1l1lll1l1_opy_(message + bstack1l11l11_opy_ (u"ࠧࡢ࡮ࠣኲ"))
    def bstack1l1ll111ll1_opy_(self, level, original_func):
        def bstack1l1ll1l11l1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstack1l11l11_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢኳ") in message or bstack1l11l11_opy_ (u"ࠢ࡜ࡕࡇࡏࡈࡒࡉ࡞ࠤኴ") in message or bstack1l11l11_opy_ (u"ࠣ࡝࡚ࡩࡧࡊࡲࡪࡸࡨࡶࡒࡵࡤࡶ࡮ࡨࡡࠧኵ") in message:
                return return_value
            bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1l1l1llll1l_opy_()
            if not bstack1l1ll1l1ll1_opy_:
                return return_value
            bstack1l1ll1111l1_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1l1ll1_opy_
                    if TestFramework.bstack1lllll1llll_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
                ),
                None,
            )
            if not bstack1l1ll1111l1_opy_:
                return return_value
            entry = bstack1ll1l1ll111_opy_(TestFramework.bstack1l1ll11l111_opy_, message, level)
            self.bstack1l1ll1llll1_opy_(bstack1l1ll1111l1_opy_, [entry])
            return return_value
        return bstack1l1ll1l11l1_opy_
    def bstack1l1l1l1lll1_opy_(self):
        def bstack1l1ll11111l_opy_(*args, **kwargs):
            self.bstack1l1lll1ll1l_opy_(*args, **kwargs)
            message = bstack1l11l11_opy_ (u"ࠩࠣࠫ኶").join(str(arg) for arg in args)
            if not message.strip():
                return
            if bstack1l11l11_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦ኷") in message:
                return
            bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1l1l1llll1l_opy_()
            if not bstack1l1ll1l1ll1_opy_:
                return
            bstack1l1ll1111l1_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1l1ll1_opy_
                    if TestFramework.bstack1lllll1llll_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
                ),
                None,
            )
            if not bstack1l1ll1111l1_opy_:
                return
            entry = bstack1ll1l1ll111_opy_(TestFramework.bstack1l1ll11l111_opy_, message, bstack1ll1l1ll11l_opy_.bstack1l1ll111l11_opy_)
            self.bstack1l1ll1llll1_opy_(bstack1l1ll1111l1_opy_, [entry])
        return bstack1l1ll11111l_opy_
    def bstack1l1ll11l1ll_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll11lll1_opy_
        levels = [bstack1l11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢኸ"), bstack1l11l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤኹ")]
        bstack1l1l1l1l1ll_opy_ = bstack1l11l11_opy_ (u"ࠨࠢኺ")
        if instance is not None:
            try:
                bstack1l1l1l1l1ll_opy_ = TestFramework.bstack1lllllll11l_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
            except Exception as e:
                self.logger.warning(bstack1l11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧኻ").format(e))
        bstack1l1ll11llll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨኼ")]
                bstack1l1l1ll1l1l_opy_ = os.path.join(bstack1l1ll1111ll_opy_, (bstack1l1lll11l1l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1l1ll1l1l_opy_):
                    self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧኽ").format(bstack1l1l1ll1l1l_opy_))
                    continue
                file_names = os.listdir(bstack1l1l1ll1l1l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1l1ll1l1l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll11lll1_opy_:
                        self.logger.info(bstack1l11l11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣኾ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l1ll1111_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l1ll1111_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l11l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢ኿"):
                                entry = bstack1ll1l1ll111_opy_(
                                    kind=bstack1l11l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢዀ"),
                                    message=bstack1l11l11_opy_ (u"ࠨࠢ዁"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1ll1l1_opy_=file_size,
                                    bstack1l1l1l1llll_opy_=bstack1l11l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢዂ"),
                                    bstack11ll111_opy_=os.path.abspath(file_path),
                                    bstack11l1ll11l_opy_=bstack1l1l1l1l1ll_opy_
                                )
                            elif level == bstack1l11l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧዃ"):
                                entry = bstack1ll1l1ll111_opy_(
                                    kind=bstack1l11l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦዄ"),
                                    message=bstack1l11l11_opy_ (u"ࠥࠦዅ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1ll1l1_opy_=file_size,
                                    bstack1l1l1l1llll_opy_=bstack1l11l11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦ዆"),
                                    bstack11ll111_opy_=os.path.abspath(file_path),
                                    bstack1l1ll1l111l_opy_=bstack1l1l1l1l1ll_opy_
                                )
                            bstack1l1ll11llll_opy_.append(entry)
                            _1l1ll11lll1_opy_.add(abs_path)
                        except Exception as bstack1l1lll1l11l_opy_:
                            self.logger.error(bstack1l11l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦ዇").format(bstack1l1lll1l11l_opy_))
        except Exception as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧወ").format(e))
        event[bstack1l11l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧዉ")] = bstack1l1ll11llll_opy_
class bstack1l1lll111l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1llll111l_opy_ = set()
        kwargs[bstack1l11l11_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥዊ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1lll1l_opy_(obj, self.bstack1l1llll111l_opy_)
def bstack1l1ll111l1l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1lll1l_opy_(obj, bstack1l1llll111l_opy_=None, max_depth=3):
    if bstack1l1llll111l_opy_ is None:
        bstack1l1llll111l_opy_ = set()
    if id(obj) in bstack1l1llll111l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1llll111l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1llll1111_opy_ = TestFramework.bstack1l1ll111111_opy_(obj)
    bstack1l1lll11l11_opy_ = next((k.lower() in bstack1l1llll1111_opy_.lower() for k in bstack1l1ll11l11l_opy_.keys()), None)
    if bstack1l1lll11l11_opy_:
        obj = TestFramework.bstack1l1lll1ll11_opy_(obj, bstack1l1ll11l11l_opy_[bstack1l1lll11l11_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l11l11_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧዋ")):
            keys = getattr(obj, bstack1l11l11_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨዌ"), [])
        elif hasattr(obj, bstack1l11l11_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨው")):
            keys = getattr(obj, bstack1l11l11_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢዎ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l11l11_opy_ (u"ࠨ࡟ࠣዏ"))}
        if not obj and bstack1l1llll1111_opy_ == bstack1l11l11_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦዐ"):
            obj = {bstack1l11l11_opy_ (u"ࠣࡲࡤࡸ࡭ࠨዑ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll111l1l_opy_(key) or str(key).startswith(bstack1l11l11_opy_ (u"ࠤࡢࠦዒ")):
            continue
        if value is not None and bstack1l1ll111l1l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1lll1l_opy_(value, bstack1l1llll111l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1lll1l_opy_(o, bstack1l1llll111l_opy_, max_depth) for o in value]))
    return result or None