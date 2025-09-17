# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import bstack1lllllll111_opy_, bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1lll11l1111_opy_, bstack1lll111l1l1_opy_, bstack1ll1lll1l11_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1lll11ll1_opy_, bstack1l1ll11ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1ll11l111_opy_ = [bstack1l11ll1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢቛ"), bstack1l11ll1_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥቜ"), bstack1l11ll1_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦቝ"), bstack1l11ll1_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࠨ቞"), bstack1l11ll1_opy_ (u"ࠨࡰࡢࡶ࡫ࠦ቟")]
bstack1l1lll1lll1_opy_ = bstack1l1ll11ll1l_opy_()
bstack1l1ll1l11ll_opy_ = bstack1l11ll1_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢበ")
bstack1l1l1l1lll1_opy_ = {
    bstack1l11ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡋࡷࡩࡲࠨቡ"): bstack1l1ll11l111_opy_,
    bstack1l11ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡓࡥࡨࡱࡡࡨࡧࠥቢ"): bstack1l1ll11l111_opy_,
    bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡑࡴࡪࡵ࡭ࡧࠥባ"): bstack1l1ll11l111_opy_,
    bstack1l11ll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡈࡲࡡࡴࡵࠥቤ"): bstack1l1ll11l111_opy_,
    bstack1l11ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠢብ"): bstack1l1ll11l111_opy_
    + [
        bstack1l11ll1_opy_ (u"ࠨ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬࡯ࡣࡰࡩࠧቦ"),
        bstack1l11ll1_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤቧ"),
        bstack1l11ll1_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦ࡫ࡱࡪࡴࠨቨ"),
        bstack1l11ll1_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦቩ"),
        bstack1l11ll1_opy_ (u"ࠥࡧࡦࡲ࡬ࡴࡲࡨࡧࠧቪ"),
        bstack1l11ll1_opy_ (u"ࠦࡨࡧ࡬࡭ࡱࡥ࡮ࠧቫ"),
        bstack1l11ll1_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦቬ"),
        bstack1l11ll1_opy_ (u"ࠨࡳࡵࡱࡳࠦቭ"),
        bstack1l11ll1_opy_ (u"ࠢࡥࡷࡵࡥࡹ࡯࡯࡯ࠤቮ"),
        bstack1l11ll1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨቯ"),
    ],
    bstack1l11ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥ࡮ࡴ࠮ࡔࡧࡶࡷ࡮ࡵ࡮ࠣተ"): [bstack1l11ll1_opy_ (u"ࠥࡷࡹࡧࡲࡵࡲࡤࡸ࡭ࠨቱ"), bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡩࡥ࡮ࡲࡥࡥࠤቲ"), bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶࡶࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨታ"), bstack1l11ll1_opy_ (u"ࠨࡩࡵࡧࡰࡷࠧቴ")],
    bstack1l11ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡤࡱࡱࡪ࡮࡭࠮ࡄࡱࡱࡪ࡮࡭ࠢት"): [bstack1l11ll1_opy_ (u"ࠣ࡫ࡱࡺࡴࡩࡡࡵ࡫ࡲࡲࡤࡶࡡࡳࡣࡰࡷࠧቶ"), bstack1l11ll1_opy_ (u"ࠤࡤࡶ࡬ࡹࠢቷ")],
    bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳ࡌࡩࡹࡶࡸࡶࡪࡊࡥࡧࠤቸ"): [bstack1l11ll1_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥቹ"), bstack1l11ll1_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨቺ"), bstack1l11ll1_opy_ (u"ࠨࡦࡶࡰࡦࠦቻ"), bstack1l11ll1_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢቼ"), bstack1l11ll1_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥች"), bstack1l11ll1_opy_ (u"ࠤ࡬ࡨࡸࠨቾ")],
    bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳࡙ࡵࡣࡔࡨࡵࡺ࡫ࡳࡵࠤቿ"): [bstack1l11ll1_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤኀ"), bstack1l11ll1_opy_ (u"ࠧࡶࡡࡳࡣࡰࠦኁ"), bstack1l11ll1_opy_ (u"ࠨࡰࡢࡴࡤࡱࡤ࡯࡮ࡥࡧࡻࠦኂ")],
    bstack1l11ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡳࡷࡱࡲࡪࡸ࠮ࡄࡣ࡯ࡰࡎࡴࡦࡰࠤኃ"): [bstack1l11ll1_opy_ (u"ࠣࡹ࡫ࡩࡳࠨኄ"), bstack1l11ll1_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࠤኅ")],
    bstack1l11ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡔ࡯ࡥࡧࡎࡩࡾࡽ࡯ࡳࡦࡶࠦኆ"): [bstack1l11ll1_opy_ (u"ࠦࡳࡵࡤࡦࠤኇ"), bstack1l11ll1_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧኈ")],
    bstack1l11ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡏࡤࡶࡰࠨ኉"): [bstack1l11ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧኊ"), bstack1l11ll1_opy_ (u"ࠣࡣࡵ࡫ࡸࠨኋ"), bstack1l11ll1_opy_ (u"ࠤ࡮ࡻࡦࡸࡧࡴࠤኌ")],
}
_1l1ll1111ll_opy_ = set()
class bstack1ll1ll1l111_opy_(bstack1ll1l1llll1_opy_):
    bstack1l1ll111l1l_opy_ = bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡨࡪࡪࡸࡲࡦࡦࠥኍ")
    bstack1l1lll11l11_opy_ = bstack1l11ll1_opy_ (u"ࠦࡎࡔࡆࡐࠤ኎")
    bstack1l1lll1l1ll_opy_ = bstack1l11ll1_opy_ (u"ࠧࡋࡒࡓࡑࡕࠦ኏")
    bstack1l1lll1l1l1_opy_: Callable
    bstack1l1l1llll1l_opy_: Callable
    def __init__(self, bstack1lll111ll11_opy_, bstack1llll1111l1_opy_):
        super().__init__()
        self.bstack1ll1111l11l_opy_ = bstack1llll1111l1_opy_
        if os.getenv(bstack1l11ll1_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡕ࠱࠲࡛ࠥነ"), bstack1l11ll1_opy_ (u"ࠢ࠲ࠤኑ")) != bstack1l11ll1_opy_ (u"ࠣ࠳ࠥኒ") or not self.is_enabled():
            self.logger.warning(bstack1l11ll1_opy_ (u"ࠤࠥና") + str(self.__class__.__name__) + bstack1l11ll1_opy_ (u"ࠥࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠨኔ"))
            return
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.PRE), self.bstack1ll11l11ll1_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), self.bstack1ll11lllll1_opy_)
        for event in bstack1ll1ll11l1l_opy_:
            for state in bstack1lll111l1l1_opy_:
                TestFramework.bstack1ll11ll111l_opy_((event, state), self.bstack1l1l1l1l11l_opy_)
        bstack1lll111ll11_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.POST), self.bstack1l1ll111lll_opy_)
        self.bstack1l1lll1l1l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1l1ll11l1_opy_(bstack1ll1ll1l111_opy_.bstack1l1lll11l11_opy_, self.bstack1l1lll1l1l1_opy_)
        self.bstack1l1l1llll1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1l1ll11l1_opy_(bstack1ll1ll1l111_opy_.bstack1l1lll1l1ll_opy_, self.bstack1l1l1llll1l_opy_)
        self.bstack1l1ll1lll1l_opy_ = builtins.print
        builtins.print = self.bstack1l1l1l1ll11_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll11111_opy_() and instance:
            bstack1l1l1ll1l11_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lllll1llll_opy_
            if test_framework_state == bstack1ll1ll11l1l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG:
                bstack1l11ll1ll_opy_ = datetime.now()
                entries = f.bstack1l1l1ll11ll_opy_(instance, bstack1lllll1llll_opy_)
                if entries:
                    self.bstack1l1l1ll1ll1_opy_(instance, entries)
                    instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦን"), datetime.now() - bstack1l11ll1ll_opy_)
                    f.bstack1l1l1ll111l_opy_(instance, bstack1lllll1llll_opy_)
                instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣኖ"), datetime.now() - bstack1l1l1ll1l11_opy_)
                return # bstack1l1l1l1l1l1_opy_ not send this event with the bstack1l1lll1ll1l_opy_ bstack1l1l1lll1ll_opy_
            elif (
                test_framework_state == bstack1ll1ll11l1l_opy_.TEST
                and test_hook_state == bstack1lll111l1l1_opy_.POST
                and not f.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)
            ):
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠨࡤࡳࡱࡳࡴ࡮ࡴࡧࠡࡦࡸࡩࠥࡺ࡯ࠡ࡮ࡤࡧࡰࠦ࡯ࡧࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࠦኗ") + str(TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)) + bstack1l11ll1_opy_ (u"ࠢࠣኘ"))
                f.bstack1llllll1ll1_opy_(instance, bstack1ll1ll1l111_opy_.bstack1l1ll111l1l_opy_, True)
                return # bstack1l1l1l1l1l1_opy_ not send this event bstack1l1ll1ll11l_opy_ bstack1l1ll11llll_opy_
            elif (
                f.bstack1llllllllll_opy_(instance, bstack1ll1ll1l111_opy_.bstack1l1ll111l1l_opy_, False)
                and test_framework_state == bstack1ll1ll11l1l_opy_.LOG_REPORT
                and test_hook_state == bstack1lll111l1l1_opy_.POST
                and f.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)
            ):
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠣ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡗࡉࡘ࡚ࠬࠡࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡒࡒࡗ࡙ࠦࠢኙ") + str(TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1l1ll1ll111_opy_)) + bstack1l11ll1_opy_ (u"ࠤࠥኚ"))
                self.bstack1l1l1l1l11l_opy_(f, instance, (bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), *args, **kwargs)
            bstack1l11ll1ll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l1l1llll_opy_ = sorted(
                filter(lambda x: x.get(bstack1l11ll1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨኛ"), None), data.pop(bstack1l11ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦኜ"), {}).values()),
                key=lambda x: x[bstack1l11ll1_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣኝ")],
            )
            if bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_ in data:
                data.pop(bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_)
            data.update({bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨኞ"): bstack1l1l1l1llll_opy_})
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧኟ"), datetime.now() - bstack1l11ll1ll_opy_)
            bstack1l11ll1ll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll111l11_opy_)
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦአ"), datetime.now() - bstack1l11ll1ll_opy_)
            self.bstack1l1l1lll1ll_opy_(instance, bstack1lllll1llll_opy_, event_json=event_json)
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧኡ"), datetime.now() - bstack1l1l1ll1l11_opy_)
    def bstack1ll11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
        bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack11l111ll11_opy_.value)
        self.bstack1ll1111l11l_opy_.bstack1l1lll1l111_opy_(instance, f, bstack1lllll1llll_opy_, *args, **kwargs)
        bstack1lll11111l1_opy_.end(EVENTS.bstack11l111ll11_opy_.value, bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥኢ"), bstack1ll111l1lll_opy_ + bstack1l11ll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤኣ"), status=True, failure=None, test_name=None)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1111l11l_opy_.bstack1l1ll1ll1l1_opy_(instance, f, bstack1lllll1llll_opy_, *args, **kwargs)
        self.bstack1l1lll11l1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1ll1l11l1_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l1lll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l11ll1_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠣ࡫ࡗࡖࡃࠡࡥࡤࡰࡱࡀࠠࡏࡱࠣࡺࡦࡲࡩࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠣኤ"))
            return
        bstack1l11ll1ll_opy_ = datetime.now()
        try:
            r = self.bstack1lll111111l_opy_.TestSessionEvent(req)
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡧࡹࡩࡳࡺࠢእ"), datetime.now() - bstack1l11ll1ll_opy_)
            f.bstack1llllll1ll1_opy_(instance, self.bstack1ll1111l11l_opy_.bstack1l1lll111l1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l11ll1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤኦ") + str(r) + bstack1l11ll1_opy_ (u"ࠣࠤኧ"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢከ") + str(e) + bstack1l11ll1_opy_ (u"ࠥࠦኩ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll111lll_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        _driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        _1l1ll11l11l_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1l1l1lll_opy_.bstack1ll11l11l11_opy_(method_name):
            return
        if f.bstack1ll1l111111_opy_(*args) == bstack1ll1l1l1lll_opy_.bstack1l1l1lllll1_opy_:
            bstack1l1l1ll1l11_opy_ = datetime.now()
            screenshot = result.get(bstack1l11ll1_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥኪ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣ࡭ࡲࡧࡧࡦࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡸࡷࠨካ"))
                return
            bstack1l1lll11lll_opy_ = self.bstack1l1ll1lllll_opy_(instance)
            if bstack1l1lll11lll_opy_:
                entry = bstack1ll1lll1l11_opy_(TestFramework.bstack1l1ll1ll1ll_opy_, screenshot)
                self.bstack1l1l1ll1ll1_opy_(bstack1l1lll11lll_opy_, [entry])
                instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡥࡹࡧࡦࡹࡹ࡫ࠢኬ"), datetime.now() - bstack1l1l1ll1l11_opy_)
            else:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠢࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡦࡵࡷࠤ࡫ࡵࡲࠡࡹ࡫࡭ࡨ࡮ࠠࡵࡪ࡬ࡷࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡺࡥࡸࠦࡴࡢ࡭ࡨࡲࠥࡨࡹࠡࡦࡵ࡭ࡻ࡫ࡲ࠾ࠢࡾࢁࠧክ").format(instance.ref()))
        event = {}
        bstack1l1lll11lll_opy_ = self.bstack1l1ll1lllll_opy_(instance)
        if bstack1l1lll11lll_opy_:
            self.bstack1l1ll1l1lll_opy_(event, bstack1l1lll11lll_opy_)
            if event.get(bstack1l11ll1_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨኮ")):
                self.bstack1l1l1ll1ll1_opy_(bstack1l1lll11lll_opy_, event[bstack1l11ll1_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢኯ")])
            else:
                self.logger.debug(bstack1l11ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡯ࡳ࡬ࡹࠠࡧࡱࡵࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡧࡹࡩࡳࡺࠢኰ"))
    @measure(event_name=EVENTS.bstack1l1l1l1ll1l_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l1l1ll1ll1_opy_(
        self,
        bstack1l1lll11lll_opy_: bstack1lll11l1111_opy_,
        entries: List[bstack1ll1lll1l11_opy_],
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll1111l1l1_opy_)
        req.execution_context.hash = str(bstack1l1lll11lll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll11lll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll11lll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll1l111l1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1l1l1l1l1ll_opy_)
            log_entry.uuid = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1ll111ll1ll_opy_)
            log_entry.test_framework_state = bstack1l1lll11lll_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l11ll1_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥ኱"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l11ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢኲ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1l111l_opy_
                log_entry.file_path = entry.bstack111l111_opy_
        def bstack1l1l1ll1lll_opy_():
            bstack1l11ll1ll_opy_ = datetime.now()
            try:
                self.bstack1lll111111l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll1ll1ll_opy_:
                    bstack1l1lll11lll_opy_.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥኳ"), datetime.now() - bstack1l11ll1ll_opy_)
                elif entry.kind == TestFramework.bstack1l1ll11lll1_opy_:
                    bstack1l1lll11lll_opy_.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦኴ"), datetime.now() - bstack1l11ll1ll_opy_)
                else:
                    bstack1l1lll11lll_opy_.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧኵ"), datetime.now() - bstack1l11ll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11ll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢ኶") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111ll1_opy_.enqueue(bstack1l1l1ll1lll_opy_)
    @measure(event_name=EVENTS.bstack1l1ll1111l1_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1l1l1lll1ll_opy_(
        self,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        event_json=None,
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_)
        req.test_framework_name = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        req.test_framework_version = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1l1l1ll_opy_)
        req.test_framework_state = bstack1lllll1llll_opy_[0].name
        req.test_hook_state = bstack1lllll1llll_opy_[1].name
        started_at = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll111l11_opy_)).encode(bstack1l11ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤ኷"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1l1ll1lll_opy_():
            bstack1l11ll1ll_opy_ = datetime.now()
            try:
                self.bstack1lll111111l_opy_.TestFrameworkEvent(req)
                instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡧࡹࡩࡳࡺࠢኸ"), datetime.now() - bstack1l11ll1ll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l11ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥኹ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111ll1_opy_.enqueue(bstack1l1l1ll1lll_opy_)
    def bstack1l1ll1lllll_opy_(self, instance: bstack1lllllll111_opy_):
        bstack1l1lll1111l_opy_ = TestFramework.bstack1lllllll1l1_opy_(instance.context)
        for t in bstack1l1lll1111l_opy_:
            bstack1l1l1l1l111_opy_ = TestFramework.bstack1llllllllll_opy_(t, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1l1l111_opy_):
                return t
    def bstack1l1ll11l1l1_opy_(self, message):
        self.bstack1l1lll1l1l1_opy_(message + bstack1l11ll1_opy_ (u"ࠨ࡜࡯ࠤኺ"))
    def log_error(self, message):
        self.bstack1l1l1llll1l_opy_(message + bstack1l11ll1_opy_ (u"ࠢ࡝ࡰࠥኻ"))
    def bstack1l1l1ll11l1_opy_(self, level, original_func):
        def bstack1l1l1ll1111_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstack1l11ll1_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤኼ") in message or bstack1l11ll1_opy_ (u"ࠤ࡞ࡗࡉࡑࡃࡍࡋࡠࠦኽ") in message or bstack1l11ll1_opy_ (u"ࠥ࡟࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࡍࡰࡦࡸࡰࡪࡣࠢኾ") in message:
                return return_value
            bstack1l1lll1111l_opy_ = TestFramework.bstack1l1lll1ll11_opy_()
            if not bstack1l1lll1111l_opy_:
                return return_value
            bstack1l1lll11lll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1lll1111l_opy_
                    if TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
                ),
                None,
            )
            if not bstack1l1lll11lll_opy_:
                return return_value
            entry = bstack1ll1lll1l11_opy_(TestFramework.bstack1l1ll1l1l1l_opy_, message, level)
            self.bstack1l1l1ll1ll1_opy_(bstack1l1lll11lll_opy_, [entry])
            return return_value
        return bstack1l1l1ll1111_opy_
    def bstack1l1l1l1ll11_opy_(self):
        def bstack1l1lll111ll_opy_(*args, **kwargs):
            try:
                self.bstack1l1ll1lll1l_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l11ll1_opy_ (u"ࠫࠥ࠭኿").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l11ll1_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨዀ") in message:
                    return
                bstack1l1lll1111l_opy_ = TestFramework.bstack1l1lll1ll11_opy_()
                if not bstack1l1lll1111l_opy_:
                    return
                bstack1l1lll11lll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l1lll1111l_opy_
                        if TestFramework.bstack1lllll11l11_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
                    ),
                    None,
                )
                if not bstack1l1lll11lll_opy_:
                    return
                entry = bstack1ll1lll1l11_opy_(TestFramework.bstack1l1ll1l1l1l_opy_, message, bstack1ll1ll1l111_opy_.bstack1l1lll11l11_opy_)
                self.bstack1l1l1ll1ll1_opy_(bstack1l1lll11lll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1ll1lll1l_opy_(bstack1llll111ll1_opy_ (u"ࠨ࡛ࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠢࡏࡳ࡬ࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦ዁"))
                except:
                    pass
        return bstack1l1lll111ll_opy_
    def bstack1l1ll1l1lll_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1111ll_opy_
        levels = [bstack1l11ll1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥዂ"), bstack1l11ll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧዃ")]
        bstack1l1l1lll1l1_opy_ = bstack1l11ll1_opy_ (u"ࠤࠥዄ")
        if instance is not None:
            try:
                bstack1l1l1lll1l1_opy_ = TestFramework.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
            except Exception as e:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡺ࡯ࡤࠡࡨࡵࡳࡲࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣዅ").format(e))
        bstack1l1l1lll111_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l11ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ዆")]
                bstack1l1ll11ll11_opy_ = os.path.join(bstack1l1lll1lll1_opy_, (bstack1l1ll1l11ll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll11ll11_opy_):
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡰࡲࡸࠥࡶࡲࡦࡵࡨࡲࡹࠦࡦࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡕࡧࡶࡸࠥࡧ࡮ࡥࠢࡅࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣ዇").format(bstack1l1ll11ll11_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll11ll11_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll11ll11_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1111ll_opy_:
                        self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦወ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l1llllll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l1llllll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l11ll1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥዉ"):
                                entry = bstack1ll1lll1l11_opy_(
                                    kind=bstack1l11ll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥዊ"),
                                    message=bstack1l11ll1_opy_ (u"ࠤࠥዋ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1l111l_opy_=file_size,
                                    bstack1l1ll1l1l11_opy_=bstack1l11ll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥዌ"),
                                    bstack111l111_opy_=os.path.abspath(file_path),
                                    bstack111ll11l_opy_=bstack1l1l1lll1l1_opy_
                                )
                            elif level == bstack1l11ll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣው"):
                                entry = bstack1ll1lll1l11_opy_(
                                    kind=bstack1l11ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢዎ"),
                                    message=bstack1l11ll1_opy_ (u"ࠨࠢዏ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1l111l_opy_=file_size,
                                    bstack1l1ll1l1l11_opy_=bstack1l11ll1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢዐ"),
                                    bstack111l111_opy_=os.path.abspath(file_path),
                                    bstack1l1l1ll1l1l_opy_=bstack1l1l1lll1l1_opy_
                                )
                            bstack1l1l1lll111_opy_.append(entry)
                            _1l1ll1111ll_opy_.add(abs_path)
                        except Exception as bstack1l1ll1l1111_opy_:
                            self.logger.error(bstack1l11ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢዑ").format(bstack1l1ll1l1111_opy_))
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣዒ").format(e))
        event[bstack1l11ll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣዓ")] = bstack1l1l1lll111_opy_
class bstack1l1ll111l11_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1lll1l11l_opy_ = set()
        kwargs[bstack1l11ll1_opy_ (u"ࠦࡸࡱࡩࡱ࡭ࡨࡽࡸࠨዔ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l1llll11_opy_(obj, self.bstack1l1lll1l11l_opy_)
def bstack1l1ll1llll1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l1llll11_opy_(obj, bstack1l1lll1l11l_opy_=None, max_depth=3):
    if bstack1l1lll1l11l_opy_ is None:
        bstack1l1lll1l11l_opy_ = set()
    if id(obj) in bstack1l1lll1l11l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1lll1l11l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1ll11111l_opy_ = TestFramework.bstack1l1ll111ll1_opy_(obj)
    bstack1l1ll1l1ll1_opy_ = next((k.lower() in bstack1l1ll11111l_opy_.lower() for k in bstack1l1l1l1lll1_opy_.keys()), None)
    if bstack1l1ll1l1ll1_opy_:
        obj = TestFramework.bstack1l1ll111111_opy_(obj, bstack1l1l1l1lll1_opy_[bstack1l1ll1l1ll1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l11ll1_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣዕ")):
            keys = getattr(obj, bstack1l11ll1_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤዖ"), [])
        elif hasattr(obj, bstack1l11ll1_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤ዗")):
            keys = getattr(obj, bstack1l11ll1_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥዘ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l11ll1_opy_ (u"ࠤࡢࠦዙ"))}
        if not obj and bstack1l1ll11111l_opy_ == bstack1l11ll1_opy_ (u"ࠥࡴࡦࡺࡨ࡭࡫ࡥ࠲ࡕࡵࡳࡪࡺࡓࡥࡹ࡮ࠢዚ"):
            obj = {bstack1l11ll1_opy_ (u"ࠦࡵࡧࡴࡩࠤዛ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll1llll1_opy_(key) or str(key).startswith(bstack1l11ll1_opy_ (u"ࠧࡥࠢዜ")):
            continue
        if value is not None and bstack1l1ll1llll1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l1llll11_opy_(value, bstack1l1lll1l11l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l1llll11_opy_(o, bstack1l1lll1l11l_opy_, max_depth) for o in value]))
    return result or None