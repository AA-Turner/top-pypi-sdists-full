# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from datetime import datetime, timezone
import os
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import bstack1llllll111l_opy_, bstack1111111111_opy_, bstack11111l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11lllll_opy_, bstack1lll1111l1l_opy_, bstack1lllll1111l_opy_, bstack1lll11111l1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1ll11l1ll_opy_, bstack1l1lll111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
bstack1l1llllll1l_opy_ = [bstack111lll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇩ"), bstack111lll_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣᇪ"), bstack111lll_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤᇫ"), bstack111lll_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦᇬ"), bstack111lll_opy_ (u"ࠦࡵࡧࡴࡩࠤᇭ")]
bstack1l1ll1l11l1_opy_ = bstack1l1lll111l1_opy_()
bstack1l1ll1l1111_opy_ = bstack111lll_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧᇮ")
bstack1l1ll11lll1_opy_ = {
    bstack111lll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦᇯ"): bstack1l1llllll1l_opy_,
    bstack111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣᇰ"): bstack1l1llllll1l_opy_,
    bstack111lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣᇱ"): bstack1l1llllll1l_opy_,
    bstack111lll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣᇲ"): bstack1l1llllll1l_opy_,
    bstack111lll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧᇳ"): bstack1l1llllll1l_opy_
    + [
        bstack111lll_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥᇴ"),
        bstack111lll_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢᇵ"),
        bstack111lll_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦᇶ"),
        bstack111lll_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤᇷ"),
        bstack111lll_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥᇸ"),
        bstack111lll_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥᇹ"),
        bstack111lll_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤᇺ"),
        bstack111lll_opy_ (u"ࠦࡸࡺ࡯ࡱࠤᇻ"),
        bstack111lll_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢᇼ"),
        bstack111lll_opy_ (u"ࠨࡷࡩࡧࡱࠦᇽ"),
    ],
    bstack111lll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨᇾ"): [bstack111lll_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦᇿ"), bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢሀ"), bstack111lll_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦሁ"), bstack111lll_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥሂ")],
    bstack111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧሃ"): [bstack111lll_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥሄ"), bstack111lll_opy_ (u"ࠢࡢࡴࡪࡷࠧህ")],
    bstack111lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢሆ"): [bstack111lll_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣሇ"), bstack111lll_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦለ"), bstack111lll_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤሉ"), bstack111lll_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧሊ"), bstack111lll_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣላ"), bstack111lll_opy_ (u"ࠢࡪࡦࡶࠦሌ")],
    bstack111lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢል"): [bstack111lll_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢሎ"), bstack111lll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤሏ"), bstack111lll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤሐ")],
    bstack111lll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢሑ"): [bstack111lll_opy_ (u"ࠨࡷࡩࡧࡱࠦሒ"), bstack111lll_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢሓ")],
    bstack111lll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤሔ"): [bstack111lll_opy_ (u"ࠤࡱࡳࡩ࡫ࠢሕ"), bstack111lll_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥሖ")],
    bstack111lll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦሗ"): [bstack111lll_opy_ (u"ࠧࡴࡡ࡮ࡧࠥመ"), bstack111lll_opy_ (u"ࠨࡡࡳࡩࡶࠦሙ"), bstack111lll_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢሚ")],
}
_1l1llll1ll1_opy_ = set()
class bstack1ll1llll11l_opy_(bstack1lll1l11ll1_opy_):
    bstack1l1ll11ll11_opy_ = bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣማ")
    bstack1l1lll11lll_opy_ = bstack111lll_opy_ (u"ࠤࡌࡒࡋࡕࠢሜ")
    bstack1l1lll11l1l_opy_ = bstack111lll_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤም")
    bstack1l1lll1ll11_opy_: Callable
    bstack1l1ll1l1l11_opy_: Callable
    def __init__(self, bstack1ll1ll1llll_opy_, bstack1lll1llllll_opy_):
        super().__init__()
        self.bstack1ll1l1lll1l_opy_ = bstack1lll1llllll_opy_
        if os.getenv(bstack111lll_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣሞ"), bstack111lll_opy_ (u"ࠧ࠷ࠢሟ")) != bstack111lll_opy_ (u"ࠨ࠱ࠣሠ") or not self.is_enabled():
            self.logger.warning(bstack111lll_opy_ (u"ࠢࠣሡ") + str(self.__class__.__name__) + bstack111lll_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦሢ"))
            return
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.PRE), self.bstack1ll1ll11111_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), self.bstack1ll11ll111l_opy_)
        for event in bstack1lll11lllll_opy_:
            for state in bstack1lllll1111l_opy_:
                TestFramework.bstack1ll11ll1l1l_opy_((event, state), self.bstack1l1lll1l11l_opy_)
        bstack1ll1ll1llll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.POST), self.bstack1l1ll1lllll_opy_)
        self.bstack1l1lll1ll11_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1llll111l_opy_(bstack1ll1llll11l_opy_.bstack1l1lll11lll_opy_, self.bstack1l1lll1ll11_opy_)
        self.bstack1l1ll1l1l11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1llll111l_opy_(bstack1ll1llll11l_opy_.bstack1l1lll11l1l_opy_, self.bstack1l1ll1l1l11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1l11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1llll1l1l_opy_() and instance:
            bstack1ll1111l1ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack11111l1l11_opy_
            if test_framework_state == bstack1lll11lllll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1lll11lllll_opy_.LOG:
                bstack11ll1ll1_opy_ = datetime.now()
                entries = f.bstack1l1lll1ll1l_opy_(instance, bstack11111l1l11_opy_)
                if entries:
                    self.bstack1l1lllll111_opy_(instance, entries)
                    instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤሣ"), datetime.now() - bstack11ll1ll1_opy_)
                    f.bstack1l1lllll1ll_opy_(instance, bstack11111l1l11_opy_)
                instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨሤ"), datetime.now() - bstack1ll1111l1ll_opy_)
                return # bstack1l1llllllll_opy_ not send this event with the bstack1l1lllll11l_opy_ bstack1l1lllllll1_opy_
            elif (
                test_framework_state == bstack1lll11lllll_opy_.TEST
                and test_hook_state == bstack1lllll1111l_opy_.POST
                and not f.bstack11111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_)
            ):
                self.logger.warning(bstack111lll_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤሥ") + str(TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_)) + bstack111lll_opy_ (u"ࠧࠨሦ"))
                f.bstack11111ll111_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1ll11ll11_opy_, True)
                return # bstack1l1llllllll_opy_ not send this event bstack1l1ll1l1ll1_opy_ bstack1l1ll1l11ll_opy_
            elif (
                f.bstack1llllll1l1l_opy_(instance, bstack1ll1llll11l_opy_.bstack1l1ll11ll11_opy_, False)
                and test_framework_state == bstack1lll11lllll_opy_.LOG_REPORT
                and test_hook_state == bstack1lllll1111l_opy_.POST
                and f.bstack11111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_)
            ):
                self.logger.warning(bstack111lll_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧሧ") + str(TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l1l_opy_)) + bstack111lll_opy_ (u"ࠢࠣረ"))
                self.bstack1l1lll1l11l_opy_(f, instance, (bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), *args, **kwargs)
            bstack11ll1ll1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1ll11111lll_opy_ = sorted(
                filter(lambda x: x.get(bstack111lll_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦሩ"), None), data.pop(bstack111lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤሪ"), {}).values()),
                key=lambda x: x[bstack111lll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨራ")],
            )
            if bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_ in data:
                data.pop(bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_)
            data.update({bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦሬ"): bstack1ll11111lll_opy_})
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥር"), datetime.now() - bstack11ll1ll1_opy_)
            bstack11ll1ll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1llll1111_opy_)
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤሮ"), datetime.now() - bstack11ll1ll1_opy_)
            self.bstack1l1lllllll1_opy_(instance, bstack11111l1l11_opy_, event_json=event_json)
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥሯ"), datetime.now() - bstack1ll1111l1ll_opy_)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
        bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack111l1l1l_opy_.value)
        self.bstack1ll1l1lll1l_opy_.bstack1l1lll1lll1_opy_(instance, f, bstack11111l1l11_opy_, *args, **kwargs)
        bstack1llll1l1l11_opy_.end(EVENTS.bstack111l1l1l_opy_.value, bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሰ"), bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሱ"), status=True, failure=None, test_name=None)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        req = self.bstack1ll1l1lll1l_opy_.bstack1l1llll1lll_opy_(instance, f, bstack11111l1l11_opy_, *args, **kwargs)
        self.bstack1ll11111ll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l1ll1ll111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1ll11111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack111lll_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨሲ"))
            return
        bstack11ll1ll1_opy_ = datetime.now()
        try:
            r = self.bstack1lll1ll1l11_opy_.TestSessionEvent(req)
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧሳ"), datetime.now() - bstack11ll1ll1_opy_)
            f.bstack11111ll111_opy_(instance, self.bstack1ll1l1lll1l_opy_.bstack1ll111111ll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack111lll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢሴ") + str(r) + bstack111lll_opy_ (u"ࠨࠢስ"))
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧሶ") + str(e) + bstack111lll_opy_ (u"ࠣࠤሷ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1lllll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        _driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        _1l1ll1lll11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1llll111lll_opy_.bstack1ll11l1l1l1_opy_(method_name):
            return
        if f.bstack1ll1l111lll_opy_(*args) == bstack1llll111lll_opy_.bstack1l1lll1l1l1_opy_:
            bstack1ll1111l1ll_opy_ = datetime.now()
            screenshot = result.get(bstack111lll_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣሸ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack111lll_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦሹ"))
                return
            bstack1l1lllll1l1_opy_ = self.bstack1l1lll111ll_opy_(instance)
            if bstack1l1lllll1l1_opy_:
                entry = bstack1lll11111l1_opy_(TestFramework.bstack1l1ll1llll1_opy_, screenshot)
                self.bstack1l1lllll111_opy_(bstack1l1lllll1l1_opy_, [entry])
                instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧሺ"), datetime.now() - bstack1ll1111l1ll_opy_)
            else:
                self.logger.warning(bstack111lll_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥሻ").format(instance.ref()))
        event = {}
        bstack1l1lllll1l1_opy_ = self.bstack1l1lll111ll_opy_(instance)
        if bstack1l1lllll1l1_opy_:
            self.bstack1ll11111111_opy_(event, bstack1l1lllll1l1_opy_)
            if event.get(bstack111lll_opy_ (u"ࠨ࡬ࡰࡩࡶࠦሼ")):
                self.bstack1l1lllll111_opy_(bstack1l1lllll1l1_opy_, event[bstack111lll_opy_ (u"ࠢ࡭ࡱࡪࡷࠧሽ")])
            else:
                self.logger.debug(bstack111lll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧሾ"))
    @measure(event_name=EVENTS.bstack1ll1111ll1l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1lllll111_opy_(
        self,
        bstack1l1lllll1l1_opy_: bstack1lll1111l1l_opy_,
        entries: List[bstack1lll11111l1_opy_],
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll1l11ll1l_opy_)
        req.execution_context.hash = str(bstack1l1lllll1l1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1lllll1l1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1lllll1l1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll11ll11ll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1l1lll1l1ll_opy_)
            log_entry.uuid = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1ll11lll11l_opy_)
            log_entry.test_framework_state = bstack1l1lllll1l1_opy_.state.name
            log_entry.message = entry.message.encode(bstack111lll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣሿ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack111lll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧቀ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1ll1ll1ll_opy_
                log_entry.file_path = entry.bstack11ll1_opy_
        def bstack1ll1111111l_opy_():
            bstack11ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1ll1llll1_opy_:
                    bstack1l1lllll1l1_opy_.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠣቁ"), datetime.now() - bstack11ll1ll1_opy_)
                elif entry.kind == TestFramework.bstack1ll111111l1_opy_:
                    bstack1l1lllll1l1_opy_.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠤቂ"), datetime.now() - bstack11ll1ll1_opy_)
                else:
                    bstack1l1lllll1l1_opy_.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥ࡬ࡰࡩࠥቃ"), datetime.now() - bstack11ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111lll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧቄ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack11111lll11_opy_.enqueue(bstack1ll1111111l_opy_)
    @measure(event_name=EVENTS.bstack1l1llll1l11_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1lllllll1_opy_(
        self,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        event_json=None,
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l11ll1l_opy_)
        req.test_framework_name = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11ll11ll_opy_)
        req.test_framework_version = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1lll1l1ll_opy_)
        req.test_framework_state = bstack11111l1l11_opy_[0].name
        req.test_hook_state = bstack11111l1l11_opy_[1].name
        started_at = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1l1llll11ll_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11111l1l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1llll1111_opy_)).encode(bstack111lll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢቅ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1ll1111111l_opy_():
            bstack11ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1lll1ll1l11_opy_.TestFrameworkEvent(req)
                instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡥࡷࡧࡱࡸࠧቆ"), datetime.now() - bstack11ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack111lll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣቇ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack11111lll11_opy_.enqueue(bstack1ll1111111l_opy_)
    def bstack1l1lll111ll_opy_(self, instance: bstack1llllll111l_opy_):
        bstack1l1ll1l111l_opy_ = TestFramework.bstack1llllll1l11_opy_(instance.context)
        for t in bstack1l1ll1l111l_opy_:
            bstack1ll1111l11l_opy_ = TestFramework.bstack1llllll1l1l_opy_(t, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
            if any(instance is d[1] for d in bstack1ll1111l11l_opy_):
                return t
    def bstack1l1llllll11_opy_(self, message):
        self.bstack1l1lll1ll11_opy_(message + bstack111lll_opy_ (u"ࠦࡡࡴࠢቈ"))
    def log_error(self, message):
        self.bstack1l1ll1l1l11_opy_(message + bstack111lll_opy_ (u"ࠧࡢ࡮ࠣ቉"))
    def bstack1l1llll111l_opy_(self, level, original_func):
        def bstack1l1ll1ll1l1_opy_(*args):
            return_value = original_func(*args)
            if not args or not isinstance(args[0], str) or not args[0].strip():
                return return_value
            message = args[0].strip()
            bstack1l1ll1l111l_opy_ = TestFramework.bstack1l1lll11111_opy_()
            if not bstack1l1ll1l111l_opy_:
                return return_value
            bstack1l1lllll1l1_opy_ = next(
                (
                    instance
                    for instance in bstack1l1ll1l111l_opy_
                    if TestFramework.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
                ),
                None,
            )
            if not bstack1l1lllll1l1_opy_:
                return
            entry = bstack1lll11111l1_opy_(TestFramework.bstack1l1lll1111l_opy_, message, level)
            self.bstack1l1lllll111_opy_(bstack1l1lllll1l1_opy_, [entry])
            return return_value
        return bstack1l1ll1ll1l1_opy_
    def bstack1ll11111111_opy_(self, event: dict, instance=None) -> None:
        global _1l1llll1ll1_opy_
        levels = [bstack111lll_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤቊ"), bstack111lll_opy_ (u"ࠢࡃࡷ࡬ࡰࡩࡒࡥࡷࡧ࡯ࠦቋ")]
        bstack1l1ll1l1lll_opy_ = bstack111lll_opy_ (u"ࠣࠤቌ")
        if instance is not None:
            try:
                bstack1l1ll1l1lll_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
            except Exception as e:
                self.logger.warning(bstack111lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡩࡨࡸࡹ࡯࡮ࡨࠢࡸࡹ࡮ࡪࠠࡧࡴࡲࡱࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠢቍ").format(e))
        bstack1l1ll1ll11l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ቎")]
                bstack1l1lll11ll1_opy_ = os.path.join(bstack1l1ll1l11l1_opy_, (bstack1l1ll1l1111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l1lll11ll1_opy_):
                    self.logger.debug(bstack111lll_opy_ (u"ࠦࡉ࡯ࡲࡦࡥࡷࡳࡷࡿࠠ࡯ࡱࡷࠤࡵࡸࡥࡴࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡔࡦࡵࡷࠤࡦࡴࡤࠡࡄࡸ࡭ࡱࡪࠠ࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢ቏").format(bstack1l1lll11ll1_opy_))
                    continue
                file_names = os.listdir(bstack1l1lll11ll1_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l1lll11ll1_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l1llll1ll1_opy_:
                        self.logger.info(bstack111lll_opy_ (u"ࠧࡖࡡࡵࡪࠣࡥࡱࡸࡥࡢࡦࡼࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡼࡿࠥቐ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1ll11ll1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1ll11ll1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack111lll_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤቑ"):
                                entry = bstack1lll11111l1_opy_(
                                    kind=bstack111lll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤቒ"),
                                    message=bstack111lll_opy_ (u"ࠣࠤቓ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1ll1ll_opy_=file_size,
                                    bstack1l1lll1llll_opy_=bstack111lll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤቔ"),
                                    bstack11ll1_opy_=os.path.abspath(file_path),
                                    bstack1ll1ll1111_opy_=bstack1l1ll1l1lll_opy_
                                )
                            elif level == bstack111lll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢቕ"):
                                entry = bstack1lll11111l1_opy_(
                                    kind=bstack111lll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨቖ"),
                                    message=bstack111lll_opy_ (u"ࠧࠨ቗"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1ll1ll1ll_opy_=file_size,
                                    bstack1l1lll1llll_opy_=bstack111lll_opy_ (u"ࠨࡍࡂࡐࡘࡅࡑࡥࡕࡑࡎࡒࡅࡉࠨቘ"),
                                    bstack11ll1_opy_=os.path.abspath(file_path),
                                    bstack1ll11111l11_opy_=bstack1l1ll1l1lll_opy_
                                )
                            bstack1l1ll1ll11l_opy_.append(entry)
                            _1l1llll1ll1_opy_.add(abs_path)
                        except Exception as bstack1l1ll1lll1l_opy_:
                            self.logger.error(bstack111lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡶࡦ࡯ࡳࡦࡦࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫ࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡿࢂࠨ቙").format(bstack1l1ll1lll1l_opy_))
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢቚ").format(e))
        event[bstack111lll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢቛ")] = bstack1l1ll1ll11l_opy_
class bstack1l1llll1111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1ll1111l111_opy_ = set()
        kwargs[bstack111lll_opy_ (u"ࠥࡷࡰ࡯ࡰ࡬ࡧࡼࡷࠧቜ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1lll11l11_opy_(obj, self.bstack1ll1111l111_opy_)
def bstack1l1ll11llll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1lll11l11_opy_(obj, bstack1ll1111l111_opy_=None, max_depth=3):
    if bstack1ll1111l111_opy_ is None:
        bstack1ll1111l111_opy_ = set()
    if id(obj) in bstack1ll1111l111_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1ll1111l111_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1lll1l111_opy_ = TestFramework.bstack1ll1111ll11_opy_(obj)
    bstack1l1llll11l1_opy_ = next((k.lower() in bstack1l1lll1l111_opy_.lower() for k in bstack1l1ll11lll1_opy_.keys()), None)
    if bstack1l1llll11l1_opy_:
        obj = TestFramework.bstack1ll1111l1l1_opy_(obj, bstack1l1ll11lll1_opy_[bstack1l1llll11l1_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack111lll_opy_ (u"ࠦࡤࡥࡳ࡭ࡱࡷࡷࡤࡥࠢቝ")):
            keys = getattr(obj, bstack111lll_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣ቞"), [])
        elif hasattr(obj, bstack111lll_opy_ (u"ࠨ࡟ࡠࡦ࡬ࡧࡹࡥ࡟ࠣ቟")):
            keys = getattr(obj, bstack111lll_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤበ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack111lll_opy_ (u"ࠣࡡࠥቡ"))}
        if not obj and bstack1l1lll1l111_opy_ == bstack111lll_opy_ (u"ࠤࡳࡥࡹ࡮࡬ࡪࡤ࠱ࡔࡴࡹࡩࡹࡒࡤࡸ࡭ࠨቢ"):
            obj = {bstack111lll_opy_ (u"ࠥࡴࡦࡺࡨࠣባ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l1ll11llll_opy_(key) or str(key).startswith(bstack111lll_opy_ (u"ࠦࡤࠨቤ")):
            continue
        if value is not None and bstack1l1ll11llll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1lll11l11_opy_(value, bstack1ll1111l111_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1lll11l11_opy_(o, bstack1ll1111l111_opy_, max_depth) for o in value]))
    return result or None