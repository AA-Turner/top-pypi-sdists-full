# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1111111111_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import (
    bstack1lll1llllll_opy_,
    bstack1llllll1l1l_opy_,
    bstack1lll1llll11_opy_,
)
from bstack_utils.helper import  bstack11ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lllll11l11_opy_, bstack1lllll111ll_opy_, bstack1lll1lll1ll_opy_, bstack1llll11ll1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll1111l_opy_ import bstack11l1lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll1lll_opy_ import bstack111111l1ll_opy_
from bstack_utils.percy import bstack11ll11l111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11lll11_opy_(bstack1lll1lllll1_opy_):
    def __init__(self, bstack1lll11l1ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1lll11l1ll1_opy_ = bstack1lll11l1ll1_opy_
        self.percy = bstack11ll11l111_opy_()
        self.bstack11ll1111l1_opy_ = bstack11l1lll1l1_opy_()
        self.bstack1lll11lll1l_opy_()
        bstack1lll1ll1l1l_opy_.bstack1lllll1llll_opy_((bstack1lll1llllll_opy_.bstack1llll1lll11_opy_, bstack1llllll1l1l_opy_.PRE), self.bstack1lll11l11l1_opy_)
        TestFramework.bstack1lllll1llll_opy_((bstack1lllll11l11_opy_.TEST, bstack1lll1lll1ll_opy_.POST), self.bstack1lllll11l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1111111l11_opy_(self, instance: bstack1lll1llll11_opy_, driver: object):
        bstack1llllllllll_opy_ = TestFramework.bstack1lllll1111l_opy_(instance.context)
        for t in bstack1llllllllll_opy_:
            bstack1llll11l1l1_opy_ = TestFramework.bstack1lllll1l11l_opy_(t, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
            if any(instance is d[1] for d in bstack1llll11l1l1_opy_) or instance == driver:
                return t
    def bstack1lll11l11l1_opy_(
        self,
        f: bstack1lll1ll1l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1llll11_opy_, str],
        bstack1llll11l111_opy_: Tuple[bstack1lll1llllll_opy_, bstack1llllll1l1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1ll1l1l_opy_.bstack1lllll11ll1_opy_(method_name):
                return
            platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_, 0)
            bstack1llllll111l_opy_ = self.bstack1111111l11_opy_(instance, driver)
            bstack1lll11ll1ll_opy_ = TestFramework.bstack1lllll1l11l_opy_(bstack1llllll111l_opy_, TestFramework.bstack1lll11l1l1l_opy_, None)
            if not bstack1lll11ll1ll_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨᄈ"))
                return
            driver_command = f.bstack1lllll1ll11_opy_(*args)
            for command in bstack1l11lll1ll_opy_:
                if command == driver_command:
                    self.bstack1ll111l1l1_opy_(driver, platform_index)
            bstack1l111ll1_opy_ = self.percy.bstack11ll111ll_opy_()
            if driver_command in bstack11l1l111ll_opy_[bstack1l111ll1_opy_]:
                self.bstack11ll1111l1_opy_.bstack1l1ll1l111_opy_(bstack1lll11ll1ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11l1111_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣᄉ"), e)
    def bstack1lllll11l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lllll111ll_opy_,
        bstack1llll11l111_opy_: Tuple[bstack1lllll11l11_opy_, bstack1lll1lll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
        bstack1llll11l1l1_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack111111l1ll_opy_.bstack1lll1l1ll11_opy_, [])
        if not bstack1llll11l1l1_opy_:
            self.logger.debug(bstack11l1111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᄊ") + str(kwargs) + bstack11l1111_opy_ (u"ࠤࠥᄋ"))
            return
        if len(bstack1llll11l1l1_opy_) > 1:
            self.logger.debug(bstack11l1111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᄌ") + str(kwargs) + bstack11l1111_opy_ (u"ࠦࠧᄍ"))
        bstack1lll11l111l_opy_, bstack1lll11ll11l_opy_ = bstack1llll11l1l1_opy_[0]
        driver = bstack1lll11l111l_opy_()
        if not driver:
            self.logger.debug(bstack11l1111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᄎ") + str(kwargs) + bstack11l1111_opy_ (u"ࠨࠢᄏ"))
            return
        bstack1lll1l11111_opy_ = {
            TestFramework.bstack1lll11lllll_opy_: bstack11l1111_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᄐ"),
            TestFramework.bstack1lll1l1ll1l_opy_: bstack11l1111_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦᄑ"),
            TestFramework.bstack1lll11l1l1l_opy_: bstack11l1111_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦᄒ")
        }
        bstack1lll11ll1l1_opy_ = { key: f.bstack1lllll1l11l_opy_(instance, key) for key in bstack1lll1l11111_opy_ }
        bstack1lll11l1lll_opy_ = [key for key, value in bstack1lll11ll1l1_opy_.items() if not value]
        if bstack1lll11l1lll_opy_:
            for key in bstack1lll11l1lll_opy_:
                self.logger.debug(bstack11l1111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨᄓ") + str(key) + bstack11l1111_opy_ (u"ࠦࠧᄔ"))
            return
        platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1ll1l1l_opy_.bstack1llllll1lll_opy_, 0)
        if self.bstack1lll11l1ll1_opy_.percy_capture_mode == bstack11l1111_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᄕ"):
            bstack111l11l1l_opy_ = bstack1lll11ll1l1_opy_.get(TestFramework.bstack1lll11l1l1l_opy_) + bstack11l1111_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᄖ")
            bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack1lll11ll111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack111l11l1l_opy_,
                bstack1lllll1l11_opy_=bstack1lll11ll1l1_opy_[TestFramework.bstack1lll11lllll_opy_],
                bstack111llllll1_opy_=bstack1lll11ll1l1_opy_[TestFramework.bstack1lll1l1ll1l_opy_],
                bstack1l1lll1l1_opy_=platform_index
            )
            bstack1lll1l1l11l_opy_.end(EVENTS.bstack1lll11ll111_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᄗ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᄘ"), True, None, None, None, None, test_name=bstack111l11l1l_opy_)
    def bstack1ll111l1l1_opy_(self, driver, platform_index):
        if self.bstack11ll1111l1_opy_.bstack11111l1ll_opy_() is True or self.bstack11ll1111l1_opy_.capturing() is True:
            return
        self.bstack11ll1111l1_opy_.bstack1lll1ll11_opy_()
        while not self.bstack11ll1111l1_opy_.bstack11111l1ll_opy_():
            bstack1lll11ll1ll_opy_ = self.bstack11ll1111l1_opy_.bstack1llll111l_opy_()
            self.bstack11l11ll1_opy_(driver, bstack1lll11ll1ll_opy_, platform_index)
        self.bstack11ll1111l1_opy_.bstack1l1l11111_opy_()
    def bstack11l11ll1_opy_(self, driver, bstack1llll111ll_opy_, platform_index, test=None):
        from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
        bstack1lll1lll11l_opy_ = bstack1lll1l1l11l_opy_.bstack1llll1lllll_opy_(EVENTS.bstack1l1l11lll_opy_.value)
        if test != None:
            bstack1lllll1l11_opy_ = getattr(test, bstack11l1111_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᄙ"), None)
            bstack111llllll1_opy_ = getattr(test, bstack11l1111_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᄚ"), None)
            PercySDK.screenshot(driver, bstack1llll111ll_opy_, bstack1lllll1l11_opy_=bstack1lllll1l11_opy_, bstack111llllll1_opy_=bstack111llllll1_opy_, bstack1l1lll1l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1llll111ll_opy_)
        bstack1lll1l1l11l_opy_.end(EVENTS.bstack1l1l11lll_opy_.value, bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᄛ"), bstack1lll1lll11l_opy_+bstack11l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᄜ"), True, None, None, None, None, test_name=bstack1llll111ll_opy_)
    def bstack1lll11lll1l_opy_(self):
        os.environ[bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫᄝ")] = str(self.bstack1lll11l1ll1_opy_.success)
        os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᄞ")] = str(self.bstack1lll11l1ll1_opy_.percy_capture_mode)
        self.percy.bstack1lll11l1l11_opy_(self.bstack1lll11l1ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1lll11llll1_opy_(self.bstack1lll11l1ll1_opy_.percy_build_id)