# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1llll11l_opy_,
)
from bstack_utils.helper import  bstack1lll111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1ll111l1l1l_opy_, TestHookState, bstack1ll11ll1l1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111ll111l_opy_ import bstack1ll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111lll_opy_ import bstack1ll11ll1lll_opy_
from bstack_utils.percy import bstack1l1l1l1l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll11l1111l_opy_(bstack1ll11l1ll11_opy_):
    def __init__(self, bstack1l1111llll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1111llll1_opy_ = bstack1l1111llll1_opy_
        self.percy = bstack1l1l1l1l_opy_()
        self.bstack111lll111l_opy_ = bstack1ll1l1l11_opy_()
        self.bstack1l1111lll1l_opy_()
        bstack1ll11l11l11_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l1111l1ll1_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1l1111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l1111ll_opy_(self, instance: bstack1ll1llll11l_opy_, driver: object):
        bstack1l11l1ll1ll_opy_ = TestFramework.bstack1ll1lll1l1l_opy_(instance.context)
        for t in bstack1l11l1ll1ll_opy_:
            bstack1l111lll111_opy_ = TestFramework.bstack1lll111l1l1_opy_(t, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
            if any(instance is d[1] for d in bstack1l111lll111_opy_) or instance == driver:
                return t
    def bstack1l1111l1ll1_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll11l11l11_opy_.bstack1l1l11lllll_opy_(method_name):
                return
            platform_index = f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_, 0)
            bstack1l111ll1lll_opy_ = self.bstack1l11l1111ll_opy_(instance, driver)
            bstack1l1111l1l11_opy_ = TestFramework.bstack1lll111l1l1_opy_(bstack1l111ll1lll_opy_, TestFramework.bstack1l1111ll1l1_opy_, None)
            if not bstack1l1111l1l11_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡷ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡢࡵࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡵࡷࡥࡷࡺࡥࡥࠤᔗ"))
                return
            driver_command = f.bstack1l1l1llll1l_opy_(*args)
            for command in bstack111ll1l1ll_opy_:
                if command == driver_command:
                    self.bstack11l1111lll_opy_(driver, platform_index)
            bstack111111l1l_opy_ = self.percy.bstack1lllll1ll_opy_()
            if driver_command in bstack1ll1ll1111_opy_[bstack111111l1l_opy_]:
                self.bstack111lll111l_opy_.bstack1lllll111l_opy_(bstack1l1111l1l11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥ࡫ࡲࡳࡱࡵࠦᔘ"), e)
    def bstack1l1l1l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
        bstack1l111lll111_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1lll_opy_.bstack1l111lllll1_opy_, [])
        if not bstack1l111lll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᔙ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠧࠨᔚ"))
            return
        if len(bstack1l111lll111_opy_) > 1:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡼ࡮ࡨࡲ࠭ࡪࡲࡪࡸࡨࡶࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᔛ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠢࠣᔜ"))
        bstack1l1111ll1ll_opy_, bstack1l1111ll111_opy_ = bstack1l111lll111_opy_[0]
        driver = bstack1l1111ll1ll_opy_()
        if not driver:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᔝ") + str(kwargs) + bstack1lll1l_opy_ (u"ࠤࠥᔞ"))
            return
        bstack1l1111lllll_opy_ = {
            TestFramework.bstack1l1l111llll_opy_: bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᔟ"),
            TestFramework.bstack1l1l1l1ll1l_opy_: bstack1lll1l_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢᔠ"),
            TestFramework.bstack1l1111ll1l1_opy_: bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࠣࡶࡪࡸࡵ࡯ࠢࡱࡥࡲ࡫ࠢᔡ")
        }
        bstack1l1111l1l1l_opy_ = { key: f.bstack1lll111l1l1_opy_(instance, key) for key in bstack1l1111lllll_opy_ }
        bstack1l1111ll11l_opy_ = [key for key, value in bstack1l1111l1l1l_opy_.items() if not value]
        if bstack1l1111ll11l_opy_:
            for key in bstack1l1111ll11l_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠤᔢ") + str(key) + bstack1lll1l_opy_ (u"ࠢࠣᔣ"))
            return
        platform_index = f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_, 0)
        if self.bstack1l1111llll1_opy_.percy_capture_mode == bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᔤ"):
            bstack11l1l11l1_opy_ = bstack1l1111l1l1l_opy_.get(TestFramework.bstack1l1111ll1l1_opy_) + bstack1lll1l_opy_ (u"ࠤ࠰ࡸࡪࡹࡴࡤࡣࡶࡩࠧᔥ")
            bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack1l1111l11ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11l1l11l1_opy_,
                bstack1llll111l_opy_=bstack1l1111l1l1l_opy_[TestFramework.bstack1l1l111llll_opy_],
                bstack111l1111ll_opy_=bstack1l1111l1l1l_opy_[TestFramework.bstack1l1l1l1ll1l_opy_],
                bstack1ll11l11ll_opy_=platform_index
            )
            bstack1l11l11ll1_opy_.end(EVENTS.bstack1l1111l11ll_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᔦ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᔧ"), True, None, None, None, None, test_name=bstack11l1l11l1_opy_)
    def bstack11l1111lll_opy_(self, driver, platform_index):
        if self.bstack111lll111l_opy_.bstack111ll1l11l_opy_() is True or self.bstack111lll111l_opy_.capturing() is True:
            return
        self.bstack111lll111l_opy_.bstack11lll111l1_opy_()
        while not self.bstack111lll111l_opy_.bstack111ll1l11l_opy_():
            bstack1l1111l1l11_opy_ = self.bstack111lll111l_opy_.bstack1l1l1l1l1_opy_()
            self.bstack1l11ll1l11_opy_(driver, bstack1l1111l1l11_opy_, platform_index)
        self.bstack111lll111l_opy_.bstack11l1lllll1_opy_()
    def bstack1l11ll1l11_opy_(self, driver, bstack1lll1l11_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
        bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack1l11llll_opy_.value)
        if test != None:
            bstack1llll111l_opy_ = getattr(test, bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᔨ"), None)
            bstack111l1111ll_opy_ = getattr(test, bstack1lll1l_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᔩ"), None)
            PercySDK.screenshot(driver, bstack1lll1l11_opy_, bstack1llll111l_opy_=bstack1llll111l_opy_, bstack111l1111ll_opy_=bstack111l1111ll_opy_, bstack1ll11l11ll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1lll1l11_opy_)
        bstack1l11l11ll1_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᔪ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᔫ"), True, None, None, None, None, test_name=bstack1lll1l11_opy_)
    def bstack1l1111lll1l_opy_(self):
        os.environ[bstack1lll1l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟ࠧᔬ")] = str(self.bstack1l1111llll1_opy_.success)
        os.environ[bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࡠࡅࡄࡔ࡙࡛ࡒࡆࡡࡐࡓࡉࡋࠧᔭ")] = str(self.bstack1l1111llll1_opy_.percy_capture_mode)
        self.percy.bstack1l1111l1lll_opy_(self.bstack1l1111llll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1111lll11_opy_(self.bstack1l1111llll1_opy_.percy_build_id)