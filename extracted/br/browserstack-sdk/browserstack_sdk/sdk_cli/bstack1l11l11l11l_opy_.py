# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l11llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
    bstack1l1ll1ll111_opy_,
)
from bstack_utils.helper import  bstack111lll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111l1l1_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l111llll11_opy_, TestHookState, bstack1llll111ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11111l11l1_opy_ import bstack111lllll11_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll111ll_opy_ import bstack1l11l1ll111_opy_
from bstack_utils.percy import bstack1llll1l11l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l11llllll1_opy_(bstack1l11llll11l_opy_):
    def __init__(self, bstack11ll1111l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11ll1111l1l_opy_ = bstack11ll1111l1l_opy_
        self.percy = bstack1llll1l11l_opy_()
        self.bstack11l1l1ll_opy_ = bstack111lllll11_opy_()
        self.bstack11ll111l111_opy_()
        bstack1l11l11111l_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1111lll1_opy_, bstack1111111ll_opy_.PRE), self.bstack11ll1111l11_opy_)
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l1111l_opy_(self, instance: bstack1l1ll1ll111_opy_, driver: object):
        bstack11ll1l1ll11_opy_ = TestFramework.bstack1l1ll111lll_opy_(instance.context)
        for t in bstack11ll1l1ll11_opy_:
            bstack11lll11l1l1_opy_ = TestFramework.bstack1l1lllll1l1_opy_(t, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])
            if any(instance is d[1] for d in bstack11lll11l1l1_opy_) or instance == driver:
                return t
    def bstack11ll1111l11_opy_(
        self,
        f: bstack1l11l11111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l11l11111l_opy_.bstack1l11111111l_opy_(method_name):
                return
            platform_index = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11llllll1ll_opy_, 0)
            bstack1l1l1l11l_opy_ = self.bstack11ll1l1111l_opy_(instance, driver)
            bstack11ll111l11l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(bstack1l1l1l11l_opy_, TestFramework.bstack11ll111111l_opy_, None)
            if not bstack11ll111l11l_opy_:
                self.logger.debug(bstack111ll11_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᝤ"))
                return
            driver_command = f.bstack1l111l1l111_opy_(*args)
            for command in bstack1l1lll11ll_opy_:
                if command == driver_command:
                    self.bstack1ll111l1ll_opy_(driver, platform_index)
            bstack11lll11lll_opy_ = self.percy.bstack11111l11l_opy_()
            if driver_command in bstack1l1l11llll_opy_[bstack11lll11lll_opy_]:
                self.bstack11l1l1ll_opy_.bstack1111l1l1l1_opy_(bstack11ll111l11l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᝥ"), e)
    def bstack1l111l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
        bstack11lll11l1l1_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l1ll111_opy_.bstack11ll1llllll_opy_, [])
        if not bstack11lll11l1l1_opy_:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᝦ") + str(kwargs) + bstack111ll11_opy_ (u"ࠨࠢᝧ"))
            return
        if len(bstack11lll11l1l1_opy_) > 1:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝨ") + str(kwargs) + bstack111ll11_opy_ (u"ࠣࠤᝩ"))
        bstack11l1lllll1l_opy_, bstack11ll11111ll_opy_ = bstack11lll11l1l1_opy_[0]
        driver = bstack11l1lllll1l_opy_()
        if not driver:
            self.logger.debug(bstack111ll11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᝪ") + str(kwargs) + bstack111ll11_opy_ (u"ࠥࠦᝫ"))
            return
        bstack11l1lllllll_opy_ = {
            TestFramework.bstack1l111l1lll1_opy_: bstack111ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᝬ"),
            TestFramework.bstack1l111l1ll1l_opy_: bstack111ll11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣ᝭"),
            TestFramework.bstack11ll111111l_opy_: bstack111ll11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᝮ")
        }
        bstack11ll1111111_opy_ = { key: f.bstack1l1lllll1l1_opy_(instance, key) for key in bstack11l1lllllll_opy_ }
        bstack11ll1111lll_opy_ = [key for key, value in bstack11ll1111111_opy_.items() if not value]
        if bstack11ll1111lll_opy_:
            for key in bstack11ll1111lll_opy_:
                self.logger.debug(bstack111ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᝯ") + str(key) + bstack111ll11_opy_ (u"ࠣࠤᝰ"))
            return
        platform_index = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11llllll1ll_opy_, 0)
        if self.bstack11ll1111l1l_opy_.percy_capture_mode == bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦ᝱"):
            bstack1111llll1_opy_ = bstack11ll1111111_opy_.get(TestFramework.bstack11ll111111l_opy_) + bstack111ll11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᝲ")
            bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack11ll1111ll1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1111llll1_opy_,
                bstack1ll11l11ll_opy_=bstack11ll1111111_opy_[TestFramework.bstack1l111l1lll1_opy_],
                bstack1l11llll11_opy_=bstack11ll1111111_opy_[TestFramework.bstack1l111l1ll1l_opy_],
                bstack111l1l1lll_opy_=platform_index
            )
            bstack1ll1l11l1_opy_.end(EVENTS.bstack11ll1111ll1_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᝳ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᝴"), True, None, None, None, None, test_name=bstack1111llll1_opy_)
    def bstack1ll111l1ll_opy_(self, driver, platform_index):
        if self.bstack11l1l1ll_opy_.bstack111l111l1l_opy_() is True or self.bstack11l1l1ll_opy_.capturing() is True:
            return
        self.bstack11l1l1ll_opy_.bstack1ll1llllll_opy_()
        while not self.bstack11l1l1ll_opy_.bstack111l111l1l_opy_():
            bstack11ll111l11l_opy_ = self.bstack11l1l1ll_opy_.bstack1111l1l1ll_opy_()
            self.bstack1llll1111_opy_(driver, bstack11ll111l11l_opy_, platform_index)
        self.bstack11l1l1ll_opy_.bstack11l1lll11l_opy_()
    def bstack1llll1111_opy_(self, driver, bstack1l1ll1llll_opy_, platform_index, test=None):
        from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
        bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack1l1ll111_opy_.value)
        if test != None:
            bstack1ll11l11ll_opy_ = getattr(test, bstack111ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᝵"), None)
            bstack1l11llll11_opy_ = getattr(test, bstack111ll11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬ᝶"), None)
            PercySDK.screenshot(driver, bstack1l1ll1llll_opy_, bstack1ll11l11ll_opy_=bstack1ll11l11ll_opy_, bstack1l11llll11_opy_=bstack1l11llll11_opy_, bstack111l1l1lll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1ll1llll_opy_)
        bstack1ll1l11l1_opy_.end(EVENTS.bstack1l1ll111_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᝷"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᝸"), True, None, None, None, None, test_name=bstack1l1ll1llll_opy_)
    def bstack11ll111l111_opy_(self):
        os.environ[bstack111ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨ᝹")] = str(self.bstack11ll1111l1l_opy_.success)
        os.environ[bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨ᝺")] = str(self.bstack11ll1111l1l_opy_.percy_capture_mode)
        self.percy.bstack11l1llllll1_opy_(self.bstack11ll1111l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack11ll11111l1_opy_(self.bstack11ll1111l1l_opy_.percy_build_id)