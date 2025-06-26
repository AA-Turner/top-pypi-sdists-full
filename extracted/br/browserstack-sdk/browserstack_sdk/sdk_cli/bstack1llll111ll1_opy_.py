# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1111111l1l_opy_,
)
from bstack_utils.helper import  bstack11111ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1ll111l_opy_, bstack1ll1l1lll1l_opy_, bstack1lll1111l1l_opy_, bstack1lll111ll1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1l11l1_opy_ import bstack1l1llllll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll111l1l1_opy_
from bstack_utils.percy import bstack11ll1l11ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l1l1l1_opy_(bstack1lll1ll1l1l_opy_):
    def __init__(self, bstack1l1l1l11lll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l11lll_opy_ = bstack1l1l1l11lll_opy_
        self.percy = bstack11ll1l11ll_opy_()
        self.bstack11l1ll1111_opy_ = bstack1l1llllll1_opy_()
        self.bstack1l1l1l1l1l1_opy_()
        bstack1ll1lllllll_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1l1l1l1llll_opy_)
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll111l1l_opy_(self, instance: bstack1111111l1l_opy_, driver: object):
        bstack1l1ll1111ll_opy_ = TestFramework.bstack1lllll1llll_opy_(instance.context)
        for t in bstack1l1ll1111ll_opy_:
            bstack1l1lll1ll11_opy_ = TestFramework.bstack11111111ll_opy_(t, bstack1lll111l1l1_opy_.bstack1l1l1ll1lll_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll1ll11_opy_) or instance == driver:
                return t
    def bstack1l1l1l1llll_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1lllllll_opy_.bstack1ll11l1lll1_opy_(method_name):
                return
            platform_index = f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_, 0)
            bstack1l1lll1l1l1_opy_ = self.bstack1l1ll111l1l_opy_(instance, driver)
            bstack1l1l1l11ll1_opy_ = TestFramework.bstack11111111ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1l1l1l111_opy_, None)
            if not bstack1l1l1l11ll1_opy_:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥኔ"))
                return
            driver_command = f.bstack1ll1l111ll1_opy_(*args)
            for command in bstack1lll1l1lll_opy_:
                if command == driver_command:
                    self.bstack11ll11l1ll_opy_(driver, platform_index)
            bstack1l1111llll_opy_ = self.percy.bstack1ll1ll11ll_opy_()
            if driver_command in bstack1l11lll1_opy_[bstack1l1111llll_opy_]:
                self.bstack11l1ll1111_opy_.bstack11lll11l_opy_(bstack1l1l1l11ll1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧን"), e)
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
        bstack1l1lll1ll11_opy_ = f.bstack11111111ll_opy_(instance, bstack1lll111l1l1_opy_.bstack1l1l1ll1lll_opy_, [])
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኖ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠨࠢኗ"))
            return
        if len(bstack1l1lll1ll11_opy_) > 1:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኘ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠣࠤኙ"))
        bstack1l1l1l1ll11_opy_, bstack1l1l1l1ll1l_opy_ = bstack1l1lll1ll11_opy_[0]
        driver = bstack1l1l1l1ll11_opy_()
        if not driver:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኚ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠥࠦኛ"))
            return
        bstack1l1l1l1l1ll_opy_ = {
            TestFramework.bstack1ll11ll11l1_opy_: bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢኜ"),
            TestFramework.bstack1ll11l11l11_opy_: bstack11ll1l1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣኝ"),
            TestFramework.bstack1l1l1l1l111_opy_: bstack11ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣኞ")
        }
        bstack1l1l1ll1111_opy_ = { key: f.bstack11111111ll_opy_(instance, key) for key in bstack1l1l1l1l1ll_opy_ }
        bstack1l1l1ll111l_opy_ = [key for key, value in bstack1l1l1ll1111_opy_.items() if not value]
        if bstack1l1l1ll111l_opy_:
            for key in bstack1l1l1ll111l_opy_:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥኟ") + str(key) + bstack11ll1l1_opy_ (u"ࠣࠤአ"))
            return
        platform_index = f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_, 0)
        if self.bstack1l1l1l11lll_opy_.percy_capture_mode == bstack11ll1l1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦኡ"):
            bstack1111111l1_opy_ = bstack1l1l1ll1111_opy_.get(TestFramework.bstack1l1l1l1l111_opy_) + bstack11ll1l1_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨኢ")
            bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack1l1l1ll11l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111111l1_opy_,
                bstack1ll1l1ll11_opy_=bstack1l1l1ll1111_opy_[TestFramework.bstack1ll11ll11l1_opy_],
                bstack11llll11l_opy_=bstack1l1l1ll1111_opy_[TestFramework.bstack1ll11l11l11_opy_],
                bstack111l11l1l_opy_=platform_index
            )
            bstack1llll11lll1_opy_.end(EVENTS.bstack1l1l1ll11l1_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦኣ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥኤ"), True, None, None, None, None, test_name=bstack1111111l1_opy_)
    def bstack11ll11l1ll_opy_(self, driver, platform_index):
        if self.bstack11l1ll1111_opy_.bstack11l1l11l11_opy_() is True or self.bstack11l1ll1111_opy_.capturing() is True:
            return
        self.bstack11l1ll1111_opy_.bstack11l1l11111_opy_()
        while not self.bstack11l1ll1111_opy_.bstack11l1l11l11_opy_():
            bstack1l1l1l11ll1_opy_ = self.bstack11l1ll1111_opy_.bstack1lll1lllll_opy_()
            self.bstack1l111ll1l1_opy_(driver, bstack1l1l1l11ll1_opy_, platform_index)
        self.bstack11l1ll1111_opy_.bstack11lll1lll1_opy_()
    def bstack1l111ll1l1_opy_(self, driver, bstack1lll1llll_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
        bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack11lll1ll11_opy_.value)
        if test != None:
            bstack1ll1l1ll11_opy_ = getattr(test, bstack11ll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫእ"), None)
            bstack11llll11l_opy_ = getattr(test, bstack11ll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬኦ"), None)
            PercySDK.screenshot(driver, bstack1lll1llll_opy_, bstack1ll1l1ll11_opy_=bstack1ll1l1ll11_opy_, bstack11llll11l_opy_=bstack11llll11l_opy_, bstack111l11l1l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll1llll_opy_)
        bstack1llll11lll1_opy_.end(EVENTS.bstack11lll1ll11_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኧ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢከ"), True, None, None, None, None, test_name=bstack1lll1llll_opy_)
    def bstack1l1l1l1l1l1_opy_(self):
        os.environ[bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨኩ")] = str(self.bstack1l1l1l11lll_opy_.success)
        os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨኪ")] = str(self.bstack1l1l1l11lll_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l1lll1_opy_(self.bstack1l1l1l11lll_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l1l11l_opy_(self.bstack1l1l1l11lll_opy_.percy_build_id)