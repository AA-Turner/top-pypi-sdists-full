# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1ll111l_opy_ import bstack1l11lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1ll_opy_ import (
    bstack1l1111l1l1_opy_,
    bstack1ll111111l_opy_,
    bstack1l1ll1111l1_opy_,
)
from bstack_utils.helper import  bstack11l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l1l111l1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l11l1ll1ll_opy_, TestHookState, bstack111l1111l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11ll111ll_opy_ import bstack11ll1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1111ll_opy_ import bstack1l1l1lll1l1_opy_
from bstack_utils.percy import bstack11ll111l1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l11l1lll1l_opy_(bstack1l11lll1l1l_opy_):
    def __init__(self, bstack11ll111l1ll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11ll111l1ll_opy_ = bstack11ll111l1ll_opy_
        self.percy = bstack11ll111l1l_opy_()
        self.bstack1l1lll11l_opy_ = bstack11ll1l11ll_opy_()
        self.bstack11ll111l111_opy_()
        bstack1l1l111l1ll_opy_.bstack1l1111ll11l_opy_((bstack1l1111l1l1_opy_.bstack1l1llllll11_opy_, bstack1ll111111l_opy_.PRE), self.bstack11ll111lll1_opy_)
        TestFramework.bstack1l1111ll11l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11llllll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l1l111_opy_(self, instance: bstack1l1ll1111l1_opy_, driver: object):
        bstack11lll1l1111_opy_ = TestFramework.bstack1l1ll11l1ll_opy_(instance.context)
        for t in bstack11lll1l1111_opy_:
            bstack11lll11ll11_opy_ = TestFramework.bstack1l1lll1ll11_opy_(t, bstack1l1l1lll1l1_opy_.bstack11ll1l1l11l_opy_, [])
            if any(instance is d[1] for d in bstack11lll11ll11_opy_) or instance == driver:
                return t
    def bstack11ll111lll1_opy_(
        self,
        f: bstack1l1l111l1ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1111l1_opy_, str],
        bstack1l1ll1ll1ll_opy_: Tuple[bstack1l1111l1l1_opy_, bstack1ll111111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l1l111l1ll_opy_.bstack1l111l11l11_opy_(method_name):
                return
            platform_index = f.bstack1l1lll1ll11_opy_(instance, bstack1l1l111l1ll_opy_.bstack1l111ll1l1l_opy_, 0)
            bstack1l11lll11l_opy_ = self.bstack11ll1l1l111_opy_(instance, driver)
            bstack11ll1111lll_opy_ = TestFramework.bstack1l1lll1ll11_opy_(bstack1l11lll11l_opy_, TestFramework.bstack11ll111ll11_opy_, None)
            if not bstack11ll1111lll_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᝈ"))
                return
            driver_command = f.bstack1l111l1ll1l_opy_(*args)
            for command in bstack11l1111l_opy_:
                if command == driver_command:
                    self.bstack1lll1ll1l_opy_(driver, platform_index)
            bstack11ll1l11l1_opy_ = self.percy.bstack11l1l11l1l_opy_()
            if driver_command in bstack111111ll_opy_[bstack11ll1l11l1_opy_]:
                self.bstack1l1lll11l_opy_.bstack111lll111_opy_(bstack11ll1111lll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll1l11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᝉ"), e)
    def bstack11llllll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll1ll_opy_,
        bstack1l1ll1ll1ll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
        bstack11lll11ll11_opy_ = f.bstack1l1lll1ll11_opy_(instance, bstack1l1l1lll1l1_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack11lll11ll11_opy_:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᝊ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠨࠢᝋ"))
            return
        if len(bstack11lll11ll11_opy_) > 1:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝌ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠣࠤᝍ"))
        bstack11ll111llll_opy_, bstack11ll11l1111_opy_ = bstack11lll11ll11_opy_[0]
        driver = bstack11ll111llll_opy_()
        if not driver:
            self.logger.debug(bstack1ll1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝎ") + str(kwargs) + bstack1ll1l11_opy_ (u"ࠥࠦᝏ"))
            return
        bstack11ll1111ll1_opy_ = {
            TestFramework.bstack1l111ll11l1_opy_: bstack1ll1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᝐ"),
            TestFramework.bstack1l111l1lll1_opy_: bstack1ll1l11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᝑ"),
            TestFramework.bstack11ll111ll11_opy_: bstack1ll1l11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᝒ")
        }
        bstack11ll1111l1l_opy_ = { key: f.bstack1l1lll1ll11_opy_(instance, key) for key in bstack11ll1111ll1_opy_ }
        bstack11ll111l11l_opy_ = [key for key, value in bstack11ll1111l1l_opy_.items() if not value]
        if bstack11ll111l11l_opy_:
            for key in bstack11ll111l11l_opy_:
                self.logger.debug(bstack1ll1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᝓ") + str(key) + bstack1ll1l11_opy_ (u"ࠣࠤ᝔"))
            return
        platform_index = f.bstack1l1lll1ll11_opy_(instance, bstack1l1l111l1ll_opy_.bstack1l111ll1l1l_opy_, 0)
        if self.bstack11ll111l1ll_opy_.percy_capture_mode == bstack1ll1l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᝕"):
            bstack1l1l1ll11_opy_ = bstack11ll1111l1l_opy_.get(TestFramework.bstack11ll111ll11_opy_) + bstack1ll1l11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᝖")
            bstack1l111ll1ll_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack11ll1111l11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1l1ll11_opy_,
                bstack111lll1lll_opy_=bstack11ll1111l1l_opy_[TestFramework.bstack1l111ll11l1_opy_],
                bstack111lll1ll_opy_=bstack11ll1111l1l_opy_[TestFramework.bstack1l111l1lll1_opy_],
                bstack11lllll1l1_opy_=platform_index
            )
            bstack11l1111l1l_opy_.end(EVENTS.bstack11ll1111l11_opy_.value, bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᝗"), bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᝘"), True, None, None, None, None, test_name=bstack1l1l1ll11_opy_)
    def bstack1lll1ll1l_opy_(self, driver, platform_index):
        if self.bstack1l1lll11l_opy_.bstack111llll11_opy_() is True or self.bstack1l1lll11l_opy_.capturing() is True:
            return
        self.bstack1l1lll11l_opy_.bstack1lllll1lll_opy_()
        while not self.bstack1l1lll11l_opy_.bstack111llll11_opy_():
            bstack11ll1111lll_opy_ = self.bstack1l1lll11l_opy_.bstack111111l1l1_opy_()
            self.bstack1lllll11l_opy_(driver, bstack11ll1111lll_opy_, platform_index)
        self.bstack1l1lll11l_opy_.bstack11111111_opy_()
    def bstack1lllll11l_opy_(self, driver, bstack11llllll1_opy_, platform_index, test=None):
        from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
        bstack1l111ll1ll_opy_ = bstack11l1111l1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack1l11lll1_opy_.value)
        if test != None:
            bstack111lll1lll_opy_ = getattr(test, bstack1ll1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᝙"), None)
            bstack111lll1ll_opy_ = getattr(test, bstack1ll1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᝚"), None)
            PercySDK.screenshot(driver, bstack11llllll1_opy_, bstack111lll1lll_opy_=bstack111lll1lll_opy_, bstack111lll1ll_opy_=bstack111lll1ll_opy_, bstack11lllll1l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11llllll1_opy_)
        bstack11l1111l1l_opy_.end(EVENTS.bstack1l11lll1_opy_.value, bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᝛"), bstack1l111ll1ll_opy_+bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᝜"), True, None, None, None, None, test_name=bstack11llllll1_opy_)
    def bstack11ll111l111_opy_(self):
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᝝")] = str(self.bstack11ll111l1ll_opy_.success)
        os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ᝞")] = str(self.bstack11ll111l1ll_opy_.percy_capture_mode)
        self.percy.bstack11ll111l1l1_opy_(self.bstack11ll111l1ll_opy_.is_percy_auto_enabled)
        self.percy.bstack11ll111ll1l_opy_(self.bstack11ll111l1ll_opy_.percy_build_id)