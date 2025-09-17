# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1lllllll111_opy_,
)
from bstack_utils.helper import  bstack1l11111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1lll11l1111_opy_, bstack1lll111l1l1_opy_, bstack1ll1lll1l11_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1lll1lllll_opy_ import bstack111ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1llll11111l_opy_
from bstack_utils.percy import bstack1111l11l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll111llll_opy_(bstack1ll1l1llll1_opy_):
    def __init__(self, bstack1l1l1l11ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l11ll1_opy_ = bstack1l1l1l11ll1_opy_
        self.percy = bstack1111l11l_opy_()
        self.bstack11ll11ll1l_opy_ = bstack111ll1111_opy_()
        self.bstack1l1l11lll1l_opy_()
        bstack1ll1l1l1lll_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1l1l1l11111_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1lllll_opy_(self, instance: bstack1lllllll111_opy_, driver: object):
        bstack1l1lll1111l_opy_ = TestFramework.bstack1lllllll1l1_opy_(instance.context)
        for t in bstack1l1lll1111l_opy_:
            bstack1l1l1l1l111_opy_ = TestFramework.bstack1llllllllll_opy_(t, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1l1l1l111_opy_) or instance == driver:
                return t
    def bstack1l1l1l11111_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1l1l1lll_opy_.bstack1ll11l11l11_opy_(method_name):
                return
            platform_index = f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_, 0)
            bstack1l1lll11lll_opy_ = self.bstack1l1ll1lllll_opy_(instance, driver)
            bstack1l1l1l11l1l_opy_ = TestFramework.bstack1llllllllll_opy_(bstack1l1lll11lll_opy_, TestFramework.bstack1l1l1l111l1_opy_, None)
            if not bstack1l1l1l11l1l_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨዝ"))
                return
            driver_command = f.bstack1ll1l111111_opy_(*args)
            for command in bstack111l1ll11_opy_:
                if command == driver_command:
                    self.bstack11l111l11_opy_(driver, platform_index)
            bstack1ll111l111_opy_ = self.percy.bstack11l1111l11_opy_()
            if driver_command in bstack111ll11l1_opy_[bstack1ll111l111_opy_]:
                self.bstack11ll11ll1l_opy_.bstack11111111_opy_(bstack1l1l1l11l1l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣዞ"), e)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
        bstack1l1l1l1l111_opy_ = f.bstack1llllllllll_opy_(instance, bstack1llll11111l_opy_.bstack1l1ll11l1ll_opy_, [])
        if not bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዟ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠤࠥዠ"))
            return
        if len(bstack1l1l1l1l111_opy_) > 1:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዡ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠦࠧዢ"))
        bstack1l1l11llll1_opy_, bstack1l1l1l11lll_opy_ = bstack1l1l1l1l111_opy_[0]
        driver = bstack1l1l11llll1_opy_()
        if not driver:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨዣ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠨࠢዤ"))
            return
        bstack1l1l11ll1ll_opy_ = {
            TestFramework.bstack1ll11llll1l_opy_: bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥዥ"),
            TestFramework.bstack1ll111ll1ll_opy_: bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦዦ"),
            TestFramework.bstack1l1l1l111l1_opy_: bstack1l11ll1_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦዧ")
        }
        bstack1l1l1l1111l_opy_ = { key: f.bstack1llllllllll_opy_(instance, key) for key in bstack1l1l11ll1ll_opy_ }
        bstack1l1l1l11l11_opy_ = [key for key, value in bstack1l1l1l1111l_opy_.items() if not value]
        if bstack1l1l1l11l11_opy_:
            for key in bstack1l1l1l11l11_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨየ") + str(key) + bstack1l11ll1_opy_ (u"ࠦࠧዩ"))
            return
        platform_index = f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_, 0)
        if self.bstack1l1l1l11ll1_opy_.percy_capture_mode == bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢዪ"):
            bstack1l1l1lll_opy_ = bstack1l1l1l1111l_opy_.get(TestFramework.bstack1l1l1l111l1_opy_) + bstack1l11ll1_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤያ")
            bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1l1l11lll11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1l1lll_opy_,
                bstack1llllll1l1_opy_=bstack1l1l1l1111l_opy_[TestFramework.bstack1ll11llll1l_opy_],
                bstack1ll111ll1l_opy_=bstack1l1l1l1111l_opy_[TestFramework.bstack1ll111ll1ll_opy_],
                bstack1ll11l11_opy_=platform_index
            )
            bstack1lll11111l1_opy_.end(EVENTS.bstack1l1l11lll11_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢዬ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨይ"), True, None, None, None, None, test_name=bstack1l1l1lll_opy_)
    def bstack11l111l11_opy_(self, driver, platform_index):
        if self.bstack11ll11ll1l_opy_.bstack11lll1l1l1_opy_() is True or self.bstack11ll11ll1l_opy_.capturing() is True:
            return
        self.bstack11ll11ll1l_opy_.bstack1ll1llll11_opy_()
        while not self.bstack11ll11ll1l_opy_.bstack11lll1l1l1_opy_():
            bstack1l1l1l11l1l_opy_ = self.bstack11ll11ll1l_opy_.bstack1ll111l1ll_opy_()
            self.bstack1llll1ll_opy_(driver, bstack1l1l1l11l1l_opy_, platform_index)
        self.bstack11ll11ll1l_opy_.bstack1llll1l1_opy_()
    def bstack1llll1ll_opy_(self, driver, bstack1l1l1ll111_opy_, platform_index, test=None):
        from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
        bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1lll1lll_opy_.value)
        if test != None:
            bstack1llllll1l1_opy_ = getattr(test, bstack1l11ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧዮ"), None)
            bstack1ll111ll1l_opy_ = getattr(test, bstack1l11ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨዯ"), None)
            PercySDK.screenshot(driver, bstack1l1l1ll111_opy_, bstack1llllll1l1_opy_=bstack1llllll1l1_opy_, bstack1ll111ll1l_opy_=bstack1ll111ll1l_opy_, bstack1ll11l11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1l1ll111_opy_)
        bstack1lll11111l1_opy_.end(EVENTS.bstack1lll1lll_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦደ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥዱ"), True, None, None, None, None, test_name=bstack1l1l1ll111_opy_)
    def bstack1l1l11lll1l_opy_(self):
        os.environ[bstack1l11ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫዲ")] = str(self.bstack1l1l1l11ll1_opy_.success)
        os.environ[bstack1l11ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫዳ")] = str(self.bstack1l1l1l11ll1_opy_.percy_capture_mode)
        self.percy.bstack1l1l11lllll_opy_(self.bstack1l1l1l11ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l111ll_opy_(self.bstack1l1l1l11ll1_opy_.percy_build_id)