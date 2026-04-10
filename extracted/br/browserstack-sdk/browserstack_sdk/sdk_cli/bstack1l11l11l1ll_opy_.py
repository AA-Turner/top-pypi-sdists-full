# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11lll1l1l_opy_ import bstack1l11ll1l111_opy_
from browserstack_sdk.sdk_cli.bstack11111ll111_opy_ import (
    bstack1111ll1l11_opy_,
    bstack1llll11lll_opy_,
    bstack1l1ll11ll11_opy_,
)
from bstack_utils.helper import  bstack1llll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11ll1llll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l11l11ll_opy_, TestHookState, bstack111l1111ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll111lll_opy_ import bstack1111lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l1llll_opy_ import bstack1l1l1llll1l_opy_
from bstack_utils.percy import bstack1ll1l11l11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l1l111l1_opy_(bstack1l11ll1l111_opy_):
    def __init__(self, bstack11ll1111l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11ll1111l1l_opy_ = bstack11ll1111l1l_opy_
        self.percy = bstack1ll1l11l11_opy_()
        self.bstack111ll11l11_opy_ = bstack1111lllll1_opy_()
        self.bstack11ll111111l_opy_()
        bstack1l11ll1llll_opy_.bstack1l1111111l1_opy_((bstack1111ll1l11_opy_.bstack1ll11111ll1_opy_, bstack1llll11lll_opy_.PRE), self.bstack11l1lllllll_opy_)
        TestFramework.bstack1l1111111l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l111ll_opy_(self, instance: bstack1l1ll11ll11_opy_, driver: object):
        bstack11lll1111l1_opy_ = TestFramework.bstack1l1ll111111_opy_(instance.context)
        for t in bstack11lll1111l1_opy_:
            bstack11lll11l1l1_opy_ = TestFramework.bstack1ll11111l11_opy_(t, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])
            if any(instance is d[1] for d in bstack11lll11l1l1_opy_) or instance == driver:
                return t
    def bstack11l1lllllll_opy_(
        self,
        f: bstack1l11ll1llll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11ll11_opy_, str],
        bstack1l1ll1lll11_opy_: Tuple[bstack1111ll1l11_opy_, bstack1llll11lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l11ll1llll_opy_.bstack1l111ll1l1l_opy_(method_name):
                return
            platform_index = f.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_, 0)
            bstack111111l1l1_opy_ = self.bstack11ll1l111ll_opy_(instance, driver)
            bstack11ll11111l1_opy_ = TestFramework.bstack1ll11111l11_opy_(bstack111111l1l1_opy_, TestFramework.bstack11ll111l1ll_opy_, None)
            if not bstack11ll11111l1_opy_:
                self.logger.debug(bstack1ll_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨᝋ"))
                return
            driver_command = f.bstack11lllllll11_opy_(*args)
            for command in bstack11l1lll1l_opy_:
                if command == driver_command:
                    self.bstack1111l1l111_opy_(driver, platform_index)
            bstack1lll1111l_opy_ = self.percy.bstack11111l1ll1_opy_()
            if driver_command in bstack1l111llll1_opy_[bstack1lll1111l_opy_]:
                self.bstack111ll11l11_opy_.bstack1lll1ll11_opy_(bstack11ll11111l1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣᝌ"), e)
    def bstack1l1111l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
        bstack11lll11l1l1_opy_ = f.bstack1ll11111l11_opy_(instance, bstack1l1l1llll1l_opy_.bstack11ll11l1111_opy_, [])
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack1ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝍ") + str(kwargs) + bstack1ll_opy_ (u"ࠤࠥᝎ"))
            return
        if len(bstack11lll11l1l1_opy_) > 1:
            self.logger.debug(bstack1ll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᝏ") + str(kwargs) + bstack1ll_opy_ (u"ࠦࠧᝐ"))
        bstack11ll1111l11_opy_, bstack11ll111l1l1_opy_ = bstack11lll11l1l1_opy_[0]
        driver = bstack11ll1111l11_opy_()
        if not driver:
            self.logger.debug(bstack1ll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᝑ") + str(kwargs) + bstack1ll_opy_ (u"ࠨࠢᝒ"))
            return
        bstack11ll1111ll1_opy_ = {
            TestFramework.bstack1l111111lll_opy_: bstack1ll_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᝓ"),
            TestFramework.bstack1l1111ll1l1_opy_: bstack1ll_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦ᝔"),
            TestFramework.bstack11ll111l1ll_opy_: bstack1ll_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦ᝕")
        }
        bstack11ll1111lll_opy_ = { key: f.bstack1ll11111l11_opy_(instance, key) for key in bstack11ll1111ll1_opy_ }
        bstack11ll111l111_opy_ = [key for key, value in bstack11ll1111lll_opy_.items() if not value]
        if bstack11ll111l111_opy_:
            for key in bstack11ll111l111_opy_:
                self.logger.debug(bstack1ll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨ᝖") + str(key) + bstack1ll_opy_ (u"ࠦࠧ᝗"))
            return
        platform_index = f.bstack1ll11111l11_opy_(instance, bstack1l11ll1llll_opy_.bstack1l1111l11l1_opy_, 0)
        if self.bstack11ll1111l1l_opy_.percy_capture_mode == bstack1ll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ᝘"):
            bstack1111l11l1l_opy_ = bstack11ll1111lll_opy_.get(TestFramework.bstack11ll111l1ll_opy_) + bstack1ll_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤ᝙")
            bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack11ll11111ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111l11l1l_opy_,
                bstack11ll1lllll_opy_=bstack11ll1111lll_opy_[TestFramework.bstack1l111111lll_opy_],
                bstack1l111l1ll1_opy_=bstack11ll1111lll_opy_[TestFramework.bstack1l1111ll1l1_opy_],
                bstack1ll1ll1l1l_opy_=platform_index
            )
            bstack1l11l1ll11_opy_.end(EVENTS.bstack11ll11111ll_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᝚"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᝛"), True, None, None, None, None, test_name=bstack1111l11l1l_opy_)
    def bstack1111l1l111_opy_(self, driver, platform_index):
        if self.bstack111ll11l11_opy_.bstack111111111l_opy_() is True or self.bstack111ll11l11_opy_.capturing() is True:
            return
        self.bstack111ll11l11_opy_.bstack11111l1lll_opy_()
        while not self.bstack111ll11l11_opy_.bstack111111111l_opy_():
            bstack11ll11111l1_opy_ = self.bstack111ll11l11_opy_.bstack111l111ll_opy_()
            self.bstack111l111l1_opy_(driver, bstack11ll11111l1_opy_, platform_index)
        self.bstack111ll11l11_opy_.bstack11l11ll1ll_opy_()
    def bstack111l111l1_opy_(self, driver, bstack1111111111_opy_, platform_index, test=None):
        from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
        bstack1lll1lll11_opy_ = bstack1l11l1ll11_opy_.bstack1111ll1111_opy_(EVENTS.bstack1l11lllll_opy_.value)
        if test != None:
            bstack11ll1lllll_opy_ = getattr(test, bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᝜"), None)
            bstack1l111l1ll1_opy_ = getattr(test, bstack1ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨ᝝"), None)
            PercySDK.screenshot(driver, bstack1111111111_opy_, bstack11ll1lllll_opy_=bstack11ll1lllll_opy_, bstack1l111l1ll1_opy_=bstack1l111l1ll1_opy_, bstack1ll1ll1l1l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1111111111_opy_)
        bstack1l11l1ll11_opy_.end(EVENTS.bstack1l11lllll_opy_.value, bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᝞"), bstack1lll1lll11_opy_+bstack1ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᝟"), True, None, None, None, None, test_name=bstack1111111111_opy_)
    def bstack11ll111111l_opy_(self):
        os.environ[bstack1ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫᝠ")] = str(self.bstack11ll1111l1l_opy_.success)
        os.environ[bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᝡ")] = str(self.bstack11ll1111l1l_opy_.percy_capture_mode)
        self.percy.bstack11ll111l11l_opy_(self.bstack11ll1111l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack11ll1111111_opy_(self.bstack11ll1111l1l_opy_.percy_build_id)