# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack1ll11ll1l11_opy_,
)
from bstack_utils.helper import  bstack1l11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1lllll1_opy_, TestHookState, bstack1l1l11lll1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1ll1l1llll_opy_ import bstack11l111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1111_opy_ import bstack1l1llll11ll_opy_
from bstack_utils.percy import bstack1lll1ll1ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1lll1ll1l_opy_(bstack1ll111l11ll_opy_):
    def __init__(self, bstack11llll11ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11llll11ll1_opy_ = bstack11llll11ll1_opy_
        self.percy = bstack1lll1ll1ll_opy_()
        self.bstack1l111ll1l_opy_ = bstack11l111l1ll_opy_()
        self.bstack11llll11l11_opy_()
        bstack1ll111l1111_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE), self.bstack11llll1l1ll_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111l11l11_opy_(self, instance: bstack1ll11ll1l11_opy_, driver: object):
        bstack1l1111ll111_opy_ = TestFramework.bstack1ll111ll1ll_opy_(instance.context)
        for t in bstack1l1111ll111_opy_:
            bstack11lllll1lll_opy_ = TestFramework.bstack1ll1l11llll_opy_(t, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
            if any(instance is d[1] for d in bstack11lllll1lll_opy_) or instance == driver:
                return t
    def bstack11llll1l1ll_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll111l1111_opy_.bstack1l1l11111ll_opy_(method_name):
                return
            platform_index = f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_, 0)
            bstack11llllll1l1_opy_ = self.bstack1l111l11l11_opy_(instance, driver)
            bstack11llll1l111_opy_ = TestFramework.bstack1ll1l11llll_opy_(bstack11llllll1l1_opy_, TestFramework.bstack11lll1lllll_opy_, None)
            if not bstack11llll1l111_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡡࡴࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡽࡪࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠣᘄ"))
                return
            driver_command = f.bstack1l11llll11l_opy_(*args)
            for command in bstack11ll1ll11_opy_:
                if command == driver_command:
                    self.bstack11111l1111_opy_(driver, platform_index)
            bstack1llll1l1_opy_ = self.percy.bstack1ll1lllll_opy_()
            if driver_command in bstack1l111lll1l_opy_[bstack1llll1l1_opy_]:
                self.bstack1l111ll1l_opy_.bstack1lll1lll_opy_(bstack11llll1l111_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡪࡸࡲࡰࡴࠥᘅ"), e)
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
        bstack11lllll1lll_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1l1llll11ll_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lllll1lll_opy_:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᘆ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠦࠧᘇ"))
            return
        if len(bstack11lllll1lll_opy_) > 1:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᘈ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᘉ"))
        bstack11llll111ll_opy_, bstack11llll11l1l_opy_ = bstack11lllll1lll_opy_[0]
        driver = bstack11llll111ll_opy_()
        if not driver:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᘊ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠣࠤᘋ"))
            return
        bstack11llll111l1_opy_ = {
            TestFramework.bstack1l11lll1l1l_opy_: bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᘌ"),
            TestFramework.bstack1l11ll11l1l_opy_: bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᘍ"),
            TestFramework.bstack11lll1lllll_opy_: bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡵࡩࡷࡻ࡮ࠡࡰࡤࡱࡪࠨᘎ")
        }
        bstack11llll11lll_opy_ = { key: f.bstack1ll1l11llll_opy_(instance, key) for key in bstack11llll111l1_opy_ }
        bstack11llll1111l_opy_ = [key for key, value in bstack11llll11lll_opy_.items() if not value]
        if bstack11llll1111l_opy_:
            for key in bstack11llll1111l_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠣᘏ") + str(key) + bstack1ll1lll_opy_ (u"ࠨࠢᘐ"))
            return
        platform_index = f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_, 0)
        if self.bstack11llll11ll1_opy_.percy_capture_mode == bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤᘑ"):
            bstack1ll11lll11_opy_ = bstack11llll11lll_opy_.get(TestFramework.bstack11lll1lllll_opy_) + bstack1ll1lll_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦᘒ")
            bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11llll11111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll11lll11_opy_,
                bstack11l11ll1l1_opy_=bstack11llll11lll_opy_[TestFramework.bstack1l11lll1l1l_opy_],
                bstack1ll1l11ll1_opy_=bstack11llll11lll_opy_[TestFramework.bstack1l11ll11l1l_opy_],
                bstack11lll1l1ll_opy_=platform_index
            )
            bstack1l1l11ll1_opy_.end(EVENTS.bstack11llll11111_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘓ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘔ"), True, None, None, None, None, test_name=bstack1ll11lll11_opy_)
    def bstack11111l1111_opy_(self, driver, platform_index):
        if self.bstack1l111ll1l_opy_.bstack1111lll11_opy_() is True or self.bstack1l111ll1l_opy_.capturing() is True:
            return
        self.bstack1l111ll1l_opy_.bstack11lll111l_opy_()
        while not self.bstack1l111ll1l_opy_.bstack1111lll11_opy_():
            bstack11llll1l111_opy_ = self.bstack1l111ll1l_opy_.bstack11l1ll1l1_opy_()
            self.bstack1l11l11l11_opy_(driver, bstack11llll1l111_opy_, platform_index)
        self.bstack1l111ll1l_opy_.bstack1llll11l11_opy_()
    def bstack1l11l11l11_opy_(self, driver, bstack11l1llll1l_opy_, platform_index, test=None):
        from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
        bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack11llll1111_opy_.value)
        if test != None:
            bstack11l11ll1l1_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᘕ"), None)
            bstack1ll1l11ll1_opy_ = getattr(test, bstack1ll1lll_opy_ (u"ࠬࡻࡵࡪࡦࠪᘖ"), None)
            PercySDK.screenshot(driver, bstack11l1llll1l_opy_, bstack11l11ll1l1_opy_=bstack11l11ll1l1_opy_, bstack1ll1l11ll1_opy_=bstack1ll1l11ll1_opy_, bstack11lll1l1ll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1llll1l_opy_)
        bstack1l1l11ll1_opy_.end(EVENTS.bstack11llll1111_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘗ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᘘ"), True, None, None, None, None, test_name=bstack11l1llll1l_opy_)
    def bstack11llll11l11_opy_(self):
        os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ᘙ")] = str(self.bstack11llll11ll1_opy_.success)
        os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ᘚ")] = str(self.bstack11llll11ll1_opy_.percy_capture_mode)
        self.percy.bstack11llll1l11l_opy_(self.bstack11llll11ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack11llll1l1l1_opy_(self.bstack11llll11ll1_opy_.percy_build_id)