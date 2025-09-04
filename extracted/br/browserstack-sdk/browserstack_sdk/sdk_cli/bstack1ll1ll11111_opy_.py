# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll1l_opy_,
)
from bstack_utils.helper import  bstack1l11l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lllll1_opy_, bstack1lll1l1ll1l_opy_, bstack1ll1llll1ll_opy_, bstack1lll1l1llll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111ll111_opy_ import bstack11l1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l1l_opy_ import bstack1llll11lll1_opy_
from bstack_utils.percy import bstack1llll111l1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llll1l11l1_opy_(bstack1lll1lll111_opy_):
    def __init__(self, bstack1l1l1l11ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l11ll1_opy_ = bstack1l1l1l11ll1_opy_
        self.percy = bstack1llll111l1_opy_()
        self.bstack11l1lll11_opy_ = bstack11l1ll11ll_opy_()
        self.bstack1l1l11lll11_opy_()
        bstack1lll1l111ll_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1l1l11llll1_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), self.bstack1ll11llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1ll1ll_opy_(self, instance: bstack1llllllll1l_opy_, driver: object):
        bstack1l1l1lll11l_opy_ = TestFramework.bstack1llllll1lll_opy_(instance.context)
        for t in bstack1l1l1lll11l_opy_:
            bstack1l1ll1lll11_opy_ = TestFramework.bstack1lllll1l11l_opy_(t, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll1lll11_opy_) or instance == driver:
                return t
    def bstack1l1l11llll1_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1l111ll_opy_.bstack1ll111l111l_opy_(method_name):
                return
            platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_, 0)
            bstack1l1l1l1ll1l_opy_ = self.bstack1l1ll1ll1ll_opy_(instance, driver)
            bstack1l1l1l111ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(bstack1l1l1l1ll1l_opy_, TestFramework.bstack1l1l1l11lll_opy_, None)
            if not bstack1l1l1l111ll_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡡࡴࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡽࡪࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠣዟ"))
                return
            driver_command = f.bstack1ll111llll1_opy_(*args)
            for command in bstack1111lllll_opy_:
                if command == driver_command:
                    self.bstack111ll1ll1_opy_(driver, platform_index)
            bstack11111ll1_opy_ = self.percy.bstack1l1l1l11_opy_()
            if driver_command in bstack1l1l11lll1_opy_[bstack11111ll1_opy_]:
                self.bstack11l1lll11_opy_.bstack111111l1_opy_(bstack1l1l1l111ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡪࡸࡲࡰࡴࠥዠ"), e)
    def bstack1ll11llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
        bstack1l1ll1lll11_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1llll11lll1_opy_.bstack1l1lll1l1l1_opy_, [])
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧዡ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠦࠧዢ"))
            return
        if len(bstack1l1ll1lll11_opy_) > 1:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዣ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠨࠢዤ"))
        bstack1l1l1l11111_opy_, bstack1l1l11lllll_opy_ = bstack1l1ll1lll11_opy_[0]
        driver = bstack1l1l1l11111_opy_()
        if not driver:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዥ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠣࠤዦ"))
            return
        bstack1l1l1l1111l_opy_ = {
            TestFramework.bstack1ll111l1l11_opy_: bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧዧ"),
            TestFramework.bstack1ll1111ll1l_opy_: bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨየ"),
            TestFramework.bstack1l1l1l11lll_opy_: bstack1111l1l_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡵࡩࡷࡻ࡮ࠡࡰࡤࡱࡪࠨዩ")
        }
        bstack1l1l11lll1l_opy_ = { key: f.bstack1lllll1l11l_opy_(instance, key) for key in bstack1l1l1l1111l_opy_ }
        bstack1l1l1l11l11_opy_ = [key for key, value in bstack1l1l11lll1l_opy_.items() if not value]
        if bstack1l1l1l11l11_opy_:
            for key in bstack1l1l1l11l11_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠣዪ") + str(key) + bstack1111l1l_opy_ (u"ࠨࠢያ"))
            return
        platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_, 0)
        if self.bstack1l1l1l11ll1_opy_.percy_capture_mode == bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤዬ"):
            bstack11l1ll1111_opy_ = bstack1l1l11lll1l_opy_.get(TestFramework.bstack1l1l1l11lll_opy_) + bstack1111l1l_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦይ")
            bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l1l1l111l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11l1ll1111_opy_,
                bstack1ll1l1111l_opy_=bstack1l1l11lll1l_opy_[TestFramework.bstack1ll111l1l11_opy_],
                bstack1l1l11l11_opy_=bstack1l1l11lll1l_opy_[TestFramework.bstack1ll1111ll1l_opy_],
                bstack1l11l11ll1_opy_=platform_index
            )
            bstack1lll11111ll_opy_.end(EVENTS.bstack1l1l1l111l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤዮ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣዯ"), True, None, None, None, None, test_name=bstack11l1ll1111_opy_)
    def bstack111ll1ll1_opy_(self, driver, platform_index):
        if self.bstack11l1lll11_opy_.bstack1l1lll1l_opy_() is True or self.bstack11l1lll11_opy_.capturing() is True:
            return
        self.bstack11l1lll11_opy_.bstack1lll11l1l1_opy_()
        while not self.bstack11l1lll11_opy_.bstack1l1lll1l_opy_():
            bstack1l1l1l111ll_opy_ = self.bstack11l1lll11_opy_.bstack11lll11ll_opy_()
            self.bstack1l1ll1ll_opy_(driver, bstack1l1l1l111ll_opy_, platform_index)
        self.bstack11l1lll11_opy_.bstack1ll1ll1l1l_opy_()
    def bstack1l1ll1ll_opy_(self, driver, bstack1lll11l11_opy_, platform_index, test=None):
        from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
        bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1ll1l11l1_opy_.value)
        if test != None:
            bstack1ll1l1111l_opy_ = getattr(test, bstack1111l1l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩደ"), None)
            bstack1l1l11l11_opy_ = getattr(test, bstack1111l1l_opy_ (u"ࠬࡻࡵࡪࡦࠪዱ"), None)
            PercySDK.screenshot(driver, bstack1lll11l11_opy_, bstack1ll1l1111l_opy_=bstack1ll1l1111l_opy_, bstack1l1l11l11_opy_=bstack1l1l11l11_opy_, bstack1l11l11ll1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll11l11_opy_)
        bstack1lll11111ll_opy_.end(EVENTS.bstack1ll1l11l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨዲ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧዳ"), True, None, None, None, None, test_name=bstack1lll11l11_opy_)
    def bstack1l1l11lll11_opy_(self):
        os.environ[bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭ዴ")] = str(self.bstack1l1l1l11ll1_opy_.success)
        os.environ[bstack1111l1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭ድ")] = str(self.bstack1l1l1l11ll1_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l1l111_opy_(self.bstack1l1l1l11ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l11l1l_opy_(self.bstack1l1l1l11ll1_opy_.percy_build_id)