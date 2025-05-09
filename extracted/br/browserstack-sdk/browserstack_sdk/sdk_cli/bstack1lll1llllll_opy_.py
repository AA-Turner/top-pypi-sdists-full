# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack11111l1l1l_opy_ import (
    bstack1lllllll1l1_opy_,
    bstack1llllllll1l_opy_,
    bstack111111l1ll_opy_,
)
from bstack_utils.helper import  bstack1llll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11111_opy_ import bstack1lll1ll1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll111ll11_opy_, bstack1lll1ll1ll1_opy_, bstack1lll1l111l1_opy_, bstack1lll1111ll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l111l1l_opy_ import bstack1lll1111ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lll1ll_opy_ import bstack1llll111l1l_opy_
from bstack_utils.percy import bstack1lll1l11ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11l11ll_opy_(bstack1lll1l1lll1_opy_):
    def __init__(self, bstack1l1ll1l1111_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll1l1111_opy_ = bstack1l1ll1l1111_opy_
        self.percy = bstack1lll1l11ll_opy_()
        self.bstack11l11l11l_opy_ = bstack1lll1111ll_opy_()
        self.bstack1l1ll1ll11l_opy_()
        bstack1lll1ll1lll_opy_.bstack1ll1ll1ll1l_opy_((bstack1lllllll1l1_opy_.bstack11111lll1l_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1l1ll1ll111_opy_)
        TestFramework.bstack1ll1ll1ll1l_opy_((bstack1lll111ll11_opy_.TEST, bstack1lll1l111l1_opy_.POST), self.bstack1ll1l11l1l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llllll11_opy_(self, instance: bstack111111l1ll_opy_, driver: object):
        bstack1ll1111l1l1_opy_ = TestFramework.bstack1111l11l11_opy_(instance.context)
        for t in bstack1ll1111l1l1_opy_:
            bstack1ll1111ll1l_opy_ = TestFramework.bstack111111l1l1_opy_(t, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])
            if any(instance is d[1] for d in bstack1ll1111ll1l_opy_) or instance == driver:
                return t
    def bstack1l1ll1ll111_opy_(
        self,
        f: bstack1lll1ll1lll_opy_,
        driver: object,
        exec: Tuple[bstack111111l1ll_opy_, str],
        bstack1111111ll1_opy_: Tuple[bstack1lllllll1l1_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1ll1lll_opy_.bstack1ll1l1l1ll1_opy_(method_name):
                return
            platform_index = f.bstack111111l1l1_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l1l111l_opy_, 0)
            bstack1l1llllll1l_opy_ = self.bstack1l1llllll11_opy_(instance, driver)
            bstack1l1ll1l11l1_opy_ = TestFramework.bstack111111l1l1_opy_(bstack1l1llllll1l_opy_, TestFramework.bstack1l1ll1l11ll_opy_, None)
            if not bstack1l1ll1l11l1_opy_:
                self.logger.debug(bstack11lll_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢሯ"))
                return
            driver_command = f.bstack1ll1l1l1l11_opy_(*args)
            for command in bstack1llllll1ll_opy_:
                if command == driver_command:
                    self.bstack11llll1l_opy_(driver, platform_index)
            bstack11l1l111l_opy_ = self.percy.bstack1ll1l11ll1_opy_()
            if driver_command in bstack11lll1l11_opy_[bstack11l1l111l_opy_]:
                self.bstack11l11l11l_opy_.bstack1l1l111111_opy_(bstack1l1ll1l11l1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11lll_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤሰ"), e)
    def bstack1ll1l11l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1ll1ll1_opy_,
        bstack1111111ll1_opy_: Tuple[bstack1lll111ll11_opy_, bstack1lll1l111l1_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
        bstack1ll1111ll1l_opy_ = f.bstack111111l1l1_opy_(instance, bstack1llll111l1l_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1ll1111ll1l_opy_:
            self.logger.debug(bstack11lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦሱ") + str(kwargs) + bstack11lll_opy_ (u"ࠥࠦሲ"))
            return
        if len(bstack1ll1111ll1l_opy_) > 1:
            self.logger.debug(bstack11lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨሳ") + str(kwargs) + bstack11lll_opy_ (u"ࠧࠨሴ"))
        bstack1l1ll1ll1l1_opy_, bstack1l1ll1l1l11_opy_ = bstack1ll1111ll1l_opy_[0]
        driver = bstack1l1ll1ll1l1_opy_()
        if not driver:
            self.logger.debug(bstack11lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢስ") + str(kwargs) + bstack11lll_opy_ (u"ࠢࠣሶ"))
            return
        bstack1l1ll1l1ll1_opy_ = {
            TestFramework.bstack1ll1ll1l1ll_opy_: bstack11lll_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦሷ"),
            TestFramework.bstack1ll1l1ll1ll_opy_: bstack11lll_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧሸ"),
            TestFramework.bstack1l1ll1l11ll_opy_: bstack11lll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧሹ")
        }
        bstack1l1ll1l1l1l_opy_ = { key: f.bstack111111l1l1_opy_(instance, key) for key in bstack1l1ll1l1ll1_opy_ }
        bstack1l1ll11lll1_opy_ = [key for key, value in bstack1l1ll1l1l1l_opy_.items() if not value]
        if bstack1l1ll11lll1_opy_:
            for key in bstack1l1ll11lll1_opy_:
                self.logger.debug(bstack11lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢሺ") + str(key) + bstack11lll_opy_ (u"ࠧࠨሻ"))
            return
        platform_index = f.bstack111111l1l1_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l1l111l_opy_, 0)
        if self.bstack1l1ll1l1111_opy_.percy_capture_mode == bstack11lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣሼ"):
            bstack1lll1111_opy_ = bstack1l1ll1l1l1l_opy_.get(TestFramework.bstack1l1ll1l11ll_opy_) + bstack11lll_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥሽ")
            bstack1ll11lll1l1_opy_ = bstack1ll1llllll1_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack1l1ll1l111l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1lll1111_opy_,
                bstack1ll1l1llll_opy_=bstack1l1ll1l1l1l_opy_[TestFramework.bstack1ll1ll1l1ll_opy_],
                bstack1ll11ll11_opy_=bstack1l1ll1l1l1l_opy_[TestFramework.bstack1ll1l1ll1ll_opy_],
                bstack1ll11111l1_opy_=platform_index
            )
            bstack1ll1llllll1_opy_.end(EVENTS.bstack1l1ll1l111l_opy_.value, bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሾ"), bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሿ"), True, None, None, None, None, test_name=bstack1lll1111_opy_)
    def bstack11llll1l_opy_(self, driver, platform_index):
        if self.bstack11l11l11l_opy_.bstack11l11l1l1_opy_() is True or self.bstack11l11l11l_opy_.capturing() is True:
            return
        self.bstack11l11l11l_opy_.bstack1ll1llll1l_opy_()
        while not self.bstack11l11l11l_opy_.bstack11l11l1l1_opy_():
            bstack1l1ll1l11l1_opy_ = self.bstack11l11l11l_opy_.bstack1l11l1ll_opy_()
            self.bstack1l11ll111_opy_(driver, bstack1l1ll1l11l1_opy_, platform_index)
        self.bstack11l11l11l_opy_.bstack11l11lll_opy_()
    def bstack1l11ll111_opy_(self, driver, bstack11l1ll1111_opy_, platform_index, test=None):
        from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
        bstack1ll11lll1l1_opy_ = bstack1ll1llllll1_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack11ll1l1l_opy_.value)
        if test != None:
            bstack1ll1l1llll_opy_ = getattr(test, bstack11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨቀ"), None)
            bstack1ll11ll11_opy_ = getattr(test, bstack11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩቁ"), None)
            PercySDK.screenshot(driver, bstack11l1ll1111_opy_, bstack1ll1l1llll_opy_=bstack1ll1l1llll_opy_, bstack1ll11ll11_opy_=bstack1ll11ll11_opy_, bstack1ll11111l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1ll1111_opy_)
        bstack1ll1llllll1_opy_.end(EVENTS.bstack11ll1l1l_opy_.value, bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧቂ"), bstack1ll11lll1l1_opy_+bstack11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦቃ"), True, None, None, None, None, test_name=bstack11l1ll1111_opy_)
    def bstack1l1ll1ll11l_opy_(self):
        os.environ[bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬቄ")] = str(self.bstack1l1ll1l1111_opy_.success)
        os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬቅ")] = str(self.bstack1l1ll1l1111_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1l1lll_opy_(self.bstack1l1ll1l1111_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll11llll_opy_(self.bstack1l1ll1l1111_opy_.percy_build_id)