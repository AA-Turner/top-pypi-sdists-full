# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack1lll1llll11_opy_, bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack111111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lllll111ll_opy_, bstack1lll1lll1ll_opy_, bstack1llll11ll1l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1llll1ll1l1_opy_, bstack1lllllll1l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1llllll11l1_opy_ = [bstack11l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨႌ"), bstack11l1111_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤႍ"), bstack11l1111_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥႎ"), bstack11l1111_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧႏ"), bstack11l1111_opy_ (u"ࠧࡶࡡࡵࡪࠥ႐")]
bstack1lllllll111_opy_ = bstack1lllllll1l1_opy_()
bstack1111111lll_opy_ = bstack11l1111_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨ႑")
bstack111111l11l_opy_ = {
    bstack11l1111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡊࡶࡨࡱࠧ႒"): bstack1llllll11l1_opy_,
    bstack11l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡒࡤࡧࡰࡧࡧࡦࠤ႓"): bstack1llllll11l1_opy_,
    bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡐࡳࡩࡻ࡬ࡦࠤ႔"): bstack1llllll11l1_opy_,
    bstack11l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡇࡱࡧࡳࡴࠤ႕"): bstack1llllll11l1_opy_,
    bstack11l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡋࡻ࡮ࡤࡶ࡬ࡳࡳࠨ႖"): bstack1llllll11l1_opy_
    + [
        bstack11l1111_opy_ (u"ࠧࡵࡲࡪࡩ࡬ࡲࡦࡲ࡮ࡢ࡯ࡨࠦ႗"),
        bstack11l1111_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣ႘"),
        bstack11l1111_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࡪࡰࡩࡳࠧ႙"),
        bstack11l1111_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥႚ"),
        bstack11l1111_opy_ (u"ࠤࡦࡥࡱࡲࡳࡱࡧࡦࠦႛ"),
        bstack11l1111_opy_ (u"ࠥࡧࡦࡲ࡬ࡰࡤ࡭ࠦႜ"),
        bstack11l1111_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥႝ"),
        bstack11l1111_opy_ (u"ࠧࡹࡴࡰࡲࠥ႞"),
        bstack11l1111_opy_ (u"ࠨࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠣ႟"),
        bstack11l1111_opy_ (u"ࠢࡸࡪࡨࡲࠧႠ"),
    ],
    bstack11l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤ࡭ࡳ࠴ࡓࡦࡵࡶ࡭ࡴࡴࠢႡ"): [bstack11l1111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡱࡣࡷ࡬ࠧႢ"), bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡴࡨࡤ࡭ࡱ࡫ࡤࠣႣ"), bstack11l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧႤ"), bstack11l1111_opy_ (u"ࠧ࡯ࡴࡦ࡯ࡶࠦႥ")],
    bstack11l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡣࡰࡰࡩ࡭࡬࠴ࡃࡰࡰࡩ࡭࡬ࠨႦ"): [bstack11l1111_opy_ (u"ࠢࡪࡰࡹࡳࡨࡧࡴࡪࡱࡱࡣࡵࡧࡲࡢ࡯ࡶࠦႧ"), bstack11l1111_opy_ (u"ࠣࡣࡵ࡫ࡸࠨႨ")],
    bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡋ࡯ࡸࡵࡷࡵࡩࡉ࡫ࡦࠣႩ"): [bstack11l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤႪ"), bstack11l1111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧႫ"), bstack11l1111_opy_ (u"ࠧ࡬ࡵ࡯ࡥࠥႬ"), bstack11l1111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨႭ"), bstack11l1111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤႮ"), bstack11l1111_opy_ (u"ࠣ࡫ࡧࡷࠧႯ")],
    bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡘࡻࡢࡓࡧࡴࡹࡪࡹࡴࠣႰ"): [bstack11l1111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣႱ"), bstack11l1111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࠥႲ"), bstack11l1111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡣ࡮ࡴࡤࡦࡺࠥႳ")],
    bstack11l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡲࡶࡰࡱࡩࡷ࠴ࡃࡢ࡮࡯ࡍࡳ࡬࡯ࠣႴ"): [bstack11l1111_opy_ (u"ࠢࡸࡪࡨࡲࠧႵ"), bstack11l1111_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࠣႶ")],
    bstack11l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡓࡵࡤࡦࡍࡨࡽࡼࡵࡲࡥࡵࠥႷ"): [bstack11l1111_opy_ (u"ࠥࡲࡴࡪࡥࠣႸ"), bstack11l1111_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦႹ")],
    bstack11l1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡎࡣࡵ࡯ࠧႺ"): [bstack11l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦႻ"), bstack11l1111_opy_ (u"ࠢࡢࡴࡪࡷࠧႼ"), bstack11l1111_opy_ (u"ࠣ࡭ࡺࡥࡷ࡭ࡳࠣႽ")],
}
_1llll11lll1_opy_ = set()
class bstack1llll1111ll_opy_(bstack1lll1lllll1_opy_):
    bstack111111111l_opy_ = bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࠤႾ")
    bstack1llll1lll1l_opy_ = bstack11l1111_opy_ (u"ࠥࡍࡓࡌࡏࠣႿ")
    bstack1llll1l1ll1_opy_ = bstack11l1111_opy_ (u"ࠦࡊࡘࡒࡐࡔࠥჀ")
    bstack1llll1llll1_opy_: Callable
    bstack1lll1l11lll_opy_: Callable
    def __init__(self, bstack1llll1l111l_opy_, bstack1llll1ll11l_opy_):
        super().__init__()
        self.bstack1lll1l111ll_opy_ = bstack1llll1ll11l_opy_
        if os.getenv(bstack11l1111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡔ࠷࠱࡚ࠤჁ"), bstack11l1111_opy_ (u"ࠨ࠱ࠣჂ")) != bstack11l1111_opy_ (u"ࠢ࠲ࠤჃ") or not self.is_enabled():
            self.logger.warning(bstack11l1111_opy_ (u"ࠣࠤჄ") + str(self.__class__.__name__) + bstack11l1111_opy_ (u"ࠤࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠧჅ"))
            return
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.PRE), self.bstack1lllll1lll1_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), self.bstack1lllll11l1l_opy_)
        for event in bstack1lllll11l11_opy_:
            for state in bstack1lll1lll1ll_opy_:
                TestFramework.bstack1lllll1llll_opy_((event, state), self.bstack1llllll1l11_opy_)
        bstack1llll1l111l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.POST), self.bstack1lll1l1l1ll_opy_)
        self.bstack1llll1llll1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1lllll111l1_opy_(bstack1llll1111ll_opy_.bstack1llll1lll1l_opy_, self.bstack1llll1llll1_opy_)
        self.bstack1lll1l11lll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1lllll111l1_opy_(bstack1llll1111ll_opy_.bstack1llll1l1ll1_opy_, self.bstack1lll1l11lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1llllll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1lllllll1ll_opy_() and instance:
            bstack1lllll1l1l1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1llll11l111_opy_
            if test_framework_state == bstack1lllll11l11_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lllll11l11_opy_.LOG:
                bstack1ll1l1l1_opy_ = datetime.now()
                entries = f.bstack1llll11ll11_opy_(instance, bstack1llll11l111_opy_)
                if entries:
                    self.bstack1lll1ll111l_opy_(instance, entries)
                    instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥ჆"), datetime.now() - bstack1ll1l1l1_opy_)
                    f.bstack1llll111ll1_opy_(instance, bstack1llll11l111_opy_)
                instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢჇ"), datetime.now() - bstack1lllll1l1l1_opy_)
                return # bstack1lll1l1llll_opy_ not send this event with the bstack1lll1l1l1l1_opy_ bstack1llll11111l_opy_
            elif (
                test_framework_state == bstack1lllll11l11_opy_.TEST
                and test_hook_state == bstack1lll1lll1ll_opy_.POST
                and not f.bstack1llllll1ll1_opy_(instance, TestFramework.bstack11111111l1_opy_)
            ):
                self.logger.warning(bstack11l1111_opy_ (u"ࠧࡪࡲࡰࡲࡳ࡭ࡳ࡭ࠠࡥࡷࡨࠤࡹࡵࠠ࡭ࡣࡦ࡯ࠥࡵࡦࠡࡴࡨࡷࡺࡲࡴࡴࠢࠥ჈") + str(TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack11111111l1_opy_)) + bstack11l1111_opy_ (u"ࠨࠢ჉"))
                f.bstack1llll111l11_opy_(instance, bstack1llll1111ll_opy_.bstack111111111l_opy_, True)
                return # bstack1lll1l1llll_opy_ not send this event bstack1lll1l1l111_opy_ bstack1llll111lll_opy_
            elif (
                f.bstack1lllll1l11l_opy_(instance, bstack1llll1111ll_opy_.bstack111111111l_opy_, False)
                and test_framework_state == bstack1lllll11l11_opy_.LOG_REPORT
                and test_hook_state == bstack1lll1lll1ll_opy_.POST
                and f.bstack1llllll1ll1_opy_(instance, TestFramework.bstack11111111l1_opy_)
            ):
                self.logger.warning(bstack11l1111_opy_ (u"ࠢࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡖࡈࡗ࡙࠲ࠠࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡑࡑࡖࡘࠥࠨ჊") + str(TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack11111111l1_opy_)) + bstack11l1111_opy_ (u"ࠣࠤ჋"))
                self.bstack1llllll1l11_opy_(f, instance, (bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), *args, **kwargs)
            bstack1ll1l1l1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1llll11l1ll_opy_ = sorted(
                filter(lambda x: x.get(bstack11l1111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧ჌"), None), data.pop(bstack11l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥჍ"), {}).values()),
                key=lambda x: x[bstack11l1111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢ჎")],
            )
            if bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_ in data:
                data.pop(bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_)
            data.update({bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧ჏"): bstack1llll11l1ll_opy_})
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦა"), datetime.now() - bstack1ll1l1l1_opy_)
            bstack1ll1l1l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1lllllllll1_opy_)
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥბ"), datetime.now() - bstack1ll1l1l1_opy_)
            self.bstack1llll11111l_opy_(instance, bstack1llll11l111_opy_, event_json=event_json)
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦგ"), datetime.now() - bstack1lllll1l1l1_opy_)
    def bstack1lllll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
        bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack1ll11111l1_opy_.value)
        self.bstack1lll1l111ll_opy_.bstack1llllllll11_opy_(instance, f, bstack1llll11l111_opy_, *args, **kwargs)
        bstack1lll1l1l11l_opy_.end(EVENTS.bstack1ll11111l1_opy_.value, bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤდ"), bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣე"), status=True, failure=None, test_name=None)
    def bstack1lllll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1lll1l111ll_opy_.bstack1llllll1111_opy_(instance, f, bstack1llll11l111_opy_, *args, **kwargs)
        self.bstack1lllll11lll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1lll1l1111l_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1lllll11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11l1111_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵࠢࡪࡖࡕࡉࠠࡤࡣ࡯ࡰ࠿ࠦࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠢვ"))
            return
        bstack1ll1l1l1_opy_ = datetime.now()
        try:
            r = self.bstack1lll1llll1l_opy_.TestSessionEvent(req)
            instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡦࡸࡨࡲࡹࠨზ"), datetime.now() - bstack1ll1l1l1_opy_)
            f.bstack1llll111l11_opy_(instance, self.bstack1lll1l111ll_opy_.bstack1111111ll1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11l1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣთ") + str(r) + bstack11l1111_opy_ (u"ࠢࠣი"))
        except grpc.RpcError as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨკ") + str(e) + bstack11l1111_opy_ (u"ࠤࠥლ"))
            traceback.print_exc()
            raise e
    def bstack1lll1l1l1ll_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        _driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        _1lll1ll11l1_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll1ll1l1l_opy_.bstack1lllll11ll1_opy_(method_name):
            return
        if f.bstack1lllll1ll11_opy_(*args) == bstack1lll1ll1l1l_opy_.bstack1lll1ll1ll1_opy_:
            bstack1lllll1l1l1_opy_ = datetime.now()
            screenshot = result.get(bstack11l1111_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤმ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11l1111_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢ࡬ࡱࡦ࡭ࡥࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡷࡶࠧნ"))
                return
            bstack1llllll111l_opy_ = self.bstack1111111l11_opy_(instance)
            if bstack1llllll111l_opy_:
                entry = bstack1llll11ll1l_opy_(TestFramework.bstack1llll1l1lll_opy_, screenshot)
                self.bstack1lll1ll111l_opy_(bstack1llllll111l_opy_, [entry])
                instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡࡧࡶࡨࡶࡤ࡫ࡸࡦࡥࡸࡸࡪࠨო"), datetime.now() - bstack1lllll1l1l1_opy_)
            else:
                self.logger.warning(bstack11l1111_opy_ (u"ࠨࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡥࡴࡶࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡩ࡫ࡶࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡹࡤࡷࠥࡺࡡ࡬ࡧࡱࠤࡧࡿࠠࡥࡴ࡬ࡺࡪࡸ࠽ࠡࡽࢀࠦპ").format(instance.ref()))
        event = {}
        bstack1llllll111l_opy_ = self.bstack1111111l11_opy_(instance)
        if bstack1llllll111l_opy_:
            self.bstack1llll1l11l1_opy_(event, bstack1llllll111l_opy_)
            if event.get(bstack11l1111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧჟ")):
                self.bstack1lll1ll111l_opy_(bstack1llllll111l_opy_, event[bstack11l1111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨრ")])
            else:
                self.logger.debug(bstack11l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡ࡮ࡲ࡫ࡸࠦࡦࡰࡴࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡦࡸࡨࡲࡹࠨს"))
    @measure(event_name=EVENTS.bstack1llll1ll111_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1lll1ll111l_opy_(
        self,
        bstack1llllll111l_opy_: bstack1lllll111ll_opy_,
        entries: List[bstack1llll11ll1l_opy_],
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1llllll1lll_opy_)
        req.execution_context.hash = str(bstack1llllll111l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1llllll111l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1llllll111l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1lll1ll1l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1lll1l11ll1_opy_)
            log_entry.uuid = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1lll1l1ll1l_opy_)
            log_entry.test_framework_state = bstack1llllll111l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1111_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤტ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1111_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨუ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack111111l1l1_opy_
                log_entry.file_path = entry.bstack1ll1l_opy_
        def bstack1llll1l11ll_opy_():
            bstack1ll1l1l1_opy_ = datetime.now()
            try:
                self.bstack1lll1llll1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1llll1l1lll_opy_:
                    bstack1llllll111l_opy_.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤფ"), datetime.now() - bstack1ll1l1l1_opy_)
                elif entry.kind == TestFramework.bstack1llll1l1l11_opy_:
                    bstack1llllll111l_opy_.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥქ"), datetime.now() - bstack1ll1l1l1_opy_)
                else:
                    bstack1llllll111l_opy_.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟࡭ࡱࡪࠦღ"), datetime.now() - bstack1ll1l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨყ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1llll1l1l1l_opy_.enqueue(bstack1llll1l11ll_opy_)
    @measure(event_name=EVENTS.bstack11111111ll_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1llll11111l_opy_(
        self,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        event_json=None,
    ):
        self.bstack1lll1lll1l1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1llllll1lll_opy_)
        req.test_framework_name = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1ll1l11_opy_)
        req.test_framework_version = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l11ll1_opy_)
        req.test_framework_state = bstack1llll11l111_opy_[0].name
        req.test_hook_state = bstack1llll11l111_opy_[1].name
        started_at = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lllll1ll1l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1lll111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1lllllllll1_opy_)).encode(bstack11l1111_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣშ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1llll1l11ll_opy_():
            bstack1ll1l1l1_opy_ = datetime.now()
            try:
                self.bstack1lll1llll1l_opy_.TestFrameworkEvent(req)
                instance.bstack1llll1l1l_opy_(bstack11l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡦࡸࡨࡲࡹࠨჩ"), datetime.now() - bstack1ll1l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤც") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1llll1l1l1l_opy_.enqueue(bstack1llll1l11ll_opy_)
    def bstack1111111l11_opy_(self, instance: bstack1lll1llll11_opy_):
        bstack1llllllllll_opy_ = TestFramework.bstack1lllll1111l_opy_(instance.context)
        for t in bstack1llllllllll_opy_:
            bstack1llll11l1l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(t, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
            if any(instance is d[1] for d in bstack1llll11l1l1_opy_):
                return t
    def bstack1llll11l11l_opy_(self, message):
        self.bstack1llll1llll1_opy_(message + bstack11l1111_opy_ (u"ࠧࡢ࡮ࠣძ"))
    def log_error(self, message):
        self.bstack1lll1l11lll_opy_(message + bstack11l1111_opy_ (u"ࠨ࡜࡯ࠤწ"))
    def bstack1lllll111l1_opy_(self, level, original_func):
        def bstack1lllll11111_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1llllllllll_opy_ = TestFramework.bstack1111111l1l_opy_()
            if not bstack1llllllllll_opy_:
                return return_value
            bstack1llllll111l_opy_ = next(
                (
                    instance
                    for instance in bstack1llllllllll_opy_
                    if TestFramework.bstack1llllll1ll1_opy_(instance, TestFramework.bstack1lll1l1ll1l_opy_)
                ),
                None,
            )
            if not bstack1llllll111l_opy_:
                return
            entry = bstack1llll11ll1l_opy_(TestFramework.bstack1lllllll11l_opy_, message, level)
            self.bstack1lll1ll111l_opy_(bstack1llllll111l_opy_, [entry])
            return return_value
        return bstack1lllll11111_opy_
    def bstack1llll1l11l1_opy_(self, event: dict, instance=None) -> None:
        global _1llll11lll1_opy_
        levels = [bstack11l1111_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥჭ"), bstack11l1111_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧხ")]
        bstack1llll111l1l_opy_ = bstack11l1111_opy_ (u"ࠤࠥჯ")
        if instance is not None:
            try:
                bstack1llll111l1l_opy_ = TestFramework.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1lll1l1ll1l_opy_)
            except Exception as e:
                self.logger.warning(bstack11l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡺ࡯ࡤࠡࡨࡵࡳࡲࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣჰ").format(e))
        bstack1lll1l111l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫჱ")]
                bstack1lllll1l111_opy_ = os.path.join(bstack1lllllll111_opy_, (bstack1111111lll_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1lllll1l111_opy_):
                    self.logger.debug(bstack11l1111_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡰࡲࡸࠥࡶࡲࡦࡵࡨࡲࡹࠦࡦࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡕࡧࡶࡸࠥࡧ࡮ࡥࠢࡅࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣჲ").format(bstack1lllll1l111_opy_))
                    continue
                file_names = os.listdir(bstack1lllll1l111_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1lllll1l111_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1llll11lll1_opy_:
                        self.logger.info(bstack11l1111_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦჳ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1lll1l1lll1_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1lll1l1lll1_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11l1111_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥჴ"):
                                entry = bstack1llll11ll1l_opy_(
                                    kind=bstack11l1111_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥჵ"),
                                    message=bstack11l1111_opy_ (u"ࠤࠥჶ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack111111l1l1_opy_=file_size,
                                    bstack1llll1l1111_opy_=bstack11l1111_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥჷ"),
                                    bstack1ll1l_opy_=os.path.abspath(file_path),
                                    bstack1l1111111_opy_=bstack1llll111l1l_opy_
                                )
                            elif level == bstack11l1111_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣჸ"):
                                entry = bstack1llll11ll1l_opy_(
                                    kind=bstack11l1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢჹ"),
                                    message=bstack11l1111_opy_ (u"ࠨࠢჺ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack111111l1l1_opy_=file_size,
                                    bstack1llll1l1111_opy_=bstack11l1111_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢ჻"),
                                    bstack1ll1l_opy_=os.path.abspath(file_path),
                                    bstack1llll111111_opy_=bstack1llll111l1l_opy_
                                )
                            bstack1lll1l111l1_opy_.append(entry)
                            _1llll11lll1_opy_.add(abs_path)
                        except Exception as bstack1llll1ll1ll_opy_:
                            self.logger.error(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢჼ").format(bstack1llll1ll1ll_opy_))
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣჽ").format(e))
        event[bstack11l1111_opy_ (u"ࠥࡰࡴ࡭ࡳࠣჾ")] = bstack1lll1l111l1_opy_
class bstack1lllllllll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1lll1ll1111_opy_ = set()
        kwargs[bstack11l1111_opy_ (u"ࠦࡸࡱࡩࡱ࡭ࡨࡽࡸࠨჿ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1llll11llll_opy_(obj, self.bstack1lll1ll1111_opy_)
def bstack1lllll1l1ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1llll11llll_opy_(obj, bstack1lll1ll1111_opy_=None, max_depth=3):
    if bstack1lll1ll1111_opy_ is None:
        bstack1lll1ll1111_opy_ = set()
    if id(obj) in bstack1lll1ll1111_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1lll1ll1111_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack111111l111_opy_ = TestFramework.bstack1lll1l11l11_opy_(obj)
    bstack1llllllll1l_opy_ = next((k.lower() in bstack111111l111_opy_.lower() for k in bstack111111l11l_opy_.keys()), None)
    if bstack1llllllll1l_opy_:
        obj = TestFramework.bstack1lll1ll11ll_opy_(obj, bstack111111l11l_opy_[bstack1llllllll1l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11l1111_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣᄀ")):
            keys = getattr(obj, bstack11l1111_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤᄁ"), [])
        elif hasattr(obj, bstack11l1111_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤᄂ")):
            keys = getattr(obj, bstack11l1111_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥᄃ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11l1111_opy_ (u"ࠤࡢࠦᄄ"))}
        if not obj and bstack111111l111_opy_ == bstack11l1111_opy_ (u"ࠥࡴࡦࡺࡨ࡭࡫ࡥ࠲ࡕࡵࡳࡪࡺࡓࡥࡹ࡮ࠢᄅ"):
            obj = {bstack11l1111_opy_ (u"ࠦࡵࡧࡴࡩࠤᄆ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1lllll1l1ll_opy_(key) or str(key).startswith(bstack11l1111_opy_ (u"ࠧࡥࠢᄇ")):
            continue
        if value is not None and bstack1lllll1l1ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1llll11llll_opy_(value, bstack1lll1ll1111_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1llll11llll_opy_(o, bstack1lll1ll1111_opy_, max_depth) for o in value]))
    return result or None