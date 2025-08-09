# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1llll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1l1l_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llll1lll11_opy_,
    bstack1lllll1ll1l_opy_,
)
from bstack_utils.helper import  bstack1ll11l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import bstack1llll1l11l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l111ll_opy_, bstack1lll1111l1l_opy_, bstack1lll1ll1l1l_opy_, bstack1llll111l1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11l1111111_opy_ import bstack1l11ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l1l1l1_opy_
from bstack_utils.percy import bstack11111111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l1llll_opy_(bstack1llll11l11l_opy_):
    def __init__(self, bstack1l1l1l1l11l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l1l11l_opy_ = bstack1l1l1l1l11l_opy_
        self.percy = bstack11111111_opy_()
        self.bstack1lllll1111_opy_ = bstack1l11ll1ll_opy_()
        self.bstack1l1l1l1l1ll_opy_()
        bstack1llll1l11l1_opy_.bstack1ll11lll111_opy_((bstack1llllllllll_opy_.bstack1llllll111l_opy_, bstack1llll1lll11_opy_.PRE), self.bstack1l1l1l1llll_opy_)
        TestFramework.bstack1ll11lll111_opy_((bstack1lll1l111ll_opy_.TEST, bstack1lll1ll1l1l_opy_.POST), self.bstack1ll11l1l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll111l_opy_(self, instance: bstack1lllll1ll1l_opy_, driver: object):
        bstack1l1ll1111ll_opy_ = TestFramework.bstack1lllllll1ll_opy_(instance.context)
        for t in bstack1l1ll1111ll_opy_:
            bstack1l1ll1ll111_opy_ = TestFramework.bstack1lllllllll1_opy_(t, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll1ll111_opy_) or instance == driver:
                return t
    def bstack1l1l1l1llll_opy_(
        self,
        f: bstack1llll1l11l1_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1lllllll11l_opy_: Tuple[bstack1llllllllll_opy_, bstack1llll1lll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll1l11l1_opy_.bstack1ll11ll111l_opy_(method_name):
                return
            platform_index = f.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_, 0)
            bstack1l1lll111l1_opy_ = self.bstack1l1l1ll111l_opy_(instance, driver)
            bstack1l1l1l11ll1_opy_ = TestFramework.bstack1lllllllll1_opy_(bstack1l1lll111l1_opy_, TestFramework.bstack1l1l1l1ll11_opy_, None)
            if not bstack1l1l1l11ll1_opy_:
                self.logger.debug(bstack11l1_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦዔ"))
                return
            driver_command = f.bstack1ll1l11l11l_opy_(*args)
            for command in bstack1l111l11l_opy_:
                if command == driver_command:
                    self.bstack11l1lll1_opy_(driver, platform_index)
            bstack1lll1l111l_opy_ = self.percy.bstack1111llll1_opy_()
            if driver_command in bstack1l1l1l1lll_opy_[bstack1lll1l111l_opy_]:
                self.bstack1lllll1111_opy_.bstack11llll11l1_opy_(bstack1l1l1l11ll1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11l1_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨዕ"), e)
    def bstack1ll11l1l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack1lllllll11l_opy_: Tuple[bstack1lll1l111ll_opy_, bstack1lll1ll1l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
        bstack1l1ll1ll111_opy_ = f.bstack1lllllllll1_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11l111_opy_, [])
        if not bstack1l1ll1ll111_opy_:
            self.logger.debug(bstack11l1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዖ") + str(kwargs) + bstack11l1_opy_ (u"ࠢࠣ዗"))
            return
        if len(bstack1l1ll1ll111_opy_) > 1:
            self.logger.debug(bstack11l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥዘ") + str(kwargs) + bstack11l1_opy_ (u"ࠤࠥዙ"))
        bstack1l1l1l11lll_opy_, bstack1l1l1l1l111_opy_ = bstack1l1ll1ll111_opy_[0]
        driver = bstack1l1l1l11lll_opy_()
        if not driver:
            self.logger.debug(bstack11l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዚ") + str(kwargs) + bstack11l1_opy_ (u"ࠦࠧዛ"))
            return
        bstack1l1l1l1l1l1_opy_ = {
            TestFramework.bstack1ll11lll1ll_opy_: bstack11l1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣዜ"),
            TestFramework.bstack1ll1l111l1l_opy_: bstack11l1_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤዝ"),
            TestFramework.bstack1l1l1l1ll11_opy_: bstack11l1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤዞ")
        }
        bstack1l1l1l11l11_opy_ = { key: f.bstack1lllllllll1_opy_(instance, key) for key in bstack1l1l1l1l1l1_opy_ }
        bstack1l1l1l1lll1_opy_ = [key for key, value in bstack1l1l1l11l11_opy_.items() if not value]
        if bstack1l1l1l1lll1_opy_:
            for key in bstack1l1l1l1lll1_opy_:
                self.logger.debug(bstack11l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦዟ") + str(key) + bstack11l1_opy_ (u"ࠤࠥዠ"))
            return
        platform_index = f.bstack1lllllllll1_opy_(instance, bstack1llll1l11l1_opy_.bstack1ll11l1ll1l_opy_, 0)
        if self.bstack1l1l1l1l11l_opy_.percy_capture_mode == bstack11l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧዡ"):
            bstack1l1l11111l_opy_ = bstack1l1l1l11l11_opy_.get(TestFramework.bstack1l1l1l1ll11_opy_) + bstack11l1_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢዢ")
            bstack1ll111llll1_opy_ = bstack1ll1ll11111_opy_.bstack1ll11lll11l_opy_(EVENTS.bstack1l1l1l111ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1l11111l_opy_,
                bstack1ll1l1l1ll_opy_=bstack1l1l1l11l11_opy_[TestFramework.bstack1ll11lll1ll_opy_],
                bstack11ll1ll1l_opy_=bstack1l1l1l11l11_opy_[TestFramework.bstack1ll1l111l1l_opy_],
                bstack111l111l1_opy_=platform_index
            )
            bstack1ll1ll11111_opy_.end(EVENTS.bstack1l1l1l111ll_opy_.value, bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧዣ"), bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦዤ"), True, None, None, None, None, test_name=bstack1l1l11111l_opy_)
    def bstack11l1lll1_opy_(self, driver, platform_index):
        if self.bstack1lllll1111_opy_.bstack1l11ll1111_opy_() is True or self.bstack1lllll1111_opy_.capturing() is True:
            return
        self.bstack1lllll1111_opy_.bstack1l1l1ll1l_opy_()
        while not self.bstack1lllll1111_opy_.bstack1l11ll1111_opy_():
            bstack1l1l1l11ll1_opy_ = self.bstack1lllll1111_opy_.bstack11l11l11ll_opy_()
            self.bstack11ll1l11ll_opy_(driver, bstack1l1l1l11ll1_opy_, platform_index)
        self.bstack1lllll1111_opy_.bstack111llll1l_opy_()
    def bstack11ll1l11ll_opy_(self, driver, bstack1l1l11111_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
        bstack1ll111llll1_opy_ = bstack1ll1ll11111_opy_.bstack1ll11lll11l_opy_(EVENTS.bstack1lll1l11l1_opy_.value)
        if test != None:
            bstack1ll1l1l1ll_opy_ = getattr(test, bstack11l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬዥ"), None)
            bstack11ll1ll1l_opy_ = getattr(test, bstack11l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ዦ"), None)
            PercySDK.screenshot(driver, bstack1l1l11111_opy_, bstack1ll1l1l1ll_opy_=bstack1ll1l1l1ll_opy_, bstack11ll1ll1l_opy_=bstack11ll1ll1l_opy_, bstack111l111l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1l11111_opy_)
        bstack1ll1ll11111_opy_.end(EVENTS.bstack1lll1l11l1_opy_.value, bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤዧ"), bstack1ll111llll1_opy_+bstack11l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣየ"), True, None, None, None, None, test_name=bstack1l1l11111_opy_)
    def bstack1l1l1l1l1ll_opy_(self):
        os.environ[bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩዩ")] = str(self.bstack1l1l1l1l11l_opy_.success)
        os.environ[bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩዪ")] = str(self.bstack1l1l1l1l11l_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l1ll1l_opy_(self.bstack1l1l1l1l11l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l11l1l_opy_(self.bstack1l1l1l1l11l_opy_.percy_build_id)