# coding: UTF-8
import sys
bstack11l1l_opy_ = sys.version_info [0] == 2
bstack1ll11_opy_ = 2048
bstack11ll11_opy_ = 7
def bstack1l111l_opy_ (bstack11l11l_opy_):
    global bstack1l11l_opy_
    bstack1l1111l_opy_ = ord (bstack11l11l_opy_ [-1])
    bstack1l1l11l_opy_ = bstack11l11l_opy_ [:-1]
    bstack111l1_opy_ = bstack1l1111l_opy_ % len (bstack1l1l11l_opy_)
    bstack11l1l1l_opy_ = bstack1l1l11l_opy_ [:bstack111l1_opy_] + bstack1l1l11l_opy_ [bstack111l1_opy_:]
    if bstack11l1l_opy_:
        bstack1111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    else:
        bstack1111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll11_opy_ - (bstack1lllll1_opy_ + bstack1l1111l_opy_) % bstack11ll11_opy_) for bstack1lllll1_opy_, char in enumerate (bstack11l1l1l_opy_)])
    return eval (bstack1111l1l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1111ll1_opy_ import bstack1l11ll1l11l_opy_
from browserstack_sdk.sdk_cli.bstack1111ll1ll1_opy_ import (
    bstack1l1l11ll1l_opy_,
    bstack1ll1llll1l_opy_,
    bstack1l1ll1lllll_opy_,
)
from bstack_utils.helper import  bstack1l111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11l1l1_opy_ import bstack1l11l1ll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l11l11111l_opy_, TestHookState, bstack1llll11ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11lllll111_opy_ import bstack1111ll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11l1l_opy_ import bstack1l11ll111l1_opy_
from bstack_utils.percy import bstack1llll1l11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l111111l_opy_(bstack1l11ll1l11l_opy_):
    def __init__(self, bstack11l1lllll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11l1lllll1l_opy_ = bstack11l1lllll1l_opy_
        self.percy = bstack1llll1l11_opy_()
        self.bstack1ll1l1l1l1_opy_ = bstack1111ll1l11_opy_()
        self.bstack11ll11111l1_opy_()
        bstack1l11l1ll1l1_opy_.bstack1l11111ll11_opy_((bstack1l1l11ll1l_opy_.bstack1l1llllllll_opy_, bstack1ll1llll1l_opy_.PRE), self.bstack11l1lllllll_opy_)
        TestFramework.bstack1l11111ll11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11111lll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l11ll1_opy_(self, instance: bstack1l1ll1lllll_opy_, driver: object):
        bstack11lll1l11l1_opy_ = TestFramework.bstack1l1ll11111l_opy_(instance.context)
        for t in bstack11lll1l11l1_opy_:
            bstack11ll11ll1l1_opy_ = TestFramework.bstack1ll111111ll_opy_(t, bstack1l11ll111l1_opy_.bstack11ll1l11111_opy_, [])
            if any(instance is d[1] for d in bstack11ll11ll1l1_opy_) or instance == driver:
                return t
    def bstack11l1lllllll_opy_(
        self,
        f: bstack1l11l1ll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1lllll_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack1l1l11ll1l_opy_, bstack1ll1llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l11l1ll1l1_opy_.bstack11lllll1ll1_opy_(method_name):
                return
            platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_, 0)
            bstack11l1l11111_opy_ = self.bstack11ll1l11ll1_opy_(instance, driver)
            bstack11ll111l111_opy_ = TestFramework.bstack1ll111111ll_opy_(bstack11l1l11111_opy_, TestFramework.bstack11ll1111l11_opy_, None)
            if not bstack11ll111l111_opy_:
                self.logger.debug(bstack1l111l_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᝤ"))
                return
            driver_command = f.bstack1l111111l11_opy_(*args)
            for command in bstack1lllllll11l_opy_:
                if command == driver_command:
                    self.bstack111l1l1lll_opy_(driver, platform_index)
            bstack11l111ll11_opy_ = self.percy.bstack1l1l1llll_opy_()
            if driver_command in bstack111l111ll1_opy_[bstack11l111ll11_opy_]:
                self.bstack1ll1l1l1l1_opy_.bstack1lllll1lll1_opy_(bstack11ll111l111_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l111l_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᝥ"), e)
    def bstack1l11111lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l11111l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
        bstack11ll11ll1l1_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l11ll111l1_opy_.bstack11ll1l11111_opy_, [])
        if not bstack11ll11ll1l1_opy_:
            self.logger.debug(bstack1l111l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᝦ") + str(kwargs) + bstack1l111l_opy_ (u"ࠨࠢᝧ"))
            return
        if len(bstack11ll11ll1l1_opy_) > 1:
            self.logger.debug(bstack1l111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝨ") + str(kwargs) + bstack1l111l_opy_ (u"ࠣࠤᝩ"))
        bstack11ll1111lll_opy_, bstack11l1llllll1_opy_ = bstack11ll11ll1l1_opy_[0]
        driver = bstack11ll1111lll_opy_()
        if not driver:
            self.logger.debug(bstack1l111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝪ") + str(kwargs) + bstack1l111l_opy_ (u"ࠥࠦᝫ"))
            return
        bstack11ll11111ll_opy_ = {
            TestFramework.bstack11llllll11l_opy_: bstack1l111l_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᝬ"),
            TestFramework.bstack1l11111llll_opy_: bstack1l111l_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣ᝭"),
            TestFramework.bstack11ll1111l11_opy_: bstack1l111l_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᝮ")
        }
        bstack11ll1111l1l_opy_ = { key: f.bstack1ll111111ll_opy_(instance, key) for key in bstack11ll11111ll_opy_ }
        bstack11ll111111l_opy_ = [key for key, value in bstack11ll1111l1l_opy_.items() if not value]
        if bstack11ll111111l_opy_:
            for key in bstack11ll111111l_opy_:
                self.logger.debug(bstack1l111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᝯ") + str(key) + bstack1l111l_opy_ (u"ࠣࠤᝰ"))
            return
        platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l1ll1l1_opy_.bstack1l111l1111l_opy_, 0)
        if self.bstack11l1lllll1l_opy_.percy_capture_mode == bstack1l111l_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᝱"):
            bstack111l1l1ll1_opy_ = bstack11ll1111l1l_opy_.get(TestFramework.bstack11ll1111l11_opy_) + bstack1l111l_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᝲ")
            bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack11ll1111111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack111l1l1ll1_opy_,
                bstack1l1111l111_opy_=bstack11ll1111l1l_opy_[TestFramework.bstack11llllll11l_opy_],
                bstack1ll1ll11l_opy_=bstack11ll1111l1l_opy_[TestFramework.bstack1l11111llll_opy_],
                bstack1ll1llll11_opy_=platform_index
            )
            bstack111ll11l1_opy_.end(EVENTS.bstack11ll1111111_opy_.value, bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᝳ"), bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᝴"), True, None, None, None, None, test_name=bstack111l1l1ll1_opy_)
    def bstack111l1l1lll_opy_(self, driver, platform_index):
        if self.bstack1ll1l1l1l1_opy_.bstack11111l1l_opy_() is True or self.bstack1ll1l1l1l1_opy_.capturing() is True:
            return
        self.bstack1ll1l1l1l1_opy_.bstack1ll1l1ll_opy_()
        while not self.bstack1ll1l1l1l1_opy_.bstack11111l1l_opy_():
            bstack11ll111l111_opy_ = self.bstack1ll1l1l1l1_opy_.bstack111ll1l11l_opy_()
            self.bstack1111ll1lll_opy_(driver, bstack11ll111l111_opy_, platform_index)
        self.bstack1ll1l1l1l1_opy_.bstack1l1ll11ll_opy_()
    def bstack1111ll1lll_opy_(self, driver, bstack1lll11l1l1_opy_, platform_index, test=None):
        from bstack_utils.bstack1llll111_opy_ import bstack111ll11l1_opy_
        bstack1l11l11l_opy_ = bstack111ll11l1_opy_.bstack11l1111ll_opy_(EVENTS.bstack11l1l111_opy_.value)
        if test != None:
            bstack1l1111l111_opy_ = getattr(test, bstack1l111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᝵"), None)
            bstack1ll1ll11l_opy_ = getattr(test, bstack1l111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᝶"), None)
            PercySDK.screenshot(driver, bstack1lll11l1l1_opy_, bstack1l1111l111_opy_=bstack1l1111l111_opy_, bstack1ll1ll11l_opy_=bstack1ll1ll11l_opy_, bstack1ll1llll11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll11l1l1_opy_)
        bstack111ll11l1_opy_.end(EVENTS.bstack11l1l111_opy_.value, bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᝷"), bstack1l11l11l_opy_+bstack1l111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᝸"), True, None, None, None, None, test_name=bstack1lll11l1l1_opy_)
    def bstack11ll11111l1_opy_(self):
        os.environ[bstack1l111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᝹")] = str(self.bstack11l1lllll1l_opy_.success)
        os.environ[bstack1l111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ᝺")] = str(self.bstack11l1lllll1l_opy_.percy_capture_mode)
        self.percy.bstack11ll1111ll1_opy_(self.bstack11l1lllll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack11ll111l11l_opy_(self.bstack11l1lllll1l_opy_.percy_build_id)