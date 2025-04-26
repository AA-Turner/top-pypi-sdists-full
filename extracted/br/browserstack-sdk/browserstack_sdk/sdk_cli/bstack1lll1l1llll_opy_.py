# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11lll1l_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
    bstack11111111ll_opy_,
)
from bstack_utils.helper import  bstack11l11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1111ll_opy_, bstack1lll1lllll1_opy_, bstack1lll1l1l11l_opy_, bstack1ll1lllllll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111l11lll_opy_ import bstack1l1l1111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11l1_opy_ import bstack1lll1l111ll_opy_
from bstack_utils.percy import bstack1l1l111lll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll11lllll_opy_(bstack1llll111111_opy_):
    def __init__(self, bstack1l1ll1ll111_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll1ll111_opy_ = bstack1l1ll1ll111_opy_
        self.percy = bstack1l1l111lll_opy_()
        self.bstack11111111l_opy_ = bstack1l1l1111_opy_()
        self.bstack1l1ll1lll11_opy_()
        bstack1lll1lll1l1_opy_.bstack1ll1ll11l1l_opy_((bstack111111lll1_opy_.bstack1111l11ll1_opy_, bstack111111l1l1_opy_.PRE), self.bstack1l1ll1l1111_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll11lll_opy_(self, instance: bstack11111111ll_opy_, driver: object):
        bstack1ll1111ll1l_opy_ = TestFramework.bstack11111l1lll_opy_(instance.context)
        for t in bstack1ll1111ll1l_opy_:
            bstack1l1lll11ll1_opy_ = TestFramework.bstack1111111111_opy_(t, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11ll1_opy_) or instance == driver:
                return t
    def bstack1l1ll1l1111_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll1lll1l1_opy_.bstack1ll1l1ll1l1_opy_(method_name):
                return
            platform_index = f.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1ll1l111lll_opy_, 0)
            bstack1ll111ll1ll_opy_ = self.bstack1l1lll11lll_opy_(instance, driver)
            bstack1l1ll1l11l1_opy_ = TestFramework.bstack1111111111_opy_(bstack1ll111ll1ll_opy_, TestFramework.bstack1l1ll1l1ll1_opy_, None)
            if not bstack1l1ll1l11l1_opy_:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢሯ"))
                return
            driver_command = f.bstack1ll1l111111_opy_(*args)
            for command in bstack1lll1llll1_opy_:
                if command == driver_command:
                    self.bstack11l11l1lll_opy_(driver, platform_index)
            bstack1l11l11l11_opy_ = self.percy.bstack1lll11l1_opy_()
            if driver_command in bstack1l11llll1l_opy_[bstack1l11l11l11_opy_]:
                self.bstack11111111l_opy_.bstack11llll1l_opy_(bstack1l1ll1l11l1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l11lll_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤሰ"), e)
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
        bstack1l1lll11ll1_opy_ = f.bstack1111111111_opy_(instance, bstack1lll1l111ll_opy_.bstack1l1llllll1l_opy_, [])
        if not bstack1l1lll11ll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦሱ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠥࠦሲ"))
            return
        if len(bstack1l1lll11ll1_opy_) > 1:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨሳ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨሴ"))
        bstack1l1ll1l11ll_opy_, bstack1l1ll1l1l1l_opy_ = bstack1l1lll11ll1_opy_[0]
        driver = bstack1l1ll1l11ll_opy_()
        if not driver:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢስ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠢࠣሶ"))
            return
        bstack1l1ll1ll1l1_opy_ = {
            TestFramework.bstack1ll1ll111l1_opy_: bstack1l11lll_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦሷ"),
            TestFramework.bstack1ll1ll11lll_opy_: bstack1l11lll_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧሸ"),
            TestFramework.bstack1l1ll1l1ll1_opy_: bstack1l11lll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧሹ")
        }
        bstack1l1ll1ll1ll_opy_ = { key: f.bstack1111111111_opy_(instance, key) for key in bstack1l1ll1ll1l1_opy_ }
        bstack1l1ll1l1l11_opy_ = [key for key, value in bstack1l1ll1ll1ll_opy_.items() if not value]
        if bstack1l1ll1l1l11_opy_:
            for key in bstack1l1ll1l1l11_opy_:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢሺ") + str(key) + bstack1l11lll_opy_ (u"ࠧࠨሻ"))
            return
        platform_index = f.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1ll1l111lll_opy_, 0)
        if self.bstack1l1ll1ll111_opy_.percy_capture_mode == bstack1l11lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣሼ"):
            bstack1l111l111l_opy_ = bstack1l1ll1ll1ll_opy_.get(TestFramework.bstack1l1ll1l1ll1_opy_) + bstack1l11lll_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥሽ")
            bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack1l1ll1l111l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l111l111l_opy_,
                bstack11l11l1l1_opy_=bstack1l1ll1ll1ll_opy_[TestFramework.bstack1ll1ll111l1_opy_],
                bstack1l1ll11l11_opy_=bstack1l1ll1ll1ll_opy_[TestFramework.bstack1ll1ll11lll_opy_],
                bstack1ll11l1l11_opy_=platform_index
            )
            bstack1ll1llll111_opy_.end(EVENTS.bstack1l1ll1l111l_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሾ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሿ"), True, None, None, None, None, test_name=bstack1l111l111l_opy_)
    def bstack11l11l1lll_opy_(self, driver, platform_index):
        if self.bstack11111111l_opy_.bstack11111ll11_opy_() is True or self.bstack11111111l_opy_.capturing() is True:
            return
        self.bstack11111111l_opy_.bstack1l11lll1ll_opy_()
        while not self.bstack11111111l_opy_.bstack11111ll11_opy_():
            bstack1l1ll1l11l1_opy_ = self.bstack11111111l_opy_.bstack11l11l11ll_opy_()
            self.bstack111lll1l_opy_(driver, bstack1l1ll1l11l1_opy_, platform_index)
        self.bstack11111111l_opy_.bstack1ll11lll1l_opy_()
    def bstack111lll1l_opy_(self, driver, bstack1l1l11lll1_opy_, platform_index, test=None):
        from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
        bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack1l11ll1l1l_opy_.value)
        if test != None:
            bstack11l11l1l1_opy_ = getattr(test, bstack1l11lll_opy_ (u"ࠪࡲࡦࡳࡥࠨቀ"), None)
            bstack1l1ll11l11_opy_ = getattr(test, bstack1l11lll_opy_ (u"ࠫࡺࡻࡩࡥࠩቁ"), None)
            PercySDK.screenshot(driver, bstack1l1l11lll1_opy_, bstack11l11l1l1_opy_=bstack11l11l1l1_opy_, bstack1l1ll11l11_opy_=bstack1l1ll11l11_opy_, bstack1ll11l1l11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1l11lll1_opy_)
        bstack1ll1llll111_opy_.end(EVENTS.bstack1l11ll1l1l_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧቂ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦቃ"), True, None, None, None, None, test_name=bstack1l1l11lll1_opy_)
    def bstack1l1ll1lll11_opy_(self):
        os.environ[bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬቄ")] = str(self.bstack1l1ll1ll111_opy_.success)
        os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬቅ")] = str(self.bstack1l1ll1ll111_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1l1lll_opy_(self.bstack1l1ll1ll111_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll1ll11l_opy_(self.bstack1l1ll1ll111_opy_.percy_build_id)