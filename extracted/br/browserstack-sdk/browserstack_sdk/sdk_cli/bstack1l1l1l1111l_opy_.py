# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack1l1ll111lll_opy_,
)
from bstack_utils.helper import  bstack1ll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l1l1ll11l1_opy_, TestHookState, bstack11l1l1l1ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11l111l1_opy_ import bstack1111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l111l1l_opy_ import bstack1l1l1111ll1_opy_
from bstack_utils.percy import bstack1l1lllll1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l1l1ll1l_opy_(bstack1l11l1l11ll_opy_):
    def __init__(self, bstack11l1lllll1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11l1lllll1l_opy_ = bstack11l1lllll1l_opy_
        self.percy = bstack1l1lllll1_opy_()
        self.bstack1llll1llll_opy_ = bstack1111l1lll_opy_()
        self.bstack11l1lllll11_opy_()
        bstack1l11lll111l_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack11ll1111111_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l111l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1l1l1l1_opy_(self, instance: bstack1l1ll111lll_opy_, driver: object):
        bstack11lll11l11l_opy_ = TestFramework.bstack1l1ll11llll_opy_(instance.context)
        for t in bstack11lll11l11l_opy_:
            bstack11ll1111ll1_opy_ = TestFramework.bstack1l1llll1111_opy_(t, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
            if any(instance is d[1] for d in bstack11ll1111ll1_opy_) or instance == driver:
                return t
    def bstack11ll1111111_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l11lll111l_opy_.bstack1l1111llll1_opy_(method_name):
                return
            platform_index = f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_, 0)
            bstack1llllllll_opy_ = self.bstack11ll1l1l1l1_opy_(instance, driver)
            bstack11l1llll1ll_opy_ = TestFramework.bstack1l1llll1111_opy_(bstack1llllllll_opy_, TestFramework.bstack11l1llll111_opy_, None)
            if not bstack11l1llll1ll_opy_:
                self.logger.debug(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨ᝵"))
                return
            driver_command = f.bstack1l111l1l1l1_opy_(*args)
            for command in bstack11lll1ll11_opy_:
                if command == driver_command:
                    self.bstack11l11llll_opy_(driver, platform_index)
            bstack1lll111l1l_opy_ = self.percy.bstack111l1lll1_opy_()
            if driver_command in bstack1lll1lll_opy_[bstack1lll111l1l_opy_]:
                self.bstack1llll1llll_opy_.bstack1l111lllll_opy_(bstack11l1llll1ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣ᝶"), e)
    def bstack1l111l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
        bstack11ll1111ll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1l1l1111ll1_opy_.bstack11ll1lll1ll_opy_, [])
        if not bstack11ll1111ll1_opy_:
            self.logger.debug(bstack111ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᝷") + str(kwargs) + bstack111ll_opy_ (u"ࠤࠥ᝸"))
            return
        if len(bstack11ll1111ll1_opy_) > 1:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᝹") + str(kwargs) + bstack111ll_opy_ (u"ࠦࠧ᝺"))
        bstack11ll111111l_opy_, bstack11l1llll11l_opy_ = bstack11ll1111ll1_opy_[0]
        driver = bstack11ll111111l_opy_()
        if not driver:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨ᝻") + str(kwargs) + bstack111ll_opy_ (u"ࠨࠢ᝼"))
            return
        bstack11ll11111ll_opy_ = {
            TestFramework.bstack1l1111lll11_opy_: bstack111ll_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥ᝽"),
            TestFramework.bstack1l11111111l_opy_: bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦ᝾"),
            TestFramework.bstack11l1llll111_opy_: bstack111ll_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦ᝿")
        }
        bstack11l1llll1l1_opy_ = { key: f.bstack1l1llll1111_opy_(instance, key) for key in bstack11ll11111ll_opy_ }
        bstack11ll1111l11_opy_ = [key for key, value in bstack11l1llll1l1_opy_.items() if not value]
        if bstack11ll1111l11_opy_:
            for key in bstack11ll1111l11_opy_:
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨក") + str(key) + bstack111ll_opy_ (u"ࠦࠧខ"))
            return
        platform_index = f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_, 0)
        if self.bstack11l1lllll1l_opy_.percy_capture_mode == bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢគ"):
            bstack111l11ll1l_opy_ = bstack11l1llll1l1_opy_.get(TestFramework.bstack11l1llll111_opy_) + bstack111ll_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤឃ")
            bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack11l1llllll1_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack111l11ll1l_opy_,
                bstack11111llll1_opy_=bstack11l1llll1l1_opy_[TestFramework.bstack1l1111lll11_opy_],
                bstack11l11111ll_opy_=bstack11l1llll1l1_opy_[TestFramework.bstack1l11111111l_opy_],
                bstack1l111lll1_opy_=platform_index
            )
            bstack111l1l1l_opy_.end(EVENTS.bstack11l1llllll1_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢង"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨច"), True, None, None, None, None, test_name=bstack111l11ll1l_opy_)
    def bstack11l11llll_opy_(self, driver, platform_index):
        if self.bstack1llll1llll_opy_.bstack11l1l11l11_opy_() is True or self.bstack1llll1llll_opy_.capturing() is True:
            return
        self.bstack1llll1llll_opy_.bstack1l1l11llll_opy_()
        while not self.bstack1llll1llll_opy_.bstack11l1l11l11_opy_():
            bstack11l1llll1ll_opy_ = self.bstack1llll1llll_opy_.bstack11l111l11_opy_()
            self.bstack11l111l1l1_opy_(driver, bstack11l1llll1ll_opy_, platform_index)
        self.bstack1llll1llll_opy_.bstack1l1l11ll_opy_()
    def bstack11l111l1l1_opy_(self, driver, bstack11l1llll11_opy_, platform_index, test=None):
        from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
        bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack11lll11l1l_opy_.value)
        if test != None:
            bstack11111llll1_opy_ = getattr(test, bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧឆ"), None)
            bstack11l11111ll_opy_ = getattr(test, bstack111ll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨជ"), None)
            PercySDK.screenshot(driver, bstack11l1llll11_opy_, bstack11111llll1_opy_=bstack11111llll1_opy_, bstack11l11111ll_opy_=bstack11l11111ll_opy_, bstack1l111lll1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1llll11_opy_)
        bstack111l1l1l_opy_.end(EVENTS.bstack11lll11l1l_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦឈ"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥញ"), True, None, None, None, None, test_name=bstack11l1llll11_opy_)
    def bstack11l1lllll11_opy_(self):
        os.environ[bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫដ")] = str(self.bstack11l1lllll1l_opy_.success)
        os.environ[bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫឋ")] = str(self.bstack11l1lllll1l_opy_.percy_capture_mode)
        self.percy.bstack11ll11111l1_opy_(self.bstack11l1lllll1l_opy_.is_percy_auto_enabled)
        self.percy.bstack11l1lllllll_opy_(self.bstack11l1lllll1l_opy_.percy_build_id)