# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1ll1llll111_opy_, bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1llllll1l_opy_, bstack1l1llll111l_opy_, bstack1ll11lll1ll_opy_, bstack1ll11l111l1_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l111lll111_opy_, bstack1l11ll1111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l11l1llll1_opy_ = [bstack11l1l11_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᐈ"), bstack11l1l11_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧᐉ"), bstack11l1l11_opy_ (u"ࠨࡣࡰࡰࡩ࡭࡬ࠨᐊ"), bstack11l1l11_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣᐋ"), bstack11l1l11_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᐌ")]
bstack1l111lll1l1_opy_ = bstack1l11ll1111l_opy_()
bstack1l11lll1111_opy_ = bstack11l1l11_opy_ (u"ࠤࡘࡴࡱࡵࡡࡥࡧࡧࡅࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠮ࠤᐍ")
bstack1l11l1111ll_opy_ = {
    bstack11l1l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡍࡹ࡫࡭ࠣᐎ"): bstack1l11l1llll1_opy_,
    bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡕࡧࡣ࡬ࡣࡪࡩࠧᐏ"): bstack1l11l1llll1_opy_,
    bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡓ࡯ࡥࡷ࡯ࡩࠧᐐ"): bstack1l11l1llll1_opy_,
    bstack11l1l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡃ࡭ࡣࡶࡷࠧᐑ"): bstack1l11l1llll1_opy_,
    bstack11l1l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡇࡷࡱࡧࡹ࡯࡯࡯ࠤᐒ"): bstack1l11l1llll1_opy_
    + [
        bstack11l1l11_opy_ (u"ࠣࡱࡵ࡭࡬࡯࡮ࡢ࡮ࡱࡥࡲ࡫ࠢᐓ"),
        bstack11l1l11_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦᐔ"),
        bstack11l1l11_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨ࡭ࡳ࡬࡯ࠣᐕ"),
        bstack11l1l11_opy_ (u"ࠦࡰ࡫ࡹࡸࡱࡵࡨࡸࠨᐖ"),
        bstack11l1l11_opy_ (u"ࠧࡩࡡ࡭࡮ࡶࡴࡪࡩࠢᐗ"),
        bstack11l1l11_opy_ (u"ࠨࡣࡢ࡮࡯ࡳࡧࡰࠢᐘ"),
        bstack11l1l11_opy_ (u"ࠢࡴࡶࡤࡶࡹࠨᐙ"),
        bstack11l1l11_opy_ (u"ࠣࡵࡷࡳࡵࠨᐚ"),
        bstack11l1l11_opy_ (u"ࠤࡧࡹࡷࡧࡴࡪࡱࡱࠦᐛ"),
        bstack11l1l11_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᐜ"),
    ],
    bstack11l1l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡩ࡯࠰ࡖࡩࡸࡹࡩࡰࡰࠥᐝ"): [bstack11l1l11_opy_ (u"ࠧࡹࡴࡢࡴࡷࡴࡦࡺࡨࠣᐞ"), bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡷ࡫ࡧࡩ࡭ࡧࡧࠦᐟ"), bstack11l1l11_opy_ (u"ࠢࡵࡧࡶࡸࡸࡩ࡯࡭࡮ࡨࡧࡹ࡫ࡤࠣᐠ"), bstack11l1l11_opy_ (u"ࠣ࡫ࡷࡩࡲࡹࠢᐡ")],
    bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡦࡳࡳ࡬ࡩࡨ࠰ࡆࡳࡳ࡬ࡩࡨࠤᐢ"): [bstack11l1l11_opy_ (u"ࠥ࡭ࡳࡼ࡯ࡤࡣࡷ࡭ࡴࡴ࡟ࡱࡣࡵࡥࡲࡹࠢᐣ"), bstack11l1l11_opy_ (u"ࠦࡦࡸࡧࡴࠤᐤ")],
    bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡇ࡫ࡻࡸࡺࡸࡥࡅࡧࡩࠦᐥ"): [bstack11l1l11_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧᐦ"), bstack11l1l11_opy_ (u"ࠢࡢࡴࡪࡲࡦࡳࡥࠣᐧ"), bstack11l1l11_opy_ (u"ࠣࡨࡸࡲࡨࠨᐨ"), bstack11l1l11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡴࠤᐩ"), bstack11l1l11_opy_ (u"ࠥࡹࡳ࡯ࡴࡵࡧࡶࡸࠧᐪ"), bstack11l1l11_opy_ (u"ࠦ࡮ࡪࡳࠣᐫ")],
    bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳࡬ࡩࡹࡶࡸࡶࡪࡹ࠮ࡔࡷࡥࡖࡪࡷࡵࡦࡵࡷࠦᐬ"): [bstack11l1l11_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫࡮ࡢ࡯ࡨࠦᐭ"), bstack11l1l11_opy_ (u"ࠢࡱࡣࡵࡥࡲࠨᐮ"), bstack11l1l11_opy_ (u"ࠣࡲࡤࡶࡦࡳ࡟ࡪࡰࡧࡩࡽࠨᐯ")],
    bstack11l1l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡵࡹࡳࡴࡥࡳ࠰ࡆࡥࡱࡲࡉ࡯ࡨࡲࠦᐰ"): [bstack11l1l11_opy_ (u"ࠥࡻ࡭࡫࡮ࠣᐱ"), bstack11l1l11_opy_ (u"ࠦࡷ࡫ࡳࡶ࡮ࡷࠦᐲ")],
    bstack11l1l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡏࡱࡧࡩࡐ࡫ࡹࡸࡱࡵࡨࡸࠨᐳ"): [bstack11l1l11_opy_ (u"ࠨ࡮ࡰࡦࡨࠦᐴ"), bstack11l1l11_opy_ (u"ࠢࡱࡣࡵࡩࡳࡺࠢᐵ")],
    bstack11l1l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡑࡦࡸ࡫ࠣᐶ"): [bstack11l1l11_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᐷ"), bstack11l1l11_opy_ (u"ࠥࡥࡷ࡭ࡳࠣᐸ"), bstack11l1l11_opy_ (u"ࠦࡰࡽࡡࡳࡩࡶࠦᐹ")],
}
_1l11l11ll1l_opy_ = set()
class bstack1ll1l1l1lll_opy_(bstack1ll11llll11_opy_):
    bstack1l11ll1l111_opy_ = bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡨࡪ࡬ࡥࡳࡴࡨࡨࠧᐺ")
    bstack1l11l111lll_opy_ = bstack11l1l11_opy_ (u"ࠨࡉࡏࡈࡒࠦᐻ")
    bstack1l11l11ll11_opy_ = bstack11l1l11_opy_ (u"ࠢࡆࡔࡕࡓࡗࠨᐼ")
    bstack1l11l11l1l1_opy_: Callable
    bstack1l11llll11l_opy_: Callable
    def __init__(self, bstack1ll11l1llll_opy_, bstack1l1llll1l11_opy_):
        super().__init__()
        self.bstack1l1l11lllll_opy_ = bstack1l1llll1l11_opy_
        if os.getenv(bstack11l1l11_opy_ (u"ࠣࡕࡇࡏࡤࡉࡌࡊࡡࡉࡐࡆࡍ࡟ࡐ࠳࠴࡝ࠧᐽ"), bstack11l1l11_opy_ (u"ࠤ࠴ࠦᐾ")) != bstack11l1l11_opy_ (u"ࠥ࠵ࠧᐿ") or not self.is_enabled():
            self.logger.warning(bstack11l1l11_opy_ (u"ࠦࠧᑀ") + str(self.__class__.__name__) + bstack11l1l11_opy_ (u"ࠧࠦࡤࡪࡵࡤࡦࡱ࡫ࡤࠣᑁ"))
            return
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.PRE), self.bstack1l1ll11111l_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), self.bstack1l1l1ll11l1_opy_)
        for event in bstack1l1llllll1l_opy_:
            for state in bstack1ll11lll1ll_opy_:
                TestFramework.bstack1l1l11lll1l_opy_((event, state), self.bstack1l11l11111l_opy_)
        bstack1ll11l1llll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.POST), self.bstack1l11l1l1l1l_opy_)
        self.bstack1l11l11l1l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11l11lll1_opy_(bstack1ll1l1l1lll_opy_.bstack1l11l111lll_opy_, self.bstack1l11l11l1l1_opy_)
        self.bstack1l11llll11l_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11l11lll1_opy_(bstack1ll1l1l1lll_opy_.bstack1l11l11ll11_opy_, self.bstack1l11llll11l_opy_)
        self.bstack1l111lll11l_opy_ = builtins.print
        builtins.print = self.bstack1l11l1l1l11_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l11ll111l1_opy_() and instance:
            bstack1l11llll1ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lll11ll111_opy_
            if test_framework_state == bstack1l1llllll1l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1l1llllll1l_opy_.LOG:
                bstack111l11l1l1_opy_ = datetime.now()
                entries = f.bstack1l11ll1l11l_opy_(instance, bstack1lll11ll111_opy_)
                if entries:
                    self.bstack1l11ll11111_opy_(instance, entries)
                    instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࠨᑂ"), datetime.now() - bstack111l11l1l1_opy_)
                    f.bstack1l11l1ll1l1_opy_(instance, bstack1lll11ll111_opy_)
                instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᑃ"), datetime.now() - bstack1l11llll1ll_opy_)
                return # bstack1l11l11llll_opy_ not send this event with the bstack1l11lll111l_opy_ bstack1l111llll11_opy_
            elif (
                test_framework_state == bstack1l1llllll1l_opy_.TEST
                and test_hook_state == bstack1ll11lll1ll_opy_.POST
                and not f.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11l1lllll_opy_)
            ):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡦࡵࡳࡵࡶࡩ࡯ࡩࠣࡨࡺ࡫ࠠࡵࡱࠣࡰࡦࡩ࡫ࠡࡱࡩࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࠨᑄ") + str(TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11l1lllll_opy_)) + bstack11l1l11_opy_ (u"ࠤࠥᑅ"))
                f.bstack1lll111ll11_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l11ll1l111_opy_, True)
                return # bstack1l11l11llll_opy_ not send this event bstack1l11lllll1l_opy_ bstack1l11llll1l1_opy_
            elif (
                f.bstack1ll1lll111l_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1l11ll1l111_opy_, False)
                and test_framework_state == bstack1l1llllll1l_opy_.LOG_REPORT
                and test_hook_state == bstack1ll11lll1ll_opy_.POST
                and f.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11l1lllll_opy_)
            ):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠥ࡭ࡳࡰࡥࡤࡶ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲࡙ࡋࡓࡕ࠮ࠣࡘࡪࡹࡴࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡔࡔ࡙ࡔࠡࠤᑆ") + str(TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l11l1lllll_opy_)) + bstack11l1l11_opy_ (u"ࠦࠧᑇ"))
                self.bstack1l11l11111l_opy_(f, instance, (bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), *args, **kwargs)
            bstack111l11l1l1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l11lllll11_opy_ = sorted(
                filter(lambda x: x.get(bstack11l1l11_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᑈ"), None), data.pop(bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᑉ"), {}).values()),
                key=lambda x: x[bstack11l1l11_opy_ (u"ࠢࡦࡸࡨࡲࡹࡥࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠥᑊ")],
            )
            if bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_ in data:
                data.pop(bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_)
            data.update({bstack11l1l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫ࡳࠣᑋ"): bstack1l11lllll11_opy_})
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠤ࡭ࡷࡴࡴ࠺ࡵࡧࡶࡸࡤ࡬ࡩࡹࡶࡸࡶࡪࡹࠢᑌ"), datetime.now() - bstack111l11l1l1_opy_)
            bstack111l11l1l1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11ll11lll_opy_)
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠥ࡮ࡸࡵ࡮࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨᑍ"), datetime.now() - bstack111l11l1l1_opy_)
            if TestFramework.bstack1l1l11lll11_opy_ in data:
                self.bstack1l111llll11_opy_(instance, bstack1lll11ll111_opy_, event_json=event_json)
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᑎ"), datetime.now() - bstack1l11llll1ll_opy_)
    def bstack1l1ll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
        bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1l1ll1l1ll_opy_.value)
        self.bstack1l1l11lllll_opy_.bstack1l11l1l11l1_opy_(instance, f, bstack1lll11ll111_opy_, *args, **kwargs)
        req = self.bstack1l1l11lllll_opy_.bstack1l111llll1l_opy_(instance, f, bstack1lll11ll111_opy_, *args, **kwargs)
        self.bstack1l11l11l111_opy_(f, instance, req)
        bstack11ll1l1l1_opy_.end(EVENTS.bstack1l1ll1l1ll_opy_.value, bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᑏ"), bstack1l1l1l1111_opy_ + bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᑐ"), status=True, failure=None, test_name=None)
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1ll1lll111l_opy_(instance, self.bstack1l1l11lllll_opy_.bstack1l11l1111l1_opy_, False):
            req = self.bstack1l1l11lllll_opy_.bstack1l111llll1l_opy_(instance, f, bstack1lll11ll111_opy_, *args, **kwargs)
            self.bstack1l11l11l111_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11ll111ll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l11l11l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡔ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡗࡩࡸࡺࡓࡦࡵࡶ࡭ࡴࡴࡅࡷࡧࡱࡸࠥ࡭ࡒࡑࡅࠣࡧࡦࡲ࡬࠻ࠢࡑࡳࠥࡼࡡ࡭࡫ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡪࡡࡵࡣࠥᑑ"))
            return
        bstack111l11l1l1_opy_ = datetime.now()
        try:
            r = self.bstack1ll1ll11111_opy_.TestSessionEvent(req)
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡩࡻ࡫࡮ࡵࠤᑒ"), datetime.now() - bstack111l11l1l1_opy_)
            f.bstack1lll111ll11_opy_(instance, self.bstack1l1l11lllll_opy_.bstack1l11l1111l1_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11l1l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᑓ") + str(r) + bstack11l1l11_opy_ (u"ࠥࠦᑔ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᑕ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨᑖ"))
            traceback.print_exc()
            raise e
    def bstack1l11l1l1l1l_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        _1l111lllll1_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l1lllll1l1_opy_.bstack1l1ll1ll1ll_opy_(method_name):
            return
        if f.bstack1l1l1l11lll_opy_(*args) == bstack1l1lllll1l1_opy_.bstack1l11l1l1ll1_opy_:
            bstack1l11llll1ll_opy_ = datetime.now()
            screenshot = result.get(bstack11l1l11_opy_ (u"ࠨࡶࡢ࡮ࡸࡩࠧᑗ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠥ࡯࡭ࡢࡩࡨࠤࡧࡧࡳࡦ࠸࠷ࠤࡸࡺࡲࠣᑘ"))
                return
            bstack1l111llllll_opy_ = self.bstack1l11ll1ll11_opy_(instance)
            if bstack1l111llllll_opy_:
                entry = bstack1ll11l111l1_opy_(TestFramework.bstack1l11l1ll1ll_opy_, screenshot)
                self.bstack1l11ll11111_opy_(bstack1l111llllll_opy_, [entry])
                instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡧࡻࡩࡨࡻࡴࡦࠤᑙ"), datetime.now() - bstack1l11llll1ll_opy_)
            else:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠤࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡶࡨࡷࡹࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷ࡬࡮ࡹࠠࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠤࡼࡧࡳࠡࡶࡤ࡯ࡪࡴࠠࡣࡻࠣࡨࡷ࡯ࡶࡦࡴࡀࠤࢀࢃࠢᑚ").format(instance.ref()))
        event = {}
        bstack1l111llllll_opy_ = self.bstack1l11ll1ll11_opy_(instance)
        if bstack1l111llllll_opy_:
            self.bstack1l11lll1l1l_opy_(event, bstack1l111llllll_opy_)
            if event.get(bstack11l1l11_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᑛ")):
                self.bstack1l11ll11111_opy_(bstack1l111llllll_opy_, event[bstack11l1l11_opy_ (u"ࠦࡱࡵࡧࡴࠤᑜ")])
            else:
                self.logger.debug(bstack11l1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡱࡵࡧࡴࠢࡩࡳࡷࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡩࡻ࡫࡮ࡵࠤᑝ"))
    @measure(event_name=EVENTS.bstack1l11l11l1ll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l11ll11111_opy_(
        self,
        bstack1l111llllll_opy_: bstack1l1llll111l_opy_,
        entries: List[bstack1ll11l111l1_opy_],
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᑞ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111llllll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111llllll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111llllll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1ll1l1lll_opy_)
            log_entry.test_framework_version = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l11l1l11ll_opy_)
            log_entry.uuid = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l1l11lll11_opy_)
            log_entry.test_framework_state = bstack1l111llllll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᑟ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1l11_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᑠ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11lll1lll_opy_
                log_entry.file_path = entry.bstack1lll1ll_opy_
        def bstack1l11l1l1lll_opy_():
            bstack111l11l1l1_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11111_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l11l1ll1ll_opy_:
                    bstack1l111llllll_opy_.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᑡ"), datetime.now() - bstack111l11l1l1_opy_)
                elif entry.kind == TestFramework.bstack1l11ll11ll1_opy_:
                    bstack1l111llllll_opy_.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠢᑢ"), datetime.now() - bstack111l11l1l1_opy_)
                else:
                    bstack1l111llllll_opy_.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࡣࡱࡵࡧࠣᑣ"), datetime.now() - bstack111l11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᑤ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll1l11111_opy_.enqueue(bstack1l11l1l1lll_opy_)
    @measure(event_name=EVENTS.bstack1l11ll1ll1l_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l111llll11_opy_(
        self,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        event_json=None,
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᑥ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1ll1l1lll_opy_)
        req.test_framework_version = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l1l11ll_opy_)
        req.test_framework_state = bstack1lll11ll111_opy_[0].name
        req.test_hook_state = bstack1lll11ll111_opy_[1].name
        started_at = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11l11l11l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l11llllll1_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11ll11lll_opy_)).encode(bstack11l1l11_opy_ (u"ࠢࡶࡶࡩ࠱࠽ࠨᑦ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11l1l1lll_opy_():
            bstack111l11l1l1_opy_ = datetime.now()
            try:
                self.bstack1ll1ll11111_opy_.TestFrameworkEvent(req)
                instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤ࡫ࡶࡦࡰࡷࠦᑧ"), datetime.now() - bstack111l11l1l1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᑨ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll1l11111_opy_.enqueue(bstack1l11l1l1lll_opy_)
    def bstack1l11ll1ll11_opy_(self, instance: bstack1ll1llll111_opy_):
        bstack1l11l111ll1_opy_ = TestFramework.bstack1ll1ll1ll11_opy_(instance.context)
        for t in bstack1l11l111ll1_opy_:
            bstack1l11llll111_opy_ = TestFramework.bstack1ll1lll111l_opy_(t, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
            if any(instance is d[1] for d in bstack1l11llll111_opy_):
                return t
    def bstack1l11l111l1l_opy_(self, message):
        self.bstack1l11l11l1l1_opy_(message + bstack11l1l11_opy_ (u"ࠥࡠࡳࠨᑩ"))
    def log_error(self, message):
        self.bstack1l11llll11l_opy_(message + bstack11l1l11_opy_ (u"ࠦࡡࡴࠢᑪ"))
    def bstack1l11l11lll1_opy_(self, level, original_func):
        def bstack1l11l1l1111_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack11l1l11_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨᑫ") in message or bstack11l1l11_opy_ (u"ࠨ࡛ࡔࡆࡎࡇࡑࡏ࡝ࠣᑬ") in message or bstack11l1l11_opy_ (u"ࠢ࡜࡙ࡨࡦࡉࡸࡩࡷࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠦᑭ") in message:
                        return return_value
                    bstack1l11l111ll1_opy_ = TestFramework.bstack1l11lll1ll1_opy_()
                    if not bstack1l11l111ll1_opy_:
                        return return_value
                    bstack1l111llllll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11l111ll1_opy_
                            if TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111llllll_opy_:
                        return return_value
                    entry = bstack1ll11l111l1_opy_(TestFramework.bstack1l111lll1ll_opy_, message, level)
                    self.bstack1l11ll11111_opy_(bstack1l111llllll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l11l1l1111_opy_
    def bstack1l11l1l1l11_opy_(self):
        def bstack1l11l1l111l_opy_(*args, **kwargs):
            try:
                self.bstack1l111lll11l_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack11l1l11_opy_ (u"ࠨࠢࠪᑮ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack11l1l11_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᑯ") in message:
                    return
                bstack1l11l111ll1_opy_ = TestFramework.bstack1l11lll1ll1_opy_()
                if not bstack1l11l111ll1_opy_:
                    return
                bstack1l111llllll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11l111ll1_opy_
                        if TestFramework.bstack1lll111l111_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
                    ),
                    None,
                )
                if not bstack1l111llllll_opy_:
                    return
                entry = bstack1ll11l111l1_opy_(TestFramework.bstack1l111lll1ll_opy_, message, bstack1ll1l1l1lll_opy_.bstack1l11l111lll_opy_)
                self.bstack1l11ll11111_opy_(bstack1l111llllll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111lll11l_opy_(bstack1lll11l11ll_opy_ (u"ࠥ࡟ࡊࡼࡥ࡯ࡶࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡓ࡯ࡥࡷ࡯ࡩࡢࠦࡌࡰࡩࠣࡧࡦࡶࡴࡶࡴࡨࠤࡪࡸࡲࡰࡴ࠽ࠤࢀ࡫ࡽࠣᑰ"))
                except:
                    pass
        return bstack1l11l1l111l_opy_
    def bstack1l11lll1l1l_opy_(self, event: dict, instance=None) -> None:
        global _1l11l11ll1l_opy_
        levels = [bstack11l1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᑱ"), bstack11l1l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᑲ")]
        bstack1l11ll11l11_opy_ = bstack11l1l11_opy_ (u"ࠨࠢᑳ")
        if instance is not None:
            try:
                bstack1l11ll11l11_opy_ = TestFramework.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
            except Exception as e:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡧࡦࡶࡷ࡭ࡳ࡭ࠠࡶࡷ࡬ࡨࠥ࡬ࡲࡰ࡯ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠧᑴ").format(e))
        bstack1l11ll1l1l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11l1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᑵ")]
                bstack1l11l111l11_opy_ = os.path.join(bstack1l111lll1l1_opy_, (bstack1l11lll1111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11l111l11_opy_):
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡇ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡴ࡯ࡵࠢࡳࡶࡪࡹࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤ࡙࡫ࡳࡵࠢࡤࡲࡩࠦࡂࡶ࡫࡯ࡨࠥࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᑶ").format(bstack1l11l111l11_opy_))
                    continue
                file_names = os.listdir(bstack1l11l111l11_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11l111l11_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11l11ll1l_opy_:
                        self.logger.info(bstack11l1l11_opy_ (u"ࠥࡔࡦࡺࡨࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥࢁࡽࠣᑷ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l11lll11ll_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l11lll11ll_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11l1l11_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᑸ"):
                                entry = bstack1ll11l111l1_opy_(
                                    kind=bstack11l1l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᑹ"),
                                    message=bstack11l1l11_opy_ (u"ࠨࠢᑺ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11lll1lll_opy_=file_size,
                                    bstack1l11ll1lll1_opy_=bstack11l1l11_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᑻ"),
                                    bstack1lll1ll_opy_=os.path.abspath(file_path),
                                    bstack111ll111ll_opy_=bstack1l11ll11l11_opy_
                                )
                            elif level == bstack11l1l11_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᑼ"):
                                entry = bstack1ll11l111l1_opy_(
                                    kind=bstack11l1l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᑽ"),
                                    message=bstack11l1l11_opy_ (u"ࠥࠦᑾ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11lll1lll_opy_=file_size,
                                    bstack1l11ll1lll1_opy_=bstack11l1l11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᑿ"),
                                    bstack1lll1ll_opy_=os.path.abspath(file_path),
                                    bstack1l11l1ll11l_opy_=bstack1l11ll11l11_opy_
                                )
                            bstack1l11ll1l1l1_opy_.append(entry)
                            _1l11l11ll1l_opy_.add(abs_path)
                        except Exception as bstack1l11ll1llll_opy_:
                            self.logger.error(bstack11l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡴࡤ࡭ࡸ࡫ࡤࠡࡹ࡫ࡩࡳࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳࠡࡽࢀࠦᒀ").format(bstack1l11ll1llll_opy_))
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡵࡥ࡮ࡹࡥࡥࠢࡺ࡬ࡪࡴࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡾࢁࠧᒁ").format(e))
        event[bstack11l1l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᒂ")] = bstack1l11ll1l1l1_opy_
class bstack1l11ll11lll_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l11ll11l1l_opy_ = set()
        kwargs[bstack11l1l11_opy_ (u"ࠣࡵ࡮࡭ࡵࡱࡥࡺࡵࠥᒃ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l11l1ll111_opy_(obj, self.bstack1l11ll11l1l_opy_)
def bstack1l11l1lll1l_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l11l1ll111_opy_(obj, bstack1l11ll11l1l_opy_=None, max_depth=3):
    if bstack1l11ll11l1l_opy_ is None:
        bstack1l11ll11l1l_opy_ = set()
    if id(obj) in bstack1l11ll11l1l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l11ll11l1l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l11l1lll11_opy_ = TestFramework.bstack1l11lll1l11_opy_(obj)
    bstack1l11ll1l1ll_opy_ = next((k.lower() in bstack1l11l1lll11_opy_.lower() for k in bstack1l11l1111ll_opy_.keys()), None)
    if bstack1l11ll1l1ll_opy_:
        obj = TestFramework.bstack1l11l111111_opy_(obj, bstack1l11l1111ll_opy_[bstack1l11ll1l1ll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11l1l11_opy_ (u"ࠤࡢࡣࡸࡲ࡯ࡵࡵࡢࡣࠧᒄ")):
            keys = getattr(obj, bstack11l1l11_opy_ (u"ࠥࡣࡤࡹ࡬ࡰࡶࡶࡣࡤࠨᒅ"), [])
        elif hasattr(obj, bstack11l1l11_opy_ (u"ࠦࡤࡥࡤࡪࡥࡷࡣࡤࠨᒆ")):
            keys = getattr(obj, bstack11l1l11_opy_ (u"ࠧࡥ࡟ࡥ࡫ࡦࡸࡤࡥࠢᒇ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11l1l11_opy_ (u"ࠨ࡟ࠣᒈ"))}
        if not obj and bstack1l11l1lll11_opy_ == bstack11l1l11_opy_ (u"ࠢࡱࡣࡷ࡬ࡱ࡯ࡢ࠯ࡒࡲࡷ࡮ࡾࡐࡢࡶ࡫ࠦᒉ"):
            obj = {bstack11l1l11_opy_ (u"ࠣࡲࡤࡸ࡭ࠨᒊ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l11l1lll1l_opy_(key) or str(key).startswith(bstack11l1l11_opy_ (u"ࠤࡢࠦᒋ")):
            continue
        if value is not None and bstack1l11l1lll1l_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l11l1ll111_opy_(value, bstack1l11ll11l1l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l11l1ll111_opy_(o, bstack1l11ll11l1l_opy_, max_depth) for o in value]))
    return result or None