# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1l1ll1_opy_ import bstack1llll1l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1l1_opy_ import (
    bstack1llllllll1l_opy_,
    bstack1lllll1l11l_opy_,
    bstack111111l111_opy_,
)
from bstack_utils.helper import  bstack11l1llllll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1111ll_opy_, bstack1ll1lll1l11_opy_, bstack1lll11ll111_opy_, bstack1lll1ll1111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11l1lll11_opy_ import bstack1lll1l111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1lll1ll1l1l_opy_
from bstack_utils.percy import bstack11ll1l1ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l11ll1_opy_(bstack1llll1l1l1l_opy_):
    def __init__(self, bstack1l1l1l1llll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l1llll_opy_ = bstack1l1l1l1llll_opy_
        self.percy = bstack11ll1l1ll_opy_()
        self.bstack1l1l1ll111_opy_ = bstack1lll1l111_opy_()
        self.bstack1l1l1l1l1l1_opy_()
        bstack1llll11l111_opy_.bstack1ll11l1l111_opy_((bstack1llllllll1l_opy_.bstack1lllll11l1l_opy_, bstack1lllll1l11l_opy_.PRE), self.bstack1l1l1l1ll1l_opy_)
        TestFramework.bstack1ll11l1l111_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll11ll111_opy_.POST), self.bstack1ll111l1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1l1l1l_opy_(self, instance: bstack111111l111_opy_, driver: object):
        bstack1l1l1lll111_opy_ = TestFramework.bstack1llll1lllll_opy_(instance.context)
        for t in bstack1l1l1lll111_opy_:
            bstack1l1llll1ll1_opy_ = TestFramework.bstack1llllll1lll_opy_(t, bstack1lll1ll1l1l_opy_.bstack1l1ll111l11_opy_, [])
            if any(instance is d[1] for d in bstack1l1llll1ll1_opy_) or instance == driver:
                return t
    def bstack1l1l1l1ll1l_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack111111l111_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1llllllll1l_opy_, bstack1lllll1l11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll11l111_opy_.bstack1ll1l111l1l_opy_(method_name):
                return
            platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll11l111_opy_.bstack1ll11ll1l11_opy_, 0)
            bstack1l1ll11l1ll_opy_ = self.bstack1l1ll1l1l1l_opy_(instance, driver)
            bstack1l1l1l1l11l_opy_ = TestFramework.bstack1llllll1lll_opy_(bstack1l1ll11l1ll_opy_, TestFramework.bstack1l1l1l1l111_opy_, None)
            if not bstack1l1l1l1l11l_opy_:
                self.logger.debug(bstack1ll1ll_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥዓ"))
                return
            driver_command = f.bstack1ll111ll1ll_opy_(*args)
            for command in bstack11l1111l1l_opy_:
                if command == driver_command:
                    self.bstack1ll1l11ll_opy_(driver, platform_index)
            bstack11ll1llll_opy_ = self.percy.bstack11l1ll111l_opy_()
            if driver_command in bstack1lll1l1ll1_opy_[bstack11ll1llll_opy_]:
                self.bstack1l1l1ll111_opy_.bstack1llllll111_opy_(bstack1l1l1l1l11l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll1ll_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧዔ"), e)
    def bstack1ll111l1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1lll1l11_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll11ll111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll11ll1l_opy_ import bstack1lll1l1ll1l_opy_
        bstack1l1llll1ll1_opy_ = f.bstack1llllll1lll_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1l1ll111l11_opy_, [])
        if not bstack1l1llll1ll1_opy_:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዕ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠨࠢዖ"))
            return
        if len(bstack1l1llll1ll1_opy_) > 1:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ዗") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠣࠤዘ"))
        bstack1l1l1l1ll11_opy_, bstack1l1l1l1lll1_opy_ = bstack1l1llll1ll1_opy_[0]
        driver = bstack1l1l1l1ll11_opy_()
        if not driver:
            self.logger.debug(bstack1ll1ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዙ") + str(kwargs) + bstack1ll1ll_opy_ (u"ࠥࠦዚ"))
            return
        bstack1l1l1l11ll1_opy_ = {
            TestFramework.bstack1ll1l111l11_opy_: bstack1ll1ll_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢዛ"),
            TestFramework.bstack1ll1l1111ll_opy_: bstack1ll1ll_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣዜ"),
            TestFramework.bstack1l1l1l1l111_opy_: bstack1ll1ll_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣዝ")
        }
        bstack1l1l1l111ll_opy_ = { key: f.bstack1llllll1lll_opy_(instance, key) for key in bstack1l1l1l11ll1_opy_ }
        bstack1l1l1l11l11_opy_ = [key for key, value in bstack1l1l1l111ll_opy_.items() if not value]
        if bstack1l1l1l11l11_opy_:
            for key in bstack1l1l1l11l11_opy_:
                self.logger.debug(bstack1ll1ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥዞ") + str(key) + bstack1ll1ll_opy_ (u"ࠣࠤዟ"))
            return
        platform_index = f.bstack1llllll1lll_opy_(instance, bstack1llll11l111_opy_.bstack1ll11ll1l11_opy_, 0)
        if self.bstack1l1l1l1llll_opy_.percy_capture_mode == bstack1ll1ll_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦዠ"):
            bstack1l1111l111_opy_ = bstack1l1l1l111ll_opy_.get(TestFramework.bstack1l1l1l1l111_opy_) + bstack1ll1ll_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨዡ")
            bstack1ll11l11l1l_opy_ = bstack1lll1l1ll1l_opy_.bstack1ll11ll11ll_opy_(EVENTS.bstack1l1l1l1l1ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1111l111_opy_,
                bstack1ll1l1llll_opy_=bstack1l1l1l111ll_opy_[TestFramework.bstack1ll1l111l11_opy_],
                bstack11lll1l11_opy_=bstack1l1l1l111ll_opy_[TestFramework.bstack1ll1l1111ll_opy_],
                bstack1l1lllll1_opy_=platform_index
            )
            bstack1lll1l1ll1l_opy_.end(EVENTS.bstack1l1l1l1l1ll_opy_.value, bstack1ll11l11l1l_opy_+bstack1ll1ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦዢ"), bstack1ll11l11l1l_opy_+bstack1ll1ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥዣ"), True, None, None, None, None, test_name=bstack1l1111l111_opy_)
    def bstack1ll1l11ll_opy_(self, driver, platform_index):
        if self.bstack1l1l1ll111_opy_.bstack1l11l1l1l1_opy_() is True or self.bstack1l1l1ll111_opy_.capturing() is True:
            return
        self.bstack1l1l1ll111_opy_.bstack1l1lllllll_opy_()
        while not self.bstack1l1l1ll111_opy_.bstack1l11l1l1l1_opy_():
            bstack1l1l1l1l11l_opy_ = self.bstack1l1l1ll111_opy_.bstack1lll1l1l11_opy_()
            self.bstack11lll1llll_opy_(driver, bstack1l1l1l1l11l_opy_, platform_index)
        self.bstack1l1l1ll111_opy_.bstack1lllll1lll_opy_()
    def bstack11lll1llll_opy_(self, driver, bstack1l1l11llll_opy_, platform_index, test=None):
        from bstack_utils.bstack11ll11ll1l_opy_ import bstack1lll1l1ll1l_opy_
        bstack1ll11l11l1l_opy_ = bstack1lll1l1ll1l_opy_.bstack1ll11ll11ll_opy_(EVENTS.bstack1l1l1llll1_opy_.value)
        if test != None:
            bstack1ll1l1llll_opy_ = getattr(test, bstack1ll1ll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫዤ"), None)
            bstack11lll1l11_opy_ = getattr(test, bstack1ll1ll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬዥ"), None)
            PercySDK.screenshot(driver, bstack1l1l11llll_opy_, bstack1ll1l1llll_opy_=bstack1ll1l1llll_opy_, bstack11lll1l11_opy_=bstack11lll1l11_opy_, bstack1l1lllll1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1l11llll_opy_)
        bstack1lll1l1ll1l_opy_.end(EVENTS.bstack1l1l1llll1_opy_.value, bstack1ll11l11l1l_opy_+bstack1ll1ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣዦ"), bstack1ll11l11l1l_opy_+bstack1ll1ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢዧ"), True, None, None, None, None, test_name=bstack1l1l11llll_opy_)
    def bstack1l1l1l1l1l1_opy_(self):
        os.environ[bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨየ")] = str(self.bstack1l1l1l1llll_opy_.success)
        os.environ[bstack1ll1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨዩ")] = str(self.bstack1l1l1l1llll_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l11lll_opy_(self.bstack1l1l1l1llll_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l11l1l_opy_(self.bstack1l1l1l1llll_opy_.percy_build_id)