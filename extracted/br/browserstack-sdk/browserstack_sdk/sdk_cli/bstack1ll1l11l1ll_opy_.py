# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import bstack1lll1l1111l_opy_, bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11lll_opy_ import bstack1ll11l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll111ll_opy_, bstack1ll111l1lll_opy_, bstack1ll1l111111_opy_, bstack1ll11l1l11l_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l1l111l1_opy_, bstack1l1l1111l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l11lllllll_opy_ = [bstack1l1111_opy_ (u"ࠣࡰࡤࡱࡪࠨፏ"), bstack1l1111_opy_ (u"ࠤࡳࡥࡷ࡫࡮ࡵࠤፐ"), bstack1l1111_opy_ (u"ࠥࡧࡴࡴࡦࡪࡩࠥፑ"), bstack1l1111_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࠧፒ"), bstack1l1111_opy_ (u"ࠧࡶࡡࡵࡪࠥፓ")]
bstack1l11ll111ll_opy_ = bstack1l1l1111l11_opy_()
bstack1l1l11l11l1_opy_ = bstack1l1111_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࠨፔ")
bstack1l1l111ll1l_opy_ = {
    bstack1l1111_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡊࡶࡨࡱࠧፕ"): bstack1l11lllllll_opy_,
    bstack1l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡒࡤࡧࡰࡧࡧࡦࠤፖ"): bstack1l11lllllll_opy_,
    bstack1l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡐࡳࡩࡻ࡬ࡦࠤፗ"): bstack1l11lllllll_opy_,
    bstack1l1111_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡇࡱࡧࡳࡴࠤፘ"): bstack1l11lllllll_opy_,
    bstack1l1111_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡋࡻ࡮ࡤࡶ࡬ࡳࡳࠨፙ"): bstack1l11lllllll_opy_
    + [
        bstack1l1111_opy_ (u"ࠧࡵࡲࡪࡩ࡬ࡲࡦࡲ࡮ࡢ࡯ࡨࠦፚ"),
        bstack1l1111_opy_ (u"ࠨ࡫ࡦࡻࡺࡳࡷࡪࡳࠣ፛"),
        bstack1l1111_opy_ (u"ࠢࡧ࡫ࡻࡸࡺࡸࡥࡪࡰࡩࡳࠧ፜"),
        bstack1l1111_opy_ (u"ࠣ࡭ࡨࡽࡼࡵࡲࡥࡵࠥ፝"),
        bstack1l1111_opy_ (u"ࠤࡦࡥࡱࡲࡳࡱࡧࡦࠦ፞"),
        bstack1l1111_opy_ (u"ࠥࡧࡦࡲ࡬ࡰࡤ࡭ࠦ፟"),
        bstack1l1111_opy_ (u"ࠦࡸࡺࡡࡳࡶࠥ፠"),
        bstack1l1111_opy_ (u"ࠧࡹࡴࡰࡲࠥ፡"),
        bstack1l1111_opy_ (u"ࠨࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠣ።"),
        bstack1l1111_opy_ (u"ࠢࡸࡪࡨࡲࠧ፣"),
    ],
    bstack1l1111_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤ࡭ࡳ࠴ࡓࡦࡵࡶ࡭ࡴࡴࠢ፤"): [bstack1l1111_opy_ (u"ࠤࡶࡸࡦࡸࡴࡱࡣࡷ࡬ࠧ፥"), bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡴࡨࡤ࡭ࡱ࡫ࡤࠣ፦"), bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡦࡳࡱࡲࡥࡤࡶࡨࡨࠧ፧"), bstack1l1111_opy_ (u"ࠧ࡯ࡴࡦ࡯ࡶࠦ፨")],
    bstack1l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡣࡰࡰࡩ࡭࡬࠴ࡃࡰࡰࡩ࡭࡬ࠨ፩"): [bstack1l1111_opy_ (u"ࠢࡪࡰࡹࡳࡨࡧࡴࡪࡱࡱࡣࡵࡧࡲࡢ࡯ࡶࠦ፪"), bstack1l1111_opy_ (u"ࠣࡣࡵ࡫ࡸࠨ፫")],
    bstack1l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡋ࡯ࡸࡵࡷࡵࡩࡉ࡫ࡦࠣ፬"): [bstack1l1111_opy_ (u"ࠥࡷࡨࡵࡰࡦࠤ፭"), bstack1l1111_opy_ (u"ࠦࡦࡸࡧ࡯ࡣࡰࡩࠧ፮"), bstack1l1111_opy_ (u"ࠧ࡬ࡵ࡯ࡥࠥ፯"), bstack1l1111_opy_ (u"ࠨࡰࡢࡴࡤࡱࡸࠨ፰"), bstack1l1111_opy_ (u"ࠢࡶࡰ࡬ࡸࡹ࡫ࡳࡵࠤ፱"), bstack1l1111_opy_ (u"ࠣ࡫ࡧࡷࠧ፲")],
    bstack1l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡩ࡭ࡽࡺࡵࡳࡧࡶ࠲ࡘࡻࡢࡓࡧࡴࡹࡪࡹࡴࠣ፳"): [bstack1l1111_opy_ (u"ࠥࡪ࡮ࡾࡴࡶࡴࡨࡲࡦࡳࡥࠣ፴"), bstack1l1111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࠥ፵"), bstack1l1111_opy_ (u"ࠧࡶࡡࡳࡣࡰࡣ࡮ࡴࡤࡦࡺࠥ፶")],
    bstack1l1111_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡲࡶࡰࡱࡩࡷ࠴ࡃࡢ࡮࡯ࡍࡳ࡬࡯ࠣ፷"): [bstack1l1111_opy_ (u"ࠢࡸࡪࡨࡲࠧ፸"), bstack1l1111_opy_ (u"ࠣࡴࡨࡷࡺࡲࡴࠣ፹")],
    bstack1l1111_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥࡷࡱ࠮ࡴࡶࡵࡹࡨࡺࡵࡳࡧࡶ࠲ࡓࡵࡤࡦࡍࡨࡽࡼࡵࡲࡥࡵࠥ፺"): [bstack1l1111_opy_ (u"ࠥࡲࡴࡪࡥࠣ፻"), bstack1l1111_opy_ (u"ࠦࡵࡧࡲࡦࡰࡷࠦ፼")],
    bstack1l1111_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡳࡡࡳ࡭࠱ࡷࡹࡸࡵࡤࡶࡸࡶࡪࡹ࠮ࡎࡣࡵ࡯ࠧ፽"): [bstack1l1111_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ፾"), bstack1l1111_opy_ (u"ࠢࡢࡴࡪࡷࠧ፿"), bstack1l1111_opy_ (u"ࠣ࡭ࡺࡥࡷ࡭ࡳࠣᎀ")],
}
_1l11lll1ll1_opy_ = set()
class bstack1ll11ll1111_opy_(bstack1ll1ll111l1_opy_):
    bstack1l11llll1l1_opy_ = bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡥࡧࡩࡩࡷࡸࡥࡥࠤᎁ")
    bstack1l1l11l111l_opy_ = bstack1l1111_opy_ (u"ࠥࡍࡓࡌࡏࠣᎂ")
    bstack1l11llll11l_opy_ = bstack1l1111_opy_ (u"ࠦࡊࡘࡒࡐࡔࠥᎃ")
    bstack1l11lll11l1_opy_: Callable
    bstack1l11ll1llll_opy_: Callable
    def __init__(self, bstack1ll111l1ll1_opy_, bstack1ll1l1ll1ll_opy_):
        super().__init__()
        self.bstack1l1lll11lll_opy_ = bstack1ll1l1ll1ll_opy_
        if os.getenv(bstack1l1111_opy_ (u"࡙ࠧࡄࡌࡡࡆࡐࡎࡥࡆࡍࡃࡊࡣࡔ࠷࠱࡚ࠤᎄ"), bstack1l1111_opy_ (u"ࠨ࠱ࠣᎅ")) != bstack1l1111_opy_ (u"ࠢ࠲ࠤᎆ") or not self.is_enabled():
            self.logger.warning(bstack1l1111_opy_ (u"ࠣࠤᎇ") + str(self.__class__.__name__) + bstack1l1111_opy_ (u"ࠤࠣࡨ࡮ࡹࡡࡣ࡮ࡨࡨࠧᎈ"))
            return
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.PRE), self.bstack1l1llll1l1l_opy_)
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.POST), self.bstack1l1ll1ll11l_opy_)
        for event in bstack1ll1ll111ll_opy_:
            for state in bstack1ll1l111111_opy_:
                TestFramework.bstack1l1lll1ll11_opy_((event, state), self.bstack1l1l1111l1l_opy_)
        bstack1ll111l1ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.POST), self.bstack1l11lll1l1l_opy_)
        self.bstack1l11lll11l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11ll111l1_opy_(bstack1ll11ll1111_opy_.bstack1l1l11l111l_opy_, self.bstack1l11lll11l1_opy_)
        self.bstack1l11ll1llll_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11ll111l1_opy_(bstack1ll11ll1111_opy_.bstack1l11llll11l_opy_, self.bstack1l11ll1llll_opy_)
        self.bstack1l11ll11l11_opy_ = builtins.print
        builtins.print = self.bstack1l11ll1l1l1_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l11lll11ll_opy_() and instance:
            bstack1l1l111llll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lll111llll_opy_
            if test_framework_state == bstack1ll1ll111ll_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll1ll111ll_opy_.LOG:
                bstack1ll1lll11l_opy_ = datetime.now()
                entries = f.bstack1l11ll11lll_opy_(instance, bstack1lll111llll_opy_)
                if entries:
                    self.bstack1l1l111l1ll_opy_(instance, entries)
                    instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡵࡨࡲࡩࡥ࡬ࡰࡩࡢࡧࡷ࡫ࡡࡵࡧࡧࡣࡪࡼࡥ࡯ࡶࠥᎉ"), datetime.now() - bstack1ll1lll11l_opy_)
                    f.bstack1l11lllll11_opy_(instance, bstack1lll111llll_opy_)
                instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧ࡬࡭ࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡹࠢᎊ"), datetime.now() - bstack1l1l111llll_opy_)
                return # bstack1l11lll111l_opy_ not send this event with the bstack1l1l11l1l1l_opy_ bstack1l11ll11l1l_opy_
            elif (
                test_framework_state == bstack1ll1ll111ll_opy_.TEST
                and test_hook_state == bstack1ll1l111111_opy_.POST
                and not f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111lll_opy_)
            ):
                self.logger.warning(bstack1l1111_opy_ (u"ࠧࡪࡲࡰࡲࡳ࡭ࡳ࡭ࠠࡥࡷࡨࠤࡹࡵࠠ࡭ࡣࡦ࡯ࠥࡵࡦࠡࡴࡨࡷࡺࡲࡴࡴࠢࠥᎋ") + str(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111lll_opy_)) + bstack1l1111_opy_ (u"ࠨࠢᎌ"))
                f.bstack1lll11l1ll1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l11llll1l1_opy_, True)
                return # bstack1l11lll111l_opy_ not send this event bstack1l11l1lllll_opy_ bstack1l1l111lll1_opy_
            elif (
                f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1111_opy_.bstack1l11llll1l1_opy_, False)
                and test_framework_state == bstack1ll1ll111ll_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1l111111_opy_.POST
                and f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111lll_opy_)
            ):
                self.logger.warning(bstack1l1111_opy_ (u"ࠢࡪࡰ࡭ࡩࡨࡺࡩ࡯ࡩࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡖࡸࡦࡺࡥ࠯ࡖࡈࡗ࡙࠲ࠠࡕࡧࡶࡸࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡑࡑࡖࡘࠥࠨᎍ") + str(TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111lll_opy_)) + bstack1l1111_opy_ (u"ࠣࠤᎎ"))
                self.bstack1l1l1111l1l_opy_(f, instance, (bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.POST), *args, **kwargs)
            bstack1ll1lll11l_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l11l1111_opy_ = sorted(
                filter(lambda x: x.get(bstack1l1111_opy_ (u"ࠤࡨࡺࡪࡴࡴࡠࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠧᎏ"), None), data.pop(bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥ᎐"), {}).values()),
                key=lambda x: x[bstack1l1111_opy_ (u"ࠦࡪࡼࡥ࡯ࡶࡢࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠢ᎑")],
            )
            if bstack1ll11l1l1l1_opy_.bstack1l11llll1ll_opy_ in data:
                data.pop(bstack1ll11l1l1l1_opy_.bstack1l11llll1ll_opy_)
            data.update({bstack1l1111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧ᎒"): bstack1l1l11l1111_opy_})
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦ᎓"), datetime.now() - bstack1ll1lll11l_opy_)
            bstack1ll1lll11l_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1l1l11111_opy_)
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥ᎔"), datetime.now() - bstack1ll1lll11l_opy_)
            self.bstack1l11ll11l1l_opy_(instance, bstack1lll111llll_opy_, event_json=event_json)
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡱ࠴࠵ࡾࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦ᎕"), datetime.now() - bstack1l1l111llll_opy_)
    def bstack1l1llll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
        bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack111lll1l11_opy_.value)
        self.bstack1l1lll11lll_opy_.bstack1l11l1llll1_opy_(instance, f, bstack1lll111llll_opy_, *args, **kwargs)
        req = self.bstack1l1lll11lll_opy_.bstack1l11llllll1_opy_(instance, f, bstack1lll111llll_opy_, *args, **kwargs)
        self.bstack1l11lll1lll_opy_(f, instance, req)
        bstack11ll111lll_opy_.end(EVENTS.bstack111lll1l11_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᎖"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᎗"), status=True, failure=None, test_name=None)
    def bstack1l1ll1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll1l11lll_opy_(instance, self.bstack1l1lll11lll_opy_.bstack1l1l111ll11_opy_, False):
            req = self.bstack1l1lll11lll_opy_.bstack1l11llllll1_opy_(instance, f, bstack1lll111llll_opy_, *args, **kwargs)
            self.bstack1l11lll1lll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11ll1l111_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l11lll1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡘࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡔࡦࡵࡷࡗࡪࡹࡳࡪࡱࡱࡉࡻ࡫࡮ࡵࠢࡪࡖࡕࡉࠠࡤࡣ࡯ࡰ࠿ࠦࡎࡰࠢࡹࡥࡱ࡯ࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡧࡥࡹࡧࠢ᎘"))
            return
        bstack1ll1lll11l_opy_ = datetime.now()
        try:
            r = self.bstack1ll1111l1ll_opy_.TestSessionEvent(req)
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡳࡦࡵࡶ࡭ࡴࡴ࡟ࡦࡸࡨࡲࡹࠨ᎙"), datetime.now() - bstack1ll1lll11l_opy_)
            f.bstack1lll11l1ll1_opy_(instance, self.bstack1l1lll11lll_opy_.bstack1l1l111ll11_opy_, r.success)
            if not r.success:
                self.logger.info(bstack1l1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ᎚") + str(r) + bstack1l1111_opy_ (u"ࠢࠣ᎛"))
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ᎜") + str(e) + bstack1l1111_opy_ (u"ࠤࠥ᎝"))
            traceback.print_exc()
            raise e
    def bstack1l11lll1l1l_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        _driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        _1l1l1111ll1_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1l111l1l_opy_.bstack1l1llll111l_opy_(method_name):
            return
        if f.bstack1l1ll111ll1_opy_(*args) == bstack1ll1l111l1l_opy_.bstack1l11ll1ll11_opy_:
            bstack1l1l111llll_opy_ = datetime.now()
            screenshot = result.get(bstack1l1111_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤ᎞"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack1l1111_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢ࡬ࡱࡦ࡭ࡥࠡࡤࡤࡷࡪ࠼࠴ࠡࡵࡷࡶࠧ᎟"))
                return
            bstack1l11l1lll11_opy_ = self.bstack1l1l11111ll_opy_(instance)
            if bstack1l11l1lll11_opy_:
                entry = bstack1ll11l1l11l_opy_(TestFramework.bstack1l11ll1lll1_opy_, screenshot)
                self.bstack1l1l111l1ll_opy_(bstack1l11l1lll11_opy_, [entry])
                instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡࡧࡶࡨࡶࡤ࡫ࡸࡦࡥࡸࡸࡪࠨᎠ"), datetime.now() - bstack1l1l111llll_opy_)
            else:
                self.logger.warning(bstack1l1111_opy_ (u"ࠨࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡺࡥࡴࡶࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡩ࡫ࡶࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡࡹࡤࡷࠥࡺࡡ࡬ࡧࡱࠤࡧࡿࠠࡥࡴ࡬ࡺࡪࡸ࠽ࠡࡽࢀࠦᎡ").format(instance.ref()))
        event = {}
        bstack1l11l1lll11_opy_ = self.bstack1l1l11111ll_opy_(instance)
        if bstack1l11l1lll11_opy_:
            self.bstack1l1l11lll1l_opy_(event, bstack1l11l1lll11_opy_)
            if event.get(bstack1l1111_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᎢ")):
                self.bstack1l1l111l1ll_opy_(bstack1l11l1lll11_opy_, event[bstack1l1111_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᎣ")])
            else:
                self.logger.debug(bstack1l1111_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡ࡮ࡲ࡫ࡸࠦࡦࡰࡴࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡦࡸࡨࡲࡹࠨᎤ"))
    @measure(event_name=EVENTS.bstack1l11l1lll1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l1l111l1ll_opy_(
        self,
        bstack1l11l1lll11_opy_: bstack1ll111l1lll_opy_,
        entries: List[bstack1ll11l1l11l_opy_],
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1ll1l11ll_opy_)
        req.client_worker_id = bstack1l1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᎥ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11l1lll11_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11l1lll11_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11l1lll11_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1lll1ll1l_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1l1l1111l_opy_)
            log_entry.uuid = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l1lll111ll_opy_)
            log_entry.test_framework_state = bstack1l11l1lll11_opy_.state.name
            log_entry.message = entry.message.encode(bstack1l1111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᎦ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack1l1111_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᎧ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l11l_opy_
                log_entry.file_path = entry.bstack1llllll1_opy_
        def bstack1l11ll1111l_opy_():
            bstack1ll1lll11l_opy_ = datetime.now()
            try:
                self.bstack1ll1111l1ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l11ll1lll1_opy_:
                    bstack1l11l1lll11_opy_.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥᎨ"), datetime.now() - bstack1ll1lll11l_opy_)
                elif entry.kind == TestFramework.bstack1l1l111l11l_opy_:
                    bstack1l11l1lll11_opy_.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠦᎩ"), datetime.now() - bstack1ll1lll11l_opy_)
                else:
                    bstack1l11l1lll11_opy_.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠ࡮ࡲ࡫ࠧᎪ"), datetime.now() - bstack1ll1lll11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎫ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll1llll1l_opy_.enqueue(bstack1l11ll1111l_opy_)
    @measure(event_name=EVENTS.bstack1l1l11111l1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l11ll11l1l_opy_(
        self,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        event_json=None,
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1ll1l11ll_opy_)
        req.client_worker_id = bstack1l1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᎬ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1l1l1111l_opy_)
        req.test_framework_state = bstack1lll111llll_opy_[0].name
        req.test_hook_state = bstack1lll111llll_opy_[1].name
        started_at = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l11lll1l11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1l11l1l11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1l1l11111_opy_)).encode(bstack1l1111_opy_ (u"ࠦࡺࡺࡦ࠮࠺ࠥᎭ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11ll1111l_opy_():
            bstack1ll1lll11l_opy_ = datetime.now()
            try:
                self.bstack1ll1111l1ll_opy_.TestFrameworkEvent(req)
                instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡨࡺࡪࡴࡴࠣᎮ"), datetime.now() - bstack1ll1lll11l_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack1l1111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᎯ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll1llll1l_opy_.enqueue(bstack1l11ll1111l_opy_)
    def bstack1l1l11111ll_opy_(self, instance: bstack1lll1l1111l_opy_):
        bstack1l11lllll1l_opy_ = TestFramework.bstack1lll11l1l11_opy_(instance.context)
        for t in bstack1l11lllll1l_opy_:
            bstack1l1l111l1l1_opy_ = TestFramework.bstack1lll1l11lll_opy_(t, bstack1ll11l1l1l1_opy_.bstack1l11llll1ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1l111l1l1_opy_):
                return t
    def bstack1l1l11ll1ll_opy_(self, message):
        self.bstack1l11lll11l1_opy_(message + bstack1l1111_opy_ (u"ࠢ࡝ࡰࠥᎰ"))
    def log_error(self, message):
        self.bstack1l11ll1llll_opy_(message + bstack1l1111_opy_ (u"ࠣ࡞ࡱࠦᎱ"))
    def bstack1l11ll111l1_opy_(self, level, original_func):
        def bstack1l11llll111_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack1l1111_opy_ (u"ࠤࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࠥᎲ") in message or bstack1l1111_opy_ (u"ࠥ࡟ࡘࡊࡋࡄࡎࡌࡡࠧᎳ") in message or bstack1l1111_opy_ (u"ࠦࡠ࡝ࡥࡣࡆࡵ࡭ࡻ࡫ࡲࡎࡱࡧࡹࡱ࡫࡝ࠣᎴ") in message:
                        return return_value
                    bstack1l11lllll1l_opy_ = TestFramework.bstack1l1l11ll111_opy_()
                    if not bstack1l11lllll1l_opy_:
                        return return_value
                    bstack1l11l1lll11_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11lllll1l_opy_
                            if TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
                        ),
                        None,
                    )
                    if not bstack1l11l1lll11_opy_:
                        return return_value
                    entry = bstack1ll11l1l11l_opy_(TestFramework.bstack1l1l11ll11l_opy_, message, level)
                    self.bstack1l1l111l1ll_opy_(bstack1l11l1lll11_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l11llll111_opy_
    def bstack1l11ll1l1l1_opy_(self):
        def bstack1l11ll11ll1_opy_(*args, **kwargs):
            try:
                self.bstack1l11ll11l11_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack1l1111_opy_ (u"ࠬࠦࠧᎵ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack1l1111_opy_ (u"ࠨࡅࡷࡧࡱࡸࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࡎࡱࡧࡹࡱ࡫ࠢᎶ") in message:
                    return
                bstack1l11lllll1l_opy_ = TestFramework.bstack1l1l11ll111_opy_()
                if not bstack1l11lllll1l_opy_:
                    return
                bstack1l11l1lll11_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11lllll1l_opy_
                        if TestFramework.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
                    ),
                    None,
                )
                if not bstack1l11l1lll11_opy_:
                    return
                entry = bstack1ll11l1l11l_opy_(TestFramework.bstack1l1l11ll11l_opy_, message, bstack1ll11ll1111_opy_.bstack1l1l11l111l_opy_)
                self.bstack1l1l111l1ll_opy_(bstack1l11l1lll11_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l11ll11l11_opy_(bstack1ll1ll1l1ll_opy_ (u"ࠢ࡜ࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦ࡟ࠣࡐࡴ࡭ࠠࡤࡣࡳࡸࡺࡸࡥࠡࡧࡵࡶࡴࡸ࠺ࠡࡽࡨࢁࠧᎷ"))
                except:
                    pass
        return bstack1l11ll11ll1_opy_
    def bstack1l1l11lll1l_opy_(self, event: dict, instance=None) -> None:
        global _1l11lll1ll1_opy_
        levels = [bstack1l1111_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᎸ"), bstack1l1111_opy_ (u"ࠤࡅࡹ࡮ࡲࡤࡍࡧࡹࡩࡱࠨᎹ")]
        bstack1l1l11l1lll_opy_ = bstack1l1111_opy_ (u"ࠥࠦᎺ")
        if instance is not None:
            try:
                bstack1l1l11l1lll_opy_ = TestFramework.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
            except Exception as e:
                self.logger.warning(bstack1l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡺࡻࡩࡥࠢࡩࡶࡴࡳࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᎻ").format(e))
        bstack1l1l11ll1l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᎼ")]
                bstack1l11ll1ll1l_opy_ = os.path.join(bstack1l11ll111ll_opy_, (bstack1l1l11l11l1_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11ll1ll1l_opy_):
                    self.logger.debug(bstack1l1111_opy_ (u"ࠨࡄࡪࡴࡨࡧࡹࡵࡲࡺࠢࡱࡳࡹࠦࡰࡳࡧࡶࡩࡳࡺࠠࡧࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡖࡨࡷࡹࠦࡡ࡯ࡦࠣࡆࡺ࡯࡬ࡥࠢ࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᎽ").format(bstack1l11ll1ll1l_opy_))
                    continue
                file_names = os.listdir(bstack1l11ll1ll1l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11ll1ll1l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11lll1ll1_opy_:
                        self.logger.info(bstack1l1111_opy_ (u"ࠢࡑࡣࡷ࡬ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡾࢁࠧᎾ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l111l111_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l111l111_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack1l1111_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᎿ"):
                                entry = bstack1ll11l1l11l_opy_(
                                    kind=bstack1l1111_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᏀ"),
                                    message=bstack1l1111_opy_ (u"ࠥࠦᏁ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11ll1l11l_opy_=file_size,
                                    bstack1l11ll1l1ll_opy_=bstack1l1111_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᏂ"),
                                    bstack1llllll1_opy_=os.path.abspath(file_path),
                                    bstack1l1l11l11l_opy_=bstack1l1l11l1lll_opy_
                                )
                            elif level == bstack1l1111_opy_ (u"ࠧࡈࡵࡪ࡮ࡧࡐࡪࡼࡥ࡭ࠤᏃ"):
                                entry = bstack1ll11l1l11l_opy_(
                                    kind=bstack1l1111_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᏄ"),
                                    message=bstack1l1111_opy_ (u"ࠢࠣᏅ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11ll1l11l_opy_=file_size,
                                    bstack1l11ll1l1ll_opy_=bstack1l1111_opy_ (u"ࠣࡏࡄࡒ࡚ࡇࡌࡠࡗࡓࡐࡔࡇࡄࠣᏆ"),
                                    bstack1llllll1_opy_=os.path.abspath(file_path),
                                    bstack1l1l11lllll_opy_=bstack1l1l11l1lll_opy_
                                )
                            bstack1l1l11ll1l1_opy_.append(entry)
                            _1l11lll1ll1_opy_.add(abs_path)
                        except Exception as bstack1l1l11l1ll1_opy_:
                            self.logger.error(bstack1l1111_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣᏇ").format(bstack1l1l11l1ll1_opy_))
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᏈ").format(e))
        event[bstack1l1111_opy_ (u"ࠦࡱࡵࡧࡴࠤᏉ")] = bstack1l1l11ll1l1_opy_
class bstack1l1l1l11111_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1l11lll11_opy_ = set()
        kwargs[bstack1l1111_opy_ (u"ࠧࡹ࡫ࡪࡲ࡮ࡩࡾࡹࠢᏊ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l11llll1_opy_(obj, self.bstack1l1l11lll11_opy_)
def bstack1l11lll1111_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l11llll1_opy_(obj, bstack1l1l11lll11_opy_=None, max_depth=3):
    if bstack1l1l11lll11_opy_ is None:
        bstack1l1l11lll11_opy_ = set()
    if id(obj) in bstack1l1l11lll11_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1l11lll11_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l11ll11111_opy_ = TestFramework.bstack1l1l11l11ll_opy_(obj)
    bstack1l1l111111l_opy_ = next((k.lower() in bstack1l11ll11111_opy_.lower() for k in bstack1l1l111ll1l_opy_.keys()), None)
    if bstack1l1l111111l_opy_:
        obj = TestFramework.bstack1l1l1111111_opy_(obj, bstack1l1l111ll1l_opy_[bstack1l1l111111l_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack1l1111_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤᏋ")):
            keys = getattr(obj, bstack1l1111_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥᏌ"), [])
        elif hasattr(obj, bstack1l1111_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥᏍ")):
            keys = getattr(obj, bstack1l1111_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦᏎ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack1l1111_opy_ (u"ࠥࡣࠧᏏ"))}
        if not obj and bstack1l11ll11111_opy_ == bstack1l1111_opy_ (u"ࠦࡵࡧࡴࡩ࡮࡬ࡦ࠳ࡖ࡯ࡴ࡫ࡻࡔࡦࡺࡨࠣᏐ"):
            obj = {bstack1l1111_opy_ (u"ࠧࡶࡡࡵࡪࠥᏑ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l11lll1111_opy_(key) or str(key).startswith(bstack1l1111_opy_ (u"ࠨ࡟ࠣᏒ")):
            continue
        if value is not None and bstack1l11lll1111_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l11llll1_opy_(value, bstack1l1l11lll11_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l11llll1_opy_(o, bstack1l1l11lll11_opy_, max_depth) for o in value]))
    return result or None