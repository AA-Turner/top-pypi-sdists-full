# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import bstack1llllllll1l_opy_, bstack1lllll11111_opy_, bstack1llll1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l1l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lllll1_opy_, bstack1lll1l1ll1l_opy_, bstack1ll1llll1ll_opy_, bstack1lll1l1llll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll1l1l1l_opy_, bstack1l1ll1l11l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll1l1l11_opy_ = [bstack1111l1l_opy_ (u"ࠦࡳࡧ࡭ࡦࠤቝ"), bstack1111l1l_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧ቞"), bstack1111l1l_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨ቟"), bstack1111l1l_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣበ"), bstack1111l1l_opy_ (u"ࠣࡲࡤࡸ࡭ࠨቡ")]
bstack1l1ll1l111l_opy_ = bstack1l1ll1l11l1_opy_()
bstack1l1l1lll111_opy_ = bstack1111l1l_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤቢ")
bstack1l1l1llll1l_opy_ = {
    bstack1111l1l_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡍࡹ࡫࡭ࠣባ"): bstack1l1ll1l1l11_opy_,
    bstack1111l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡕࡧࡣ࡬ࡣࡪࡩࠧቤ"): bstack1l1ll1l1l11_opy_,
    bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡓ࡯ࡥࡷ࡯ࡩࠧብ"): bstack1l1ll1l1l11_opy_,
    bstack1111l1l_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡃ࡭ࡣࡶࡷࠧቦ"): bstack1l1ll1l1l11_opy_,
    bstack1111l1l_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡇࡷࡱࡧࡹ࡯࡯࡯ࠤቧ"): bstack1l1ll1l1l11_opy_
    + [
        bstack1111l1l_opy_ (u"ࠣࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡱࡥࡲ࡫ࠢቨ"),
        bstack1111l1l_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦቩ"),
        bstack1111l1l_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨ࡭ࡳ࡬࡯ࠣቪ"),
        bstack1111l1l_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨቫ"),
        bstack1111l1l_opy_ (u"ࠧࡩࡡ࡭࡮ࡶࡴࡪࡩࠢቬ"),
        bstack1111l1l_opy_ (u"ࠨࡣࡢ࡮࡯ࡳࡧࡰࠢቭ"),
        bstack1111l1l_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨቮ"),
        bstack1111l1l_opy_ (u"ࠣࡵࡷࡳࡵࠨቯ"),
        bstack1111l1l_opy_ (u"ࠤࡧࡹࡷࡧࡴࡪࡱࡱࠦተ"),
        bstack1111l1l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣቱ"),
    ],
    bstack1111l1l_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡩ࡯࠰ࡖࡩࡸࡹࡩࡰࡰࠥቲ"): [bstack1111l1l_opy_ (u"ࠧࡹࡴࡢࡴࡷࡴࡦࡺࡨࠣታ"), bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡷ࡫ࡧࡩ࡭ࡧࡧࠦቴ"), bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸࡸࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣት"), bstack1111l1l_opy_ (u"ࠣ࡫ࡷࡩࡲࡹࠢቶ")],
    bstack1111l1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡦࡳࡳ࡬ࡩࡨ࠰ࡆࡳࡳ࡬ࡩࡨࠤቷ"): [bstack1111l1l_opy_ (u"ࠥ࡭ࡳࡼ࡯ࡤࡣࡷ࡭ࡴࡴ࡟ࡱࡣࡵࡥࡲࡹࠢቸ"), bstack1111l1l_opy_ (u"ࠦࡦࡸࡧࡴࠤቹ")],
    bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡇ࡫ࡻࡸࡺࡸࡥࡅࡧࡩࠦቺ"): [bstack1111l1l_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧቻ"), bstack1111l1l_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣቼ"), bstack1111l1l_opy_ (u"ࠣࡨࡸࡲࡨࠨች"), bstack1111l1l_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤቾ"), bstack1111l1l_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧቿ"), bstack1111l1l_opy_ (u"ࠦ࡮ࡪࡳࠣኀ")],
    bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡔࡷࡥࡖࡪࡷࡵࡦࡵࡷࠦኁ"): [bstack1111l1l_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦኂ"), bstack1111l1l_opy_ (u"ࠢࡱࡣࡵࡥࡲࠨኃ"), bstack1111l1l_opy_ (u"ࠣࡲࡤࡶࡦࡳ࡟ࡪࡰࡧࡩࡽࠨኄ")],
    bstack1111l1l_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡵࡹࡳࡴࡥࡳ࠰ࡆࡥࡱࡲࡉ࡯ࡨࡲࠦኅ"): [bstack1111l1l_opy_ (u"ࠥࡻ࡭࡫࡮ࠣኆ"), bstack1111l1l_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࠦኇ")],
    bstack1111l1l_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡏࡱࡧࡩࡐ࡫ࡹࡸࡱࡵࡨࡸࠨኈ"): [bstack1111l1l_opy_ (u"ࠨ࡮ࡰࡦࡨࠦ኉"), bstack1111l1l_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢኊ")],
    bstack1111l1l_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡑࡦࡸ࡫ࠣኋ"): [bstack1111l1l_opy_ (u"ࠤࡱࡥࡲ࡫ࠢኌ"), bstack1111l1l_opy_ (u"ࠥࡥࡷ࡭ࡳࠣኍ"), bstack1111l1l_opy_ (u"ࠦࡰࡽࡡࡳࡩࡶࠦ኎")],
}
_1l1l1ll11ll_opy_ = set()
class bstack1lll1l11lll_opy_(bstack1lll1lll111_opy_):
    bstack1l1lll111ll_opy_ = bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࠧ኏")
    bstack1l1lll11lll_opy_ = bstack1111l1l_opy_ (u"ࠨࡉࡏࡈࡒࠦነ")
    bstack1l1l1ll111l_opy_ = bstack1111l1l_opy_ (u"ࠢࡆࡔࡕࡓࡗࠨኑ")
    bstack1l1lll11111_opy_: Callable
    bstack1l1ll111l11_opy_: Callable
    def __init__(self, bstack1ll1l1l1l11_opy_, bstack1lll1l11111_opy_):
        super().__init__()
        self.bstack1ll11llll1l_opy_ = bstack1lll1l11111_opy_
        if os.getenv(bstack1111l1l_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡐ࠳࠴࡝ࠧኒ"), bstack1111l1l_opy_ (u"ࠤ࠴ࠦና")) != bstack1111l1l_opy_ (u"ࠥ࠵ࠧኔ") or not self.is_enabled():
            self.logger.warning(bstack1111l1l_opy_ (u"ࠦࠧን") + str(self.__class__.__name__) + bstack1111l1l_opy_ (u"ࠧࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠣኖ"))
            return
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.PRE), self.bstack1ll1111l1l1_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), self.bstack1ll11llll11_opy_)
        for event in bstack1lll1lllll1_opy_:
            for state in bstack1ll1llll1ll_opy_:
                TestFramework.bstack1ll111lll1l_opy_((event, state), self.bstack1l1ll111l1l_opy_)
        bstack1ll1l1l1l11_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.POST), self.bstack1l1l1llllll_opy_)
        self.bstack1l1lll11111_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1l1lll1l1_opy_(bstack1lll1l11lll_opy_.bstack1l1lll11lll_opy_, self.bstack1l1lll11111_opy_)
        self.bstack1l1ll111l11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1l1lll1l1_opy_(bstack1lll1l11lll_opy_.bstack1l1l1ll111l_opy_, self.bstack1l1ll111l11_opy_)
        self.bstack1l1lll1l111_opy_ = builtins.print
        builtins.print = self.bstack1l1ll111ll1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1l1llll11_opy_() and instance:
            bstack1l1ll1l1lll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lllll11ll1_opy_
            if test_framework_state == bstack1lll1lllll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll1lllll1_opy_.LOG:
                bstack1ll1l1lll_opy_ = datetime.now()
                entries = f.bstack1l1ll1l11ll_opy_(instance, bstack1lllll11ll1_opy_)
                if entries:
                    self.bstack1l1l1ll1lll_opy_(instance, entries)
                    instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨኗ"), datetime.now() - bstack1ll1l1lll_opy_)
                    f.bstack1l1ll1ll1l1_opy_(instance, bstack1lllll11ll1_opy_)
                instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥኘ"), datetime.now() - bstack1l1ll1l1lll_opy_)
                return # bstack1l1l1l1l1ll_opy_ not send this event with the bstack1l1l1l1l1l1_opy_ bstack1l1ll1111ll_opy_
            elif (
                test_framework_state == bstack1lll1lllll1_opy_.TEST
                and test_hook_state == bstack1ll1llll1ll_opy_.POST
                and not f.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)
            ):
                self.logger.warning(bstack1111l1l_opy_ (u"ࠣࡦࡵࡳࡵࡶࡩ࡯ࡩࠣࡨࡺ࡫ࠠࡵࡱࠣࡰࡦࡩ࡫ࠡࡱࡩࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࠨኙ") + str(TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)) + bstack1111l1l_opy_ (u"ࠤࠥኚ"))
                f.bstack1lllllllll1_opy_(instance, bstack1lll1l11lll_opy_.bstack1l1lll111ll_opy_, True)
                return # bstack1l1l1l1l1ll_opy_ not send this event bstack1l1ll11l11l_opy_ bstack1l1ll11111l_opy_
            elif (
                f.bstack1lllll1l11l_opy_(instance, bstack1lll1l11lll_opy_.bstack1l1lll111ll_opy_, False)
                and test_framework_state == bstack1lll1lllll1_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1llll1ll_opy_.POST
                and f.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)
            ):
                self.logger.warning(bstack1111l1l_opy_ (u"ࠥ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲࡙ࡋࡓࡕ࠮ࠣࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡔࡔ࡙ࡔࠡࠤኛ") + str(TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1l1lll111l1_opy_)) + bstack1111l1l_opy_ (u"ࠦࠧኜ"))
                self.bstack1l1ll111l1l_opy_(f, instance, (bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), *args, **kwargs)
            bstack1ll1l1lll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l1lll1ll_opy_ = sorted(
                filter(lambda x: x.get(bstack1111l1l_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣኝ"), None), data.pop(bstack1111l1l_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨኞ"), {}).values()),
                key=lambda x: x[bstack1111l1l_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥኟ")],
            )
            if bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_ in data:
                data.pop(bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_)
            data.update({bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣአ"): bstack1l1l1lll1ll_opy_})
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢኡ"), datetime.now() - bstack1ll1l1lll_opy_)
            bstack1ll1l1lll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll11l1l1_opy_)
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨኢ"), datetime.now() - bstack1ll1l1lll_opy_)
            self.bstack1l1ll1111ll_opy_(instance, bstack1lllll11ll1_opy_, event_json=event_json)
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢኣ"), datetime.now() - bstack1l1ll1l1lll_opy_)
    def bstack1ll1111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
        bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11l1lll11l_opy_.value)
        self.bstack1ll11llll1l_opy_.bstack1l1ll111111_opy_(instance, f, bstack1lllll11ll1_opy_, *args, **kwargs)
        bstack1lll11111ll_opy_.end(EVENTS.bstack11l1lll11l_opy_.value, bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧኤ"), bstack1ll111l1ll1_opy_ + bstack1111l1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦእ"), status=True, failure=None, test_name=None)
    def bstack1ll11llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11llll1l_opy_.bstack1l1ll1llll1_opy_(instance, f, bstack1lllll11ll1_opy_, *args, **kwargs)
        self.bstack1l1lll11l1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll1ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l1lll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥኦ"))
            return
        bstack1ll1l1lll_opy_ = datetime.now()
        try:
            r = self.bstack1ll1ll11l11_opy_.TestSessionEvent(req)
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤኧ"), datetime.now() - bstack1ll1l1lll_opy_)
            f.bstack1lllllllll1_opy_(instance, self.bstack1ll11llll1l_opy_.bstack1l1ll1ll111_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1111l1l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦከ") + str(r) + bstack1111l1l_opy_ (u"ࠥࠦኩ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤኪ") + str(e) + bstack1111l1l_opy_ (u"ࠧࠨካ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        _driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        _1l1l1lllll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1l111ll_opy_.bstack1ll111l111l_opy_(method_name):
            return
        if f.bstack1ll111llll1_opy_(*args) == bstack1lll1l111ll_opy_.bstack1l1lll1ll11_opy_:
            bstack1l1ll1l1lll_opy_ = datetime.now()
            screenshot = result.get(bstack1111l1l_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧኬ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲࠣክ"))
                return
            bstack1l1l1l1ll1l_opy_ = self.bstack1l1ll1ll1ll_opy_(instance)
            if bstack1l1l1l1ll1l_opy_:
                entry = bstack1lll1l1llll_opy_(TestFramework.bstack1l1ll1111l1_opy_, screenshot)
                self.bstack1l1l1ll1lll_opy_(bstack1l1l1l1ll1l_opy_, [entry])
                instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤኮ"), datetime.now() - bstack1l1ll1l1lll_opy_)
            else:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢኯ").format(instance.ref()))
        event = {}
        bstack1l1l1l1ll1l_opy_ = self.bstack1l1ll1ll1ll_opy_(instance)
        if bstack1l1l1l1ll1l_opy_:
            self.bstack1l1lll1lll1_opy_(event, bstack1l1l1l1ll1l_opy_)
            if event.get(bstack1111l1l_opy_ (u"ࠥࡰࡴ࡭ࡳࠣኰ")):
                self.bstack1l1l1ll1lll_opy_(bstack1l1l1l1ll1l_opy_, event[bstack1111l1l_opy_ (u"ࠦࡱࡵࡧࡴࠤ኱")])
            else:
                self.logger.debug(bstack1111l1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤኲ"))
    @measure(event_name=EVENTS.bstack1l1lll1l11l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l1l1ll1lll_opy_(
        self,
        bstack1l1l1l1ll1l_opy_: bstack1lll1l1ll1l_opy_,
        entries: List[bstack1lll1l1llll_opy_],
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll11l1ll1l_opy_)
        req.execution_context.hash = str(bstack1l1l1l1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l1l1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l1l1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll111lll11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1l1ll11llll_opy_)
            log_entry.uuid = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1ll1111ll1l_opy_)
            log_entry.test_framework_state = bstack1l1l1l1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack1111l1l_opy_ (u"ࠨࡵࡵࡨ࠰࠼ࠧኳ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1111l1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤኴ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l1ll1111_opy_
                log_entry.file_path = entry.bstack1l1llll_opy_
        def bstack1l1ll1lll1l_opy_():
            bstack1ll1l1lll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll1111l1_opy_:
                    bstack1l1l1l1ll1l_opy_.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧኵ"), datetime.now() - bstack1ll1l1lll_opy_)
                elif entry.kind == TestFramework.bstack1l1ll11ll11_opy_:
                    bstack1l1l1l1ll1l_opy_.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠨ኶"), datetime.now() - bstack1ll1l1lll_opy_)
                else:
                    bstack1l1l1l1ll1l_opy_.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡰࡴ࡭ࠢ኷"), datetime.now() - bstack1ll1l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l1l_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤኸ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1lll1l_opy_)
    @measure(event_name=EVENTS.bstack1l1lll1111l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1l1ll1111ll_opy_(
        self,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        event_json=None,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll11l1ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111lll11_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_)
        req.test_framework_state = bstack1lllll11ll1_opy_[0].name
        req.test_hook_state = bstack1lllll11ll1_opy_[1].name
        started_at = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1ll1ll11l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll11l1l1_opy_)).encode(bstack1111l1l_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦኹ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1ll1lll1l_opy_():
            bstack1ll1l1lll_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11l11_opy_.TestFrameworkEvent(req)
                instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡩࡻ࡫࡮ࡵࠤኺ"), datetime.now() - bstack1ll1l1lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1111l1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧኻ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111ll1_opy_.enqueue(bstack1l1ll1lll1l_opy_)
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1llllllll1l_opy_):
        bstack1l1l1lll11l_opy_ = TestFramework.bstack1llllll1lll_opy_(instance.context)
        for t in bstack1l1l1lll11l_opy_:
            bstack1l1ll1lll11_opy_ = TestFramework.bstack1lllll1l11l_opy_(t, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll1lll11_opy_):
                return t
    def bstack1l1ll1l1111_opy_(self, message):
        self.bstack1l1lll11111_opy_(message + bstack1111l1l_opy_ (u"ࠣ࡞ࡱࠦኼ"))
    def log_error(self, message):
        self.bstack1l1ll111l11_opy_(message + bstack1111l1l_opy_ (u"ࠤ࡟ࡲࠧኽ"))
    def bstack1l1l1lll1l1_opy_(self, level, original_func):
        def bstack1l1l1l1l11l_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstack1111l1l_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦኾ") in message or bstack1111l1l_opy_ (u"ࠦࡠ࡙ࡄࡌࡅࡏࡍࡢࠨ኿") in message or bstack1111l1l_opy_ (u"ࠧࡡࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠤዀ") in message:
                return return_value
            bstack1l1l1lll11l_opy_ = TestFramework.bstack1l1l1ll1l1l_opy_()
            if not bstack1l1l1lll11l_opy_:
                return return_value
            bstack1l1l1l1ll1l_opy_ = next(
                (
                    instance
                    for instance in bstack1l1l1lll11l_opy_
                    if TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
                ),
                None,
            )
            if not bstack1l1l1l1ll1l_opy_:
                return return_value
            entry = bstack1lll1l1llll_opy_(TestFramework.bstack1l1lll11l11_opy_, message, level)
            self.bstack1l1l1ll1lll_opy_(bstack1l1l1l1ll1l_opy_, [entry])
            return return_value
        return bstack1l1l1l1l11l_opy_
    def bstack1l1ll111ll1_opy_(self):
        def bstack1l1l1ll11l1_opy_(*args, **kwargs):
            try:
                self.bstack1l1lll1l111_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1111l1l_opy_ (u"࠭ࠠࠨ዁").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1111l1l_opy_ (u"ࠢࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥࠣዂ") in message:
                    return
                bstack1l1l1lll11l_opy_ = TestFramework.bstack1l1l1ll1l1l_opy_()
                if not bstack1l1l1lll11l_opy_:
                    return
                bstack1l1l1l1ll1l_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1l1lll11l_opy_
                        if TestFramework.bstack1llll1l11ll_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
                    ),
                    None,
                )
                if not bstack1l1l1l1ll1l_opy_:
                    return
                entry = bstack1lll1l1llll_opy_(TestFramework.bstack1l1lll11l11_opy_, message, bstack1lll1l11lll_opy_.bstack1l1lll11lll_opy_)
                self.bstack1l1l1ll1lll_opy_(bstack1l1l1l1ll1l_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1lll1l111_opy_(bstack1lll11lll1l_opy_ (u"ࠣ࡝ࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠤࡑࡵࡧࠡࡥࡤࡴࡹࡻࡲࡦࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨዃ"))
                except:
                    pass
        return bstack1l1l1ll11l1_opy_
    def bstack1l1lll1lll1_opy_(self, event: dict, instance=None) -> None:
        global _1l1l1ll11ll_opy_
        levels = [bstack1111l1l_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧዄ"), bstack1111l1l_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢዅ")]
        bstack1l1ll11ll1l_opy_ = bstack1111l1l_opy_ (u"ࠦࠧ዆")
        if instance is not None:
            try:
                bstack1l1ll11ll1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
            except Exception as e:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡵࡪࡦࠣࡪࡷࡵ࡭ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥ዇").format(e))
        bstack1l1ll111lll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1111l1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ወ")]
                bstack1l1lll1l1ll_opy_ = os.path.join(bstack1l1ll1l111l_opy_, (bstack1l1l1lll111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1lll1l1ll_opy_):
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡲࡴࡺࠠࡱࡴࡨࡷࡪࡴࡴࠡࡨࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡗࡩࡸࡺࠠࡢࡰࡧࠤࡇࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥዉ").format(bstack1l1lll1l1ll_opy_))
                    continue
                file_names = os.listdir(bstack1l1lll1l1ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1lll1l1ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1l1ll11ll_opy_:
                        self.logger.info(bstack1111l1l_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨዊ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll11l1ll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll11l1ll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1111l1l_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧዋ"):
                                entry = bstack1lll1l1llll_opy_(
                                    kind=bstack1111l1l_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧዌ"),
                                    message=bstack1111l1l_opy_ (u"ࠦࠧው"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l1ll1111_opy_=file_size,
                                    bstack1l1ll1l1ll1_opy_=bstack1111l1l_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧዎ"),
                                    bstack1l1llll_opy_=os.path.abspath(file_path),
                                    bstack1lll1ll11l_opy_=bstack1l1ll11ll1l_opy_
                                )
                            elif level == bstack1111l1l_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥዏ"):
                                entry = bstack1lll1l1llll_opy_(
                                    kind=bstack1111l1l_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤዐ"),
                                    message=bstack1111l1l_opy_ (u"ࠣࠤዑ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l1ll1111_opy_=file_size,
                                    bstack1l1ll1l1ll1_opy_=bstack1111l1l_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤዒ"),
                                    bstack1l1llll_opy_=os.path.abspath(file_path),
                                    bstack1l1lll11ll1_opy_=bstack1l1ll11ll1l_opy_
                                )
                            bstack1l1ll111lll_opy_.append(entry)
                            _1l1l1ll11ll_opy_.add(abs_path)
                        except Exception as bstack1l1ll11l111_opy_:
                            self.logger.error(bstack1111l1l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤዓ").format(bstack1l1ll11l111_opy_))
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥዔ").format(e))
        event[bstack1111l1l_opy_ (u"ࠧࡲ࡯ࡨࡵࠥዕ")] = bstack1l1ll111lll_opy_
class bstack1l1ll11l1l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1l1ll1l11_opy_ = set()
        kwargs[bstack1111l1l_opy_ (u"ࠨࡳ࡬࡫ࡳ࡯ࡪࡿࡳࠣዖ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1ll1lllll_opy_(obj, self.bstack1l1l1ll1l11_opy_)
def bstack1l1l1l1llll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1ll1lllll_opy_(obj, bstack1l1l1ll1l11_opy_=None, max_depth=3):
    if bstack1l1l1ll1l11_opy_ is None:
        bstack1l1l1ll1l11_opy_ = set()
    if id(obj) in bstack1l1l1ll1l11_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1l1ll1l11_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1l1ll1ll1_opy_ = TestFramework.bstack1l1ll11lll1_opy_(obj)
    bstack1l1lll1llll_opy_ = next((k.lower() in bstack1l1l1ll1ll1_opy_.lower() for k in bstack1l1l1llll1l_opy_.keys()), None)
    if bstack1l1lll1llll_opy_:
        obj = TestFramework.bstack1l1l1l1lll1_opy_(obj, bstack1l1l1llll1l_opy_[bstack1l1lll1llll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1111l1l_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥ዗")):
            keys = getattr(obj, bstack1111l1l_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦዘ"), [])
        elif hasattr(obj, bstack1111l1l_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦዙ")):
            keys = getattr(obj, bstack1111l1l_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧዚ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1111l1l_opy_ (u"ࠦࡤࠨዛ"))}
        if not obj and bstack1l1l1ll1ll1_opy_ == bstack1111l1l_opy_ (u"ࠧࡶࡡࡵࡪ࡯࡭ࡧ࠴ࡐࡰࡵ࡬ࡼࡕࡧࡴࡩࠤዜ"):
            obj = {bstack1111l1l_opy_ (u"ࠨࡰࡢࡶ࡫ࠦዝ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1l1l1llll_opy_(key) or str(key).startswith(bstack1111l1l_opy_ (u"ࠢࡠࠤዞ")):
            continue
        if value is not None and bstack1l1l1l1llll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1ll1lllll_opy_(value, bstack1l1l1ll1l11_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1ll1lllll_opy_(o, bstack1l1l1ll1l11_opy_, max_depth) for o in value]))
    return result or None