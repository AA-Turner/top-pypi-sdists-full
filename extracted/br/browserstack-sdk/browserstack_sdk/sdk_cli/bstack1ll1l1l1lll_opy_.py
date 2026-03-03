# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import bstack1ll1lll1111_opy_, bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11llll_opy_ import bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1ll1l111111_opy_, bstack1l1llll1l1l_opy_, bstack1ll1l1l11ll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l11l1111ll_opy_, bstack1l11llll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l111lll1l1_opy_ = [bstack11ll111_opy_ (u"ࠣࡰࡤࡱࡪࠨᐅ"), bstack11ll111_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤᐆ"), bstack11ll111_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥᐇ"), bstack11ll111_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧᐈ"), bstack11ll111_opy_ (u"ࠧࡶࡡࡵࡪࠥᐉ")]
bstack1l11lll1111_opy_ = bstack1l11llll11l_opy_()
bstack1l11lll1l11_opy_ = bstack11ll111_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᐊ")
bstack1l11l1l1111_opy_ = {
    bstack11ll111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡊࡶࡨࡱࠧᐋ"): bstack1l111lll1l1_opy_,
    bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡒࡤࡧࡰࡧࡧࡦࠤᐌ"): bstack1l111lll1l1_opy_,
    bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡐࡳࡩࡻ࡬ࡦࠤᐍ"): bstack1l111lll1l1_opy_,
    bstack11ll111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡇࡱࡧࡳࡴࠤᐎ"): bstack1l111lll1l1_opy_,
    bstack11ll111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡋࡻ࡮ࡤࡶ࡬ࡳࡳࠨᐏ"): bstack1l111lll1l1_opy_
    + [
        bstack11ll111_opy_ (u"ࠧࡵࡲࡪࡩ࡬ࡲࡦࡲ࡮ࡢ࡯ࡨࠦᐐ"),
        bstack11ll111_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᐑ"),
        bstack11ll111_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࡪࡰࡩࡳࠧᐒ"),
        bstack11ll111_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᐓ"),
        bstack11ll111_opy_ (u"ࠤࡦࡥࡱࡲࡳࡱࡧࡦࠦᐔ"),
        bstack11ll111_opy_ (u"ࠥࡧࡦࡲ࡬ࡰࡤ࡭ࠦᐕ"),
        bstack11ll111_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥᐖ"),
        bstack11ll111_opy_ (u"ࠧࡹࡴࡰࡲࠥᐗ"),
        bstack11ll111_opy_ (u"ࠨࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠣᐘ"),
        bstack11ll111_opy_ (u"ࠢࡸࡪࡨࡲࠧᐙ"),
    ],
    bstack11ll111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤ࡭ࡳ࠴ࡓࡦࡵࡶ࡭ࡴࡴࠢᐚ"): [bstack11ll111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡱࡣࡷ࡬ࠧᐛ"), bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡴࡨࡤ࡭ࡱ࡫ࡤࠣᐜ"), bstack11ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧᐝ"), bstack11ll111_opy_ (u"ࠧ࡯ࡴࡦ࡯ࡶࠦᐞ")],
    bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡣࡰࡰࡩ࡭࡬࠴ࡃࡰࡰࡩ࡭࡬ࠨᐟ"): [bstack11ll111_opy_ (u"ࠢࡪࡰࡹࡳࡨࡧࡴࡪࡱࡱࡣࡵࡧࡲࡢ࡯ࡶࠦᐠ"), bstack11ll111_opy_ (u"ࠣࡣࡵ࡫ࡸࠨᐡ")],
    bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡋ࡯ࡸࡵࡷࡵࡩࡉ࡫ࡦࠣᐢ"): [bstack11ll111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᐣ"), bstack11ll111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᐤ"), bstack11ll111_opy_ (u"ࠧ࡬ࡵ࡯ࡥࠥᐥ"), bstack11ll111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᐦ"), bstack11ll111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᐧ"), bstack11ll111_opy_ (u"ࠣ࡫ࡧࡷࠧᐨ")],
    bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡘࡻࡢࡓࡧࡴࡹࡪࡹࡴࠣᐩ"): [bstack11ll111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᐪ"), bstack11ll111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࠥᐫ"), bstack11ll111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡣ࡮ࡴࡤࡦࡺࠥᐬ")],
    bstack11ll111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡲࡶࡰࡱࡩࡷ࠴ࡃࡢ࡮࡯ࡍࡳ࡬࡯ࠣᐭ"): [bstack11ll111_opy_ (u"ࠢࡸࡪࡨࡲࠧᐮ"), bstack11ll111_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࠣᐯ")],
    bstack11ll111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡓࡵࡤࡦࡍࡨࡽࡼࡵࡲࡥࡵࠥᐰ"): [bstack11ll111_opy_ (u"ࠥࡲࡴࡪࡥࠣᐱ"), bstack11ll111_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᐲ")],
    bstack11ll111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡎࡣࡵ࡯ࠧᐳ"): [bstack11ll111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐴ"), bstack11ll111_opy_ (u"ࠢࡢࡴࡪࡷࠧᐵ"), bstack11ll111_opy_ (u"ࠣ࡭ࡺࡥࡷ࡭ࡳࠣᐶ")],
}
_1l11l1ll1l1_opy_ = set()
class bstack1l1llll1l11_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l111lll1ll_opy_ = bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࠤᐷ")
    bstack1l11ll1lll1_opy_ = bstack11ll111_opy_ (u"ࠥࡍࡓࡌࡏࠣᐸ")
    bstack1l111ll1ll1_opy_ = bstack11ll111_opy_ (u"ࠦࡊࡘࡒࡐࡔࠥᐹ")
    bstack1l11lll1ll1_opy_: Callable
    bstack1l11l111111_opy_: Callable
    def __init__(self, bstack1ll11111l1l_opy_, bstack1l1llllll11_opy_):
        super().__init__()
        self.bstack1l1ll11llll_opy_ = bstack1l1llllll11_opy_
        if os.getenv(bstack11ll111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡔ࠷࠱࡚ࠤᐺ"), bstack11ll111_opy_ (u"ࠨ࠱ࠣᐻ")) != bstack11ll111_opy_ (u"ࠢ࠲ࠤᐼ") or not self.is_enabled():
            self.logger.warning(bstack11ll111_opy_ (u"ࠣࠤᐽ") + str(self.__class__.__name__) + bstack11ll111_opy_ (u"ࠤࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠧᐾ"))
            return
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.PRE), self.bstack1l1ll1111ll_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), self.bstack1l1ll111ll1_opy_)
        for event in bstack1ll1ll11l1l_opy_:
            for state in bstack1l1llll1l1l_opy_:
                TestFramework.bstack1l1l1lll11l_opy_((event, state), self.bstack1l11l11111l_opy_)
        bstack1ll11111l1l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.POST), self.bstack1l11l1l1l11_opy_)
        self.bstack1l11lll1ll1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11llll111_opy_(bstack1l1llll1l11_opy_.bstack1l11ll1lll1_opy_, self.bstack1l11lll1ll1_opy_)
        self.bstack1l11l111111_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11llll111_opy_(bstack1l1llll1l11_opy_.bstack1l111ll1ll1_opy_, self.bstack1l11l111111_opy_)
        self.bstack1l11l1lllll_opy_ = builtins.print
        builtins.print = self.bstack1l11l11lll1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l11l111lll_opy_() and instance:
            bstack1l111llll11_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1ll1llll_opy_
            if test_framework_state == bstack1ll1ll11l1l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1ll11l1l_opy_.LOG:
                bstack11lll11111_opy_ = datetime.now()
                entries = f.bstack1l111lll11l_opy_(instance, bstack1ll1ll1llll_opy_)
                if entries:
                    self.bstack1l11l11l1l1_opy_(instance, entries)
                    instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥᐿ"), datetime.now() - bstack11lll11111_opy_)
                    f.bstack1l111llllll_opy_(instance, bstack1ll1ll1llll_opy_)
                instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᑀ"), datetime.now() - bstack1l111llll11_opy_)
                return # bstack1l11l1l1ll1_opy_ not send this event with the bstack1l11l1l11ll_opy_ bstack1l11ll11lll_opy_
            elif (
                test_framework_state == bstack1ll1ll11l1l_opy_.TEST
                and test_hook_state == bstack1l1llll1l1l_opy_.POST
                and not f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
            ):
                self.logger.warning(bstack11ll111_opy_ (u"ࠧࡪࡲࡰࡲࡳ࡭ࡳ࡭ࠠࡥࡷࡨࠤࡹࡵࠠ࡭ࡣࡦ࡯ࠥࡵࡦࠡࡴࡨࡷࡺࡲࡴࡴࠢࠥᑁ") + str(TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)) + bstack11ll111_opy_ (u"ࠨࠢᑂ"))
                f.bstack1lll11l1111_opy_(instance, bstack1l1llll1l11_opy_.bstack1l111lll1ll_opy_, True)
                return # bstack1l11l1l1ll1_opy_ not send this event bstack1l11ll11l1l_opy_ bstack1l11ll11111_opy_
            elif (
                f.bstack1ll1lllll11_opy_(instance, bstack1l1llll1l11_opy_.bstack1l111lll1ll_opy_, False)
                and test_framework_state == bstack1ll1ll11l1l_opy_.LOG_REPORT
                and test_hook_state == bstack1l1llll1l1l_opy_.POST
                and f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
            ):
                self.logger.warning(bstack11ll111_opy_ (u"ࠢࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡖࡈࡗ࡙࠲ࠠࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡑࡑࡖࡘࠥࠨᑃ") + str(TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)) + bstack11ll111_opy_ (u"ࠣࠤᑄ"))
                self.bstack1l11l11111l_opy_(f, instance, (bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), *args, **kwargs)
            bstack11lll11111_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l11l1lll1l_opy_ = sorted(
                filter(lambda x: x.get(bstack11ll111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᑅ"), None), data.pop(bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᑆ"), {}).values()),
                key=lambda x: x[bstack11ll111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᑇ")],
            )
            if bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_ in data:
                data.pop(bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_)
            data.update({bstack11ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᑈ"): bstack1l11l1lll1l_opy_})
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᑉ"), datetime.now() - bstack11lll11111_opy_)
            bstack11lll11111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11l11l11l_opy_)
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᑊ"), datetime.now() - bstack11lll11111_opy_)
            if TestFramework.bstack1l1l11ll1ll_opy_ in data:
                self.bstack1l11ll11lll_opy_(instance, bstack1ll1ll1llll_opy_, event_json=event_json)
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᑋ"), datetime.now() - bstack1l111llll11_opy_)
    def bstack1l1ll1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
        bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1l11ll1ll_opy_.value)
        self.bstack1l1ll11llll_opy_.bstack1l11l1111l1_opy_(instance, f, bstack1ll1ll1llll_opy_, *args, **kwargs)
        req = self.bstack1l1ll11llll_opy_.bstack1l11l11l1ll_opy_(instance, f, bstack1ll1ll1llll_opy_, *args, **kwargs)
        self.bstack1l111lllll1_opy_(f, instance, req)
        bstack1111l1l1l_opy_.end(EVENTS.bstack1l11ll1ll_opy_.value, bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᑌ"), bstack11llllllll_opy_ + bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᑍ"), status=True, failure=None, test_name=None)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1lllll11_opy_(instance, self.bstack1l1ll11llll_opy_.bstack1l11l1ll11l_opy_, False):
            req = self.bstack1l1ll11llll_opy_.bstack1l11l11l1ll_opy_(instance, f, bstack1ll1ll1llll_opy_, *args, **kwargs)
            self.bstack1l111lllll1_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11ll1ll11_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l111lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵࠢࡪࡖࡕࡉࠠࡤࡣ࡯ࡰ࠿ࠦࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠢᑎ"))
            return
        bstack11lll11111_opy_ = datetime.now()
        try:
            r = self.bstack1l1llllll1l_opy_.TestSessionEvent(req)
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡦࡸࡨࡲࡹࠨᑏ"), datetime.now() - bstack11lll11111_opy_)
            f.bstack1lll11l1111_opy_(instance, self.bstack1l1ll11llll_opy_.bstack1l11l1ll11l_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11ll111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᑐ") + str(r) + bstack11ll111_opy_ (u"ࠢࠣᑑ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᑒ") + str(e) + bstack11ll111_opy_ (u"ࠤࠥᑓ"))
            traceback.print_exc()
            raise e
    def bstack1l11l1l1l11_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        _1l11l11ll1l_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1111ll11_opy_.bstack1l1l1l11111_opy_(method_name):
            return
        if f.bstack1l1l11ll111_opy_(*args) == bstack1ll1111ll11_opy_.bstack1l11ll1l111_opy_:
            bstack1l111llll11_opy_ = datetime.now()
            screenshot = result.get(bstack11ll111_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᑔ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11ll111_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢ࡬ࡱࡦ࡭ࡥࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡷࡶࠧᑕ"))
                return
            bstack1l11ll11ll1_opy_ = self.bstack1l11l111l1l_opy_(instance)
            if bstack1l11ll11ll1_opy_:
                entry = bstack1ll1l1l11ll_opy_(TestFramework.bstack1l11llll1ll_opy_, screenshot)
                self.bstack1l11l11l1l1_opy_(bstack1l11ll11ll1_opy_, [entry])
                instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡࡧࡶࡨࡶࡤ࡫ࡸࡦࡥࡸࡸࡪࠨᑖ"), datetime.now() - bstack1l111llll11_opy_)
            else:
                self.logger.warning(bstack11ll111_opy_ (u"ࠨࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡥࡴࡶࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡩ࡫ࡶࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡹࡤࡷࠥࡺࡡ࡬ࡧࡱࠤࡧࡿࠠࡥࡴ࡬ࡺࡪࡸ࠽ࠡࡽࢀࠦᑗ").format(instance.ref()))
        event = {}
        bstack1l11ll11ll1_opy_ = self.bstack1l11l111l1l_opy_(instance)
        if bstack1l11ll11ll1_opy_:
            self.bstack1l11l111l11_opy_(event, bstack1l11ll11ll1_opy_)
            if event.get(bstack11ll111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᑘ")):
                self.bstack1l11l11l1l1_opy_(bstack1l11ll11ll1_opy_, event[bstack11ll111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᑙ")])
            else:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡ࡮ࡲ࡫ࡸࠦࡦࡰࡴࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡦࡸࡨࡲࡹࠨᑚ"))
    @measure(event_name=EVENTS.bstack1l11l1llll1_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l11l11l1l1_opy_(
        self,
        bstack1l11ll11ll1_opy_: bstack1ll1l111111_opy_,
        entries: List[bstack1ll1l1l11ll_opy_],
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1ll1lll11_opy_)
        req.client_worker_id = bstack11ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᑛ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11ll11ll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11ll11ll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11ll11ll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1ll1ll1l1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l11l1l11l1_opy_)
            log_entry.uuid = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l1l11ll1ll_opy_)
            log_entry.test_framework_state = bstack1l11ll11ll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11ll111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᑜ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11ll111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᑝ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l1ll_opy_
                log_entry.file_path = entry.bstack1_opy_
        def bstack1l11ll1l11l_opy_():
            bstack11lll11111_opy_ = datetime.now()
            try:
                self.bstack1l1llllll1l_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l11llll1ll_opy_:
                    bstack1l11ll11ll1_opy_.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᑞ"), datetime.now() - bstack11lll11111_opy_)
                elif entry.kind == TestFramework.bstack1l11lll1l1l_opy_:
                    bstack1l11ll11ll1_opy_.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᑟ"), datetime.now() - bstack11lll11111_opy_)
                else:
                    bstack1l11ll11ll1_opy_.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧᑠ"), datetime.now() - bstack11lll11111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᑡ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll11llll1_opy_.enqueue(bstack1l11ll1l11l_opy_)
    @measure(event_name=EVENTS.bstack1l11ll1111l_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l11ll11lll_opy_(
        self,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        event_json=None,
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_)
        req.client_worker_id = bstack11ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᑢ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1l11l1_opy_)
        req.test_framework_state = bstack1ll1ll1llll_opy_[0].name
        req.test_hook_state = bstack1ll1ll1llll_opy_[1].name
        started_at = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l1lll11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l11l11llll_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11l11l11l_opy_)).encode(bstack11ll111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᑣ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11ll1l11l_opy_():
            bstack11lll11111_opy_ = datetime.now()
            try:
                self.bstack1l1llllll1l_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣᑤ"), datetime.now() - bstack11lll11111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11ll111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᑥ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll11llll1_opy_.enqueue(bstack1l11ll1l11l_opy_)
    def bstack1l11l111l1l_opy_(self, instance: bstack1ll1lll1111_opy_):
        bstack1l11ll11l11_opy_ = TestFramework.bstack1lll11l11l1_opy_(instance.context)
        for t in bstack1l11ll11l11_opy_:
            bstack1l11lll111l_opy_ = TestFramework.bstack1ll1lllll11_opy_(t, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
            if not bstack1l11l1111ll_opy_() and len(bstack1l11lll111l_opy_) == 0:
                bstack1l11lll111l_opy_ = TestFramework.bstack1ll1lllll11_opy_(t, bstack1ll11l1ll1l_opy_.bstack1l11l1l1l1l_opy_, [])
            if any(instance is d[1] for d in bstack1l11lll111l_opy_):
                return t
    def bstack1l11ll1l1l1_opy_(self, message):
        self.bstack1l11lll1ll1_opy_(message + bstack11ll111_opy_ (u"ࠢ࡝ࡰࠥᑦ"))
    def log_error(self, message):
        self.bstack1l11l111111_opy_(message + bstack11ll111_opy_ (u"ࠣ࡞ࡱࠦᑧ"))
    def bstack1l11llll111_opy_(self, level, original_func):
        def bstack1l11lll11ll_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack11ll111_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᑨ") in message or bstack11ll111_opy_ (u"ࠥ࡟ࡘࡊࡋࡄࡎࡌࡡࠧᑩ") in message or bstack11ll111_opy_ (u"ࠦࡠ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠣᑪ") in message:
                        return return_value
                    bstack1l11ll11l11_opy_ = TestFramework.bstack1l11lllll11_opy_()
                    if not bstack1l11ll11l11_opy_:
                        return return_value
                    bstack1l11ll11ll1_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11ll11l11_opy_
                            if TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
                        ),
                        None,
                    )
                    if not bstack1l11ll11ll1_opy_:
                        return return_value
                    entry = bstack1ll1l1l11ll_opy_(TestFramework.bstack1l111lll111_opy_, message, level)
                    self.bstack1l11l11l1l1_opy_(bstack1l11ll11ll1_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l11lll11ll_opy_
    def bstack1l11l11lll1_opy_(self):
        def bstack1l11lll11l1_opy_(*args, **kwargs):
            try:
                self.bstack1l11l1lllll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack11ll111_opy_ (u"ࠬࠦࠧᑫ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack11ll111_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢᑬ") in message:
                    return
                bstack1l11ll11l11_opy_ = TestFramework.bstack1l11lllll11_opy_()
                if not bstack1l11ll11l11_opy_:
                    return
                bstack1l11ll11ll1_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11ll11l11_opy_
                        if TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
                    ),
                    None,
                )
                if not bstack1l11ll11ll1_opy_:
                    return
                entry = bstack1ll1l1l11ll_opy_(TestFramework.bstack1l111lll111_opy_, message, bstack1l1llll1l11_opy_.bstack1l11ll1lll1_opy_)
                self.bstack1l11l11l1l1_opy_(bstack1l11ll11ll1_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l11l1lllll_opy_(bstack1lll11111l1_opy_ (u"ࠢ࡜ࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠣࡐࡴ࡭ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧᑭ"))
                except:
                    pass
        return bstack1l11lll11l1_opy_
    def bstack1l11l111l11_opy_(self, event: dict, instance=None) -> None:
        global _1l11l1ll1l1_opy_
        levels = [bstack11ll111_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᑮ"), bstack11ll111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᑯ")]
        bstack1l11llll1l1_opy_ = bstack11ll111_opy_ (u"ࠥࠦᑰ")
        if instance is not None:
            try:
                bstack1l11llll1l1_opy_ = TestFramework.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
            except Exception as e:
                self.logger.warning(bstack11ll111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡻࡩࡥࠢࡩࡶࡴࡳࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᑱ").format(e))
        bstack1l11l111ll1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᑲ")]
                bstack1l11ll111ll_opy_ = os.path.join(bstack1l11lll1111_opy_, (bstack1l11lll1l11_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11ll111ll_opy_):
                    self.logger.debug(bstack11ll111_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡱࡳࡹࠦࡰࡳࡧࡶࡩࡳࡺࠠࡧࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡖࡨࡷࡹࠦࡡ࡯ࡦࠣࡆࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᑳ").format(bstack1l11ll111ll_opy_))
                    continue
                file_names = os.listdir(bstack1l11ll111ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11ll111ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11l1ll1l1_opy_:
                        self.logger.info(bstack11ll111_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᑴ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l11ll1llll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l11ll1llll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11ll111_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᑵ"):
                                entry = bstack1ll1l1l11ll_opy_(
                                    kind=bstack11ll111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᑶ"),
                                    message=bstack11ll111_opy_ (u"ࠥࠦᑷ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11ll1l1ll_opy_=file_size,
                                    bstack1l11l11ll11_opy_=bstack11ll111_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᑸ"),
                                    bstack1_opy_=os.path.abspath(file_path),
                                    bstack11ll11l1ll_opy_=bstack1l11llll1l1_opy_
                                )
                            elif level == bstack11ll111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᑹ"):
                                entry = bstack1ll1l1l11ll_opy_(
                                    kind=bstack11ll111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᑺ"),
                                    message=bstack11ll111_opy_ (u"ࠢࠣᑻ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11ll1l1ll_opy_=file_size,
                                    bstack1l11l11ll11_opy_=bstack11ll111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᑼ"),
                                    bstack1_opy_=os.path.abspath(file_path),
                                    bstack1l11lll1lll_opy_=bstack1l11llll1l1_opy_
                                )
                            bstack1l11l111ll1_opy_.append(entry)
                            _1l11l1ll1l1_opy_.add(abs_path)
                        except Exception as bstack1l11l1l111l_opy_:
                            self.logger.error(bstack11ll111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣᑽ").format(bstack1l11l1l111l_opy_))
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᑾ").format(e))
        event[bstack11ll111_opy_ (u"ࠦࡱࡵࡧࡴࠤᑿ")] = bstack1l11l111ll1_opy_
class bstack1l11l11l11l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l111llll1l_opy_ = set()
        kwargs[bstack11ll111_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢᒀ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l11l1ll1ll_opy_(obj, self.bstack1l111llll1l_opy_)
def bstack1l11l1ll111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l11l1ll1ll_opy_(obj, bstack1l111llll1l_opy_=None, max_depth=3):
    if bstack1l111llll1l_opy_ is None:
        bstack1l111llll1l_opy_ = set()
    if id(obj) in bstack1l111llll1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l111llll1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l11lllll1l_opy_ = TestFramework.bstack1l111ll1lll_opy_(obj)
    bstack1l11l1l1lll_opy_ = next((k.lower() in bstack1l11lllll1l_opy_.lower() for k in bstack1l11l1l1111_opy_.keys()), None)
    if bstack1l11l1l1lll_opy_:
        obj = TestFramework.bstack1l11ll111l1_opy_(obj, bstack1l11l1l1111_opy_[bstack1l11l1l1lll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11ll111_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤᒁ")):
            keys = getattr(obj, bstack11ll111_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥᒂ"), [])
        elif hasattr(obj, bstack11ll111_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥᒃ")):
            keys = getattr(obj, bstack11ll111_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦᒄ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11ll111_opy_ (u"ࠥࡣࠧᒅ"))}
        if not obj and bstack1l11lllll1l_opy_ == bstack11ll111_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣᒆ"):
            obj = {bstack11ll111_opy_ (u"ࠧࡶࡡࡵࡪࠥᒇ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l11l1ll111_opy_(key) or str(key).startswith(bstack11ll111_opy_ (u"ࠨ࡟ࠣᒈ")):
            continue
        if value is not None and bstack1l11l1ll111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l11l1ll1ll_opy_(value, bstack1l111llll1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l11l1ll1ll_opy_(o, bstack1l111llll1l_opy_, max_depth) for o in value]))
    return result or None