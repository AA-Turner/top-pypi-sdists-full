# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack1ll11l1l111_opy_,
)
from bstack_utils.helper import  bstack111l1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111lllll_opy_, TestHookState, bstack1l1l1l1l1ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l11111l11_opy_ import bstack1l1111lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111lll_opy_ import bstack1l1ll1ll1l1_opy_
from bstack_utils.percy import bstack1l11lll1ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l1llll1l_opy_(bstack1l1llll1l11_opy_):
    def __init__(self, bstack11llll1l11l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11llll1l11l_opy_ = bstack11llll1l11l_opy_
        self.percy = bstack1l11lll1ll_opy_()
        self.bstack1111l11l_opy_ = bstack1l1111lll1_opy_()
        self.bstack11lllll11l1_opy_()
        bstack1l1llll1111_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack11lllll111l_opy_)
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111111111_opy_(self, instance: bstack1ll11l1l111_opy_, driver: object):
        bstack1l11111l1ll_opy_ = TestFramework.bstack1ll11l11ll1_opy_(instance.context)
        for t in bstack1l11111l1ll_opy_:
            bstack1l11111ll11_opy_ = TestFramework.bstack1ll1lll11ll_opy_(t, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])
            if any(instance is d[1] for d in bstack1l11111ll11_opy_) or instance == driver:
                return t
    def bstack11lllll111l_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l1llll1111_opy_.bstack1l1l111l1ll_opy_(method_name):
                return
            platform_index = f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_, 0)
            bstack1l1111ll111_opy_ = self.bstack1l111111111_opy_(instance, driver)
            bstack11llll11lll_opy_ = TestFramework.bstack1ll1lll11ll_opy_(bstack1l1111ll111_opy_, TestFramework.bstack11lllll1111_opy_, None)
            if not bstack11llll11lll_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡥࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡸࡺࡡࡳࡶࡨࡨࠧᗬ"))
                return
            driver_command = f.bstack1l1l1111l1l_opy_(*args)
            for command in bstack1ll1l11lll_opy_:
                if command == driver_command:
                    self.bstack11lll1lll_opy_(driver, platform_index)
            bstack11ll1l11_opy_ = self.percy.bstack1lll11ll1l_opy_()
            if driver_command in bstack11ll11lll_opy_[bstack11ll1l11_opy_]:
                self.bstack1111l11l_opy_.bstack1lll1lll1_opy_(bstack11llll11lll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡧࡵࡶࡴࡸࠢᗭ"), e)
    def bstack1l11lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
        bstack1l11111ll11_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1l1ll1ll1l1_opy_.bstack11lllll1l11_opy_, [])
        if not bstack1l11111ll11_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᗮ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠣࠤᗯ"))
            return
        if len(bstack1l11111ll11_opy_) > 1:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᗰ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠥࠦᗱ"))
        bstack11llll1llll_opy_, bstack11llll1ll11_opy_ = bstack1l11111ll11_opy_[0]
        driver = bstack11llll1llll_opy_()
        if not driver:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᗲ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠧࠨᗳ"))
            return
        bstack11lllll11ll_opy_ = {
            TestFramework.bstack1l1l111111l_opy_: bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᗴ"),
            TestFramework.bstack1l1l1111l11_opy_: bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥᗵ"),
            TestFramework.bstack11lllll1111_opy_: bstack1ll1lll_opy_ (u"ࠣࡶࡨࡷࡹࠦࡲࡦࡴࡸࡲࠥࡴࡡ࡮ࡧࠥᗶ")
        }
        bstack11llll1l111_opy_ = { key: f.bstack1ll1lll11ll_opy_(instance, key) for key in bstack11lllll11ll_opy_ }
        bstack11llll1ll1l_opy_ = [key for key, value in bstack11llll1l111_opy_.items() if not value]
        if bstack11llll1ll1l_opy_:
            for key in bstack11llll1ll1l_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠧᗷ") + str(key) + bstack1ll1lll_opy_ (u"ࠥࠦᗸ"))
            return
        platform_index = f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_, 0)
        if self.bstack11llll1l11l_opy_.percy_capture_mode == bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᗹ"):
            bstack11ll1lllll_opy_ = bstack11llll1l111_opy_.get(TestFramework.bstack11lllll1111_opy_) + bstack1ll1lll_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᗺ")
            bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11llll1lll1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11ll1lllll_opy_,
                bstack11llll11l_opy_=bstack11llll1l111_opy_[TestFramework.bstack1l1l111111l_opy_],
                bstack1l111l1111_opy_=bstack11llll1l111_opy_[TestFramework.bstack1l1l1111l11_opy_],
                bstack1l111l11l1_opy_=platform_index
            )
            bstack1lll1lll11_opy_.end(EVENTS.bstack11llll1lll1_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᗻ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᗼ"), True, None, None, None, None, test_name=bstack11ll1lllll_opy_)
    def bstack11lll1lll_opy_(self, driver, platform_index):
        if self.bstack1111l11l_opy_.bstack11ll1l1ll1_opy_() is True or self.bstack1111l11l_opy_.capturing() is True:
            return
        self.bstack1111l11l_opy_.bstack1l1ll1ll1_opy_()
        while not self.bstack1111l11l_opy_.bstack11ll1l1ll1_opy_():
            bstack11llll11lll_opy_ = self.bstack1111l11l_opy_.bstack11l111ll1l_opy_()
            self.bstack1l111l111_opy_(driver, bstack11llll11lll_opy_, platform_index)
        self.bstack1111l11l_opy_.bstack11l1l111l1_opy_()
    def bstack1l111l111_opy_(self, driver, bstack1ll1ll111_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
        bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack111l11111l_opy_.value)
        if test != None:
            bstack11llll11l_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗽ"), None)
            bstack1l111l1111_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗾ"), None)
            PercySDK.screenshot(driver, bstack1ll1ll111_opy_, bstack11llll11l_opy_=bstack11llll11l_opy_, bstack1l111l1111_opy_=bstack1l111l1111_opy_, bstack1l111l11l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1ll1ll111_opy_)
        bstack1lll1lll11_opy_.end(EVENTS.bstack111l11111l_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᗿ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘀ"), True, None, None, None, None, test_name=bstack1ll1ll111_opy_)
    def bstack11lllll11l1_opy_(self):
        os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᘁ")] = str(self.bstack11llll1l11l_opy_.success)
        os.environ[bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᘂ")] = str(self.bstack11llll1l11l_opy_.percy_capture_mode)
        self.percy.bstack11llll1l1ll_opy_(self.bstack11llll1l11l_opy_.is_percy_auto_enabled)
        self.percy.bstack11llll1l1l1_opy_(self.bstack11llll1l11l_opy_.percy_build_id)