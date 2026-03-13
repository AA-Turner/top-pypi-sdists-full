# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1l1lll1l_opy_,
)
from bstack_utils.helper import  bstack1l11l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111lllll_opy_, TestHookState, bstack1l1lllllll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1111l11l_opy_ import bstack1l1111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1ll11l1ll_opy_
from bstack_utils.percy import bstack1llll111ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1ll1lll1l_opy_(bstack1ll1111l1ll_opy_):
    def __init__(self, bstack11lllllll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11lllllll1l_opy_ = bstack11lllllll1l_opy_
        self.percy = bstack1llll111ll_opy_()
        self.bstack1ll1lll11l_opy_ = bstack1l1111l1l_opy_()
        self.bstack1l111111l1l_opy_()
        bstack1ll111ll1ll_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack11lllllllll_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111lll1l1_opy_(self, instance: bstack1ll1l1lll1l_opy_, driver: object):
        bstack1l11l111111_opy_ = TestFramework.bstack1ll1l111ll1_opy_(instance.context)
        for t in bstack1l11l111111_opy_:
            bstack1l111lll11l_opy_ = TestFramework.bstack1ll1lll1l11_opy_(t, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
            if any(instance is d[1] for d in bstack1l111lll11l_opy_) or instance == driver:
                return t
    def bstack11lllllllll_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll111ll1ll_opy_.bstack1l1l1111111_opy_(method_name):
                return
            platform_index = f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_, 0)
            bstack1l111lll1ll_opy_ = self.bstack1l111lll1l1_opy_(instance, driver)
            bstack1l111111lll_opy_ = TestFramework.bstack1ll1lll1l11_opy_(bstack1l111lll1ll_opy_, TestFramework.bstack1l11111l111_opy_, None)
            if not bstack1l111111lll_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡥࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡸࡺࡡࡳࡶࡨࡨࠧᖻ"))
                return
            driver_command = f.bstack1l11llll1ll_opy_(*args)
            for command in bstack11ll1l1lll_opy_:
                if command == driver_command:
                    self.bstack11l1ll1l11_opy_(driver, platform_index)
            bstack11l11111ll_opy_ = self.percy.bstack11l11l11_opy_()
            if driver_command in bstack1llll11l1l_opy_[bstack11l11111ll_opy_]:
                self.bstack1ll1lll11l_opy_.bstack111111ll1_opy_(bstack1l111111lll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡧࡵࡶࡴࡸࠢᖼ"), e)
    def bstack1l11ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
        bstack1l111lll11l_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1l1ll11l1ll_opy_.bstack1l111ll1l1l_opy_, [])
        if not bstack1l111lll11l_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᖽ") + str(kwargs) + bstack1111l_opy_ (u"ࠣࠤᖾ"))
            return
        if len(bstack1l111lll11l_opy_) > 1:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᖿ") + str(kwargs) + bstack1111l_opy_ (u"ࠥࠦᗀ"))
        bstack1l11111l11l_opy_, bstack1l111111ll1_opy_ = bstack1l111lll11l_opy_[0]
        driver = bstack1l11111l11l_opy_()
        if not driver:
            self.logger.debug(bstack1111l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᗁ") + str(kwargs) + bstack1111l_opy_ (u"ࠧࠨᗂ"))
            return
        bstack1l1111111ll_opy_ = {
            TestFramework.bstack1l1l111llll_opy_: bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᗃ"),
            TestFramework.bstack1l11ll1ll1l_opy_: bstack1111l_opy_ (u"ࠢࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥᗄ"),
            TestFramework.bstack1l11111l111_opy_: bstack1111l_opy_ (u"ࠣࡶࡨࡷࡹࠦࡲࡦࡴࡸࡲࠥࡴࡡ࡮ࡧࠥᗅ")
        }
        bstack11llllllll1_opy_ = { key: f.bstack1ll1lll1l11_opy_(instance, key) for key in bstack1l1111111ll_opy_ }
        bstack1l111111111_opy_ = [key for key, value in bstack11llllllll1_opy_.items() if not value]
        if bstack1l111111111_opy_:
            for key in bstack1l111111111_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠧᗆ") + str(key) + bstack1111l_opy_ (u"ࠥࠦᗇ"))
            return
        platform_index = f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_, 0)
        if self.bstack11lllllll1l_opy_.percy_capture_mode == bstack1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᗈ"):
            bstack1111ll1l_opy_ = bstack11llllllll1_opy_.get(TestFramework.bstack1l11111l111_opy_) + bstack1111l_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣᗉ")
            bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l111111l11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111ll1l_opy_,
                bstack111llll1_opy_=bstack11llllllll1_opy_[TestFramework.bstack1l1l111llll_opy_],
                bstack1l111lll1l_opy_=bstack11llllllll1_opy_[TestFramework.bstack1l11ll1ll1l_opy_],
                bstack11lllllll_opy_=platform_index
            )
            bstack1l11ll1l1_opy_.end(EVENTS.bstack1l111111l11_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᗊ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᗋ"), True, None, None, None, None, test_name=bstack1111ll1l_opy_)
    def bstack11l1ll1l11_opy_(self, driver, platform_index):
        if self.bstack1ll1lll11l_opy_.bstack1l11ll1ll1_opy_() is True or self.bstack1ll1lll11l_opy_.capturing() is True:
            return
        self.bstack1ll1lll11l_opy_.bstack1l1111l1l1_opy_()
        while not self.bstack1ll1lll11l_opy_.bstack1l11ll1ll1_opy_():
            bstack1l111111lll_opy_ = self.bstack1ll1lll11l_opy_.bstack111l11ll1l_opy_()
            self.bstack1ll1111ll_opy_(driver, bstack1l111111lll_opy_, platform_index)
        self.bstack1ll1lll11l_opy_.bstack11lll1llll_opy_()
    def bstack1ll1111ll_opy_(self, driver, bstack1l1l1l11l_opy_, platform_index, test=None):
        from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
        bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l1111llll_opy_.value)
        if test != None:
            bstack111llll1_opy_ = getattr(test, bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗌ"), None)
            bstack1l111lll1l_opy_ = getattr(test, bstack1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᗍ"), None)
            PercySDK.screenshot(driver, bstack1l1l1l11l_opy_, bstack111llll1_opy_=bstack111llll1_opy_, bstack1l111lll1l_opy_=bstack1l111lll1l_opy_, bstack11lllllll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1l1l11l_opy_)
        bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1111llll_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᗎ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᗏ"), True, None, None, None, None, test_name=bstack1l1l1l11l_opy_)
    def bstack1l111111l1l_opy_(self):
        os.environ[bstack1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪᗐ")] = str(self.bstack11lllllll1l_opy_.success)
        os.environ[bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪᗑ")] = str(self.bstack11lllllll1l_opy_.percy_capture_mode)
        self.percy.bstack1l11111111l_opy_(self.bstack11lllllll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1111111l1_opy_(self.bstack11lllllll1l_opy_.percy_build_id)