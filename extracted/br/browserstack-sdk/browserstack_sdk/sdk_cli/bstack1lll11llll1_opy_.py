# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1llll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lllllll11l_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1111111ll1_opy_,
    bstack1111111l1l_opy_,
)
from bstack_utils.helper import  bstack11l1ll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1lll1l1l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1llll111_opy_, bstack1ll1llllll1_opy_, bstack1ll1lllll1l_opy_, bstack1lll11ll111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1ll1l1ll1_opy_ import bstack11ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1llll1l1ll1_opy_
from bstack_utils.percy import bstack11llll1111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11ll1ll_opy_(bstack1llll1111ll_opy_):
    def __init__(self, bstack1l1l1l11lll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l11lll_opy_ = bstack1l1l1l11lll_opy_
        self.percy = bstack11llll1111_opy_()
        self.bstack1lll11l1l1_opy_ = bstack11ll1lll_opy_()
        self.bstack1l1l1l1l11l_opy_()
        bstack1lll1l1l1ll_opy_.bstack1ll11llll11_opy_((bstack1lllll1lll1_opy_.bstack1llllllll11_opy_, bstack1111111ll1_opy_.PRE), self.bstack1l1l1ll1111_opy_)
        TestFramework.bstack1ll11llll11_opy_((bstack1ll1llll111_opy_.TEST, bstack1ll1lllll1l_opy_.POST), self.bstack1ll11l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll111111_opy_(self, instance: bstack1111111l1l_opy_, driver: object):
        bstack1l1lll1llll_opy_ = TestFramework.bstack1llllll1l1l_opy_(instance.context)
        for t in bstack1l1lll1llll_opy_:
            bstack1l1ll11111l_opy_ = TestFramework.bstack111111l111_opy_(t, bstack1llll1l1ll1_opy_.bstack1l1ll11ll11_opy_, [])
            if any(instance is d[1] for d in bstack1l1ll11111l_opy_) or instance == driver:
                return t
    def bstack1l1l1ll1111_opy_(
        self,
        f: bstack1lll1l1l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllll1111_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1111111ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1l1l1ll_opy_.bstack1ll111lll1l_opy_(method_name):
                return
            platform_index = f.bstack111111l111_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1ll11l1l111_opy_, 0)
            bstack1l1l1ll1l11_opy_ = self.bstack1l1ll111111_opy_(instance, driver)
            bstack1l1l1l1llll_opy_ = TestFramework.bstack111111l111_opy_(bstack1l1l1ll1l11_opy_, TestFramework.bstack1l1l1l1ll1l_opy_, None)
            if not bstack1l1l1l1llll_opy_:
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥኔ"))
                return
            driver_command = f.bstack1ll1l1l111l_opy_(*args)
            for command in bstack11111l1l_opy_:
                if command == driver_command:
                    self.bstack1lll1ll1_opy_(driver, platform_index)
            bstack11l1ll1l11_opy_ = self.percy.bstack11llll1l11_opy_()
            if driver_command in bstack1lll11l1l_opy_[bstack11l1ll1l11_opy_]:
                self.bstack1lll11l1l1_opy_.bstack1llllllll_opy_(bstack1l1l1l1llll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1ll1_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧን"), e)
    def bstack1ll11l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1llllll1_opy_,
        bstack1llllll1111_opy_: Tuple[bstack1ll1llll111_opy_, bstack1ll1lllll1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l11l1llll_opy_ import bstack1lll11l1l11_opy_
        bstack1l1ll11111l_opy_ = f.bstack111111l111_opy_(instance, bstack1llll1l1ll1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1ll11111l_opy_:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢኖ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠨࠢኗ"))
            return
        if len(bstack1l1ll11111l_opy_) > 1:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤኘ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠣࠤኙ"))
        bstack1l1l1l1l1ll_opy_, bstack1l1l1l1ll11_opy_ = bstack1l1ll11111l_opy_[0]
        driver = bstack1l1l1l1l1ll_opy_()
        if not driver:
            self.logger.debug(bstack1l1ll1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥኚ") + str(kwargs) + bstack1l1ll1_opy_ (u"ࠥࠦኛ"))
            return
        bstack1l1l1l1lll1_opy_ = {
            TestFramework.bstack1ll11llllll_opy_: bstack1l1ll1_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢኜ"),
            TestFramework.bstack1ll11l1l1ll_opy_: bstack1l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣኝ"),
            TestFramework.bstack1l1l1l1ll1l_opy_: bstack1l1ll1_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣኞ")
        }
        bstack1l1l1ll11ll_opy_ = { key: f.bstack111111l111_opy_(instance, key) for key in bstack1l1l1l1lll1_opy_ }
        bstack1l1l1ll111l_opy_ = [key for key, value in bstack1l1l1ll11ll_opy_.items() if not value]
        if bstack1l1l1ll111l_opy_:
            for key in bstack1l1l1ll111l_opy_:
                self.logger.debug(bstack1l1ll1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥኟ") + str(key) + bstack1l1ll1_opy_ (u"ࠣࠤአ"))
            return
        platform_index = f.bstack111111l111_opy_(instance, bstack1lll1l1l1ll_opy_.bstack1ll11l1l111_opy_, 0)
        if self.bstack1l1l1l11lll_opy_.percy_capture_mode == bstack1l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦኡ"):
            bstack1l1llllll_opy_ = bstack1l1l1ll11ll_opy_.get(TestFramework.bstack1l1l1l1ll1l_opy_) + bstack1l1ll1_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨኢ")
            bstack1ll111l1lll_opy_ = bstack1lll11l1l11_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1l1l1l1l1l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1llllll_opy_,
                bstack1l111l111_opy_=bstack1l1l1ll11ll_opy_[TestFramework.bstack1ll11llllll_opy_],
                bstack1lll11l1ll_opy_=bstack1l1l1ll11ll_opy_[TestFramework.bstack1ll11l1l1ll_opy_],
                bstack1l1l1l1l11_opy_=platform_index
            )
            bstack1lll11l1l11_opy_.end(EVENTS.bstack1l1l1l1l1l1_opy_.value, bstack1ll111l1lll_opy_+bstack1l1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦኣ"), bstack1ll111l1lll_opy_+bstack1l1ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥኤ"), True, None, None, None, None, test_name=bstack1l1llllll_opy_)
    def bstack1lll1ll1_opy_(self, driver, platform_index):
        if self.bstack1lll11l1l1_opy_.bstack1l1lllll1_opy_() is True or self.bstack1lll11l1l1_opy_.capturing() is True:
            return
        self.bstack1lll11l1l1_opy_.bstack1l1l11llll_opy_()
        while not self.bstack1lll11l1l1_opy_.bstack1l1lllll1_opy_():
            bstack1l1l1l1llll_opy_ = self.bstack1lll11l1l1_opy_.bstack1lll111l_opy_()
            self.bstack111l1ll1_opy_(driver, bstack1l1l1l1llll_opy_, platform_index)
        self.bstack1lll11l1l1_opy_.bstack1111l11l_opy_()
    def bstack111l1ll1_opy_(self, driver, bstack1111111l_opy_, platform_index, test=None):
        from bstack_utils.bstack1l11l1llll_opy_ import bstack1lll11l1l11_opy_
        bstack1ll111l1lll_opy_ = bstack1lll11l1l11_opy_.bstack1ll1l111111_opy_(EVENTS.bstack11l1l11l1_opy_.value)
        if test != None:
            bstack1l111l111_opy_ = getattr(test, bstack1l1ll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫእ"), None)
            bstack1lll11l1ll_opy_ = getattr(test, bstack1l1ll1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬኦ"), None)
            PercySDK.screenshot(driver, bstack1111111l_opy_, bstack1l111l111_opy_=bstack1l111l111_opy_, bstack1lll11l1ll_opy_=bstack1lll11l1ll_opy_, bstack1l1l1l1l11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1111111l_opy_)
        bstack1lll11l1l11_opy_.end(EVENTS.bstack11l1l11l1_opy_.value, bstack1ll111l1lll_opy_+bstack1l1ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኧ"), bstack1ll111l1lll_opy_+bstack1l1ll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢከ"), True, None, None, None, None, test_name=bstack1111111l_opy_)
    def bstack1l1l1l1l11l_opy_(self):
        os.environ[bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨኩ")] = str(self.bstack1l1l1l11lll_opy_.success)
        os.environ[bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨኪ")] = str(self.bstack1l1l1l11lll_opy_.percy_capture_mode)
        self.percy.bstack1l1l1ll11l1_opy_(self.bstack1l1l1l11lll_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l1l111_opy_(self.bstack1l1l1l11lll_opy_.percy_build_id)