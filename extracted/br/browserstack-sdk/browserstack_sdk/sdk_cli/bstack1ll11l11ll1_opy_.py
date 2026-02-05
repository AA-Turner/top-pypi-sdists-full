# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1lll11lll1l_opy_, bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l11_opy_ import bstack1ll1l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11l1l1l1_opy_, bstack1ll1ll111l1_opy_, bstack1ll1111llll_opy_, bstack1ll1lll11ll_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l1l1111ll1_opy_, bstack1l11ll1ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l11lll1l11_opy_ = [bstack11l1ll1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧፕ"), bstack11l1ll1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࠣፖ"), bstack11l1ll1_opy_ (u"ࠤࡦࡳࡳ࡬ࡩࡨࠤፗ"), bstack11l1ll1_opy_ (u"ࠥࡷࡪࡹࡳࡪࡱࡱࠦፘ"), bstack11l1ll1_opy_ (u"ࠦࡵࡧࡴࡩࠤፙ")]
bstack1l1l111ll1l_opy_ = bstack1l11ll1ll1l_opy_()
bstack1l11ll1l111_opy_ = bstack11l1ll1_opy_ (u"࡛ࠧࡰ࡭ࡱࡤࡨࡪࡪࡁࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠱ࠧፚ")
bstack1l1l1111lll_opy_ = {
    bstack11l1ll1_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴ࡰࡺࡶ࡫ࡳࡳ࠴ࡉࡵࡧࡰࠦ፛"): bstack1l11lll1l11_opy_,
    bstack11l1ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡱࡻࡷ࡬ࡴࡴ࠮ࡑࡣࡦ࡯ࡦ࡭ࡥࠣ፜"): bstack1l11lll1l11_opy_,
    bstack11l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡏࡲࡨࡺࡲࡥࠣ፝"): bstack1l11lll1l11_opy_,
    bstack11l1ll1_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡆࡰࡦࡹࡳࠣ፞"): bstack1l11lll1l11_opy_,
    bstack11l1ll1_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡊࡺࡴࡣࡵ࡫ࡲࡲࠧ፟"): bstack1l11lll1l11_opy_
    + [
        bstack11l1ll1_opy_ (u"ࠦࡴࡸࡩࡨ࡫ࡱࡥࡱࡴࡡ࡮ࡧࠥ፠"),
        bstack11l1ll1_opy_ (u"ࠧࡱࡥࡺࡹࡲࡶࡩࡹࠢ፡"),
        bstack11l1ll1_opy_ (u"ࠨࡦࡪࡺࡷࡹࡷ࡫ࡩ࡯ࡨࡲࠦ።"),
        bstack11l1ll1_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤ፣"),
        bstack11l1ll1_opy_ (u"ࠣࡥࡤࡰࡱࡹࡰࡦࡥࠥ፤"),
        bstack11l1ll1_opy_ (u"ࠤࡦࡥࡱࡲ࡯ࡣ࡬ࠥ፥"),
        bstack11l1ll1_opy_ (u"ࠥࡷࡹࡧࡲࡵࠤ፦"),
        bstack11l1ll1_opy_ (u"ࠦࡸࡺ࡯ࡱࠤ፧"),
        bstack11l1ll1_opy_ (u"ࠧࡪࡵࡳࡣࡷ࡭ࡴࡴࠢ፨"),
        bstack11l1ll1_opy_ (u"ࠨࡷࡩࡧࡱࠦ፩"),
    ],
    bstack11l1ll1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮࡮ࡣ࡬ࡲ࠳࡙ࡥࡴࡵ࡬ࡳࡳࠨ፪"): [bstack11l1ll1_opy_ (u"ࠣࡵࡷࡥࡷࡺࡰࡢࡶ࡫ࠦ፫"), bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡳࡧࡣ࡬ࡰࡪࡪࠢ፬"), bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡴࡥࡲࡰࡱ࡫ࡣࡵࡧࡧࠦ፭"), bstack11l1ll1_opy_ (u"ࠦ࡮ࡺࡥ࡮ࡵࠥ፮")],
    bstack11l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡩ࡯࡯ࡨ࡬࡫࠳ࡉ࡯࡯ࡨ࡬࡫ࠧ፯"): [bstack11l1ll1_opy_ (u"ࠨࡩ࡯ࡸࡲࡧࡦࡺࡩࡰࡰࡢࡴࡦࡸࡡ࡮ࡵࠥ፰"), bstack11l1ll1_opy_ (u"ࠢࡢࡴࡪࡷࠧ፱")],
    bstack11l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡊ࡮ࡾࡴࡶࡴࡨࡈࡪ࡬ࠢ፲"): [bstack11l1ll1_opy_ (u"ࠤࡶࡧࡴࡶࡥࠣ፳"), bstack11l1ll1_opy_ (u"ࠥࡥࡷ࡭࡮ࡢ࡯ࡨࠦ፴"), bstack11l1ll1_opy_ (u"ࠦ࡫ࡻ࡮ࡤࠤ፵"), bstack11l1ll1_opy_ (u"ࠧࡶࡡࡳࡣࡰࡷࠧ፶"), bstack11l1ll1_opy_ (u"ࠨࡵ࡯࡫ࡷࡸࡪࡹࡴࠣ፷"), bstack11l1ll1_opy_ (u"ࠢࡪࡦࡶࠦ፸")],
    bstack11l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡨ࡬ࡼࡹࡻࡲࡦࡵ࠱ࡗࡺࡨࡒࡦࡳࡸࡩࡸࡺࠢ፹"): [bstack11l1ll1_opy_ (u"ࠤࡩ࡭ࡽࡺࡵࡳࡧࡱࡥࡲ࡫ࠢ፺"), bstack11l1ll1_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࠤ፻"), bstack11l1ll1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡢ࡭ࡳࡪࡥࡹࠤ፼")],
    bstack11l1ll1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡸࡵ࡯ࡰࡨࡶ࠳ࡉࡡ࡭࡮ࡌࡲ࡫ࡵࠢ፽"): [bstack11l1ll1_opy_ (u"ࠨࡷࡩࡧࡱࠦ፾"), bstack11l1ll1_opy_ (u"ࠢࡳࡧࡶࡹࡱࡺࠢ፿")],
    bstack11l1ll1_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯࡯ࡤࡶࡰ࠴ࡳࡵࡴࡸࡧࡹࡻࡲࡦࡵ࠱ࡒࡴࡪࡥࡌࡧࡼࡻࡴࡸࡤࡴࠤᎀ"): [bstack11l1ll1_opy_ (u"ࠤࡱࡳࡩ࡫ࠢᎁ"), bstack11l1ll1_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥᎂ")],
    bstack11l1ll1_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡲࡧࡲ࡬࠰ࡶࡸࡷࡻࡣࡵࡷࡵࡩࡸ࠴ࡍࡢࡴ࡮ࠦᎃ"): [bstack11l1ll1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎄ"), bstack11l1ll1_opy_ (u"ࠨࡡࡳࡩࡶࠦᎅ"), bstack11l1ll1_opy_ (u"ࠢ࡬ࡹࡤࡶ࡬ࡹࠢᎆ")],
}
_1l11llll111_opy_ = set()
class bstack1ll111l1lll_opy_(bstack1ll1l11l1ll_opy_):
    bstack1l11lllllll_opy_ = bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡤࡦࡨࡨࡶࡷ࡫ࡤࠣᎇ")
    bstack1l1l111l111_opy_ = bstack11l1ll1_opy_ (u"ࠤࡌࡒࡋࡕࠢᎈ")
    bstack1l11ll1111l_opy_ = bstack11l1ll1_opy_ (u"ࠥࡉࡗࡘࡏࡓࠤᎉ")
    bstack1l11ll1l1ll_opy_: Callable
    bstack1l11lllll11_opy_: Callable
    def __init__(self, bstack1ll1lllll1l_opy_, bstack1ll1llllll1_opy_):
        super().__init__()
        self.bstack1l1l1lll1ll_opy_ = bstack1ll1llllll1_opy_
        if os.getenv(bstack11l1ll1_opy_ (u"ࠦࡘࡊࡋࡠࡅࡏࡍࡤࡌࡌࡂࡉࡢࡓ࠶࠷࡙ࠣᎊ"), bstack11l1ll1_opy_ (u"ࠧ࠷ࠢᎋ")) != bstack11l1ll1_opy_ (u"ࠨ࠱ࠣᎌ") or not self.is_enabled():
            self.logger.warning(bstack11l1ll1_opy_ (u"ࠢࠣᎍ") + str(self.__class__.__name__) + bstack11l1ll1_opy_ (u"ࠣࠢࡧ࡭ࡸࡧࡢ࡭ࡧࡧࠦᎎ"))
            return
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.PRE), self.bstack1l1ll11ll11_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), self.bstack1l1llll1ll1_opy_)
        for event in bstack1ll11l1l1l1_opy_:
            for state in bstack1ll1111llll_opy_:
                TestFramework.bstack1l1ll11llll_opy_((event, state), self.bstack1l1l111ll11_opy_)
        bstack1ll1lllll1l_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.POST), self.bstack1l1l111l1ll_opy_)
        self.bstack1l11ll1l1ll_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l1l11lll1l_opy_(bstack1ll111l1lll_opy_.bstack1l1l111l111_opy_, self.bstack1l11ll1l1ll_opy_)
        self.bstack1l11lllll11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l1l11lll1l_opy_(bstack1ll111l1lll_opy_.bstack1l11ll1111l_opy_, self.bstack1l11lllll11_opy_)
        self.bstack1l1l11lllll_opy_ = builtins.print
        builtins.print = self.bstack1l1l11l1lll_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1l11l11l1_opy_() and instance:
            bstack1l11l1llll1_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lll1l1ll11_opy_
            if test_framework_state == bstack1ll11l1l1l1_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll11l1l1l1_opy_.LOG:
                bstack111ll1ll1_opy_ = datetime.now()
                entries = f.bstack1l11llll1ll_opy_(instance, bstack1lll1l1ll11_opy_)
                if entries:
                    self.bstack1l11lll1lll_opy_(instance, entries)
                    instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࠤᎏ"), datetime.now() - bstack111ll1ll1_opy_)
                    f.bstack1l11lll11ll_opy_(instance, bstack1lll1l1ll11_opy_)
                instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠥࡳ࠶࠷ࡹ࠻ࡱࡱࡣࡦࡲ࡬ࡠࡶࡨࡷࡹࡥࡥࡷࡧࡱࡸࡸࠨ᎐"), datetime.now() - bstack1l11l1llll1_opy_)
                return # bstack1l1l11l1111_opy_ not send this event with the bstack1l1l11ll1l1_opy_ bstack1l11l1ll11l_opy_
            elif (
                test_framework_state == bstack1ll11l1l1l1_opy_.TEST
                and test_hook_state == bstack1ll1111llll_opy_.POST
                and not f.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
            ):
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠦࡩࡸ࡯ࡱࡲ࡬ࡲ࡬ࠦࡤࡶࡧࠣࡸࡴࠦ࡬ࡢࡥ࡮ࠤࡴ࡬ࠠࡳࡧࡶࡹࡱࡺࡳࠡࠤ᎑") + str(TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)) + bstack11l1ll1_opy_ (u"ࠧࠨ᎒"))
                f.bstack1lll1l1111l_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11lllllll_opy_, True)
                return # bstack1l1l11l1111_opy_ not send this event bstack1l11ll11111_opy_ bstack1l11ll11l11_opy_
            elif (
                f.bstack1lll1ll11l1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l11lllllll_opy_, False)
                and test_framework_state == bstack1ll11l1l1l1_opy_.LOG_REPORT
                and test_hook_state == bstack1ll1111llll_opy_.POST
                and f.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
            ):
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠨࡩ࡯࡬ࡨࡧࡹ࡯࡮ࡨࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡕࡇࡖࡘ࠱ࠦࡔࡦࡵࡷࡌࡴࡵ࡫ࡔࡶࡤࡸࡪ࠴ࡐࡐࡕࡗࠤࠧ᎓") + str(TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)) + bstack11l1ll1_opy_ (u"ࠢࠣ᎔"))
                self.bstack1l1l111ll11_opy_(f, instance, (bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), *args, **kwargs)
            bstack111ll1ll1_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l11ll1ll_opy_ = sorted(
                filter(lambda x: x.get(bstack11l1ll1_opy_ (u"ࠣࡧࡹࡩࡳࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠦ᎕"), None), data.pop(bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡴࠤ᎖"), {}).values()),
                key=lambda x: x[bstack11l1ll1_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨ᎗")],
            )
            if bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_ in data:
                data.pop(bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_)
            data.update({bstack11l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦ᎘"): bstack1l1l11ll1ll_opy_})
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠧࡰࡳࡰࡰ࠽ࡸࡪࡹࡴࡠࡨ࡬ࡼࡹࡻࡲࡦࡵࠥ᎙"), datetime.now() - bstack111ll1ll1_opy_)
            bstack111ll1ll1_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l1l11llll1_opy_)
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠨࡪࡴࡱࡱ࠾ࡴࡴ࡟ࡢ࡮࡯ࡣࡹ࡫ࡳࡵࡡࡨࡺࡪࡴࡴࡴࠤ᎚"), datetime.now() - bstack111ll1ll1_opy_)
            if TestFramework.bstack1l1llll1l11_opy_ in data:
                self.bstack1l11l1ll11l_opy_(instance, bstack1lll1l1ll11_opy_, event_json=event_json)
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠢࡰ࠳࠴ࡽ࠿ࡵ࡮ࡠࡣ࡯ࡰࡤࡺࡥࡴࡶࡢࡩࡻ࡫࡮ࡵࡵࠥ᎛"), datetime.now() - bstack1l11l1llll1_opy_)
    def bstack1l1ll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
        bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack1111l1lll_opy_.value)
        self.bstack1l1l1lll1ll_opy_.bstack1l1l1111l1l_opy_(instance, f, bstack1lll1l1ll11_opy_, *args, **kwargs)
        req = self.bstack1l1l1lll1ll_opy_.bstack1l11ll111l1_opy_(instance, f, bstack1lll1l1ll11_opy_, *args, **kwargs)
        self.bstack1l11ll11lll_opy_(f, instance, req)
        bstack1ll1111ll_opy_.end(EVENTS.bstack1111l1lll_opy_.value, bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᎜"), bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᎝"), status=True, failure=None, test_name=None)
    def bstack1l1llll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll1ll11l1_opy_(instance, self.bstack1l1l1lll1ll_opy_.bstack1l1l1111l11_opy_, False):
            req = self.bstack1l1l1lll1ll_opy_.bstack1l11ll111l1_opy_(instance, f, bstack1lll1l1ll11_opy_, *args, **kwargs)
            self.bstack1l11ll11lll_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11ll11ll1_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l11ll11lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡗࡰ࡯ࡰࡱ࡫ࡱ࡫࡚ࠥࡥࡴࡶࡖࡩࡸࡹࡩࡰࡰࡈࡺࡪࡴࡴࠡࡩࡕࡔࡈࠦࡣࡢ࡮࡯࠾ࠥࡔ࡯ࠡࡸࡤࡰ࡮ࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡦࡤࡸࡦࠨ᎞"))
            return
        bstack111ll1ll1_opy_ = datetime.now()
        try:
            r = self.bstack1ll1llll1ll_opy_.TestSessionEvent(req)
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡥࡷࡧࡱࡸࠧ᎟"), datetime.now() - bstack111ll1ll1_opy_)
            f.bstack1lll1l1111l_opy_(instance, self.bstack1l1l1lll1ll_opy_.bstack1l1l1111l11_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11l1ll1_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᎠ") + str(r) + bstack11l1ll1_opy_ (u"ࠨࠢᎡ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᎢ") + str(e) + bstack11l1ll1_opy_ (u"ࠣࠤᎣ"))
            traceback.print_exc()
            raise e
    def bstack1l1l111l1ll_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        _driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        _1l1l111l11l_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1ll1ll1lll1_opy_.bstack1l1ll111111_opy_(method_name):
            return
        if f.bstack1l1llll11l1_opy_(*args) == bstack1ll1ll1lll1_opy_.bstack1l1l11l11ll_opy_:
            bstack1l11l1llll1_opy_ = datetime.now()
            screenshot = result.get(bstack11l1ll1_opy_ (u"ࠤࡹࡥࡱࡻࡥࠣᎤ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠥ࡭ࡳࡼࡡ࡭࡫ࡧࠤࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࠡ࡫ࡰࡥ࡬࡫ࠠࡣࡣࡶࡩ࠻࠺ࠠࡴࡶࡵࠦᎥ"))
                return
            bstack1l11lll1ll1_opy_ = self.bstack1l1l11ll111_opy_(instance)
            if bstack1l11lll1ll1_opy_:
                entry = bstack1ll1lll11ll_opy_(TestFramework.bstack1l1l11ll11l_opy_, screenshot)
                self.bstack1l11lll1lll_opy_(bstack1l11lll1ll1_opy_, [entry])
                instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠦࡴ࠷࠱ࡺ࠼ࡲࡲࡤࡧࡦࡵࡧࡵࡣࡪࡾࡥࡤࡷࡷࡩࠧᎦ"), datetime.now() - bstack1l11l1llll1_opy_)
            else:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠧࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡦࡨࡸࡪࡸ࡭ࡪࡰࡨࠤࡹ࡫ࡳࡵࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺࡨࡪࡵࠣࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠠࡸࡣࡶࠤࡹࡧ࡫ࡦࡰࠣࡦࡾࠦࡤࡳ࡫ࡹࡩࡷࡃࠠࡼࡿࠥᎧ").format(instance.ref()))
        event = {}
        bstack1l11lll1ll1_opy_ = self.bstack1l1l11ll111_opy_(instance)
        if bstack1l11lll1ll1_opy_:
            self.bstack1l11ll1l11l_opy_(event, bstack1l11lll1ll1_opy_)
            if event.get(bstack11l1ll1_opy_ (u"ࠨ࡬ࡰࡩࡶࠦᎨ")):
                self.bstack1l11lll1lll_opy_(bstack1l11lll1ll1_opy_, event[bstack11l1ll1_opy_ (u"ࠢ࡭ࡱࡪࡷࠧᎩ")])
            else:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡭ࡱࡪࡷࠥ࡬࡯ࡳࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡥࡷࡧࡱࡸࠧᎪ"))
    @measure(event_name=EVENTS.bstack1l11l1lll1l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l11lll1lll_opy_(
        self,
        bstack1l11lll1ll1_opy_: bstack1ll1ll111l1_opy_,
        entries: List[bstack1ll1lll11ll_opy_],
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1l1lll1l1_opy_)
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᎫ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l11lll1ll1_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l11lll1ll1_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l11lll1ll1_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1llllll11_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1l111llll_opy_)
            log_entry.uuid = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l1llll1l11_opy_)
            log_entry.test_framework_state = bstack1l11lll1ll1_opy_.state.name
            log_entry.message = entry.message.encode(bstack11l1ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᎬ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11l1ll1_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᎭ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l11ll1l1l1_opy_
                log_entry.file_path = entry.bstack1ll1lll_opy_
        def bstack1l11ll1llll_opy_():
            bstack111ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1ll1llll1ll_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1l11ll11l_opy_:
                    bstack1l11lll1ll1_opy_.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡷࡪࡴࡤࡠ࡮ࡲ࡫ࡤࡩࡲࡦࡣࡷࡩࡩࡥࡥࡷࡧࡱࡸࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤᎮ"), datetime.now() - bstack111ll1ll1_opy_)
                elif entry.kind == TestFramework.bstack1l11l1lllll_opy_:
                    bstack1l11lll1ll1_opy_.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡ࡯ࡳ࡬ࡥࡣࡳࡧࡤࡸࡪࡪ࡟ࡦࡸࡨࡲࡹࡥࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠥᎯ"), datetime.now() - bstack111ll1ll1_opy_)
                else:
                    bstack1l11lll1ll1_opy_.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟࡭ࡱࡪࠦᎰ"), datetime.now() - bstack111ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1ll1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᎱ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll1llll11_opy_.enqueue(bstack1l11ll1llll_opy_)
    @measure(event_name=EVENTS.bstack1l11lll1111_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l11l1ll11l_opy_(
        self,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        event_json=None,
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_)
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᎲ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llllll11_opy_)
        req.test_framework_version = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l111llll_opy_)
        req.test_framework_state = bstack1lll1l1ll11_opy_[0].name
        req.test_hook_state = bstack1lll1l1ll11_opy_[1].name
        started_at = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l11ll1ll11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l11lll11_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l1l11llll1_opy_)).encode(bstack11l1ll1_opy_ (u"ࠥࡹࡹ࡬࠭࠹ࠤᎳ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l11ll1llll_opy_():
            bstack111ll1ll1_opy_ = datetime.now()
            try:
                self.bstack1ll1llll1ll_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟ࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡧࡹࡩࡳࡺࠢᎴ"), datetime.now() - bstack111ll1ll1_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11l1ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᎵ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll1llll11_opy_.enqueue(bstack1l11ll1llll_opy_)
    def bstack1l1l11ll111_opy_(self, instance: bstack1lll11lll1l_opy_):
        bstack1l11llllll1_opy_ = TestFramework.bstack1lll11l11ll_opy_(instance.context)
        for t in bstack1l11llllll1_opy_:
            bstack1l1l111111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(t, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1l111111l_opy_):
                return t
    def bstack1l11lll11l1_opy_(self, message):
        self.bstack1l11ll1l1ll_opy_(message + bstack11l1ll1_opy_ (u"ࠨ࡜࡯ࠤᎶ"))
    def log_error(self, message):
        self.bstack1l11lllll11_opy_(message + bstack11l1ll1_opy_ (u"ࠢ࡝ࡰࠥᎷ"))
    def bstack1l1l11lll1l_opy_(self, level, original_func):
        def bstack1l1l11111l1_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack11l1ll1_opy_ (u"ࠣࡇࡹࡩࡳࡺࡄࡪࡵࡳࡥࡹࡩࡨࡦࡴࡐࡳࡩࡻ࡬ࡦࠤᎸ") in message or bstack11l1ll1_opy_ (u"ࠤ࡞ࡗࡉࡑࡃࡍࡋࡠࠦᎹ") in message or bstack11l1ll1_opy_ (u"ࠥ࡟࡜࡫ࡢࡅࡴ࡬ࡺࡪࡸࡍࡰࡦࡸࡰࡪࡣࠢᎺ") in message:
                        return return_value
                    bstack1l11llllll1_opy_ = TestFramework.bstack1l11l1ll1ll_opy_()
                    if not bstack1l11llllll1_opy_:
                        return return_value
                    bstack1l11lll1ll1_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11llllll1_opy_
                            if TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
                        ),
                        None,
                    )
                    if not bstack1l11lll1ll1_opy_:
                        return return_value
                    entry = bstack1ll1lll11ll_opy_(TestFramework.bstack1l1l11l1l1l_opy_, message, level)
                    self.bstack1l11lll1lll_opy_(bstack1l11lll1ll1_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l1l11111l1_opy_
    def bstack1l1l11l1lll_opy_(self):
        def bstack1l1l111l1l1_opy_(*args, **kwargs):
            try:
                self.bstack1l1l11lllll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack11l1ll1_opy_ (u"ࠫࠥ࠭Ꮋ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack11l1ll1_opy_ (u"ࠧࡋࡶࡦࡰࡷࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࡍࡰࡦࡸࡰࡪࠨᎼ") in message:
                    return
                bstack1l11llllll1_opy_ = TestFramework.bstack1l11l1ll1ll_opy_()
                if not bstack1l11llllll1_opy_:
                    return
                bstack1l11lll1ll1_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11llllll1_opy_
                        if TestFramework.bstack1lll11l1111_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
                    ),
                    None,
                )
                if not bstack1l11lll1ll1_opy_:
                    return
                entry = bstack1ll1lll11ll_opy_(TestFramework.bstack1l1l11l1l1l_opy_, message, bstack1ll111l1lll_opy_.bstack1l1l111l111_opy_)
                self.bstack1l11lll1lll_opy_(bstack1l11lll1ll1_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1l11lllll_opy_(bstack1ll1ll11l1l_opy_ (u"ࠨ࡛ࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠢࡏࡳ࡬ࠦࡣࡢࡲࡷࡹࡷ࡫ࠠࡦࡴࡵࡳࡷࡀࠠࡼࡧࢀࠦᎽ"))
                except:
                    pass
        return bstack1l1l111l1l1_opy_
    def bstack1l11ll1l11l_opy_(self, event: dict, instance=None) -> None:
        global _1l11llll111_opy_
        levels = [bstack11l1ll1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᎾ"), bstack11l1ll1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪࡌࡦࡸࡨࡰࠧᎿ")]
        bstack1l11lll1l1l_opy_ = bstack11l1ll1_opy_ (u"ࠤࠥᏀ")
        if instance is not None:
            try:
                bstack1l11lll1l1l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
            except Exception as e:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡪࡩࡹࡺࡩ࡯ࡩࠣࡹࡺ࡯ࡤࠡࡨࡵࡳࡲࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠣᏁ").format(e))
        bstack1l11l1ll1l1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᏂ")]
                bstack1l11llll11l_opy_ = os.path.join(bstack1l1l111ll1l_opy_, (bstack1l11ll1l111_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11llll11l_opy_):
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡊࡩࡳࡧࡦࡸࡴࡸࡹࠡࡰࡲࡸࠥࡶࡲࡦࡵࡨࡲࡹࠦࡦࡰࡴࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡕࡧࡶࡸࠥࡧ࡮ࡥࠢࡅࡹ࡮ࡲࡤࠡ࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣᏃ").format(bstack1l11llll11l_opy_))
                    continue
                file_names = os.listdir(bstack1l11llll11l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11llll11l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11llll111_opy_:
                        self.logger.info(bstack11l1ll1_opy_ (u"ࠨࡐࡢࡶ࡫ࠤࡦࡲࡲࡦࡣࡧࡽࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡽࢀࠦᏄ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l11llll1l1_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l11llll1l1_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11l1ll1_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᏅ"):
                                entry = bstack1ll1lll11ll_opy_(
                                    kind=bstack11l1ll1_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᏆ"),
                                    message=bstack11l1ll1_opy_ (u"ࠤࠥᏇ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11ll1l1l1_opy_=file_size,
                                    bstack1l11lll111l_opy_=bstack11l1ll1_opy_ (u"ࠥࡑࡆࡔࡕࡂࡎࡢ࡙ࡕࡒࡏࡂࡆࠥᏈ"),
                                    bstack1ll1lll_opy_=os.path.abspath(file_path),
                                    bstack111lllll1l_opy_=bstack1l11lll1l1l_opy_
                                )
                            elif level == bstack11l1ll1_opy_ (u"ࠦࡇࡻࡩ࡭ࡦࡏࡩࡻ࡫࡬ࠣᏉ"):
                                entry = bstack1ll1lll11ll_opy_(
                                    kind=bstack11l1ll1_opy_ (u"࡚ࠧࡅࡔࡖࡢࡅ࡙࡚ࡁࡄࡊࡐࡉࡓ࡚ࠢᏊ"),
                                    message=bstack11l1ll1_opy_ (u"ࠨࠢᏋ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l11ll1l1l1_opy_=file_size,
                                    bstack1l11lll111l_opy_=bstack11l1ll1_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᏌ"),
                                    bstack1ll1lll_opy_=os.path.abspath(file_path),
                                    bstack1l1l11l1l11_opy_=bstack1l11lll1l1l_opy_
                                )
                            bstack1l11l1ll1l1_opy_.append(entry)
                            _1l11llll111_opy_.add(abs_path)
                        except Exception as bstack1l1l1111111_opy_:
                            self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡷࡧࡩࡴࡧࡧࠤࡼ࡮ࡥ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶࠤࢀࢃࠢᏍ").format(bstack1l1l1111111_opy_))
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡸࡡࡪࡵࡨࡨࠥࡽࡨࡦࡰࠣࡴࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࢁࡽࠣᏎ").format(e))
        event[bstack11l1ll1_opy_ (u"ࠥࡰࡴ࡭ࡳࠣᏏ")] = bstack1l11l1ll1l1_opy_
class bstack1l1l11llll1_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l1l111lll1_opy_ = set()
        kwargs[bstack11l1ll1_opy_ (u"ࠦࡸࡱࡩࡱ࡭ࡨࡽࡸࠨᏐ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l11ll1lll1_opy_(obj, self.bstack1l1l111lll1_opy_)
def bstack1l11ll111ll_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l11ll1lll1_opy_(obj, bstack1l1l111lll1_opy_=None, max_depth=3):
    if bstack1l1l111lll1_opy_ is None:
        bstack1l1l111lll1_opy_ = set()
    if id(obj) in bstack1l1l111lll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l1l111lll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l11lllll1l_opy_ = TestFramework.bstack1l1l11l1ll1_opy_(obj)
    bstack1l1l11111ll_opy_ = next((k.lower() in bstack1l11lllll1l_opy_.lower() for k in bstack1l1l1111lll_opy_.keys()), None)
    if bstack1l1l11111ll_opy_:
        obj = TestFramework.bstack1l11l1lll11_opy_(obj, bstack1l1l1111lll_opy_[bstack1l1l11111ll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11l1ll1_opy_ (u"ࠧࡥ࡟ࡴ࡮ࡲࡸࡸࡥ࡟ࠣᏑ")):
            keys = getattr(obj, bstack11l1ll1_opy_ (u"ࠨ࡟ࡠࡵ࡯ࡳࡹࡹ࡟ࡠࠤᏒ"), [])
        elif hasattr(obj, bstack11l1ll1_opy_ (u"ࠢࡠࡡࡧ࡭ࡨࡺ࡟ࡠࠤᏓ")):
            keys = getattr(obj, bstack11l1ll1_opy_ (u"ࠣࡡࡢࡨ࡮ࡩࡴࡠࡡࠥᏔ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11l1ll1_opy_ (u"ࠤࡢࠦᏕ"))}
        if not obj and bstack1l11lllll1l_opy_ == bstack11l1ll1_opy_ (u"ࠥࡴࡦࡺࡨ࡭࡫ࡥ࠲ࡕࡵࡳࡪࡺࡓࡥࡹ࡮ࠢᏖ"):
            obj = {bstack11l1ll1_opy_ (u"ࠦࡵࡧࡴࡩࠤᏗ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l11ll111ll_opy_(key) or str(key).startswith(bstack11l1ll1_opy_ (u"ࠧࡥࠢᏘ")):
            continue
        if value is not None and bstack1l11ll111ll_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l11ll1lll1_opy_(value, bstack1l1l111lll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l11ll1lll1_opy_(o, bstack1l1l111lll1_opy_, max_depth) for o in value]))
    return result or None