# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack1lllll1ll1l_opy_,
)
from bstack_utils.helper import  bstack1ll11lllll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1lll_opy_, bstack1lll1lllll1_opy_, bstack1lll111llll_opy_, bstack1ll1lll1l11_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11llllllll_opy_ import bstack1ll11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1ll1ll1ll1l_opy_
from bstack_utils.percy import bstack1111l11l1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll1ll11ll1_opy_(bstack1llll1l1l11_opy_):
    def __init__(self, bstack1l1l1l1l1l1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l1l1l1_opy_ = bstack1l1l1l1l1l1_opy_
        self.percy = bstack1111l11l1_opy_()
        self.bstack1111l11l_opy_ = bstack1ll11l11l_opy_()
        self.bstack1l1l1l11ll1_opy_()
        bstack1lll1l11l11_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1l1111l_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), self.bstack1ll111lll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11111l_opy_(self, instance: bstack1lllll1ll1l_opy_, driver: object):
        bstack1l1ll1ll1ll_opy_ = TestFramework.bstack11111111l1_opy_(instance.context)
        for t in bstack1l1ll1ll1ll_opy_:
            bstack1l1ll1lll11_opy_ = TestFramework.bstack1111111l1l_opy_(t, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll1lll11_opy_) or instance == driver:
                return t
    def bstack1l1l1l1111l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1l11l11_opy_.bstack1ll11l1111l_opy_(method_name):
                return
            platform_index = f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_, 0)
            bstack1l1lll111ll_opy_ = self.bstack1l1ll11111l_opy_(instance, driver)
            bstack1l1l1l11l11_opy_ = TestFramework.bstack1111111l1l_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1l1l1l111_opy_, None)
            if not bstack1l1l1l11l11_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤዒ"))
                return
            driver_command = f.bstack1ll11llllll_opy_(*args)
            for command in bstack1l1l1l111_opy_:
                if command == driver_command:
                    self.bstack1l1lll1lll_opy_(driver, platform_index)
            bstack11lllll11l_opy_ = self.percy.bstack1l111llll1_opy_()
            if driver_command in bstack1111111ll_opy_[bstack11lllll11l_opy_]:
                self.bstack1111l11l_opy_.bstack1lll1111l_opy_(bstack1l1l1l11l11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦዓ"), e)
    def bstack1ll111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
        bstack1l1ll1lll11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1ll1ll1ll1l_opy_.bstack1l1llll111l_opy_, [])
        if not bstack1l1ll1lll11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨዔ") + str(kwargs) + bstack111l111_opy_ (u"ࠧࠨዕ"))
            return
        if len(bstack1l1ll1lll11_opy_) > 1:
            self.logger.debug(bstack111l111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣዖ") + str(kwargs) + bstack111l111_opy_ (u"ࠢࠣ዗"))
        bstack1l1l1l11lll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1ll1lll11_opy_[0]
        driver = bstack1l1l1l11lll_opy_()
        if not driver:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዘ") + str(kwargs) + bstack111l111_opy_ (u"ࠤࠥዙ"))
            return
        bstack1l1l1l11l1l_opy_ = {
            TestFramework.bstack1ll111l111l_opy_: bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨዚ"),
            TestFramework.bstack1ll11l11l1l_opy_: bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢዛ"),
            TestFramework.bstack1l1l1l1l111_opy_: bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢዜ")
        }
        bstack1l1l1l1l1ll_opy_ = { key: f.bstack1111111l1l_opy_(instance, key) for key in bstack1l1l1l11l1l_opy_ }
        bstack1l1l1l11111_opy_ = [key for key, value in bstack1l1l1l1l1ll_opy_.items() if not value]
        if bstack1l1l1l11111_opy_:
            for key in bstack1l1l1l11111_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤዝ") + str(key) + bstack111l111_opy_ (u"ࠢࠣዞ"))
            return
        platform_index = f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_, 0)
        if self.bstack1l1l1l1l1l1_opy_.percy_capture_mode == bstack111l111_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥዟ"):
            bstack11ll11111l_opy_ = bstack1l1l1l1l1ll_opy_.get(TestFramework.bstack1l1l1l1l111_opy_) + bstack111l111_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧዠ")
            bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1l1l1l1l11l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11ll11111l_opy_,
                bstack1l111l11l1_opy_=bstack1l1l1l1l1ll_opy_[TestFramework.bstack1ll111l111l_opy_],
                bstack11l11l1l1_opy_=bstack1l1l1l1l1ll_opy_[TestFramework.bstack1ll11l11l1l_opy_],
                bstack111llllll1_opy_=platform_index
            )
            bstack1llll1111l1_opy_.end(EVENTS.bstack1l1l1l1l11l_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥዡ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤዢ"), True, None, None, None, None, test_name=bstack11ll11111l_opy_)
    def bstack1l1lll1lll_opy_(self, driver, platform_index):
        if self.bstack1111l11l_opy_.bstack1l111llll_opy_() is True or self.bstack1111l11l_opy_.capturing() is True:
            return
        self.bstack1111l11l_opy_.bstack1111l1ll_opy_()
        while not self.bstack1111l11l_opy_.bstack1l111llll_opy_():
            bstack1l1l1l11l11_opy_ = self.bstack1111l11l_opy_.bstack1l1l1111l_opy_()
            self.bstack11l11111_opy_(driver, bstack1l1l1l11l11_opy_, platform_index)
        self.bstack1111l11l_opy_.bstack1ll1ll111_opy_()
    def bstack11l11111_opy_(self, driver, bstack1l111l11_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
        bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1l1ll1ll11_opy_.value)
        if test != None:
            bstack1l111l11l1_opy_ = getattr(test, bstack111l111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪዣ"), None)
            bstack11l11l1l1_opy_ = getattr(test, bstack111l111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫዤ"), None)
            PercySDK.screenshot(driver, bstack1l111l11_opy_, bstack1l111l11l1_opy_=bstack1l111l11l1_opy_, bstack11l11l1l1_opy_=bstack11l11l1l1_opy_, bstack111llllll1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l111l11_opy_)
        bstack1llll1111l1_opy_.end(EVENTS.bstack1l1ll1ll11_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢዥ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨዦ"), True, None, None, None, None, test_name=bstack1l111l11_opy_)
    def bstack1l1l1l11ll1_opy_(self):
        os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧዧ")] = str(self.bstack1l1l1l1l1l1_opy_.success)
        os.environ[bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧየ")] = str(self.bstack1l1l1l1l1l1_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l111ll_opy_(self.bstack1l1l1l1l1l1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l111l1_opy_(self.bstack1l1l1l1l1l1_opy_.percy_build_id)