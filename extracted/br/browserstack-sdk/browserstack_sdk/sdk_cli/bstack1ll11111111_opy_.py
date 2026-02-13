# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import bstack1ll1l1ll1ll_opy_, bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11lllll1_opy_ import bstack1ll1l111l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1lllllll1_opy_, bstack1ll11l111ll_opy_, bstack1l1lllll1ll_opy_, bstack1l1lll1l11l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l111lllll1_opy_, bstack1l11l11l11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l11ll1lll1_opy_ = [bstack11l11_opy_ (u"ࠣࡰࡤࡱࡪࠨ᏾"), bstack11l11_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤ᏿"), bstack11l11_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥ᐀"), bstack11l11_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧᐁ"), bstack11l11_opy_ (u"ࠧࡶࡡࡵࡪࠥᐂ")]
bstack1l11l1ll11l_opy_ = bstack1l11l11l11l_opy_()
bstack1l111l1l1l1_opy_ = bstack11l11_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨᐃ")
bstack1l11l1l1ll1_opy_ = {
    bstack11l11_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡊࡶࡨࡱࠧᐄ"): bstack1l11ll1lll1_opy_,
    bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡒࡤࡧࡰࡧࡧࡦࠤᐅ"): bstack1l11ll1lll1_opy_,
    bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡐࡳࡩࡻ࡬ࡦࠤᐆ"): bstack1l11ll1lll1_opy_,
    bstack11l11_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡇࡱࡧࡳࡴࠤᐇ"): bstack1l11ll1lll1_opy_,
    bstack11l11_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡋࡻ࡮ࡤࡶ࡬ࡳࡳࠨᐈ"): bstack1l11ll1lll1_opy_
    + [
        bstack11l11_opy_ (u"ࠧࡵࡲࡪࡩ࡬ࡲࡦࡲ࡮ࡢ࡯ࡨࠦᐉ"),
        bstack11l11_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣᐊ"),
        bstack11l11_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࡪࡰࡩࡳࠧᐋ"),
        bstack11l11_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥᐌ"),
        bstack11l11_opy_ (u"ࠤࡦࡥࡱࡲࡳࡱࡧࡦࠦᐍ"),
        bstack11l11_opy_ (u"ࠥࡧࡦࡲ࡬ࡰࡤ࡭ࠦᐎ"),
        bstack11l11_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥᐏ"),
        bstack11l11_opy_ (u"ࠧࡹࡴࡰࡲࠥᐐ"),
        bstack11l11_opy_ (u"ࠨࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠣᐑ"),
        bstack11l11_opy_ (u"ࠢࡸࡪࡨࡲࠧᐒ"),
    ],
    bstack11l11_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤ࡭ࡳ࠴ࡓࡦࡵࡶ࡭ࡴࡴࠢᐓ"): [bstack11l11_opy_ (u"ࠤࡶࡸࡦࡸࡴࡱࡣࡷ࡬ࠧᐔ"), bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡴࡨࡤ࡭ࡱ࡫ࡤࠣᐕ"), bstack11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧᐖ"), bstack11l11_opy_ (u"ࠧ࡯ࡴࡦ࡯ࡶࠦᐗ")],
    bstack11l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡣࡰࡰࡩ࡭࡬࠴ࡃࡰࡰࡩ࡭࡬ࠨᐘ"): [bstack11l11_opy_ (u"ࠢࡪࡰࡹࡳࡨࡧࡴࡪࡱࡱࡣࡵࡧࡲࡢ࡯ࡶࠦᐙ"), bstack11l11_opy_ (u"ࠣࡣࡵ࡫ࡸࠨᐚ")],
    bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡋ࡯ࡸࡵࡷࡵࡩࡉ࡫ࡦࠣᐛ"): [bstack11l11_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤᐜ"), bstack11l11_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧᐝ"), bstack11l11_opy_ (u"ࠧ࡬ࡵ࡯ࡥࠥᐞ"), bstack11l11_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨᐟ"), bstack11l11_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤᐠ"), bstack11l11_opy_ (u"ࠣ࡫ࡧࡷࠧᐡ")],
    bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡘࡻࡢࡓࡧࡴࡹࡪࡹࡴࠣᐢ"): [bstack11l11_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣᐣ"), bstack11l11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࠥᐤ"), bstack11l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡣ࡮ࡴࡤࡦࡺࠥᐥ")],
    bstack11l11_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡲࡶࡰࡱࡩࡷ࠴ࡃࡢ࡮࡯ࡍࡳ࡬࡯ࠣᐦ"): [bstack11l11_opy_ (u"ࠢࡸࡪࡨࡲࠧᐧ"), bstack11l11_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࠣᐨ")],
    bstack11l11_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡓࡵࡤࡦࡍࡨࡽࡼࡵࡲࡥࡵࠥᐩ"): [bstack11l11_opy_ (u"ࠥࡲࡴࡪࡥࠣᐪ"), bstack11l11_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦᐫ")],
    bstack11l11_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡎࡣࡵ࡯ࠧᐬ"): [bstack11l11_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᐭ"), bstack11l11_opy_ (u"ࠢࡢࡴࡪࡷࠧᐮ"), bstack11l11_opy_ (u"ࠣ࡭ࡺࡥࡷ࡭ࡳࠣᐯ")],
}
_1l111lll1ll_opy_ = set()
class bstack1ll11ll1lll_opy_(bstack1l1ll1lll11_opy_):
    bstack1l11ll11lll_opy_ = bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࠤᐰ")
    bstack1l11ll1ll1l_opy_ = bstack11l11_opy_ (u"ࠥࡍࡓࡌࡏࠣᐱ")
    bstack1l11l1l1111_opy_ = bstack11l11_opy_ (u"ࠦࡊࡘࡒࡐࡔࠥᐲ")
    bstack1l111ll11ll_opy_: Callable
    bstack1l11l1ll1ll_opy_: Callable
    def __init__(self, bstack1ll1111ll1l_opy_, bstack1ll111l1l1l_opy_):
        super().__init__()
        self.bstack1l1l11llll1_opy_ = bstack1ll111l1l1l_opy_
        if os.getenv(bstack11l11_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡔ࠷࠱࡚ࠤᐳ"), bstack11l11_opy_ (u"ࠨ࠱ࠣᐴ")) != bstack11l11_opy_ (u"ࠢ࠲ࠤᐵ") or not self.is_enabled():
            self.logger.warning(bstack11l11_opy_ (u"ࠣࠤᐶ") + str(self.__class__.__name__) + bstack11l11_opy_ (u"ࠤࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠧᐷ"))
            return
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.PRE), self.bstack1l1l11ll111_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), self.bstack1l1l1llll11_opy_)
        for event in bstack1l1lllllll1_opy_:
            for state in bstack1l1lllll1ll_opy_:
                TestFramework.bstack1l1l1l111ll_opy_((event, state), self.bstack1l11ll1l1ll_opy_)
        bstack1ll1111ll1l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.POST), self.bstack1l11l1l1l11_opy_)
        self.bstack1l111ll11ll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11l111ll1_opy_(bstack1ll11ll1lll_opy_.bstack1l11ll1ll1l_opy_, self.bstack1l111ll11ll_opy_)
        self.bstack1l11l1ll1ll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11l111ll1_opy_(bstack1ll11ll1lll_opy_.bstack1l11l1l1111_opy_, self.bstack1l11l1ll1ll_opy_)
        self.bstack1l111l1l1ll_opy_ = builtins.print
        builtins.print = self.bstack1l11ll11111_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l11l1lll1l_opy_() and instance:
            bstack1l111ll1lll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1ll1l1lll1l_opy_
            if test_framework_state == bstack1l1lllllll1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1l1lllllll1_opy_.LOG:
                bstack1lllll111_opy_ = datetime.now()
                entries = f.bstack1l11l11lll1_opy_(instance, bstack1ll1l1lll1l_opy_)
                if entries:
                    self.bstack1l11l11l111_opy_(instance, entries)
                    instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥᐸ"), datetime.now() - bstack1lllll111_opy_)
                    f.bstack1l111llll11_opy_(instance, bstack1ll1l1lll1l_opy_)
                instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᐹ"), datetime.now() - bstack1l111ll1lll_opy_)
                return # bstack1l111llllll_opy_ not send this event with the bstack1l11l1llll1_opy_ bstack1l11l1lll11_opy_
            elif (
                test_framework_state == bstack1l1lllllll1_opy_.TEST
                and test_hook_state == bstack1l1lllll1ll_opy_.POST
                and not f.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l111llll1l_opy_)
            ):
                self.logger.warning(bstack11l11_opy_ (u"ࠧࡪࡲࡰࡲࡳ࡭ࡳ࡭ࠠࡥࡷࡨࠤࡹࡵࠠ࡭ࡣࡦ࡯ࠥࡵࡦࠡࡴࡨࡷࡺࡲࡴࡴࠢࠥᐺ") + str(TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l111llll1l_opy_)) + bstack11l11_opy_ (u"ࠨࠢᐻ"))
                f.bstack1ll1lll111l_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l11ll11lll_opy_, True)
                return # bstack1l111llllll_opy_ not send this event bstack1l11ll111ll_opy_ bstack1l11l11llll_opy_
            elif (
                f.bstack1lll111111l_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l11ll11lll_opy_, False)
                and test_framework_state == bstack1l1lllllll1_opy_.LOG_REPORT
                and test_hook_state == bstack1l1lllll1ll_opy_.POST
                and f.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l111llll1l_opy_)
            ):
                self.logger.warning(bstack11l11_opy_ (u"ࠢࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡖࡈࡗ࡙࠲ࠠࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡑࡑࡖࡘࠥࠨᐼ") + str(TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l111llll1l_opy_)) + bstack11l11_opy_ (u"ࠣࠤᐽ"))
                self.bstack1l11ll1l1ll_opy_(f, instance, (bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), *args, **kwargs)
            bstack1lllll111_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l11l11l1l1_opy_ = sorted(
                filter(lambda x: x.get(bstack11l11_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᐾ"), None), data.pop(bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥᐿ"), {}).values()),
                key=lambda x: x[bstack11l11_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢᑀ")],
            )
            if bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_ in data:
                data.pop(bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_)
            data.update({bstack11l11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᑁ"): bstack1l11l11l1l1_opy_})
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᑂ"), datetime.now() - bstack1lllll111_opy_)
            bstack1lllll111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11ll11l11_opy_)
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥᑃ"), datetime.now() - bstack1lllll111_opy_)
            if TestFramework.bstack1l1l11l11l1_opy_ in data:
                self.bstack1l11l1lll11_opy_(instance, bstack1ll1l1lll1l_opy_, event_json=event_json)
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᑄ"), datetime.now() - bstack1l111ll1lll_opy_)
    def bstack1l1l11ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
        bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1111lll11l_opy_.value)
        self.bstack1l1l11llll1_opy_.bstack1l11l1ll1l1_opy_(instance, f, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        req = self.bstack1l1l11llll1_opy_.bstack1l11l111l1l_opy_(instance, f, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        self.bstack1l11ll1llll_opy_(f, instance, req)
        bstack111l1lllll_opy_.end(EVENTS.bstack1111lll11l_opy_.value, bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᑅ"), bstack1l111l111l_opy_ + bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᑆ"), status=True, failure=None, test_name=None)
    def bstack1l1l1llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll111111l_opy_(instance, self.bstack1l1l11llll1_opy_.bstack1l11l1lllll_opy_, False):
            req = self.bstack1l1l11llll1_opy_.bstack1l11l111l1l_opy_(instance, f, bstack1ll1l1lll1l_opy_, *args, **kwargs)
            self.bstack1l11ll1llll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11ll11ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l11ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵࠢࡪࡖࡕࡉࠠࡤࡣ࡯ࡰ࠿ࠦࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠢᑇ"))
            return
        bstack1lllll111_opy_ = datetime.now()
        try:
            r = self.bstack1ll1l1l1lll_opy_.TestSessionEvent(req)
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡦࡸࡨࡲࡹࠨᑈ"), datetime.now() - bstack1lllll111_opy_)
            f.bstack1ll1lll111l_opy_(instance, self.bstack1l1l11llll1_opy_.bstack1l11l1lllll_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᑉ") + str(r) + bstack11l11_opy_ (u"ࠢࠣᑊ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᑋ") + str(e) + bstack11l11_opy_ (u"ࠤࠥᑌ"))
            traceback.print_exc()
            raise e
    def bstack1l11l1l1l11_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        _driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        _1l111ll1ll1_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1l1llllllll_opy_.bstack1l1l1l1ll1l_opy_(method_name):
            return
        if f.bstack1l1l11ll11l_opy_(*args) == bstack1l1llllllll_opy_.bstack1l11l11111l_opy_:
            bstack1l111ll1lll_opy_ = datetime.now()
            screenshot = result.get(bstack11l11_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤᑍ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11l11_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢ࡬ࡱࡦ࡭ࡥࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡷࡶࠧᑎ"))
                return
            bstack1l111l1ll1l_opy_ = self.bstack1l11ll111l1_opy_(instance)
            if bstack1l111l1ll1l_opy_:
                entry = bstack1l1lll1l11l_opy_(TestFramework.bstack1l111lll111_opy_, screenshot)
                self.bstack1l11l11l111_opy_(bstack1l111l1ll1l_opy_, [entry])
                instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡࡧࡶࡨࡶࡤ࡫ࡸࡦࡥࡸࡸࡪࠨᑏ"), datetime.now() - bstack1l111ll1lll_opy_)
            else:
                self.logger.warning(bstack11l11_opy_ (u"ࠨࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡥࡴࡶࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡩ࡫ࡶࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡹࡤࡷࠥࡺࡡ࡬ࡧࡱࠤࡧࡿࠠࡥࡴ࡬ࡺࡪࡸ࠽ࠡࡽࢀࠦᑐ").format(instance.ref()))
        event = {}
        bstack1l111l1ll1l_opy_ = self.bstack1l11ll111l1_opy_(instance)
        if bstack1l111l1ll1l_opy_:
            self.bstack1l11l111lll_opy_(event, bstack1l111l1ll1l_opy_)
            if event.get(bstack11l11_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᑑ")):
                self.bstack1l11l11l111_opy_(bstack1l111l1ll1l_opy_, event[bstack11l11_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᑒ")])
            else:
                self.logger.debug(bstack11l11_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡ࡮ࡲ࡫ࡸࠦࡦࡰࡴࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡦࡸࡨࡲࡹࠨᑓ"))
    @measure(event_name=EVENTS.bstack1l11l1l1lll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l11l11l111_opy_(
        self,
        bstack1l111l1ll1l_opy_: bstack1ll11l111ll_opy_,
        entries: List[bstack1l1lll1l11l_opy_],
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l111l11l_opy_)
        req.client_worker_id = bstack11l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᑔ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l111l1ll1l_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l111l1ll1l_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l111l1ll1l_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l1l11l11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l11l111l11_opy_)
            log_entry.uuid = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l1l11l11l1_opy_)
            log_entry.test_framework_state = bstack1l111l1ll1l_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᑕ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l11_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᑖ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l111ll11l1_opy_
                log_entry.file_path = entry.bstack1111l1_opy_
        def bstack1l11ll11l1l_opy_():
            bstack1lllll111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1lll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l111lll111_opy_:
                    bstack1l111l1ll1l_opy_.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᑗ"), datetime.now() - bstack1lllll111_opy_)
                elif entry.kind == TestFramework.bstack1l111ll1l11_opy_:
                    bstack1l111l1ll1l_opy_.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᑘ"), datetime.now() - bstack1lllll111_opy_)
                else:
                    bstack1l111l1ll1l_opy_.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧᑙ"), datetime.now() - bstack1lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᑚ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll111lll1_opy_.enqueue(bstack1l11ll11l1l_opy_)
    @measure(event_name=EVENTS.bstack1l11l1l111l_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l11l1lll11_opy_(
        self,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        event_json=None,
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l111l11l_opy_)
        req.client_worker_id = bstack11l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᑛ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l1l11l11_opy_)
        req.test_framework_version = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l11l111l11_opy_)
        req.test_framework_state = bstack1ll1l1lll1l_opy_[0].name
        req.test_hook_state = bstack1ll1l1lll1l_opy_[1].name
        started_at = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l111ll1l1l_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l11l1ll111_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11ll11l11_opy_)).encode(bstack11l11_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᑜ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11ll11l1l_opy_():
            bstack1lllll111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1lll_opy_.TestFrameworkEvent(req)
                instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣᑝ"), datetime.now() - bstack1lllll111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᑞ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll111lll1_opy_.enqueue(bstack1l11ll11l1l_opy_)
    def bstack1l11ll111l1_opy_(self, instance: bstack1ll1l1ll1ll_opy_):
        bstack1l111ll1111_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance.context)
        for t in bstack1l111ll1111_opy_:
            bstack1l11l11l1ll_opy_ = TestFramework.bstack1lll111111l_opy_(t, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
            if any(instance is d[1] for d in bstack1l11l11l1ll_opy_):
                return t
    def bstack1l11l1l11l1_opy_(self, message):
        self.bstack1l111ll11ll_opy_(message + bstack11l11_opy_ (u"ࠢ࡝ࡰࠥᑟ"))
    def log_error(self, message):
        self.bstack1l11l1ll1ll_opy_(message + bstack11l11_opy_ (u"ࠣ࡞ࡱࠦᑠ"))
    def bstack1l11l111ll1_opy_(self, level, original_func):
        def bstack1l111l1llll_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack11l11_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᑡ") in message or bstack11l11_opy_ (u"ࠥ࡟ࡘࡊࡋࡄࡎࡌࡡࠧᑢ") in message or bstack11l11_opy_ (u"ࠦࡠ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠣᑣ") in message:
                        return return_value
                    bstack1l111ll1111_opy_ = TestFramework.bstack1l11ll1111l_opy_()
                    if not bstack1l111ll1111_opy_:
                        return return_value
                    bstack1l111l1ll1l_opy_ = next(
                        (
                            instance
                            for instance in bstack1l111ll1111_opy_
                            if TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
                        ),
                        None,
                    )
                    if not bstack1l111l1ll1l_opy_:
                        return return_value
                    entry = bstack1l1lll1l11l_opy_(TestFramework.bstack1l11ll1l111_opy_, message, level)
                    self.bstack1l11l11l111_opy_(bstack1l111l1ll1l_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l111l1llll_opy_
    def bstack1l11ll11111_opy_(self):
        def bstack1l11l1111l1_opy_(*args, **kwargs):
            try:
                self.bstack1l111l1l1ll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack11l11_opy_ (u"ࠬࠦࠧᑤ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack11l11_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢᑥ") in message:
                    return
                bstack1l111ll1111_opy_ = TestFramework.bstack1l11ll1111l_opy_()
                if not bstack1l111ll1111_opy_:
                    return
                bstack1l111l1ll1l_opy_ = next(
                    (
                        instance
                        for instance in bstack1l111ll1111_opy_
                        if TestFramework.bstack1ll1l1lll11_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
                    ),
                    None,
                )
                if not bstack1l111l1ll1l_opy_:
                    return
                entry = bstack1l1lll1l11l_opy_(TestFramework.bstack1l11ll1l111_opy_, message, bstack1ll11ll1lll_opy_.bstack1l11ll1ll1l_opy_)
                self.bstack1l11l11l111_opy_(bstack1l111l1ll1l_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l111l1l1ll_opy_(bstack1ll1lllll11_opy_ (u"ࠢ࡜ࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠣࡐࡴ࡭ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧᑦ"))
                except:
                    pass
        return bstack1l11l1111l1_opy_
    def bstack1l11l111lll_opy_(self, event: dict, instance=None) -> None:
        global _1l111lll1ll_opy_
        levels = [bstack11l11_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᑧ"), bstack11l11_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᑨ")]
        bstack1l11l11ll11_opy_ = bstack11l11_opy_ (u"ࠥࠦᑩ")
        if instance is not None:
            try:
                bstack1l11l11ll11_opy_ = TestFramework.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
            except Exception as e:
                self.logger.warning(bstack11l11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡻࡩࡥࠢࡩࡶࡴࡳࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᑪ").format(e))
        bstack1l111l1l11l_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᑫ")]
                bstack1l11l1111ll_opy_ = os.path.join(bstack1l11l1ll11l_opy_, (bstack1l111l1l1l1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11l1111ll_opy_):
                    self.logger.debug(bstack11l11_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡱࡳࡹࠦࡰࡳࡧࡶࡩࡳࡺࠠࡧࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡖࡨࡷࡹࠦࡡ࡯ࡦࠣࡆࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᑬ").format(bstack1l11l1111ll_opy_))
                    continue
                file_names = os.listdir(bstack1l11l1111ll_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11l1111ll_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l111lll1ll_opy_:
                        self.logger.info(bstack11l11_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᑭ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l111ll111l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l111ll111l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11l11_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᑮ"):
                                entry = bstack1l1lll1l11l_opy_(
                                    kind=bstack11l11_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᑯ"),
                                    message=bstack11l11_opy_ (u"ࠥࠦᑰ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l111ll11l1_opy_=file_size,
                                    bstack1l11l11ll1l_opy_=bstack11l11_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᑱ"),
                                    bstack1111l1_opy_=os.path.abspath(file_path),
                                    bstack1ll1l1111l_opy_=bstack1l11l11ll11_opy_
                                )
                            elif level == bstack11l11_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᑲ"):
                                entry = bstack1l1lll1l11l_opy_(
                                    kind=bstack11l11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᑳ"),
                                    message=bstack11l11_opy_ (u"ࠢࠣᑴ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l111ll11l1_opy_=file_size,
                                    bstack1l11l11ll1l_opy_=bstack11l11_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᑵ"),
                                    bstack1111l1_opy_=os.path.abspath(file_path),
                                    bstack1l111lll1l1_opy_=bstack1l11l11ll11_opy_
                                )
                            bstack1l111l1l11l_opy_.append(entry)
                            _1l111lll1ll_opy_.add(abs_path)
                        except Exception as bstack1l11ll1l11l_opy_:
                            self.logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣᑶ").format(bstack1l11ll1l11l_opy_))
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᑷ").format(e))
        event[bstack11l11_opy_ (u"ࠦࡱࡵࡧࡴࠤᑸ")] = bstack1l111l1l11l_opy_
class bstack1l11ll11l11_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l111lll11l_opy_ = set()
        kwargs[bstack11l11_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢᑹ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l11l1l1l1l_opy_(obj, self.bstack1l111lll11l_opy_)
def bstack1l111l1ll11_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l11l1l1l1l_opy_(obj, bstack1l111lll11l_opy_=None, max_depth=3):
    if bstack1l111lll11l_opy_ is None:
        bstack1l111lll11l_opy_ = set()
    if id(obj) in bstack1l111lll11l_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l111lll11l_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l111l1lll1_opy_ = TestFramework.bstack1l11ll1l1l1_opy_(obj)
    bstack1l11l111111_opy_ = next((k.lower() in bstack1l111l1lll1_opy_.lower() for k in bstack1l11l1l1ll1_opy_.keys()), None)
    if bstack1l11l111111_opy_:
        obj = TestFramework.bstack1l11ll1ll11_opy_(obj, bstack1l11l1l1ll1_opy_[bstack1l11l111111_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11l11_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤᑺ")):
            keys = getattr(obj, bstack11l11_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥᑻ"), [])
        elif hasattr(obj, bstack11l11_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥᑼ")):
            keys = getattr(obj, bstack11l11_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦᑽ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11l11_opy_ (u"ࠥࡣࠧᑾ"))}
        if not obj and bstack1l111l1lll1_opy_ == bstack11l11_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣᑿ"):
            obj = {bstack11l11_opy_ (u"ࠧࡶࡡࡵࡪࠥᒀ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l111l1ll11_opy_(key) or str(key).startswith(bstack11l11_opy_ (u"ࠨ࡟ࠣᒁ")):
            continue
        if value is not None and bstack1l111l1ll11_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l11l1l1l1l_opy_(value, bstack1l111lll11l_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l11l1l1l1l_opy_(o, bstack1l111lll11l_opy_, max_depth) for o in value]))
    return result or None