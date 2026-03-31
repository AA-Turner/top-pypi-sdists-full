# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack1ll111lllll_opy_,
)
from bstack_utils.helper import  bstack1l1111l111_opy_
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1l111l1_opy_, TestHookState, bstack1l1l1l1lll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111l11l111_opy_ import bstack1l11111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l111_opy_ import bstack1l1l1l11ll1_opy_
from bstack_utils.percy import bstack1l1l1ll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l11ll1ll_opy_(bstack1ll111l11ll_opy_):
    def __init__(self, bstack11lll1lll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11lll1lll1l_opy_ = bstack11lll1lll1l_opy_
        self.percy = bstack1l1l1ll1l1_opy_()
        self.bstack1l11lll11l_opy_ = bstack1l11111l_opy_()
        self.bstack11llll1l111_opy_()
        bstack1ll11111111_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack11llll11111_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l111111l1l_opy_(self, instance: bstack1ll111lllll_opy_, driver: object):
        bstack1l11111ll11_opy_ = TestFramework.bstack1ll11lll1ll_opy_(instance.context)
        for t in bstack1l11111ll11_opy_:
            bstack11lllll11l1_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(t, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
            if any(instance is d[1] for d in bstack11lllll11l1_opy_) or instance == driver:
                return t
    def bstack11llll11111_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll11111111_opy_.bstack1l11l1l1lll_opy_(method_name):
                return
            platform_index = f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_, 0)
            bstack1l1111ll11l_opy_ = self.bstack1l111111l1l_opy_(instance, driver)
            bstack11llll1111l_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(bstack1l1111ll11l_opy_, TestFramework.bstack11lll1llll1_opy_, None)
            if not bstack11llll1111l_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦᘕ"))
                return
            driver_command = f.bstack1l1l111ll11_opy_(*args)
            for command in bstack111llll111_opy_:
                if command == driver_command:
                    self.bstack11l11111_opy_(driver, platform_index)
            bstack11l11ll1_opy_ = self.percy.bstack11l11l11l1_opy_()
            if driver_command in bstack1l1l11llll_opy_[bstack11l11ll1_opy_]:
                self.bstack1l11lll11l_opy_.bstack1llll11ll_opy_(bstack11llll1111l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨᘖ"), e)
    def bstack1l11ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
        bstack11lllll11l1_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1l1l1l11ll1_opy_.bstack1l1111ll1l1_opy_, [])
        if not bstack11lllll11l1_opy_:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᘗ") + str(kwargs) + bstack1ll11_opy_ (u"ࠢࠣᘘ"))
            return
        if len(bstack11lllll11l1_opy_) > 1:
            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᘙ") + str(kwargs) + bstack1ll11_opy_ (u"ࠤࠥᘚ"))
        bstack11llll111l1_opy_, bstack11llll11l11_opy_ = bstack11lllll11l1_opy_[0]
        driver = bstack11llll111l1_opy_()
        if not driver:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᘛ") + str(kwargs) + bstack1ll11_opy_ (u"ࠦࠧᘜ"))
            return
        bstack11lll1lllll_opy_ = {
            TestFramework.bstack1l11ll1ll1l_opy_: bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᘝ"),
            TestFramework.bstack1l11l1lll11_opy_: bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᘞ"),
            TestFramework.bstack11lll1llll1_opy_: bstack1ll11_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤᘟ")
        }
        bstack11llll1l11l_opy_ = { key: f.bstack1ll1ll1l1l1_opy_(instance, key) for key in bstack11lll1lllll_opy_ }
        bstack11llll11l1l_opy_ = [key for key, value in bstack11llll1l11l_opy_.items() if not value]
        if bstack11llll11l1l_opy_:
            for key in bstack11llll11l1l_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦᘠ") + str(key) + bstack1ll11_opy_ (u"ࠤࠥᘡ"))
            return
        platform_index = f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_, 0)
        if self.bstack11lll1lll1l_opy_.percy_capture_mode == bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧᘢ"):
            bstack1111lll11_opy_ = bstack11llll1l11l_opy_.get(TestFramework.bstack11lll1llll1_opy_) + bstack1ll11_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᘣ")
            bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11llll11ll1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111lll11_opy_,
                bstack1llll1l111_opy_=bstack11llll1l11l_opy_[TestFramework.bstack1l11ll1ll1l_opy_],
                bstack111111ll11_opy_=bstack11llll1l11l_opy_[TestFramework.bstack1l11l1lll11_opy_],
                bstack1lll1111l_opy_=platform_index
            )
            bstack11ll11l1ll_opy_.end(EVENTS.bstack11llll11ll1_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘤ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘥ"), True, None, None, None, None, test_name=bstack1111lll11_opy_)
    def bstack11l11111_opy_(self, driver, platform_index):
        if self.bstack1l11lll11l_opy_.bstack1llll1ll11_opy_() is True or self.bstack1l11lll11l_opy_.capturing() is True:
            return
        self.bstack1l11lll11l_opy_.bstack1l11ll11ll_opy_()
        while not self.bstack1l11lll11l_opy_.bstack1llll1ll11_opy_():
            bstack11llll1111l_opy_ = self.bstack1l11lll11l_opy_.bstack11lllll11l_opy_()
            self.bstack11lll111l1_opy_(driver, bstack11llll1111l_opy_, platform_index)
        self.bstack1l11lll11l_opy_.bstack11l1l1llll_opy_()
    def bstack11lll111l1_opy_(self, driver, bstack1lll1lll11_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
        bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11ll11l111_opy_.value)
        if test != None:
            bstack1llll1l111_opy_ = getattr(test, bstack1ll11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᘦ"), None)
            bstack111111ll11_opy_ = getattr(test, bstack1ll11_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᘧ"), None)
            PercySDK.screenshot(driver, bstack1lll1lll11_opy_, bstack1llll1l111_opy_=bstack1llll1l111_opy_, bstack111111ll11_opy_=bstack111111ll11_opy_, bstack1lll1111l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll1lll11_opy_)
        bstack11ll11l1ll_opy_.end(EVENTS.bstack11ll11l111_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘨ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘩ"), True, None, None, None, None, test_name=bstack1lll1lll11_opy_)
    def bstack11llll1l111_opy_(self):
        os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩᘪ")] = str(self.bstack11lll1lll1l_opy_.success)
        os.environ[bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩᘫ")] = str(self.bstack11lll1lll1l_opy_.percy_capture_mode)
        self.percy.bstack11llll11lll_opy_(self.bstack11lll1lll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack11llll111ll_opy_(self.bstack11lll1lll1l_opy_.percy_build_id)