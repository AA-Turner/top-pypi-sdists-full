# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1ll11llllll_opy_,
)
from bstack_utils.helper import  bstack111ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111l1111_opy_, TestHookState, bstack1l1ll1111ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l11ll1l1_opy_ import bstack11111ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1lll111_opy_ import bstack1l1ll111111_opy_
from bstack_utils.percy import bstack1l1ll11l11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll111lll1l_opy_(bstack1l1lllllll1_opy_):
    def __init__(self, bstack11llll1lll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11llll1lll1_opy_ = bstack11llll1lll1_opy_
        self.percy = bstack1l1ll11l11_opy_()
        self.bstack1ll1l1llll_opy_ = bstack11111ll111_opy_()
        self.bstack11llll1l1l1_opy_()
        bstack1ll111l11ll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.PRE), self.bstack11llll1ll1l_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llllll111_opy_(self, instance: bstack1ll11llllll_opy_, driver: object):
        bstack1l111111111_opy_ = TestFramework.bstack1ll11lllll1_opy_(instance.context)
        for t in bstack1l111111111_opy_:
            bstack1l111llll1l_opy_ = TestFramework.bstack1ll1l1l1111_opy_(t, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
            if any(instance is d[1] for d in bstack1l111llll1l_opy_) or instance == driver:
                return t
    def bstack11llll1ll1l_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll111l11ll_opy_.bstack1l11ll1ll11_opy_(method_name):
                return
            platform_index = f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_, 0)
            bstack1l1111lllll_opy_ = self.bstack11llllll111_opy_(instance, driver)
            bstack11lllll11ll_opy_ = TestFramework.bstack1ll1l1l1111_opy_(bstack1l1111lllll_opy_, TestFramework.bstack11lllll1111_opy_, None)
            if not bstack11lllll11ll_opy_:
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤᗰ"))
                return
            driver_command = f.bstack1l11l1lll11_opy_(*args)
            for command in bstack111ll11ll1_opy_:
                if command == driver_command:
                    self.bstack11l1l11ll_opy_(driver, platform_index)
            bstack11llll11_opy_ = self.percy.bstack1llllll11l_opy_()
            if driver_command in bstack111l111l11_opy_[bstack11llll11_opy_]:
                self.bstack1ll1l1llll_opy_.bstack11111llll_opy_(bstack11lllll11ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦᗱ"), e)
    def bstack1l1l11l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
        bstack1l111llll1l_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1l1ll111111_opy_.bstack11llllll11l_opy_, [])
        if not bstack1l111llll1l_opy_:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᗲ") + str(kwargs) + bstack11lll1_opy_ (u"ࠧࠨᗳ"))
            return
        if len(bstack1l111llll1l_opy_) > 1:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᗴ") + str(kwargs) + bstack11lll1_opy_ (u"ࠢࠣᗵ"))
        bstack11llll1llll_opy_, bstack11lllll111l_opy_ = bstack1l111llll1l_opy_[0]
        driver = bstack11llll1llll_opy_()
        if not driver:
            self.logger.debug(bstack11lll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᗶ") + str(kwargs) + bstack11lll1_opy_ (u"ࠤࠥᗷ"))
            return
        bstack11llll1ll11_opy_ = {
            TestFramework.bstack1l11ll1llll_opy_: bstack11lll1_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᗸ"),
            TestFramework.bstack1l11llll11l_opy_: bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢᗹ"),
            TestFramework.bstack11lllll1111_opy_: bstack11lll1_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢᗺ")
        }
        bstack11llll1l11l_opy_ = { key: f.bstack1ll1l1l1111_opy_(instance, key) for key in bstack11llll1ll11_opy_ }
        bstack11llll11lll_opy_ = [key for key, value in bstack11llll1l11l_opy_.items() if not value]
        if bstack11llll11lll_opy_:
            for key in bstack11llll11lll_opy_:
                self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤᗻ") + str(key) + bstack11lll1_opy_ (u"ࠢࠣᗼ"))
            return
        platform_index = f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_, 0)
        if self.bstack11llll1lll1_opy_.percy_capture_mode == bstack11lll1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᗽ"):
            bstack1l11111l11_opy_ = bstack11llll1l11l_opy_.get(TestFramework.bstack11lllll1111_opy_) + bstack11lll1_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᗾ")
            bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11lllll11l1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l11111l11_opy_,
                bstack1l11lll11l_opy_=bstack11llll1l11l_opy_[TestFramework.bstack1l11ll1llll_opy_],
                bstack1lll1l1ll1_opy_=bstack11llll1l11l_opy_[TestFramework.bstack1l11llll11l_opy_],
                bstack111l1lll1l_opy_=platform_index
            )
            bstack1llll11l_opy_.end(EVENTS.bstack11lllll11l1_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᗿ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘀ"), True, None, None, None, None, test_name=bstack1l11111l11_opy_)
    def bstack11l1l11ll_opy_(self, driver, platform_index):
        if self.bstack1ll1l1llll_opy_.bstack1ll1ll111_opy_() is True or self.bstack1ll1l1llll_opy_.capturing() is True:
            return
        self.bstack1ll1l1llll_opy_.bstack1l1l11l11l_opy_()
        while not self.bstack1ll1l1llll_opy_.bstack1ll1ll111_opy_():
            bstack11lllll11ll_opy_ = self.bstack1ll1l1llll_opy_.bstack11lll11l_opy_()
            self.bstack1ll1111l_opy_(driver, bstack11lllll11ll_opy_, platform_index)
        self.bstack1ll1l1llll_opy_.bstack1l11111l_opy_()
    def bstack1ll1111l_opy_(self, driver, bstack111lll1l_opy_, platform_index, test=None):
        from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
        bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack11l11l1lll_opy_.value)
        if test != None:
            bstack1l11lll11l_opy_ = getattr(test, bstack11lll1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᘁ"), None)
            bstack1lll1l1ll1_opy_ = getattr(test, bstack11lll1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘂ"), None)
            PercySDK.screenshot(driver, bstack111lll1l_opy_, bstack1l11lll11l_opy_=bstack1l11lll11l_opy_, bstack1lll1l1ll1_opy_=bstack1lll1l1ll1_opy_, bstack111l1lll1l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack111lll1l_opy_)
        bstack1llll11l_opy_.end(EVENTS.bstack11l11l1lll_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘃ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘄ"), True, None, None, None, None, test_name=bstack111lll1l_opy_)
    def bstack11llll1l1l1_opy_(self):
        os.environ[bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᘅ")] = str(self.bstack11llll1lll1_opy_.success)
        os.environ[bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᘆ")] = str(self.bstack11llll1lll1_opy_.percy_capture_mode)
        self.percy.bstack11llll1l1ll_opy_(self.bstack11llll1lll1_opy_.is_percy_auto_enabled)
        self.percy.bstack11llll1l111_opy_(self.bstack11llll1lll1_opy_.percy_build_id)