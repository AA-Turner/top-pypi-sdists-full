# coding: UTF-8
import sys
bstack1ll11l1_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack11lll_opy_ = 7
def bstack1l11l11_opy_ (bstack1llll11_opy_):
    global bstack11ll1l1_opy_
    bstack111l111_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11lll11_opy_ = bstack1llll11_opy_ [:-1]
    bstack1ll11_opy_ = bstack111l111_opy_ % len (bstack11lll11_opy_)
    bstack1l1l_opy_ = bstack11lll11_opy_ [:bstack1ll11_opy_] + bstack11lll11_opy_ [bstack1ll11_opy_:]
    if bstack1ll11l1_opy_:
        bstack11l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    else:
        bstack11l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack111l1l1_opy_ + bstack111l111_opy_) % bstack11lll_opy_) for bstack111l1l1_opy_, char in enumerate (bstack1l1l_opy_)])
    return eval (bstack11l1l1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l111ll_opy_ import bstack1lll1l11lll_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1llll1l1lll_opy_,
    bstack1lllllllll1_opy_,
    bstack1lllll111ll_opy_,
)
from bstack_utils.helper import  bstack1l111ll111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1111_opy_ import bstack1ll1llll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1lll1_opy_, bstack1lll11l1l11_opy_, bstack1lll1llll11_opy_, bstack1ll1l1ll111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1lll1lll_opy_ import bstack1lll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1ll_opy_ import bstack1lll111llll_opy_
from bstack_utils.percy import bstack1l11l11l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11lll1l_opy_(bstack1lll1l11lll_opy_):
    def __init__(self, bstack1l1l1l1l1l1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l1l1l1_opy_ = bstack1l1l1l1l1l1_opy_
        self.percy = bstack1l11l11l_opy_()
        self.bstack1l1l1l1l1_opy_ = bstack1lll11l11l_opy_()
        self.bstack1l1l1l1111l_opy_()
        bstack1ll1llll111_opy_.bstack1ll1l111l11_opy_((bstack1llll1l1lll_opy_.bstack1llll1ll111_opy_, bstack1lllllllll1_opy_.PRE), self.bstack1l1l1l11l1l_opy_)
        TestFramework.bstack1ll1l111l11_opy_((bstack1lll1l1lll1_opy_.TEST, bstack1lll1llll11_opy_.POST), self.bstack1ll1111llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll11lll_opy_(self, instance: bstack1lllll111ll_opy_, driver: object):
        bstack1l1ll1l1ll1_opy_ = TestFramework.bstack1lllll11l11_opy_(instance.context)
        for t in bstack1l1ll1l1ll1_opy_:
            bstack1l1lll1l111_opy_ = TestFramework.bstack1lllllll11l_opy_(t, bstack1lll111llll_opy_.bstack1l1lll11111_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1l111_opy_) or instance == driver:
                return t
    def bstack1l1l1l11l1l_opy_(
        self,
        f: bstack1ll1llll111_opy_,
        driver: object,
        exec: Tuple[bstack1lllll111ll_opy_, str],
        bstack1llllll11l1_opy_: Tuple[bstack1llll1l1lll_opy_, bstack1lllllllll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1llll111_opy_.bstack1ll11l1llll_opy_(method_name):
                return
            platform_index = f.bstack1lllllll11l_opy_(instance, bstack1ll1llll111_opy_.bstack1ll11l1l11l_opy_, 0)
            bstack1l1ll1111l1_opy_ = self.bstack1l1lll11lll_opy_(instance, driver)
            bstack1l1l1l111ll_opy_ = TestFramework.bstack1lllllll11l_opy_(bstack1l1ll1111l1_opy_, TestFramework.bstack1l1l1l11ll1_opy_, None)
            if not bstack1l1l1l111ll_opy_:
                self.logger.debug(bstack1l11l11_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥዓ"))
                return
            driver_command = f.bstack1ll11l1lll1_opy_(*args)
            for command in bstack11ll11l11_opy_:
                if command == driver_command:
                    self.bstack1l11llll1l_opy_(driver, platform_index)
            bstack1ll1l11111_opy_ = self.percy.bstack1l1ll111l_opy_()
            if driver_command in bstack1l11l1111_opy_[bstack1ll1l11111_opy_]:
                self.bstack1l1l1l1l1_opy_.bstack1l1llll1l_opy_(bstack1l1l1l111ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l11l11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧዔ"), e)
    def bstack1ll1111llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1l11_opy_,
        bstack1llllll11l1_opy_: Tuple[bstack1lll1l1lll1_opy_, bstack1lll1llll11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1ll1l1lllll_opy_
        bstack1l1lll1l111_opy_ = f.bstack1lllllll11l_opy_(instance, bstack1lll111llll_opy_.bstack1l1lll11111_opy_, [])
        if not bstack1l1lll1l111_opy_:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዕ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠨࠢዖ"))
            return
        if len(bstack1l1lll1l111_opy_) > 1:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ዗") + str(kwargs) + bstack1l11l11_opy_ (u"ࠣࠤዘ"))
        bstack1l1l11lllll_opy_, bstack1l1l1l1l11l_opy_ = bstack1l1lll1l111_opy_[0]
        driver = bstack1l1l11lllll_opy_()
        if not driver:
            self.logger.debug(bstack1l11l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዙ") + str(kwargs) + bstack1l11l11_opy_ (u"ࠥࠦዚ"))
            return
        bstack1l1l11llll1_opy_ = {
            TestFramework.bstack1ll11lll1l1_opy_: bstack1l11l11_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢዛ"),
            TestFramework.bstack1ll1l1111l1_opy_: bstack1l11l11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣዜ"),
            TestFramework.bstack1l1l1l11ll1_opy_: bstack1l11l11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣዝ")
        }
        bstack1l1l1l1l111_opy_ = { key: f.bstack1lllllll11l_opy_(instance, key) for key in bstack1l1l11llll1_opy_ }
        bstack1l1l1l11lll_opy_ = [key for key, value in bstack1l1l1l1l111_opy_.items() if not value]
        if bstack1l1l1l11lll_opy_:
            for key in bstack1l1l1l11lll_opy_:
                self.logger.debug(bstack1l11l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥዞ") + str(key) + bstack1l11l11_opy_ (u"ࠣࠤዟ"))
            return
        platform_index = f.bstack1lllllll11l_opy_(instance, bstack1ll1llll111_opy_.bstack1ll11l1l11l_opy_, 0)
        if self.bstack1l1l1l1l1l1_opy_.percy_capture_mode == bstack1l11l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦዠ"):
            bstack1l1ll11l1_opy_ = bstack1l1l1l1l111_opy_.get(TestFramework.bstack1l1l1l11ll1_opy_) + bstack1l11l11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨዡ")
            bstack1ll11l1l111_opy_ = bstack1ll1l1lllll_opy_.bstack1ll11llllll_opy_(EVENTS.bstack1l1l1l11l11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1ll11l1_opy_,
                bstack111l11lll_opy_=bstack1l1l1l1l111_opy_[TestFramework.bstack1ll11lll1l1_opy_],
                bstack1lll1ll111_opy_=bstack1l1l1l1l111_opy_[TestFramework.bstack1ll1l1111l1_opy_],
                bstack1ll11ll111_opy_=platform_index
            )
            bstack1ll1l1lllll_opy_.end(EVENTS.bstack1l1l1l11l11_opy_.value, bstack1ll11l1l111_opy_+bstack1l11l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦዢ"), bstack1ll11l1l111_opy_+bstack1l11l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥዣ"), True, None, None, None, None, test_name=bstack1l1ll11l1_opy_)
    def bstack1l11llll1l_opy_(self, driver, platform_index):
        if self.bstack1l1l1l1l1_opy_.bstack111l1l111_opy_() is True or self.bstack1l1l1l1l1_opy_.capturing() is True:
            return
        self.bstack1l1l1l1l1_opy_.bstack11lll1111l_opy_()
        while not self.bstack1l1l1l1l1_opy_.bstack111l1l111_opy_():
            bstack1l1l1l111ll_opy_ = self.bstack1l1l1l1l1_opy_.bstack1llllll11l_opy_()
            self.bstack11l1lll1ll_opy_(driver, bstack1l1l1l111ll_opy_, platform_index)
        self.bstack1l1l1l1l1_opy_.bstack111lll11_opy_()
    def bstack11l1lll1ll_opy_(self, driver, bstack11l1ll11l1_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1l11llll_opy_ import bstack1ll1l1lllll_opy_
        bstack1ll11l1l111_opy_ = bstack1ll1l1lllll_opy_.bstack1ll11llllll_opy_(EVENTS.bstack11ll11l111_opy_.value)
        if test != None:
            bstack111l11lll_opy_ = getattr(test, bstack1l11l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫዤ"), None)
            bstack1lll1ll111_opy_ = getattr(test, bstack1l11l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬዥ"), None)
            PercySDK.screenshot(driver, bstack11l1ll11l1_opy_, bstack111l11lll_opy_=bstack111l11lll_opy_, bstack1lll1ll111_opy_=bstack1lll1ll111_opy_, bstack1ll11ll111_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1ll11l1_opy_)
        bstack1ll1l1lllll_opy_.end(EVENTS.bstack11ll11l111_opy_.value, bstack1ll11l1l111_opy_+bstack1l11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣዦ"), bstack1ll11l1l111_opy_+bstack1l11l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢዧ"), True, None, None, None, None, test_name=bstack11l1ll11l1_opy_)
    def bstack1l1l1l1111l_opy_(self):
        os.environ[bstack1l11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨየ")] = str(self.bstack1l1l1l1l1l1_opy_.success)
        os.environ[bstack1l11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨዩ")] = str(self.bstack1l1l1l1l1l1_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l11111_opy_(self.bstack1l1l1l1l1l1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l111l1_opy_(self.bstack1l1l1l1l1l1_opy_.percy_build_id)