# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import bstack1lllll1ll1l_opy_, bstack1lllllll11l_opy_, bstack1llllll1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1ll1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1lll_opy_, bstack1lll1lllll1_opy_, bstack1lll111llll_opy_, bstack1ll1lll1l11_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll11llll_opy_, bstack1l1lll11111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1lll1lll1_opy_ = [bstack111l111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦቑ"), bstack111l111_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢቒ"), bstack111l111_opy_ (u"ࠣࡥࡲࡲ࡫࡯ࡧࠣቓ"), bstack111l111_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࠥቔ"), bstack111l111_opy_ (u"ࠥࡴࡦࡺࡨࠣቕ")]
bstack1l1ll1ll111_opy_ = bstack1l1lll11111_opy_()
bstack1l1ll11l11l_opy_ = bstack111l111_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࠦቖ")
bstack1l1lll1l11l_opy_ = {
    bstack111l111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡏࡴࡦ࡯ࠥ቗"): bstack1l1lll1lll1_opy_,
    bstack111l111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡐࡢࡥ࡮ࡥ࡬࡫ࠢቘ"): bstack1l1lll1lll1_opy_,
    bstack111l111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡎࡱࡧࡹࡱ࡫ࠢ቙"): bstack1l1lll1lll1_opy_,
    bstack111l111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡅ࡯ࡥࡸࡹࠢቚ"): bstack1l1lll1lll1_opy_,
    bstack111l111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡉࡹࡳࡩࡴࡪࡱࡱࠦቛ"): bstack1l1lll1lll1_opy_
    + [
        bstack111l111_opy_ (u"ࠥࡳࡷ࡯ࡧࡪࡰࡤࡰࡳࡧ࡭ࡦࠤቜ"),
        bstack111l111_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨቝ"),
        bstack111l111_opy_ (u"ࠧ࡬ࡩࡹࡶࡸࡶࡪ࡯࡮ࡧࡱࠥ቞"),
        bstack111l111_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣ቟"),
        bstack111l111_opy_ (u"ࠢࡤࡣ࡯ࡰࡸࡶࡥࡤࠤበ"),
        bstack111l111_opy_ (u"ࠣࡥࡤࡰࡱࡵࡢ࡫ࠤቡ"),
        bstack111l111_opy_ (u"ࠤࡶࡸࡦࡸࡴࠣቢ"),
        bstack111l111_opy_ (u"ࠥࡷࡹࡵࡰࠣባ"),
        bstack111l111_opy_ (u"ࠦࡩࡻࡲࡢࡶ࡬ࡳࡳࠨቤ"),
        bstack111l111_opy_ (u"ࠧࡽࡨࡦࡰࠥብ"),
    ],
    bstack111l111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢ࡫ࡱ࠲ࡘ࡫ࡳࡴ࡫ࡲࡲࠧቦ"): [bstack111l111_opy_ (u"ࠢࡴࡶࡤࡶࡹࡶࡡࡵࡪࠥቧ"), bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡹࡦࡢ࡫࡯ࡩࡩࠨቨ"), bstack111l111_opy_ (u"ࠤࡷࡩࡸࡺࡳࡤࡱ࡯ࡰࡪࡩࡴࡦࡦࠥቩ"), bstack111l111_opy_ (u"ࠥ࡭ࡹ࡫࡭ࡴࠤቪ")],
    bstack111l111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡨࡵ࡮ࡧ࡫ࡪ࠲ࡈࡵ࡮ࡧ࡫ࡪࠦቫ"): [bstack111l111_opy_ (u"ࠧ࡯࡮ࡷࡱࡦࡥࡹ࡯࡯࡯ࡡࡳࡥࡷࡧ࡭ࡴࠤቬ"), bstack111l111_opy_ (u"ࠨࡡࡳࡩࡶࠦቭ")],
    bstack111l111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡉ࡭ࡽࡺࡵࡳࡧࡇࡩ࡫ࠨቮ"): [bstack111l111_opy_ (u"ࠣࡵࡦࡳࡵ࡫ࠢቯ"), bstack111l111_opy_ (u"ࠤࡤࡶ࡬ࡴࡡ࡮ࡧࠥተ"), bstack111l111_opy_ (u"ࠥࡪࡺࡴࡣࠣቱ"), bstack111l111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡶࠦቲ"), bstack111l111_opy_ (u"ࠧࡻ࡮ࡪࡶࡷࡩࡸࡺࠢታ"), bstack111l111_opy_ (u"ࠨࡩࡥࡵࠥቴ")],
    bstack111l111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡧ࡫ࡻࡸࡺࡸࡥࡴ࠰ࡖࡹࡧࡘࡥࡲࡷࡨࡷࡹࠨት"): [bstack111l111_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦࡰࡤࡱࡪࠨቶ"), bstack111l111_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࠣቷ"), bstack111l111_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡡ࡬ࡲࡩ࡫ࡸࠣቸ")],
    bstack111l111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡷࡻ࡮࡯ࡧࡵ࠲ࡈࡧ࡬࡭ࡋࡱࡪࡴࠨቹ"): [bstack111l111_opy_ (u"ࠧࡽࡨࡦࡰࠥቺ"), bstack111l111_opy_ (u"ࠨࡲࡦࡵࡸࡰࡹࠨቻ")],
    bstack111l111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣࡵ࡯࠳ࡹࡴࡳࡷࡦࡸࡺࡸࡥࡴ࠰ࡑࡳࡩ࡫ࡋࡦࡻࡺࡳࡷࡪࡳࠣቼ"): [bstack111l111_opy_ (u"ࠣࡰࡲࡨࡪࠨች"), bstack111l111_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤቾ")],
    bstack111l111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡓࡡࡳ࡭ࠥቿ"): [bstack111l111_opy_ (u"ࠦࡳࡧ࡭ࡦࠤኀ"), bstack111l111_opy_ (u"ࠧࡧࡲࡨࡵࠥኁ"), bstack111l111_opy_ (u"ࠨ࡫ࡸࡣࡵ࡫ࡸࠨኂ")],
}
_1l1ll1l1111_opy_ = set()
class bstack1lll111l11l_opy_(bstack1llll1l1l11_opy_):
    bstack1l1l1lll1l1_opy_ = bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡪࡥࡧࡧࡵࡶࡪࡪࠢኃ")
    bstack1l1ll1l1l1l_opy_ = bstack111l111_opy_ (u"ࠣࡋࡑࡊࡔࠨኄ")
    bstack1l1l1lllll1_opy_ = bstack111l111_opy_ (u"ࠤࡈࡖࡗࡕࡒࠣኅ")
    bstack1l1lll1l1l1_opy_: Callable
    bstack1l1l1llll1l_opy_: Callable
    def __init__(self, bstack1lll1l1ll1l_opy_, bstack1ll1ll1ll11_opy_):
        super().__init__()
        self.bstack1ll11ll11ll_opy_ = bstack1ll1ll1ll11_opy_
        if os.getenv(bstack111l111_opy_ (u"ࠥࡗࡉࡑ࡟ࡄࡎࡌࡣࡋࡒࡁࡈࡡࡒ࠵࠶࡟ࠢኆ"), bstack111l111_opy_ (u"ࠦ࠶ࠨኇ")) != bstack111l111_opy_ (u"ࠧ࠷ࠢኈ") or not self.is_enabled():
            self.logger.warning(bstack111l111_opy_ (u"ࠨࠢ኉") + str(self.__class__.__name__) + bstack111l111_opy_ (u"ࠢࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦࠥኊ"))
            return
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), self.bstack1ll111lll11_opy_)
        for event in bstack1ll1lll1lll_opy_:
            for state in bstack1lll111llll_opy_:
                TestFramework.bstack1ll11l1l11l_opy_((event, state), self.bstack1l1lll1111l_opy_)
        bstack1lll1l1ll1l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.POST), self.bstack1l1l1lll111_opy_)
        self.bstack1l1lll1l1l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1lll1llll_opy_(bstack1lll111l11l_opy_.bstack1l1ll1l1l1l_opy_, self.bstack1l1lll1l1l1_opy_)
        self.bstack1l1l1llll1l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1lll1llll_opy_(bstack1lll111l11l_opy_.bstack1l1l1lllll1_opy_, self.bstack1l1l1llll1l_opy_)
        self.bstack1l1ll1l1l11_opy_ = builtins.print
        builtins.print = self.bstack1l1ll1llll1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1lll1ll11_opy_() and instance:
            bstack1l1lll11lll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llllll111l_opy_
            if test_framework_state == bstack1ll1lll1lll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1lll1lll_opy_.LOG:
                bstack1l1111lll_opy_ = datetime.now()
                entries = f.bstack1l1ll1ll11l_opy_(instance, bstack1llllll111l_opy_)
                if entries:
                    self.bstack1l1l1ll1l11_opy_(instance, entries)
                    instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࠣኋ"), datetime.now() - bstack1l1111lll_opy_)
                    f.bstack1l1lll1ll1l_opy_(instance, bstack1llllll111l_opy_)
                instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧኌ"), datetime.now() - bstack1l1lll11lll_opy_)
                return # bstack1l1l1ll1lll_opy_ not send this event with the bstack1l1l1ll11l1_opy_ bstack1l1lll11l11_opy_
            elif (
                test_framework_state == bstack1ll1lll1lll_opy_.TEST
                and test_hook_state == bstack1lll111llll_opy_.POST
                and not f.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1ll11ll11_opy_)
            ):
                self.logger.warning(bstack111l111_opy_ (u"ࠥࡨࡷࡵࡰࡱ࡫ࡱ࡫ࠥࡪࡵࡦࠢࡷࡳࠥࡲࡡࡤ࡭ࠣࡳ࡫ࠦࡲࡦࡵࡸࡰࡹࡹࠠࠣኍ") + str(TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1ll11ll11_opy_)) + bstack111l111_opy_ (u"ࠦࠧ኎"))
                f.bstack1111111111_opy_(instance, bstack1lll111l11l_opy_.bstack1l1l1lll1l1_opy_, True)
                return # bstack1l1l1ll1lll_opy_ not send this event bstack1l1llll11l1_opy_ bstack1l1ll1lllll_opy_
            elif (
                f.bstack1111111l1l_opy_(instance, bstack1lll111l11l_opy_.bstack1l1l1lll1l1_opy_, False)
                and test_framework_state == bstack1ll1lll1lll_opy_.LOG_REPORT
                and test_hook_state == bstack1lll111llll_opy_.POST
                and f.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1ll11ll11_opy_)
            ):
                self.logger.warning(bstack111l111_opy_ (u"ࠧ࡯࡮࡫ࡧࡦࡸ࡮ࡴࡧࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡔࡶࡤࡸࡪ࠴ࡔࡆࡕࡗ࠰࡚ࠥࡥࡴࡶࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࡖࡏࡔࡖࠣࠦ኏") + str(TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1l1ll11ll11_opy_)) + bstack111l111_opy_ (u"ࠨࠢነ"))
                self.bstack1l1lll1111l_opy_(f, instance, (bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), *args, **kwargs)
            bstack1l1111lll_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l1llllll_opy_ = sorted(
                filter(lambda x: x.get(bstack111l111_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥኑ"), None), data.pop(bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣኒ"), {}).values()),
                key=lambda x: x[bstack111l111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧና")],
            )
            if bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_ in data:
                data.pop(bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_)
            data.update({bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥኔ"): bstack1l1l1llllll_opy_})
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠦ࡯ࡹ࡯࡯࠼ࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤን"), datetime.now() - bstack1l1111lll_opy_)
            bstack1l1111lll_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1ll1l11l1_opy_)
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣኖ"), datetime.now() - bstack1l1111lll_opy_)
            self.bstack1l1lll11l11_opy_(instance, bstack1llllll111l_opy_, event_json=event_json)
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤኗ"), datetime.now() - bstack1l1lll11lll_opy_)
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
        bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack11l1l11ll_opy_.value)
        self.bstack1ll11ll11ll_opy_.bstack1l1lll1l1ll_opy_(instance, f, bstack1llllll111l_opy_, *args, **kwargs)
        bstack1llll1111l1_opy_.end(EVENTS.bstack11l1l11ll_opy_.value, bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢኘ"), bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨኙ"), status=True, failure=None, test_name=None)
    def bstack1ll111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll11ll11ll_opy_.bstack1l1ll111111_opy_(instance, f, bstack1llllll111l_opy_, *args, **kwargs)
        self.bstack1l1ll111l1l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1lll11ll1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l1ll111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡖ࡯࡮ࡶࡰࡪࡰࡪࠤ࡙࡫ࡳࡵࡕࡨࡷࡸ࡯࡯࡯ࡇࡹࡩࡳࡺࠠࡨࡔࡓࡇࠥࡩࡡ࡭࡮࠽ࠤࡓࡵࠠࡷࡣ࡯࡭ࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡥࡣࡷࡥࠧኚ"))
            return
        bstack1l1111lll_opy_ = datetime.now()
        try:
            r = self.bstack1lll1l11l1l_opy_.TestSessionEvent(req)
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡤ࡫ࡶࡦࡰࡷࠦኛ"), datetime.now() - bstack1l1111lll_opy_)
            f.bstack1111111111_opy_(instance, self.bstack1ll11ll11ll_opy_.bstack1l1l1llll11_opy_, r.success)
            if not r.success:
                self.logger.info(bstack111l111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨኜ") + str(r) + bstack111l111_opy_ (u"ࠧࠨኝ"))
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦኞ") + str(e) + bstack111l111_opy_ (u"ࠢࠣኟ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1lll111_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        _driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        _1l1llll11ll_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1l11l11_opy_.bstack1ll11l1111l_opy_(method_name):
            return
        if f.bstack1ll11llllll_opy_(*args) == bstack1lll1l11l11_opy_.bstack1l1ll11ll1l_opy_:
            bstack1l1lll11lll_opy_ = datetime.now()
            screenshot = result.get(bstack111l111_opy_ (u"ࠣࡸࡤࡰࡺ࡫ࠢአ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack111l111_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡪ࡯ࡤ࡫ࡪࠦࡢࡢࡵࡨ࠺࠹ࠦࡳࡵࡴࠥኡ"))
                return
            bstack1l1lll111ll_opy_ = self.bstack1l1ll11111l_opy_(instance)
            if bstack1l1lll111ll_opy_:
                entry = bstack1ll1lll1l11_opy_(TestFramework.bstack1l1ll1l111l_opy_, screenshot)
                self.bstack1l1l1ll1l11_opy_(bstack1l1lll111ll_opy_, [entry])
                instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡩࡽ࡫ࡣࡶࡶࡨࠦኢ"), datetime.now() - bstack1l1lll11lll_opy_)
            else:
                self.logger.warning(bstack111l111_opy_ (u"ࠦࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡸࡪࡹࡴࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹ࡮ࡩࡴࠢࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠦࡷࡢࡵࠣࡸࡦࡱࡥ࡯ࠢࡥࡽࠥࡪࡲࡪࡸࡨࡶࡂࠦࡻࡾࠤኣ").format(instance.ref()))
        event = {}
        bstack1l1lll111ll_opy_ = self.bstack1l1ll11111l_opy_(instance)
        if bstack1l1lll111ll_opy_:
            self.bstack1l1l1l1llll_opy_(event, bstack1l1lll111ll_opy_)
            if event.get(bstack111l111_opy_ (u"ࠧࡲ࡯ࡨࡵࠥኤ")):
                self.bstack1l1l1ll1l11_opy_(bstack1l1lll111ll_opy_, event[bstack111l111_opy_ (u"ࠨ࡬ࡰࡩࡶࠦእ")])
            else:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦ࡬ࡰࡩࡶࠤ࡫ࡵࡲࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥ࡫ࡶࡦࡰࡷࠦኦ"))
    @measure(event_name=EVENTS.bstack1l1ll111l11_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l1l1ll1l11_opy_(
        self,
        bstack1l1lll111ll_opy_: bstack1lll1lllll1_opy_,
        entries: List[bstack1ll1lll1l11_opy_],
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll11l1lll1_opy_)
        req.execution_context.hash = str(bstack1l1lll111ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lll111ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lll111ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll111ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1l1ll1ll1_opy_)
            log_entry.uuid = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1ll11l11l1l_opy_)
            log_entry.test_framework_state = bstack1l1lll111ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack111l111_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢኧ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111l111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦከ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll111lll_opy_
                log_entry.file_path = entry.bstack11l111_opy_
        def bstack1l1l1lll1ll_opy_():
            bstack1l1111lll_opy_ = datetime.now()
            try:
                self.bstack1lll1l11l1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll1l111l_opy_:
                    bstack1l1lll111ll_opy_.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠢኩ"), datetime.now() - bstack1l1111lll_opy_)
                elif entry.kind == TestFramework.bstack1l1l1ll111l_opy_:
                    bstack1l1lll111ll_opy_.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠣኪ"), datetime.now() - bstack1l1111lll_opy_)
                else:
                    bstack1l1lll111ll_opy_.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡲ࡯ࡨࠤካ"), datetime.now() - bstack1l1111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦኬ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111lll_opy_.enqueue(bstack1l1l1lll1ll_opy_)
    @measure(event_name=EVENTS.bstack1l1lll111l1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1l1lll11l11_opy_(
        self,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        event_json=None,
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_)
        req.test_framework_name = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_)
        req.test_framework_state = bstack1llllll111l_opy_[0].name
        req.test_hook_state = bstack1llllll111l_opy_[1].name
        started_at = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1l1l1lll1_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1ll1l11l1_opy_)).encode(bstack111l111_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨክ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1l1lll1ll_opy_():
            bstack1l1111lll_opy_ = datetime.now()
            try:
                self.bstack1lll1l11l1l_opy_.TestFrameworkEvent(req)
                instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦኮ"), datetime.now() - bstack1l1111lll_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111l111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢኯ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1111111lll_opy_.enqueue(bstack1l1l1lll1ll_opy_)
    def bstack1l1ll11111l_opy_(self, instance: bstack1lllll1ll1l_opy_):
        bstack1l1ll1ll1ll_opy_ = TestFramework.bstack11111111l1_opy_(instance.context)
        for t in bstack1l1ll1ll1ll_opy_:
            bstack1l1ll1lll11_opy_ = TestFramework.bstack1111111l1l_opy_(t, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll1lll11_opy_):
                return t
    def bstack1l1l1ll1l1l_opy_(self, message):
        self.bstack1l1lll1l1l1_opy_(message + bstack111l111_opy_ (u"ࠥࡠࡳࠨኰ"))
    def log_error(self, message):
        self.bstack1l1l1llll1l_opy_(message + bstack111l111_opy_ (u"ࠦࡡࡴࠢ኱"))
    def bstack1l1lll1llll_opy_(self, level, original_func):
        def bstack1l1ll1111ll_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            if bstack111l111_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨኲ") in message or bstack111l111_opy_ (u"ࠨ࡛ࡔࡆࡎࡇࡑࡏ࡝ࠣኳ") in message or bstack111l111_opy_ (u"ࠢ࡜࡙ࡨࡦࡉࡸࡩࡷࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠦኴ") in message:
                return return_value
            bstack1l1ll1ll1ll_opy_ = TestFramework.bstack1l1ll11l111_opy_()
            if not bstack1l1ll1ll1ll_opy_:
                return return_value
            bstack1l1lll111ll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1ll1ll_opy_
                    if TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
                ),
                None,
            )
            if not bstack1l1lll111ll_opy_:
                return return_value
            entry = bstack1ll1lll1l11_opy_(TestFramework.bstack1l1ll11lll1_opy_, message, level)
            self.bstack1l1l1ll1l11_opy_(bstack1l1lll111ll_opy_, [entry])
            return return_value
        return bstack1l1ll1111ll_opy_
    def bstack1l1ll1llll1_opy_(self):
        def bstack1l1l1lll11l_opy_(*args, **kwargs):
            self.bstack1l1ll1l1l11_opy_(*args, **kwargs)
            message = bstack111l111_opy_ (u"ࠨࠢࠪኵ").join(str(arg) for arg in args)
            if not message.strip():
                return
            if bstack111l111_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥ኶") in message:
                return
            bstack1l1ll1ll1ll_opy_ = TestFramework.bstack1l1ll11l111_opy_()
            if not bstack1l1ll1ll1ll_opy_:
                return
            bstack1l1lll111ll_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1ll1ll_opy_
                    if TestFramework.bstack1lllll1l111_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
                ),
                None,
            )
            if not bstack1l1lll111ll_opy_:
                return
            entry = bstack1ll1lll1l11_opy_(TestFramework.bstack1l1ll11lll1_opy_, message, bstack1lll111l11l_opy_.bstack1l1ll1l1l1l_opy_)
            self.bstack1l1l1ll1l11_opy_(bstack1l1lll111ll_opy_, [entry])
        return bstack1l1l1lll11l_opy_
    def bstack1l1l1l1llll_opy_(self, event: dict, instance=None) -> None:
        global _1l1ll1l1111_opy_
        levels = [bstack111l111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨ኷"), bstack111l111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣኸ")]
        bstack1l1ll1l1ll1_opy_ = bstack111l111_opy_ (u"ࠧࠨኹ")
        if instance is not None:
            try:
                bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
            except Exception as e:
                self.logger.warning(bstack111l111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡵࡶ࡫ࡧࠤ࡫ࡸ࡯࡮ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠦኺ").format(e))
        bstack1l1l1ll11ll_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧኻ")]
                bstack1l1ll111ll1_opy_ = os.path.join(bstack1l1ll1ll111_opy_, (bstack1l1ll11l11l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1ll111ll1_opy_):
                    self.logger.debug(bstack111l111_opy_ (u"ࠣࡆ࡬ࡶࡪࡩࡴࡰࡴࡼࠤࡳࡵࡴࠡࡲࡵࡩࡸ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡘࡪࡹࡴࠡࡣࡱࡨࠥࡈࡵࡪ࡮ࡧࠤࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦኼ").format(bstack1l1ll111ll1_opy_))
                    continue
                file_names = os.listdir(bstack1l1ll111ll1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1ll111ll1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1ll1l1111_opy_:
                        self.logger.info(bstack111l111_opy_ (u"ࠤࡓࡥࡹ࡮ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤࢀࢃࠢኽ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll1111l1_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll1111l1_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack111l111_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨኾ"):
                                entry = bstack1ll1lll1l11_opy_(
                                    kind=bstack111l111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨ኿"),
                                    message=bstack111l111_opy_ (u"ࠧࠨዀ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll111lll_opy_=file_size,
                                    bstack1l1ll1l1lll_opy_=bstack111l111_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨ዁"),
                                    bstack11l111_opy_=os.path.abspath(file_path),
                                    bstack1l111111l1_opy_=bstack1l1ll1l1ll1_opy_
                                )
                            elif level == bstack111l111_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦዂ"):
                                entry = bstack1ll1lll1l11_opy_(
                                    kind=bstack111l111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥዃ"),
                                    message=bstack111l111_opy_ (u"ࠤࠥዄ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll111lll_opy_=file_size,
                                    bstack1l1ll1l1lll_opy_=bstack111l111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥዅ"),
                                    bstack11l111_opy_=os.path.abspath(file_path),
                                    bstack1l1ll1l11ll_opy_=bstack1l1ll1l1ll1_opy_
                                )
                            bstack1l1l1ll11ll_opy_.append(entry)
                            _1l1ll1l1111_opy_.add(abs_path)
                        except Exception as bstack1l1ll11l1ll_opy_:
                            self.logger.error(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥ዆").format(bstack1l1ll11l1ll_opy_))
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦ዇").format(e))
        event[bstack111l111_opy_ (u"ࠨ࡬ࡰࡩࡶࠦወ")] = bstack1l1l1ll11ll_opy_
class bstack1l1ll1l11l1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1l1l1ll1l_opy_ = set()
        kwargs[bstack111l111_opy_ (u"ࠢࡴ࡭࡬ࡴࡰ࡫ࡹࡴࠤዉ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1llll1111_opy_(obj, self.bstack1l1l1l1ll1l_opy_)
def bstack1l1ll1lll1l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1llll1111_opy_(obj, bstack1l1l1l1ll1l_opy_=None, max_depth=3):
    if bstack1l1l1l1ll1l_opy_ is None:
        bstack1l1l1l1ll1l_opy_ = set()
    if id(obj) in bstack1l1l1l1ll1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1l1l1ll1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1lll11l1l_opy_ = TestFramework.bstack1l1lll1l111_opy_(obj)
    bstack1l1l1ll1111_opy_ = next((k.lower() in bstack1l1lll11l1l_opy_.lower() for k in bstack1l1lll1l11l_opy_.keys()), None)
    if bstack1l1l1ll1111_opy_:
        obj = TestFramework.bstack1l1ll11l1l1_opy_(obj, bstack1l1lll1l11l_opy_[bstack1l1l1ll1111_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack111l111_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦዊ")):
            keys = getattr(obj, bstack111l111_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧዋ"), [])
        elif hasattr(obj, bstack111l111_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧዌ")):
            keys = getattr(obj, bstack111l111_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨው"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack111l111_opy_ (u"ࠧࡥࠢዎ"))}
        if not obj and bstack1l1lll11l1l_opy_ == bstack111l111_opy_ (u"ࠨࡰࡢࡶ࡫ࡰ࡮ࡨ࠮ࡑࡱࡶ࡭ࡽࡖࡡࡵࡪࠥዏ"):
            obj = {bstack111l111_opy_ (u"ࠢࡱࡣࡷ࡬ࠧዐ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll1lll1l_opy_(key) or str(key).startswith(bstack111l111_opy_ (u"ࠣࡡࠥዑ")):
            continue
        if value is not None and bstack1l1ll1lll1l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1llll1111_opy_(value, bstack1l1l1l1ll1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1llll1111_opy_(o, bstack1l1l1l1ll1l_opy_, max_depth) for o in value]))
    return result or None