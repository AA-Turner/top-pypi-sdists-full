# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llllllll1l_opy_,
    bstack11111111l1_opy_,
)
from bstack_utils.helper import  bstack11ll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1l1lll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l11l1l_opy_, bstack1ll1ll11l1l_opy_, bstack1lll111l111_opy_, bstack1ll1l1ll11l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l11l1111l_opy_ import bstack11llll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l1ll1_opy_
from bstack_utils.percy import bstack111l1ll1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llll1111l1_opy_(bstack1ll1l1ll1ll_opy_):
    def __init__(self, bstack1l1l1l11ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l11ll1_opy_ = bstack1l1l1l11ll1_opy_
        self.percy = bstack111l1ll1l_opy_()
        self.bstack1ll1ll1l11_opy_ = bstack11llll1lll_opy_()
        self.bstack1l1l1l11l1l_opy_()
        bstack1ll1l1lll11_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1l1l1l1l1ll_opy_)
        TestFramework.bstack1ll1l11ll1l_opy_((bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.POST), self.bstack1ll11ll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1llll11_opy_(self, instance: bstack11111111l1_opy_, driver: object):
        bstack1l1ll1lll11_opy_ = TestFramework.bstack1llllll1111_opy_(instance.context)
        for t in bstack1l1ll1lll11_opy_:
            bstack1l1l1lll1ll_opy_ = TestFramework.bstack1llllll1l1l_opy_(t, bstack1lll11l1ll1_opy_.bstack1l1lll11l11_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1lll1ll_opy_) or instance == driver:
                return t
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1l1lll11_opy_.bstack1ll111l1111_opy_(method_name):
                return
            platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_, 0)
            bstack1l1l1l1llll_opy_ = self.bstack1l1l1llll11_opy_(instance, driver)
            bstack1l1l1l11l11_opy_ = TestFramework.bstack1llllll1l1l_opy_(bstack1l1l1l1llll_opy_, TestFramework.bstack1l1l1l111ll_opy_, None)
            if not bstack1l1l1l11l11_opy_:
                self.logger.debug(bstackl_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥዓ"))
                return
            driver_command = f.bstack1ll11l1ll1l_opy_(*args)
            for command in bstack11l1llll_opy_:
                if command == driver_command:
                    self.bstack1ll11l1l_opy_(driver, platform_index)
            bstack1l1lll111l_opy_ = self.percy.bstack1l1l111111_opy_()
            if driver_command in bstack1llll11111_opy_[bstack1l1lll111l_opy_]:
                self.bstack1ll1ll1l11_opy_.bstack1llll11l1_opy_(bstack1l1l1l11l11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstackl_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧዔ"), e)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
        bstack1l1l1lll1ll_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1l1lll11l11_opy_, [])
        if not bstack1l1l1lll1ll_opy_:
            self.logger.debug(bstackl_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዕ") + str(kwargs) + bstackl_opy_ (u"ࠨࠢዖ"))
            return
        if len(bstack1l1l1lll1ll_opy_) > 1:
            self.logger.debug(bstackl_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ዗") + str(kwargs) + bstackl_opy_ (u"ࠣࠤዘ"))
        bstack1l1l1l1l111_opy_, bstack1l1l1l1111l_opy_ = bstack1l1l1lll1ll_opy_[0]
        driver = bstack1l1l1l1l111_opy_()
        if not driver:
            self.logger.debug(bstackl_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዙ") + str(kwargs) + bstackl_opy_ (u"ࠥࠦዚ"))
            return
        bstack1l1l11lllll_opy_ = {
            TestFramework.bstack1ll1l111l1l_opy_: bstackl_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢዛ"),
            TestFramework.bstack1ll11l11lll_opy_: bstackl_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣዜ"),
            TestFramework.bstack1l1l1l111ll_opy_: bstackl_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣዝ")
        }
        bstack1l1l1l11111_opy_ = { key: f.bstack1llllll1l1l_opy_(instance, key) for key in bstack1l1l11lllll_opy_ }
        bstack1l1l1l11lll_opy_ = [key for key, value in bstack1l1l1l11111_opy_.items() if not value]
        if bstack1l1l1l11lll_opy_:
            for key in bstack1l1l1l11lll_opy_:
                self.logger.debug(bstackl_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥዞ") + str(key) + bstackl_opy_ (u"ࠣࠤዟ"))
            return
        platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_, 0)
        if self.bstack1l1l1l11ll1_opy_.percy_capture_mode == bstackl_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦዠ"):
            bstack1l1l1lll11_opy_ = bstack1l1l1l11111_opy_.get(TestFramework.bstack1l1l1l111ll_opy_) + bstackl_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨዡ")
            bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack1l1l1l111l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1l1lll11_opy_,
                bstack11ll1111l_opy_=bstack1l1l1l11111_opy_[TestFramework.bstack1ll1l111l1l_opy_],
                bstack1ll1lllll1_opy_=bstack1l1l1l11111_opy_[TestFramework.bstack1ll11l11lll_opy_],
                bstack111l11ll_opy_=platform_index
            )
            bstack1lll11lll1l_opy_.end(EVENTS.bstack1l1l1l111l1_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦዢ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠧࡀࡥ࡯ࡦࠥዣ"), True, None, None, None, None, test_name=bstack1l1l1lll11_opy_)
    def bstack1ll11l1l_opy_(self, driver, platform_index):
        if self.bstack1ll1ll1l11_opy_.bstack11lll1ll1l_opy_() is True or self.bstack1ll1ll1l11_opy_.capturing() is True:
            return
        self.bstack1ll1ll1l11_opy_.bstack11l11ll1l_opy_()
        while not self.bstack1ll1ll1l11_opy_.bstack11lll1ll1l_opy_():
            bstack1l1l1l11l11_opy_ = self.bstack1ll1ll1l11_opy_.bstack11lllll1_opy_()
            self.bstack1ll1l111l_opy_(driver, bstack1l1l1l11l11_opy_, platform_index)
        self.bstack1ll1ll1l11_opy_.bstack11ll1llll1_opy_()
    def bstack1ll1l111l_opy_(self, driver, bstack1111lll1l_opy_, platform_index, test=None):
        from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
        bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack111l1111l_opy_.value)
        if test != None:
            bstack11ll1111l_opy_ = getattr(test, bstackl_opy_ (u"࠭࡮ࡢ࡯ࡨࠫዤ"), None)
            bstack1ll1lllll1_opy_ = getattr(test, bstackl_opy_ (u"ࠧࡶࡷ࡬ࡨࠬዥ"), None)
            PercySDK.screenshot(driver, bstack1111lll1l_opy_, bstack11ll1111l_opy_=bstack11ll1111l_opy_, bstack1ll1lllll1_opy_=bstack1ll1lllll1_opy_, bstack111l11ll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1111lll1l_opy_)
        bstack1lll11lll1l_opy_.end(EVENTS.bstack111l1111l_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣዦ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠤ࠽ࡩࡳࡪࠢዧ"), True, None, None, None, None, test_name=bstack1111lll1l_opy_)
    def bstack1l1l1l11l1l_opy_(self):
        os.environ[bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨየ")] = str(self.bstack1l1l1l11ll1_opy_.success)
        os.environ[bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨዩ")] = str(self.bstack1l1l1l11ll1_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l1l1l1_opy_(self.bstack1l1l1l11ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l1l11l_opy_(self.bstack1l1l1l11ll1_opy_.percy_build_id)