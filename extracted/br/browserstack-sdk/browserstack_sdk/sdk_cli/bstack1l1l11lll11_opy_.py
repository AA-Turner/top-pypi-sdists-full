# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1l1lll111ll_opy_,
)
from bstack_utils.helper import  bstack11ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l111ll1l_opy_, TestHookState, bstack1111lll111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1ll1l1l1_opy_ import bstack111llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1l1l111ll11_opy_
from bstack_utils.percy import bstack111111l111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l1lll111_opy_(bstack1l11ll11111_opy_):
    def __init__(self, bstack11ll111lll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11ll111lll1_opy_ = bstack11ll111lll1_opy_
        self.percy = bstack111111l111_opy_()
        self.bstack111l11ll1l_opy_ = bstack111llll1l_opy_()
        self.bstack11ll111l111_opy_()
        bstack1l1l1ll11ll_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11ll111l1l1_opy_)
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll11l1l11_opy_(self, instance: bstack1l1lll111ll_opy_, driver: object):
        bstack11ll1l1l111_opy_ = TestFramework.bstack1l1ll11ll1l_opy_(instance.context)
        for t in bstack11ll1l1l111_opy_:
            bstack11lll1l1l11_opy_ = TestFramework.bstack1ll111l1111_opy_(t, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])
            if any(instance is d[1] for d in bstack11lll1l1l11_opy_) or instance == driver:
                return t
    def bstack11ll111l1l1_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l1l1ll11ll_opy_.bstack1l111l1l1l1_opy_(method_name):
                return
            platform_index = f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_, 0)
            bstack1l1llll1_opy_ = self.bstack11ll11l1l11_opy_(instance, driver)
            bstack11ll1111l1l_opy_ = TestFramework.bstack1ll111l1111_opy_(bstack1l1llll1_opy_, TestFramework.bstack11ll111ll11_opy_, None)
            if not bstack11ll1111l1l_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᝈ"))
                return
            driver_command = f.bstack1l111ll11ll_opy_(*args)
            for command in bstack1lllll11ll_opy_:
                if command == driver_command:
                    self.bstack1ll1lllll1_opy_(driver, platform_index)
            bstack11l11111l1_opy_ = self.percy.bstack11l11l1l1_opy_()
            if driver_command in bstack11l1l1111l_opy_[bstack11l11111l1_opy_]:
                self.bstack111l11ll1l_opy_.bstack11ll1lllll_opy_(bstack11ll1111l1l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᝉ"), e)
    def bstack1l1111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
        bstack11lll1l1l11_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1l111ll11_opy_.bstack11ll1l1l11l_opy_, [])
        if not bstack11lll1l1l11_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᝊ") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢᝋ"))
            return
        if len(bstack11lll1l1l11_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝌ") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤᝍ"))
        bstack11ll111l1ll_opy_, bstack11ll1111ll1_opy_ = bstack11lll1l1l11_opy_[0]
        driver = bstack11ll111l1ll_opy_()
        if not driver:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝎ") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦᝏ"))
            return
        bstack11ll111ll1l_opy_ = {
            TestFramework.bstack1l11111l111_opy_: bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᝐ"),
            TestFramework.bstack1l111l11l1l_opy_: bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᝑ"),
            TestFramework.bstack11ll111ll11_opy_: bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᝒ")
        }
        bstack11ll1111lll_opy_ = { key: f.bstack1ll111l1111_opy_(instance, key) for key in bstack11ll111ll1l_opy_ }
        bstack11ll11l1111_opy_ = [key for key, value in bstack11ll1111lll_opy_.items() if not value]
        if bstack11ll11l1111_opy_:
            for key in bstack11ll11l1111_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᝓ") + str(key) + bstack11ll11_opy_ (u"ࠣࠤ᝔"))
            return
        platform_index = f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_, 0)
        if self.bstack11ll111lll1_opy_.percy_capture_mode == bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᝕"):
            bstack1llll111l1_opy_ = bstack11ll1111lll_opy_.get(TestFramework.bstack11ll111ll11_opy_) + bstack11ll11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨ᝖")
            bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack11ll111l11l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1llll111l1_opy_,
                bstack111llll111_opy_=bstack11ll1111lll_opy_[TestFramework.bstack1l11111l111_opy_],
                bstack1llll11ll1_opy_=bstack11ll1111lll_opy_[TestFramework.bstack1l111l11l1l_opy_],
                bstack11ll1l1lll_opy_=platform_index
            )
            bstack1ll111lll_opy_.end(EVENTS.bstack11ll111l11l_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᝗"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᝘"), True, None, None, None, None, test_name=bstack1llll111l1_opy_)
    def bstack1ll1lllll1_opy_(self, driver, platform_index):
        if self.bstack111l11ll1l_opy_.bstack1l1l111lll_opy_() is True or self.bstack111l11ll1l_opy_.capturing() is True:
            return
        self.bstack111l11ll1l_opy_.bstack1l111111l1_opy_()
        while not self.bstack111l11ll1l_opy_.bstack1l1l111lll_opy_():
            bstack11ll1111l1l_opy_ = self.bstack111l11ll1l_opy_.bstack1l11llll1_opy_()
            self.bstack11111lll_opy_(driver, bstack11ll1111l1l_opy_, platform_index)
        self.bstack111l11ll1l_opy_.bstack11ll1ll111_opy_()
    def bstack11111lll_opy_(self, driver, bstack11l11l11l_opy_, platform_index, test=None):
        from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
        bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack11l1l111ll_opy_.value)
        if test != None:
            bstack111llll111_opy_ = getattr(test, bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᝙"), None)
            bstack1llll11ll1_opy_ = getattr(test, bstack11ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᝚"), None)
            PercySDK.screenshot(driver, bstack11l11l11l_opy_, bstack111llll111_opy_=bstack111llll111_opy_, bstack1llll11ll1_opy_=bstack1llll11ll1_opy_, bstack11ll1l1lll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l11l11l_opy_)
        bstack1ll111lll_opy_.end(EVENTS.bstack11l1l111ll_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᝛"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᝜"), True, None, None, None, None, test_name=bstack11l11l11l_opy_)
    def bstack11ll111l111_opy_(self):
        os.environ[bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᝝")] = str(self.bstack11ll111lll1_opy_.success)
        os.environ[bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ᝞")] = str(self.bstack11ll111lll1_opy_.percy_capture_mode)
        self.percy.bstack11ll1111l11_opy_(self.bstack11ll111lll1_opy_.is_percy_auto_enabled)
        self.percy.bstack11ll111llll_opy_(self.bstack11ll111lll1_opy_.percy_build_id)