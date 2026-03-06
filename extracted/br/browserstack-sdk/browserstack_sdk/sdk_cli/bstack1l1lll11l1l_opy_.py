# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1ll1ll1l111_opy_,
)
from bstack_utils.helper import  bstack1lll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll11ll111l_opy_, TestHookState, bstack1ll11lllll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11lll1llll_opy_ import bstack111l111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll11_opy_ import bstack1ll1l111l1l_opy_
from bstack_utils.percy import bstack1l111llll1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll11l1l1ll_opy_(bstack1ll111l1l1l_opy_):
    def __init__(self, bstack1l1111l1l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1111l1l1l_opy_ = bstack1l1111l1l1l_opy_
        self.percy = bstack1l111llll1_opy_()
        self.bstack1l1l1ll1ll_opy_ = bstack111l111ll1_opy_()
        self.bstack1l1111l11ll_opy_()
        bstack1ll11l11111_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l1111l1l11_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111l1l1ll_opy_(self, instance: bstack1ll1ll1l111_opy_, driver: object):
        bstack1l1111llll1_opy_ = TestFramework.bstack1ll1l1ll11l_opy_(instance.context)
        for t in bstack1l1111llll1_opy_:
            bstack1l111l1l111_opy_ = TestFramework.bstack1lll1l11111_opy_(t, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
            if any(instance is d[1] for d in bstack1l111l1l111_opy_) or instance == driver:
                return t
    def bstack1l1111l1l11_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll11l11111_opy_.bstack1l1l111l1ll_opy_(method_name):
                return
            platform_index = f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_, 0)
            bstack1l111ll11l1_opy_ = self.bstack1l111l1l1ll_opy_(instance, driver)
            bstack1l1111ll111_opy_ = TestFramework.bstack1lll1l11111_opy_(bstack1l111ll11l1_opy_, TestFramework.bstack1l1111lll11_opy_, None)
            if not bstack1l1111ll111_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᔘ"))
                return
            driver_command = f.bstack1l1l1l11lll_opy_(*args)
            for command in bstack111111l1l_opy_:
                if command == driver_command:
                    self.bstack1l1l1l1l_opy_(driver, platform_index)
            bstack111lll11l1_opy_ = self.percy.bstack11l1l1lll1_opy_()
            if driver_command in bstack11ll11lll1_opy_[bstack111lll11l1_opy_]:
                self.bstack1l1l1ll1ll_opy_.bstack111l11ll_opy_(bstack1l1111ll111_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᔙ"), e)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
        bstack1l111l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l11l1111l1_opy_, [])
        if not bstack1l111l1l111_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᔚ") + str(kwargs) + bstack1111_opy_ (u"ࠨࠢᔛ"))
            return
        if len(bstack1l111l1l111_opy_) > 1:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔜ") + str(kwargs) + bstack1111_opy_ (u"ࠣࠤᔝ"))
        bstack1l1111ll11l_opy_, bstack1l1111l1lll_opy_ = bstack1l111l1l111_opy_[0]
        driver = bstack1l1111ll11l_opy_()
        if not driver:
            self.logger.debug(bstack1111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᔞ") + str(kwargs) + bstack1111_opy_ (u"ࠥࠦᔟ"))
            return
        bstack1l1111ll1l1_opy_ = {
            TestFramework.bstack1l1l11lll11_opy_: bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᔠ"),
            TestFramework.bstack1l1l11l1l1l_opy_: bstack1111_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᔡ"),
            TestFramework.bstack1l1111lll11_opy_: bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᔢ")
        }
        bstack1l1111l1ll1_opy_ = { key: f.bstack1lll1l11111_opy_(instance, key) for key in bstack1l1111ll1l1_opy_ }
        bstack1l1111l111l_opy_ = [key for key, value in bstack1l1111l1ll1_opy_.items() if not value]
        if bstack1l1111l111l_opy_:
            for key in bstack1l1111l111l_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᔣ") + str(key) + bstack1111_opy_ (u"ࠣࠤᔤ"))
            return
        platform_index = f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_, 0)
        if self.bstack1l1111l1l1l_opy_.percy_capture_mode == bstack1111_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᔥ"):
            bstack1llll1l1_opy_ = bstack1l1111l1ll1_opy_.get(TestFramework.bstack1l1111lll11_opy_) + bstack1111_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᔦ")
            bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1l1111ll1ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1llll1l1_opy_,
                bstack1l1l11lll_opy_=bstack1l1111l1ll1_opy_[TestFramework.bstack1l1l11lll11_opy_],
                bstack1lll111l1_opy_=bstack1l1111l1ll1_opy_[TestFramework.bstack1l1l11l1l1l_opy_],
                bstack11l1ll1ll_opy_=platform_index
            )
            bstack1l11l1ll_opy_.end(EVENTS.bstack1l1111ll1ll_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᔧ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᔨ"), True, None, None, None, None, test_name=bstack1llll1l1_opy_)
    def bstack1l1l1l1l_opy_(self, driver, platform_index):
        if self.bstack1l1l1ll1ll_opy_.bstack1lll1l11l1_opy_() is True or self.bstack1l1l1ll1ll_opy_.capturing() is True:
            return
        self.bstack1l1l1ll1ll_opy_.bstack1ll1l111l_opy_()
        while not self.bstack1l1l1ll1ll_opy_.bstack1lll1l11l1_opy_():
            bstack1l1111ll111_opy_ = self.bstack1l1l1ll1ll_opy_.bstack111llll11_opy_()
            self.bstack11lllllll1_opy_(driver, bstack1l1111ll111_opy_, platform_index)
        self.bstack1l1l1ll1ll_opy_.bstack1lll1ll1l_opy_()
    def bstack11lllllll1_opy_(self, driver, bstack11ll1111l1_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
        bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1lll1llll_opy_.value)
        if test != None:
            bstack1l1l11lll_opy_ = getattr(test, bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᔩ"), None)
            bstack1lll111l1_opy_ = getattr(test, bstack1111_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᔪ"), None)
            PercySDK.screenshot(driver, bstack11ll1111l1_opy_, bstack1l1l11lll_opy_=bstack1l1l11lll_opy_, bstack1lll111l1_opy_=bstack1lll111l1_opy_, bstack11l1ll1ll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11ll1111l1_opy_)
        bstack1l11l1ll_opy_.end(EVENTS.bstack1lll1llll_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᔫ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᔬ"), True, None, None, None, None, test_name=bstack11ll1111l1_opy_)
    def bstack1l1111l11ll_opy_(self):
        os.environ[bstack1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᔭ")] = str(self.bstack1l1111l1l1l_opy_.success)
        os.environ[bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᔮ")] = str(self.bstack1l1111l1l1l_opy_.percy_capture_mode)
        self.percy.bstack1l1111lll1l_opy_(self.bstack1l1111l1l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1111l11l1_opy_(self.bstack1l1111l1l1l_opy_.percy_build_id)