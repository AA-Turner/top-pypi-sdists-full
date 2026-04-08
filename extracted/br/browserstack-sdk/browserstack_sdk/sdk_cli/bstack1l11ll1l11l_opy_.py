# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l111l1l1_opy_,
)
from bstack_utils.helper import  bstack1llll11111_opy_
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l11ll11l_opy_, TestHookState, bstack11lllllll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l111ll1ll_opy_ import bstack1l1l111l11_opy_
from browserstack_sdk.sdk_cli.bstack1l11111111l_opy_ import bstack1l1111l111l_opy_
from bstack_utils.percy import bstack11llll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l111ll1lll_opy_(bstack1l111111l1l_opy_):
    def __init__(self, bstack11l1l1l1l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11l1l1l1l1l_opy_ = bstack11l1l1l1l1l_opy_
        self.percy = bstack11llll1l1_opy_()
        self.bstack11l111l1l_opy_ = bstack1l1l111l11_opy_()
        self.bstack11l1l1lllll_opy_()
        bstack1l11l11l11l_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11l1l1lll1l_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11lll1ll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11l1lllllll_opy_(self, instance: bstack1l1l111l1l1_opy_, driver: object):
        bstack11l1lllll1l_opy_ = TestFramework.bstack1l1l111111l_opy_(instance.context)
        for t in bstack11l1lllll1l_opy_:
            bstack11l1ll1ll1l_opy_ = TestFramework.bstack1ll111111ll_opy_(t, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
            if any(instance is d[1] for d in bstack11l1ll1ll1l_opy_) or instance == driver:
                return t
    def bstack11l1l1lll1l_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l11l11l11l_opy_.bstack11llll111l1_opy_(method_name):
                return
            platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_, 0)
            bstack1lll1l1lll_opy_ = self.bstack11l1lllllll_opy_(instance, driver)
            bstack11l1l1lll11_opy_ = TestFramework.bstack1ll111111ll_opy_(bstack1lll1l1lll_opy_, TestFramework.bstack1l1ll11ll11_opy_, None)
            if not bstack11l1l1lll11_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡲࡦࡶࡸࡶࡳ࡯࡮ࡨࠢࡤࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡩࡴࠢࡱࡳࡹࠦࡹࡦࡶࠣࡷࡹࡧࡲࡵࡧࡧࠦៜ"))
                return
            driver_command = f.bstack11lll1ll11l_opy_(*args)
            for command in bstack11l1ll1ll_opy_:
                if command == driver_command:
                    self.bstack11l1ll1l_opy_(driver, platform_index)
            bstack11l11ll11l_opy_ = self.percy.bstack11ll1ll1_opy_()
            if driver_command in bstack1l11ll11ll_opy_[bstack11l11ll11l_opy_]:
                self.bstack11l111l1l_opy_.bstack11ll1l1ll1_opy_(bstack11l1l1lll11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡦࡴࡵࡳࡷࠨ៝"), e)
    def bstack11lll1ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
        bstack11l1ll1ll1l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1111l111l_opy_.bstack11ll11ll111_opy_, [])
        if not bstack11l1ll1ll1l_opy_:
            self.logger.debug(bstack111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ៞") + str(kwargs) + bstack111l_opy_ (u"ࠢࠣ៟"))
            return
        if len(bstack11l1ll1ll1l_opy_) > 1:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡥࡴ࡬ࡺࡪࡸ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ០") + str(kwargs) + bstack111l_opy_ (u"ࠤࠥ១"))
        bstack11l1l1ll1ll_opy_, bstack11l1l1l1lll_opy_ = bstack11l1ll1ll1l_opy_[0]
        driver = bstack11l1l1ll1ll_opy_()
        if not driver:
            self.logger.debug(bstack111l_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ២") + str(kwargs) + bstack111l_opy_ (u"ࠦࠧ៣"))
            return
        bstack11l1l1ll1l1_opy_ = {
            TestFramework.bstack1l1ll1lll1l_opy_: bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣ៤"),
            TestFramework.bstack1l1l1lll11l_opy_: bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤ៥"),
            TestFramework.bstack1l1ll11ll11_opy_: bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࠥࡸࡥࡳࡷࡱࠤࡳࡧ࡭ࡦࠤ៦")
        }
        bstack11l1l1l1l11_opy_ = { key: f.bstack1ll111111ll_opy_(instance, key) for key in bstack11l1l1ll1l1_opy_ }
        bstack11l1l1ll111_opy_ = [key for key, value in bstack11l1l1l1l11_opy_.items() if not value]
        if bstack11l1l1ll111_opy_:
            for key in bstack11l1l1ll111_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠦ៧") + str(key) + bstack111l_opy_ (u"ࠤࠥ៨"))
            return
        platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_, 0)
        if self.bstack11l1l1l1l1l_opy_.percy_capture_mode == bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ៩"):
            bstack1l1lll1ll_opy_ = bstack11l1l1l1l11_opy_.get(TestFramework.bstack1l1ll11ll11_opy_) + bstack111l_opy_ (u"ࠦ࠲ࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ៪")
            bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack11l1l1l1ll1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1lll1ll_opy_,
                bstack111l1ll11_opy_=bstack11l1l1l1l11_opy_[TestFramework.bstack1l1ll1lll1l_opy_],
                bstack1l11ll1111_opy_=bstack11l1l1l1l11_opy_[TestFramework.bstack1l1l1lll11l_opy_],
                bstack111llll1l1_opy_=platform_index
            )
            bstack11lll11111_opy_.end(EVENTS.bstack11l1l1l1ll1_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ៫"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ៬"), True, None, None, None, None, test_name=bstack1l1lll1ll_opy_)
    def bstack11l1ll1l_opy_(self, driver, platform_index):
        if self.bstack11l111l1l_opy_.bstack11llll1ll_opy_() is True or self.bstack11l111l1l_opy_.capturing() is True:
            return
        self.bstack11l111l1l_opy_.bstack1l111llll1_opy_()
        while not self.bstack11l111l1l_opy_.bstack11llll1ll_opy_():
            bstack11l1l1lll11_opy_ = self.bstack11l111l1l_opy_.bstack1llll1l1_opy_()
            self.bstack1l111ll11_opy_(driver, bstack11l1l1lll11_opy_, platform_index)
        self.bstack11l111l1l_opy_.bstack1llll1l1l_opy_()
    def bstack1l111ll11_opy_(self, driver, bstack1lll1l1l1_opy_, platform_index, test=None):
        from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
        bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack1l1l1l1lll_opy_.value)
        if test != None:
            bstack111l1ll11_opy_ = getattr(test, bstack111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ៭"), None)
            bstack1l11ll1111_opy_ = getattr(test, bstack111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭៮"), None)
            PercySDK.screenshot(driver, bstack1lll1l1l1_opy_, bstack111l1ll11_opy_=bstack111l1ll11_opy_, bstack1l11ll1111_opy_=bstack1l11ll1111_opy_, bstack111llll1l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll1l1l1_opy_)
        bstack11lll11111_opy_.end(EVENTS.bstack1l1l1l1lll_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ៯"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ៰"), True, None, None, None, None, test_name=bstack1lll1l1l1_opy_)
    def bstack11l1l1lllll_opy_(self):
        os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࠩ៱")] = str(self.bstack11l1l1l1l1l_opy_.success)
        os.environ[bstack111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࡢࡇࡆࡖࡔࡖࡔࡈࡣࡒࡕࡄࡆࠩ៲")] = str(self.bstack11l1l1l1l1l_opy_.percy_capture_mode)
        self.percy.bstack11l1l1llll1_opy_(self.bstack11l1l1l1l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack11l1l1ll11l_opy_(self.bstack11l1l1l1l1l_opy_.percy_build_id)