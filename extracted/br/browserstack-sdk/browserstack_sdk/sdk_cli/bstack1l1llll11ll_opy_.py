# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1l1l111l_opy_,
)
from bstack_utils.helper import  bstack11llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll11l1ll1l_opy_, TestHookState, bstack1l1ll11l111_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1l1llll_opy_ import bstack1ll1llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll111_opy_ import bstack1ll111l1lll_opy_
from bstack_utils.percy import bstack1ll11111l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1lll1llll_opy_(bstack1ll11111l11_opy_):
    def __init__(self, bstack1l111111l11_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l111111l11_opy_ = bstack1l111111l11_opy_
        self.percy = bstack1ll11111l_opy_()
        self.bstack1lll111ll1_opy_ = bstack1ll1llll11_opy_()
        self.bstack1l111111ll1_opy_()
        bstack1ll11lll111_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack1l11111l111_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11111ll1l_opy_(self, instance: bstack1ll1l1l111l_opy_, driver: object):
        bstack1l11l11l1l1_opy_ = TestFramework.bstack1ll1l1111ll_opy_(instance.context)
        for t in bstack1l11l11l1l1_opy_:
            bstack1l11l111lll_opy_ = TestFramework.bstack1lll111lll1_opy_(t, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
            if any(instance is d[1] for d in bstack1l11l111lll_opy_) or instance == driver:
                return t
    def bstack1l11111l111_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll11lll111_opy_.bstack1l1l111111l_opy_(method_name):
                return
            platform_index = f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_, 0)
            bstack1l111l11l1l_opy_ = self.bstack1l11111ll1l_opy_(instance, driver)
            bstack1l1111111ll_opy_ = TestFramework.bstack1lll111lll1_opy_(bstack1l111l11l1l_opy_, TestFramework.bstack1l11111l1l1_opy_, None)
            if not bstack1l1111111ll_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤᖀ"))
                return
            driver_command = f.bstack1l1l11l1l11_opy_(*args)
            for command in bstack1111lll1l_opy_:
                if command == driver_command:
                    self.bstack1l11l1111_opy_(driver, platform_index)
            bstack1l111111l_opy_ = self.percy.bstack1ll11l111l_opy_()
            if driver_command in bstack1l111l1lll_opy_[bstack1l111111l_opy_]:
                self.bstack1lll111ll1_opy_.bstack1ll1l1lll_opy_(bstack1l1111111ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦᖁ"), e)
    def bstack1l11lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
        bstack1l11l111lll_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll111l1lll_opy_.bstack1l111l1l1l1_opy_, [])
        if not bstack1l11l111lll_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᖂ") + str(kwargs) + bstack1ll111_opy_ (u"ࠧࠨᖃ"))
            return
        if len(bstack1l11l111lll_opy_) > 1:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᖄ") + str(kwargs) + bstack1ll111_opy_ (u"ࠢࠣᖅ"))
        bstack1l111111111_opy_, bstack11lllllllll_opy_ = bstack1l11l111lll_opy_[0]
        driver = bstack1l111111111_opy_()
        if not driver:
            self.logger.debug(bstack1ll111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᖆ") + str(kwargs) + bstack1ll111_opy_ (u"ࠤࠥᖇ"))
            return
        bstack11llllllll1_opy_ = {
            TestFramework.bstack1l1l11llll1_opy_: bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᖈ"),
            TestFramework.bstack1l1l1ll11ll_opy_: bstack1ll111_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢᖉ"),
            TestFramework.bstack1l11111l1l1_opy_: bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢᖊ")
        }
        bstack1l1111111l1_opy_ = { key: f.bstack1lll111lll1_opy_(instance, key) for key in bstack11llllllll1_opy_ }
        bstack1l11111111l_opy_ = [key for key, value in bstack1l1111111l1_opy_.items() if not value]
        if bstack1l11111111l_opy_:
            for key in bstack1l11111111l_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤᖋ") + str(key) + bstack1ll111_opy_ (u"ࠢࠣᖌ"))
            return
        platform_index = f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_, 0)
        if self.bstack1l111111l11_opy_.percy_capture_mode == bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᖍ"):
            bstack11l11ll1ll_opy_ = bstack1l1111111l1_opy_.get(TestFramework.bstack1l11111l1l1_opy_) + bstack1ll111_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᖎ")
            bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1l111111lll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11l11ll1ll_opy_,
                bstack1llll11l1_opy_=bstack1l1111111l1_opy_[TestFramework.bstack1l1l11llll1_opy_],
                bstack1ll11l1ll1_opy_=bstack1l1111111l1_opy_[TestFramework.bstack1l1l1ll11ll_opy_],
                bstack1llll11111_opy_=platform_index
            )
            bstack111ll11111_opy_.end(EVENTS.bstack1l111111lll_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᖏ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᖐ"), True, None, None, None, None, test_name=bstack11l11ll1ll_opy_)
    def bstack1l11l1111_opy_(self, driver, platform_index):
        if self.bstack1lll111ll1_opy_.bstack11lll111_opy_() is True or self.bstack1lll111ll1_opy_.capturing() is True:
            return
        self.bstack1lll111ll1_opy_.bstack1111l111l1_opy_()
        while not self.bstack1lll111ll1_opy_.bstack11lll111_opy_():
            bstack1l1111111ll_opy_ = self.bstack1lll111ll1_opy_.bstack11ll1111l_opy_()
            self.bstack1l1ll1111_opy_(driver, bstack1l1111111ll_opy_, platform_index)
        self.bstack1lll111ll1_opy_.bstack1lll1l1l1l_opy_()
    def bstack1l1ll1111_opy_(self, driver, bstack1l111ll1ll_opy_, platform_index, test=None):
        from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
        bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack111ll111ll_opy_.value)
        if test != None:
            bstack1llll11l1_opy_ = getattr(test, bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᖑ"), None)
            bstack1ll11l1ll1_opy_ = getattr(test, bstack1ll111_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖒ"), None)
            PercySDK.screenshot(driver, bstack1l111ll1ll_opy_, bstack1llll11l1_opy_=bstack1llll11l1_opy_, bstack1ll11l1ll1_opy_=bstack1ll11l1ll1_opy_, bstack1llll11111_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l111ll1ll_opy_)
        bstack111ll11111_opy_.end(EVENTS.bstack111ll111ll_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᖓ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᖔ"), True, None, None, None, None, test_name=bstack1l111ll1ll_opy_)
    def bstack1l111111ll1_opy_(self):
        os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᖕ")] = str(self.bstack1l111111l11_opy_.success)
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᖖ")] = str(self.bstack1l111111l11_opy_.percy_capture_mode)
        self.percy.bstack1l11111l11l_opy_(self.bstack1l111111l11_opy_.is_percy_auto_enabled)
        self.percy.bstack1l111111l1l_opy_(self.bstack1l111111l11_opy_.percy_build_id)