# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from datetime import datetime, timezone
import os
import builtins
from pathlib import Path
from typing import Any, Tuple, Callable, List
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import bstack1lll1l1l11l_opy_, bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l11l_opy_ import bstack1ll11l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11111l1l_opy_, bstack1ll11111ll1_opy_, bstack1ll11l1l11l_opy_, bstack1ll1l11ll11_opy_
from json import dumps, JSONEncoder
import grpc
from browserstack_sdk import sdk_pb2 as structs
import sys
import traceback
import time
import json
from bstack_utils.helper import bstack1l11llll111_opy_, bstack1l11lll1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
import threading
bstack1l1l1111l11_opy_ = [bstack11lllll_opy_ (u"ࠤࡱࡥࡲ࡫ࠢ፥"), bstack11lllll_opy_ (u"ࠥࡴࡦࡸࡥ࡯ࡶࠥ፦"), bstack11lllll_opy_ (u"ࠦࡨࡵ࡮ࡧ࡫ࡪࠦ፧"), bstack11lllll_opy_ (u"ࠧࡹࡥࡴࡵ࡬ࡳࡳࠨ፨"), bstack11lllll_opy_ (u"ࠨࡰࡢࡶ࡫ࠦ፩")]
bstack1l1l11l1ll1_opy_ = bstack1l11lll1lll_opy_()
bstack1l11l1ll11l_opy_ = bstack11lllll_opy_ (u"ࠢࡖࡲ࡯ࡳࡦࡪࡥࡥࡃࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸ࠳ࠢ፪")
bstack1l11ll1llll_opy_ = {
    bstack11lllll_opy_ (u"ࠣࡲࡼࡸࡪࡹࡴ࠯ࡲࡼࡸ࡭ࡵ࡮࠯ࡋࡷࡩࡲࠨ፫"): bstack1l1l1111l11_opy_,
    bstack11lllll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡳࡽࡹ࡮࡯࡯࠰ࡓࡥࡨࡱࡡࡨࡧࠥ፬"): bstack1l1l1111l11_opy_,
    bstack11lllll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡴࡾࡺࡨࡰࡰ࠱ࡑࡴࡪࡵ࡭ࡧࠥ፭"): bstack1l1l1111l11_opy_,
    bstack11lllll_opy_ (u"ࠦࡵࡿࡴࡦࡵࡷ࠲ࡵࡿࡴࡩࡱࡱ࠲ࡈࡲࡡࡴࡵࠥ፮"): bstack1l1l1111l11_opy_,
    bstack11lllll_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸ࠳ࡶࡹࡵࡪࡲࡲ࠳ࡌࡵ࡯ࡥࡷ࡭ࡴࡴࠢ፯"): bstack1l1l1111l11_opy_
    + [
        bstack11lllll_opy_ (u"ࠨ࡯ࡳ࡫ࡪ࡭ࡳࡧ࡬࡯ࡣࡰࡩࠧ፰"),
        bstack11lllll_opy_ (u"ࠢ࡬ࡧࡼࡻࡴࡸࡤࡴࠤ፱"),
        bstack11lllll_opy_ (u"ࠣࡨ࡬ࡼࡹࡻࡲࡦ࡫ࡱࡪࡴࠨ፲"),
        bstack11lllll_opy_ (u"ࠤ࡮ࡩࡾࡽ࡯ࡳࡦࡶࠦ፳"),
        bstack11lllll_opy_ (u"ࠥࡧࡦࡲ࡬ࡴࡲࡨࡧࠧ፴"),
        bstack11lllll_opy_ (u"ࠦࡨࡧ࡬࡭ࡱࡥ࡮ࠧ፵"),
        bstack11lllll_opy_ (u"ࠧࡹࡴࡢࡴࡷࠦ፶"),
        bstack11lllll_opy_ (u"ࠨࡳࡵࡱࡳࠦ፷"),
        bstack11lllll_opy_ (u"ࠢࡥࡷࡵࡥࡹ࡯࡯࡯ࠤ፸"),
        bstack11lllll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨ፹"),
    ],
    bstack11lllll_opy_ (u"ࠤࡳࡽࡹ࡫ࡳࡵ࠰ࡰࡥ࡮ࡴ࠮ࡔࡧࡶࡷ࡮ࡵ࡮ࠣ፺"): [bstack11lllll_opy_ (u"ࠥࡷࡹࡧࡲࡵࡲࡤࡸ࡭ࠨ፻"), bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡵࡩࡥ࡮ࡲࡥࡥࠤ፼"), bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡶࡧࡴࡲ࡬ࡦࡥࡷࡩࡩࠨ፽"), bstack11lllll_opy_ (u"ࠨࡩࡵࡧࡰࡷࠧ፾")],
    bstack11lllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡤࡱࡱࡪ࡮࡭࠮ࡄࡱࡱࡪ࡮࡭ࠢ፿"): [bstack11lllll_opy_ (u"ࠣ࡫ࡱࡺࡴࡩࡡࡵ࡫ࡲࡲࡤࡶࡡࡳࡣࡰࡷࠧᎀ"), bstack11lllll_opy_ (u"ࠤࡤࡶ࡬ࡹࠢᎁ")],
    bstack11lllll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳ࡌࡩࡹࡶࡸࡶࡪࡊࡥࡧࠤᎂ"): [bstack11lllll_opy_ (u"ࠦࡸࡩ࡯ࡱࡧࠥᎃ"), bstack11lllll_opy_ (u"ࠧࡧࡲࡨࡰࡤࡱࡪࠨᎄ"), bstack11lllll_opy_ (u"ࠨࡦࡶࡰࡦࠦᎅ"), bstack11lllll_opy_ (u"ࠢࡱࡣࡵࡥࡲࡹࠢᎆ"), bstack11lllll_opy_ (u"ࠣࡷࡱ࡭ࡹࡺࡥࡴࡶࠥᎇ"), bstack11lllll_opy_ (u"ࠤ࡬ࡨࡸࠨᎈ")],
    bstack11lllll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡪ࡮ࡾࡴࡶࡴࡨࡷ࠳࡙ࡵࡣࡔࡨࡵࡺ࡫ࡳࡵࠤᎉ"): [bstack11lllll_opy_ (u"ࠦ࡫࡯ࡸࡵࡷࡵࡩࡳࡧ࡭ࡦࠤᎊ"), bstack11lllll_opy_ (u"ࠧࡶࡡࡳࡣࡰࠦᎋ"), bstack11lllll_opy_ (u"ࠨࡰࡢࡴࡤࡱࡤ࡯࡮ࡥࡧࡻࠦᎌ")],
    bstack11lllll_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠮ࡳࡷࡱࡲࡪࡸ࠮ࡄࡣ࡯ࡰࡎࡴࡦࡰࠤᎍ"): [bstack11lllll_opy_ (u"ࠣࡹ࡫ࡩࡳࠨᎎ"), bstack11lllll_opy_ (u"ࠤࡵࡩࡸࡻ࡬ࡵࠤᎏ")],
    bstack11lllll_opy_ (u"ࠥࡴࡾࡺࡥࡴࡶ࠱ࡱࡦࡸ࡫࠯ࡵࡷࡶࡺࡩࡴࡶࡴࡨࡷ࠳ࡔ࡯ࡥࡧࡎࡩࡾࡽ࡯ࡳࡦࡶࠦ᎐"): [bstack11lllll_opy_ (u"ࠦࡳࡵࡤࡦࠤ᎑"), bstack11lllll_opy_ (u"ࠧࡶࡡࡳࡧࡱࡸࠧ᎒")],
    bstack11lllll_opy_ (u"ࠨࡰࡺࡶࡨࡷࡹ࠴࡭ࡢࡴ࡮࠲ࡸࡺࡲࡶࡥࡷࡹࡷ࡫ࡳ࠯ࡏࡤࡶࡰࠨ᎓"): [bstack11lllll_opy_ (u"ࠢ࡯ࡣࡰࡩࠧ᎔"), bstack11lllll_opy_ (u"ࠣࡣࡵ࡫ࡸࠨ᎕"), bstack11lllll_opy_ (u"ࠤ࡮ࡻࡦࡸࡧࡴࠤ᎖")],
}
_1l11ll1lll1_opy_ = set()
class bstack1ll11llll11_opy_(bstack1lll1l1l1l1_opy_):
    bstack1l11l1ll1l1_opy_ = bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡦࡨࡪࡪࡸࡲࡦࡦࠥ᎗")
    bstack1l1l11111ll_opy_ = bstack11lllll_opy_ (u"ࠦࡎࡔࡆࡐࠤ᎘")
    bstack1l11l1llll1_opy_ = bstack11lllll_opy_ (u"ࠧࡋࡒࡓࡑࡕࠦ᎙")
    bstack1l11lll11l1_opy_: Callable
    bstack1l1l11l1l11_opy_: Callable
    def __init__(self, bstack1ll11lll111_opy_, bstack1ll1lll11l1_opy_):
        super().__init__()
        self.bstack1l1l1l1ll11_opy_ = bstack1ll1lll11l1_opy_
        if os.getenv(bstack11lllll_opy_ (u"ࠨࡓࡅࡍࡢࡇࡑࡏ࡟ࡇࡎࡄࡋࡤࡕ࠱࠲࡛ࠥ᎚"), bstack11lllll_opy_ (u"ࠢ࠲ࠤ᎛")) != bstack11lllll_opy_ (u"ࠣ࠳ࠥ᎜") or not self.is_enabled():
            self.logger.warning(bstack11lllll_opy_ (u"ࠤࠥ᎝") + str(self.__class__.__name__) + bstack11lllll_opy_ (u"ࠥࠤࡩ࡯ࡳࡢࡤ࡯ࡩࡩࠨ᎞"))
            return
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.PRE), self.bstack1l1lll1111l_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), self.bstack1l1l1l1l1ll_opy_)
        for event in bstack1ll11111l1l_opy_:
            for state in bstack1ll11l1l11l_opy_:
                TestFramework.bstack1lll1l1l1ll_opy_((event, state), self.bstack1l11lll1l11_opy_)
        bstack1ll11lll111_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.POST), self.bstack1l1l11llll1_opy_)
        self.bstack1l11lll11l1_opy_ = sys.stdout.write
        sys.stdout.write = self.bstack1l11lllll11_opy_(bstack1ll11llll11_opy_.bstack1l1l11111ll_opy_, self.bstack1l11lll11l1_opy_)
        self.bstack1l1l11l1l11_opy_ = sys.stderr.write
        sys.stderr.write = self.bstack1l11lllll11_opy_(bstack1ll11llll11_opy_.bstack1l11l1llll1_opy_, self.bstack1l1l11l1l11_opy_)
        self.bstack1l1l11l1lll_opy_ = builtins.print
        builtins.print = self.bstack1l1l1111lll_opy_()
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        if f.bstack1l1l11ll1l1_opy_() and instance:
            bstack1l11l1ll1ll_opy_ = datetime.now()
            test_framework_state, test_hook_state = bstack1lll1l11lll_opy_
            if test_framework_state == bstack1ll11111l1l_opy_.SETUP_FIXTURE:
                return
            elif test_framework_state == bstack1ll11111l1l_opy_.LOG:
                bstack1l1111l111_opy_ = datetime.now()
                entries = f.bstack1l11ll1111l_opy_(instance, bstack1lll1l11lll_opy_)
                if entries:
                    self.bstack1l1l111lll1_opy_(instance, entries)
                    instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡶࡩࡳࡪ࡟࡭ࡱࡪࡣࡨࡸࡥࡢࡶࡨࡨࡤ࡫ࡶࡦࡰࡷࠦ᎟"), datetime.now() - bstack1l1111l111_opy_)
                    f.bstack1l1l11111l1_opy_(instance, bstack1lll1l11lll_opy_)
                instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠧࡵ࠱࠲ࡻ࠽ࡳࡳࡥࡡ࡭࡮ࡢࡸࡪࡹࡴࡠࡧࡹࡩࡳࡺࡳࠣᎠ"), datetime.now() - bstack1l11l1ll1ll_opy_)
                return # bstack1l11lll11ll_opy_ not send this event with the bstack1l1l11lll1l_opy_ bstack1l11ll11lll_opy_
            elif (
                test_framework_state == bstack1ll11111l1l_opy_.TEST
                and test_hook_state == bstack1ll11l1l11l_opy_.POST
                and not f.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_)
            ):
                self.logger.warning(bstack11lllll_opy_ (u"ࠨࡤࡳࡱࡳࡴ࡮ࡴࡧࠡࡦࡸࡩࠥࡺ࡯ࠡ࡮ࡤࡧࡰࠦ࡯ࡧࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࠦᎡ") + str(TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_)) + bstack11lllll_opy_ (u"ࠢࠣᎢ"))
                f.bstack1lll1ll1lll_opy_(instance, bstack1ll11llll11_opy_.bstack1l11l1ll1l1_opy_, True)
                return # bstack1l11lll11ll_opy_ not send this event bstack1l11ll1l111_opy_ bstack1l11llll1l1_opy_
            elif (
                f.bstack1lll1l1l111_opy_(instance, bstack1ll11llll11_opy_.bstack1l11l1ll1l1_opy_, False)
                and test_framework_state == bstack1ll11111l1l_opy_.LOG_REPORT
                and test_hook_state == bstack1ll11l1l11l_opy_.POST
                and f.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_)
            ):
                self.logger.warning(bstack11lllll_opy_ (u"ࠣ࡫ࡱ࡮ࡪࡩࡴࡪࡰࡪࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡗࡉࡘ࡚ࠬࠡࡖࡨࡷࡹࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡒࡒࡗ࡙ࠦࠢᎣ") + str(TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1l111ll11_opy_)) + bstack11lllll_opy_ (u"ࠤࠥᎤ"))
                self.bstack1l11lll1l11_opy_(f, instance, (bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), *args, **kwargs)
            bstack1l1111l111_opy_ = datetime.now()
            data = instance.data.copy()
            bstack1l1l11l11l1_opy_ = sorted(
                filter(lambda x: x.get(bstack11lllll_opy_ (u"ࠥࡩࡻ࡫࡮ࡵࡡࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹࠨᎥ"), None), data.pop(bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡩ࡭ࡽࡺࡵࡳࡧࡶࠦᎦ"), {}).values()),
                key=lambda x: x[bstack11lllll_opy_ (u"ࠧ࡫ࡶࡦࡰࡷࡣࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᎧ")],
            )
            if bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_ in data:
                data.pop(bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_)
            data.update({bstack11lllll_opy_ (u"ࠨࡴࡦࡵࡷࡣ࡫࡯ࡸࡵࡷࡵࡩࡸࠨᎨ"): bstack1l1l11l11l1_opy_})
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢ࡫ࡵࡲࡲ࠿ࡺࡥࡴࡶࡢࡪ࡮ࡾࡴࡶࡴࡨࡷࠧᎩ"), datetime.now() - bstack1l1111l111_opy_)
            bstack1l1111l111_opy_ = datetime.now()
            event_json = dumps(data, cls=bstack1l11l1lll1l_opy_)
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠣ࡬ࡶࡳࡳࡀ࡯࡯ࡡࡤࡰࡱࡥࡴࡦࡵࡷࡣࡪࡼࡥ࡯ࡶࡶࠦᎪ"), datetime.now() - bstack1l1111l111_opy_)
            if TestFramework.bstack1l1lll1l111_opy_ in data:
                self.bstack1l11ll11lll_opy_(instance, bstack1lll1l11lll_opy_, event_json=event_json)
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠤࡲ࠵࠶ࡿ࠺ࡰࡰࡢࡥࡱࡲ࡟ࡵࡧࡶࡸࡤ࡫ࡶࡦࡰࡷࡷࠧᎫ"), datetime.now() - bstack1l11l1ll1ll_opy_)
    def bstack1l1lll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
        bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1111l111l_opy_.value)
        self.bstack1l1l1l1ll11_opy_.bstack1l11ll11111_opy_(instance, f, bstack1lll1l11lll_opy_, *args, **kwargs)
        req = self.bstack1l1l1l1ll11_opy_.bstack1l11ll111ll_opy_(instance, f, bstack1lll1l11lll_opy_, *args, **kwargs)
        self.bstack1l1l111111l_opy_(f, instance, req)
        bstack1lll11l1ll_opy_.end(EVENTS.bstack1111l111l_opy_.value, bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᎬ"), bstack1ll11111l_opy_ + bstack11lllll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᎭ"), status=True, failure=None, test_name=None)
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        if not f.bstack1lll1l1l111_opy_(instance, self.bstack1l1l1l1ll11_opy_.bstack1l11l1ll111_opy_, False):
            req = self.bstack1l1l1l1ll11_opy_.bstack1l11ll111ll_opy_(instance, f, bstack1lll1l11lll_opy_, *args, **kwargs)
            self.bstack1l1l111111l_opy_(f, instance, req)
    @measure(event_name=EVENTS.bstack1l11lll111l_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1l111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        req: structs.TestSessionEventRequest
    ):
        if not req:
            self.logger.debug(bstack11lllll_opy_ (u"࡙ࠧ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡕࡧࡶࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡊࡼࡥ࡯ࡶࠣ࡫ࡗࡖࡃࠡࡥࡤࡰࡱࡀࠠࡏࡱࠣࡺࡦࡲࡩࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡨࡦࡺࡡࠣᎮ"))
            return
        bstack1l1111l111_opy_ = datetime.now()
        try:
            r = self.bstack1ll1l1l1ll1_opy_.TestSessionEvent(req)
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡠࡧࡹࡩࡳࡺࠢᎯ"), datetime.now() - bstack1l1111l111_opy_)
            f.bstack1lll1ll1lll_opy_(instance, self.bstack1l1l1l1ll11_opy_.bstack1l11l1ll111_opy_, r.success)
            if not r.success:
                self.logger.info(bstack11lllll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᎰ") + str(r) + bstack11lllll_opy_ (u"ࠣࠤᎱ"))
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᎲ") + str(e) + bstack11lllll_opy_ (u"ࠥࠦᎳ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11llll1_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        _driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        _1l1l11lll11_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if not bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_(method_name):
            return
        if f.bstack1l1l1lll11l_opy_(*args) == bstack1lll11lllll_opy_.bstack1l11l1lll11_opy_:
            bstack1l11l1ll1ll_opy_ = datetime.now()
            screenshot = result.get(bstack11lllll_opy_ (u"ࠦࡻࡧ࡬ࡶࡧࠥᎴ"), None) if isinstance(result, dict) else None
            if not isinstance(screenshot, str) or len(screenshot) <= 0:
                self.logger.warning(bstack11lllll_opy_ (u"ࠧ࡯࡮ࡷࡣ࡯࡭ࡩࠦࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠣ࡭ࡲࡧࡧࡦࠢࡥࡥࡸ࡫࠶࠵ࠢࡶࡸࡷࠨᎵ"))
                return
            bstack1l1l111l1ll_opy_ = self.bstack1l11lllllll_opy_(instance)
            if bstack1l1l111l1ll_opy_:
                entry = bstack1ll1l11ll11_opy_(TestFramework.bstack1l1l1111ll1_opy_, screenshot)
                self.bstack1l1l111lll1_opy_(bstack1l1l111l1ll_opy_, [entry])
                instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨ࡯࠲࠳ࡼ࠾ࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡥࡹࡧࡦࡹࡹ࡫ࠢᎶ"), datetime.now() - bstack1l11l1ll1ll_opy_)
            else:
                self.logger.warning(bstack11lllll_opy_ (u"ࠢࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡨࡪࡺࡥࡳ࡯࡬ࡲࡪࠦࡴࡦࡵࡷࠤ࡫ࡵࡲࠡࡹ࡫࡭ࡨ࡮ࠠࡵࡪ࡬ࡷࠥࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠢࡺࡥࡸࠦࡴࡢ࡭ࡨࡲࠥࡨࡹࠡࡦࡵ࡭ࡻ࡫ࡲ࠾ࠢࡾࢁࠧᎷ").format(instance.ref()))
        event = {}
        bstack1l1l111l1ll_opy_ = self.bstack1l11lllllll_opy_(instance)
        if bstack1l1l111l1ll_opy_:
            self.bstack1l1l11l111l_opy_(event, bstack1l1l111l1ll_opy_)
            if event.get(bstack11lllll_opy_ (u"ࠣ࡮ࡲ࡫ࡸࠨᎸ")):
                self.bstack1l1l111lll1_opy_(bstack1l1l111l1ll_opy_, event[bstack11lllll_opy_ (u"ࠤ࡯ࡳ࡬ࡹࠢᎹ")])
            else:
                self.logger.debug(bstack11lllll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢ࡯ࡳ࡬ࡹࠠࡧࡱࡵࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡧࡹࡩࡳࡺࠢᎺ"))
    @measure(event_name=EVENTS.bstack1l11ll1l1ll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1l111lll1_opy_(
        self,
        bstack1l1l111l1ll_opy_: bstack1ll11111ll1_opy_,
        entries: List[bstack1ll1l11ll11_opy_],
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.LogCreatedEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1l1lllll1_opy_)
        req.client_worker_id = bstack11lllll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᎻ").format(threading.get_ident(), os.getpid())
        req.execution_context.hash = str(bstack1l1l111l1ll_opy_.context.hash)
        req.execution_context.thread_id = str(bstack1l1l111l1ll_opy_.context.thread_id)
        req.execution_context.process_id = str(bstack1l1l111l1ll_opy_.context.process_id)
        for entry in entries:
            log_entry = req.logs.add()
            log_entry.test_framework_name = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1ll111ll1_opy_)
            log_entry.test_framework_version = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l11ll1ll1l_opy_)
            log_entry.uuid = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l1lll1l111_opy_)
            log_entry.test_framework_state = bstack1l1l111l1ll_opy_.state.name
            log_entry.message = entry.message.encode(bstack11lllll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᎼ"))
            log_entry.kind = entry.kind
            log_entry.timestamp = (
                entry.timestamp.isoformat()
                if isinstance(entry.timestamp, datetime)
                else datetime.now(tz=timezone.utc).isoformat()
            )
            if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                log_entry.level = entry.level.strip()
            if entry.kind == bstack11lllll_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᎽ"):
                log_entry.file_name = entry.fileName
                log_entry.file_size = entry.bstack1l1l111l11l_opy_
                log_entry.file_path = entry.bstack1111ll1_opy_
        def bstack1l1l11l11ll_opy_():
            bstack1l1111l111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1ll1_opy_.LogCreatedEvent(req)
                if entry.kind == TestFramework.bstack1l1l1111ll1_opy_:
                    bstack1l1l111l1ll_opy_.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡹࡥ࡯ࡦࡢࡰࡴ࡭࡟ࡤࡴࡨࡥࡹ࡫ࡤࡠࡧࡹࡩࡳࡺ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦᎾ"), datetime.now() - bstack1l1111l111_opy_)
                elif entry.kind == TestFramework.bstack1l11ll1ll11_opy_:
                    bstack1l1l111l1ll_opy_.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡳࡦࡰࡧࡣࡱࡵࡧࡠࡥࡵࡩࡦࡺࡥࡥࡡࡨࡺࡪࡴࡴࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠧᎿ"), datetime.now() - bstack1l1111l111_opy_)
                else:
                    bstack1l1l111l1ll_opy_.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡴࡧࡱࡨࡤࡲ࡯ࡨࡡࡦࡶࡪࡧࡴࡦࡦࡢࡩࡻ࡫࡮ࡵࡡ࡯ࡳ࡬ࠨᏀ"), datetime.now() - bstack1l1111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lllll_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᏁ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll11ll111_opy_.enqueue(bstack1l1l11l11ll_opy_)
    @measure(event_name=EVENTS.bstack1l1l111l111_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l11ll11lll_opy_(
        self,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        event_json=None,
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.TestFrameworkEventRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_)
        req.client_worker_id = bstack11lllll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᏂ").format(threading.get_ident(), os.getpid())
        req.test_framework_name = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1ll111ll1_opy_)
        req.test_framework_version = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        req.test_framework_state = bstack1lll1l11lll_opy_[0].name
        req.test_hook_state = bstack1lll1l11lll_opy_[1].name
        started_at = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l11ll11l11_opy_, None)
        if started_at:
            req.started_at = started_at.isoformat()
        ended_at = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1l1111l1l_opy_, None)
        if ended_at:
            req.ended_at = ended_at.isoformat()
        req.uuid = instance.ref()
        req.event_json = (event_json if event_json else dumps(instance.data, cls=bstack1l11l1lll1l_opy_)).encode(bstack11lllll_opy_ (u"ࠧࡻࡴࡧ࠯࠻ࠦᏃ"))
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        def bstack1l1l11l11ll_opy_():
            bstack1l1111l111_opy_ = datetime.now()
            try:
                self.bstack1ll1l1l1ll1_opy_.TestFrameworkEvent(req)
                instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡸ࡫࡮ࡥࡡࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡩࡻ࡫࡮ࡵࠤᏄ"), datetime.now() - bstack1l1111l111_opy_)
            except grpc.RpcError as e:
                self.log_error(bstack11lllll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᏅ") + str(e))
                traceback.print_exc()
                raise e
        self.bstack1lll11ll111_opy_.enqueue(bstack1l1l11l11ll_opy_)
    def bstack1l11lllllll_opy_(self, instance: bstack1lll1l1l11l_opy_):
        bstack1l11ll1l1l1_opy_ = TestFramework.bstack1lll11l1111_opy_(instance.context)
        for t in bstack1l11ll1l1l1_opy_:
            bstack1l1l11ll111_opy_ = TestFramework.bstack1lll1l1l111_opy_(t, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
            if any(instance is d[1] for d in bstack1l1l11ll111_opy_):
                return t
    def bstack1l11lll1l1l_opy_(self, message):
        self.bstack1l11lll11l1_opy_(message + bstack11lllll_opy_ (u"ࠣ࡞ࡱࠦᏆ"))
    def log_error(self, message):
        self.bstack1l1l11l1l11_opy_(message + bstack11lllll_opy_ (u"ࠤ࡟ࡲࠧᏇ"))
    def bstack1l11lllll11_opy_(self, level, original_func):
        def bstack1l1l11ll1ll_opy_(*args):
            try:
                try:
                    return_value = original_func(*args)
                except Exception:
                    return None
                try:
                    if not args or not isinstance(args[0], str) or not args[0].strip():
                        return return_value
                    message = args[0].strip()
                    if bstack11lllll_opy_ (u"ࠥࡉࡻ࡫࡮ࡵࡆ࡬ࡷࡵࡧࡴࡤࡪࡨࡶࡒࡵࡤࡶ࡮ࡨࠦᏈ") in message or bstack11lllll_opy_ (u"ࠦࡠ࡙ࡄࡌࡅࡏࡍࡢࠨᏉ") in message or bstack11lllll_opy_ (u"ࠧࡡࡗࡦࡤࡇࡶ࡮ࡼࡥࡳࡏࡲࡨࡺࡲࡥ࡞ࠤᏊ") in message:
                        return return_value
                    bstack1l11ll1l1l1_opy_ = TestFramework.bstack1l11ll11l1l_opy_()
                    if not bstack1l11ll1l1l1_opy_:
                        return return_value
                    bstack1l1l111l1ll_opy_ = next(
                        (
                            instance
                            for instance in bstack1l11ll1l1l1_opy_
                            if TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
                        ),
                        None,
                    )
                    if not bstack1l1l111l1ll_opy_:
                        return return_value
                    entry = bstack1ll1l11ll11_opy_(TestFramework.bstack1l11ll111l1_opy_, message, level)
                    self.bstack1l1l111lll1_opy_(bstack1l1l111l1ll_opy_, [entry])
                except Exception:
                    pass
                return return_value
            except Exception:
                return None
        return bstack1l1l11ll1ll_opy_
    def bstack1l1l1111lll_opy_(self):
        def bstack1l1l111llll_opy_(*args, **kwargs):
            try:
                self.bstack1l1l11l1lll_opy_(*args, **kwargs)
                if not args:
                    return
                message = bstack11lllll_opy_ (u"࠭ࠠࠨᏋ").join(str(arg) for arg in args)
                if not message.strip():
                    return
                if bstack11lllll_opy_ (u"ࠢࡆࡸࡨࡲࡹࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࡏࡲࡨࡺࡲࡥࠣᏌ") in message:
                    return
                bstack1l11ll1l1l1_opy_ = TestFramework.bstack1l11ll11l1l_opy_()
                if not bstack1l11ll1l1l1_opy_:
                    return
                bstack1l1l111l1ll_opy_ = next(
                    (
                        instance
                        for instance in bstack1l11ll1l1l1_opy_
                        if TestFramework.bstack1lll111ll11_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
                    ),
                    None,
                )
                if not bstack1l1l111l1ll_opy_:
                    return
                entry = bstack1ll1l11ll11_opy_(TestFramework.bstack1l11ll111l1_opy_, message, bstack1ll11llll11_opy_.bstack1l1l11111ll_opy_)
                self.bstack1l1l111lll1_opy_(bstack1l1l111l1ll_opy_, [entry])
            except Exception as e:
                try:
                    self.bstack1l1l11l1lll_opy_(bstack1llll11111l_opy_ (u"ࠣ࡝ࡈࡺࡪࡴࡴࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࡑࡴࡪࡵ࡭ࡧࡠࠤࡑࡵࡧࠡࡥࡤࡴࡹࡻࡲࡦࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࡩࢂࠨᏍ"))
                except:
                    pass
        return bstack1l1l111llll_opy_
    def bstack1l1l11l111l_opy_(self, event: dict, instance=None) -> None:
        global _1l11ll1lll1_opy_
        levels = [bstack11lllll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᏎ"), bstack11lllll_opy_ (u"ࠥࡆࡺ࡯࡬ࡥࡎࡨࡺࡪࡲࠢᏏ")]
        bstack1l11lllll1l_opy_ = bstack11lllll_opy_ (u"ࠦࠧᏐ")
        if instance is not None:
            try:
                bstack1l11lllll1l_opy_ = TestFramework.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
            except Exception as e:
                self.logger.warning(bstack11lllll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡻࡵࡪࡦࠣࡪࡷࡵ࡭ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠥᏑ").format(e))
        bstack1l11llllll1_opy_ = []
        try:
            for level in levels:
                platform_index = os.environ[bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮢ")]
                bstack1l11ll1l11l_opy_ = os.path.join(bstack1l1l11l1ll1_opy_, (bstack1l11l1ll11l_opy_ + str(platform_index)), level)
                if not os.path.isdir(bstack1l11ll1l11l_opy_):
                    self.logger.debug(bstack11lllll_opy_ (u"ࠢࡅ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡲࡴࡺࠠࡱࡴࡨࡷࡪࡴࡴࠡࡨࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡗࡩࡸࡺࠠࡢࡰࡧࠤࡇࡻࡩ࡭ࡦࠣࡰࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᏓ").format(bstack1l11ll1l11l_opy_))
                    continue
                file_names = os.listdir(bstack1l11ll1l11l_opy_)
                for file_name in file_names:
                    file_path = os.path.join(bstack1l11ll1l11l_opy_, file_name)
                    abs_path = os.path.abspath(file_path)
                    if abs_path in _1l11ll1lll1_opy_:
                        self.logger.info(bstack11lllll_opy_ (u"ࠣࡒࡤࡸ࡭ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡿࢂࠨᏔ").format(abs_path))
                        continue
                    if os.path.isfile(file_path):
                        try:
                            bstack1l1l111ll1l_opy_ = os.path.getmtime(file_path)
                            timestamp = datetime.fromtimestamp(bstack1l1l111ll1l_opy_, tz=timezone.utc).isoformat()
                            file_size = os.path.getsize(file_path)
                            if level == bstack11lllll_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᏕ"):
                                entry = bstack1ll1l11ll11_opy_(
                                    kind=bstack11lllll_opy_ (u"ࠥࡘࡊ࡙ࡔࡠࡃࡗࡘࡆࡉࡈࡎࡇࡑࡘࠧᏖ"),
                                    message=bstack11lllll_opy_ (u"ࠦࠧᏗ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l111l11l_opy_=file_size,
                                    bstack1l1l11l1l1l_opy_=bstack11lllll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᏘ"),
                                    bstack1111ll1_opy_=os.path.abspath(file_path),
                                    bstack1l1l11l111_opy_=bstack1l11lllll1l_opy_
                                )
                            elif level == bstack11lllll_opy_ (u"ࠨࡂࡶ࡫࡯ࡨࡑ࡫ࡶࡦ࡮ࠥᏙ"):
                                entry = bstack1ll1l11ll11_opy_(
                                    kind=bstack11lllll_opy_ (u"ࠢࡕࡇࡖࡘࡤࡇࡔࡕࡃࡆࡌࡒࡋࡎࡕࠤᏚ"),
                                    message=bstack11lllll_opy_ (u"ࠣࠤᏛ"),
                                    level=level,
                                    timestamp=timestamp,
                                    fileName=file_name,
                                    bstack1l1l111l11l_opy_=file_size,
                                    bstack1l1l11l1l1l_opy_=bstack11lllll_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᏜ"),
                                    bstack1111ll1_opy_=os.path.abspath(file_path),
                                    bstack1l11lll1111_opy_=bstack1l11lllll1l_opy_
                                )
                            bstack1l11llllll1_opy_.append(entry)
                            _1l11ll1lll1_opy_.add(abs_path)
                        except Exception as bstack1l11llll11l_opy_:
                            self.logger.error(bstack11lllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡲࡢ࡫ࡶࡩࡩࠦࡷࡩࡧࡱࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࠦࡻࡾࠤᏝ").format(bstack1l11llll11l_opy_))
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡳࡣ࡬ࡷࡪࡪࠠࡸࡪࡨࡲࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡼࡿࠥᏞ").format(e))
        event[bstack11lllll_opy_ (u"ࠧࡲ࡯ࡨࡵࠥᏟ")] = bstack1l11llllll1_opy_
class bstack1l11l1lll1l_opy_(JSONEncoder):
    def __init__(self, **kwargs):
        self.bstack1l11lll1ll1_opy_ = set()
        kwargs[bstack11lllll_opy_ (u"ࠨࡳ࡬࡫ࡳ࡯ࡪࡿࡳࠣᏠ")] = True
        super().__init__(**kwargs)
    def default(self, obj):
        return bstack1l1l111l1l1_opy_(obj, self.bstack1l11lll1ll1_opy_)
def bstack1l11ll11ll1_opy_(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))
def bstack1l1l111l1l1_opy_(obj, bstack1l11lll1ll1_opy_=None, max_depth=3):
    if bstack1l11lll1ll1_opy_ is None:
        bstack1l11lll1ll1_opy_ = set()
    if id(obj) in bstack1l11lll1ll1_opy_ or max_depth <= 0:
        return None
    max_depth -= 1
    bstack1l11lll1ll1_opy_.add(id(obj))
    if isinstance(obj, datetime):
        return obj.isoformat()
    bstack1l1l1111111_opy_ = TestFramework.bstack1l11llll1ll_opy_(obj)
    bstack1l11l1lllll_opy_ = next((k.lower() in bstack1l1l1111111_opy_.lower() for k in bstack1l11ll1llll_opy_.keys()), None)
    if bstack1l11l1lllll_opy_:
        obj = TestFramework.bstack1l1l11ll11l_opy_(obj, bstack1l11ll1llll_opy_[bstack1l11l1lllll_opy_])
    if not isinstance(obj, dict):
        keys = []
        if hasattr(obj, bstack11lllll_opy_ (u"ࠢࡠࡡࡶࡰࡴࡺࡳࡠࡡࠥᏡ")):
            keys = getattr(obj, bstack11lllll_opy_ (u"ࠣࡡࡢࡷࡱࡵࡴࡴࡡࡢࠦᏢ"), [])
        elif hasattr(obj, bstack11lllll_opy_ (u"ࠤࡢࡣࡩ࡯ࡣࡵࡡࡢࠦᏣ")):
            keys = getattr(obj, bstack11lllll_opy_ (u"ࠥࡣࡤࡪࡩࡤࡶࡢࡣࠧᏤ"), {}).keys()
        else:
            keys = dir(obj)
        obj = {k: getattr(obj, k, None) for k in keys if not str(k).startswith(bstack11lllll_opy_ (u"ࠦࡤࠨᏥ"))}
        if not obj and bstack1l1l1111111_opy_ == bstack11lllll_opy_ (u"ࠧࡶࡡࡵࡪ࡯࡭ࡧ࠴ࡐࡰࡵ࡬ࡼࡕࡧࡴࡩࠤᏦ"):
            obj = {bstack11lllll_opy_ (u"ࠨࡰࡢࡶ࡫ࠦᏧ"): str(obj)}
    result = {}
    for key, value in obj.items():
        if not bstack1l11ll11ll1_opy_(key) or str(key).startswith(bstack11lllll_opy_ (u"ࠢࡠࠤᏨ")):
            continue
        if value is not None and bstack1l11ll11ll1_opy_(value):
            result[key] = value
        elif isinstance(value, dict):
            r = bstack1l1l111l1l1_opy_(value, bstack1l11lll1ll1_opy_, max_depth)
            if r is not None:
                result[key] = r
        elif isinstance(value, (list, tuple, set, frozenset)):
            result[key] = list(filter(None, [bstack1l1l111l1l1_opy_(o, bstack1l11lll1ll1_opy_, max_depth) for o in value]))
    return result or None