# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1l1ll_opy_ import bstack1ll1llll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1111111lll_opy_ import (
    bstack1llllllllll_opy_,
    bstack11111lll1l_opy_,
    bstack11111ll111_opy_,
)
from bstack_utils.helper import  bstack1l111l11_opy_
from browserstack_sdk.sdk_cli.bstack1lllll11111_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1ll1l1_opy_, bstack1llllll11ll_opy_, bstack1llll1lll1l_opy_, bstack1lll1l111l1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l111llll_opy_ import bstack11ll11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1ll1lllll11_opy_
from bstack_utils.percy import bstack11ll1lllll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1l1ll1l_opy_(bstack1ll1llll1ll_opy_):
    def __init__(self, bstack1l1ll1ll11l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll1ll11l_opy_ = bstack1l1ll1ll11l_opy_
        self.percy = bstack11ll1lllll_opy_()
        self.bstack11l11lll1l_opy_ = bstack11ll11ll1_opy_()
        self.bstack1l1ll1ll1ll_opy_()
        bstack1lll11lllll_opy_.bstack1ll1ll1l111_opy_((bstack1llllllllll_opy_.bstack1111l11111_opy_, bstack11111lll1l_opy_.PRE), self.bstack1l1ll1l11l1_opy_)
        TestFramework.bstack1ll1ll1l111_opy_((bstack1llll1ll1l1_opy_.TEST, bstack1llll1lll1l_opy_.POST), self.bstack1ll1l1l1lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lllll11l_opy_(self, instance: bstack11111ll111_opy_, driver: object):
        bstack1ll111ll1l1_opy_ = TestFramework.bstack111111111l_opy_(instance.context)
        for t in bstack1ll111ll1l1_opy_:
            bstack1l1lll11lll_opy_ = TestFramework.bstack11111l11l1_opy_(t, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11lll_opy_) or instance == driver:
                return t
    def bstack1l1ll1l11l1_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack11111ll111_opy_, str],
        bstack1lllllll1l1_opy_: Tuple[bstack1llllllllll_opy_, bstack11111lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll11lllll_opy_.bstack1ll1ll11111_opy_(method_name):
                return
            platform_index = f.bstack11111l11l1_opy_(instance, bstack1lll11lllll_opy_.bstack1ll1l1lllll_opy_, 0)
            bstack1l1llllll11_opy_ = self.bstack1l1lllll11l_opy_(instance, driver)
            bstack1l1ll1l1111_opy_ = TestFramework.bstack11111l11l1_opy_(bstack1l1llllll11_opy_, TestFramework.bstack1l1ll1l11ll_opy_, None)
            if not bstack1l1ll1l1111_opy_:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢሯ"))
                return
            driver_command = f.bstack1ll1l111lll_opy_(*args)
            for command in bstack11l11l1l1_opy_:
                if command == driver_command:
                    self.bstack1l1l1l1l1_opy_(driver, platform_index)
            bstack1ll1lllll_opy_ = self.percy.bstack1llll1ll1l_opy_()
            if driver_command in bstack111l1lll_opy_[bstack1ll1lllll_opy_]:
                self.bstack11l11lll1l_opy_.bstack1ll111l11_opy_(bstack1l1ll1l1111_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1lll_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤሰ"), e)
    def bstack1ll1l1l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1llllll11ll_opy_,
        bstack1lllllll1l1_opy_: Tuple[bstack1llll1ll1l1_opy_, bstack1llll1lll1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
        bstack1l1lll11lll_opy_ = f.bstack11111l11l1_opy_(instance, bstack1ll1lllll11_opy_.bstack1ll111lllll_opy_, [])
        if not bstack1l1lll11lll_opy_:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦሱ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠥࠦሲ"))
            return
        if len(bstack1l1lll11lll_opy_) > 1:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨሳ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠧࠨሴ"))
        bstack1l1ll1ll111_opy_, bstack1l1ll1lll11_opy_ = bstack1l1lll11lll_opy_[0]
        driver = bstack1l1ll1ll111_opy_()
        if not driver:
            self.logger.debug(bstack1l1lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢስ") + str(kwargs) + bstack1l1lll_opy_ (u"ࠢࠣሶ"))
            return
        bstack1l1ll1l1l1l_opy_ = {
            TestFramework.bstack1ll1l11ll11_opy_: bstack1l1lll_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦሷ"),
            TestFramework.bstack1ll1l1l11l1_opy_: bstack1l1lll_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧሸ"),
            TestFramework.bstack1l1ll1l11ll_opy_: bstack1l1lll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧሹ")
        }
        bstack1l1ll1l1l11_opy_ = { key: f.bstack11111l11l1_opy_(instance, key) for key in bstack1l1ll1l1l1l_opy_ }
        bstack1l1ll1l1lll_opy_ = [key for key, value in bstack1l1ll1l1l11_opy_.items() if not value]
        if bstack1l1ll1l1lll_opy_:
            for key in bstack1l1ll1l1lll_opy_:
                self.logger.debug(bstack1l1lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢሺ") + str(key) + bstack1l1lll_opy_ (u"ࠧࠨሻ"))
            return
        platform_index = f.bstack11111l11l1_opy_(instance, bstack1lll11lllll_opy_.bstack1ll1l1lllll_opy_, 0)
        if self.bstack1l1ll1ll11l_opy_.percy_capture_mode == bstack1l1lll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣሼ"):
            bstack1ll1ll111l_opy_ = bstack1l1ll1l1l11_opy_.get(TestFramework.bstack1l1ll1l11ll_opy_) + bstack1l1lll_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥሽ")
            bstack1ll1l11lll1_opy_ = bstack1lll1lll111_opy_.bstack1ll1l1ll1l1_opy_(EVENTS.bstack1l1ll1l111l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll1ll111l_opy_,
                bstack1l111lll11_opy_=bstack1l1ll1l1l11_opy_[TestFramework.bstack1ll1l11ll11_opy_],
                bstack1lll1l1l1_opy_=bstack1l1ll1l1l11_opy_[TestFramework.bstack1ll1l1l11l1_opy_],
                bstack1l1lll111_opy_=platform_index
            )
            bstack1lll1lll111_opy_.end(EVENTS.bstack1l1ll1l111l_opy_.value, bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሾ"), bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሿ"), True, None, None, None, None, test_name=bstack1ll1ll111l_opy_)
    def bstack1l1l1l1l1_opy_(self, driver, platform_index):
        if self.bstack11l11lll1l_opy_.bstack1llllll111_opy_() is True or self.bstack11l11lll1l_opy_.capturing() is True:
            return
        self.bstack11l11lll1l_opy_.bstack1ll1111111_opy_()
        while not self.bstack11l11lll1l_opy_.bstack1llllll111_opy_():
            bstack1l1ll1l1111_opy_ = self.bstack11l11lll1l_opy_.bstack1l1l1111ll_opy_()
            self.bstack1l1lll111l_opy_(driver, bstack1l1ll1l1111_opy_, platform_index)
        self.bstack11l11lll1l_opy_.bstack111l111ll_opy_()
    def bstack1l1lll111l_opy_(self, driver, bstack11lll11ll_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
        bstack1ll1l11lll1_opy_ = bstack1lll1lll111_opy_.bstack1ll1l1ll1l1_opy_(EVENTS.bstack1l1l1l1ll1_opy_.value)
        if test != None:
            bstack1l111lll11_opy_ = getattr(test, bstack1l1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨቀ"), None)
            bstack1lll1l1l1_opy_ = getattr(test, bstack1l1lll_opy_ (u"ࠫࡺࡻࡩࡥࠩቁ"), None)
            PercySDK.screenshot(driver, bstack11lll11ll_opy_, bstack1l111lll11_opy_=bstack1l111lll11_opy_, bstack1lll1l1l1_opy_=bstack1lll1l1l1_opy_, bstack1l1lll111_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11lll11ll_opy_)
        bstack1lll1lll111_opy_.end(EVENTS.bstack1l1l1l1ll1_opy_.value, bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧቂ"), bstack1ll1l11lll1_opy_+bstack1l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦቃ"), True, None, None, None, None, test_name=bstack11lll11ll_opy_)
    def bstack1l1ll1ll1ll_opy_(self):
        os.environ[bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬቄ")] = str(self.bstack1l1ll1ll11l_opy_.success)
        os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬቅ")] = str(self.bstack1l1ll1ll11l_opy_.percy_capture_mode)
        self.percy.bstack1l1ll1ll1l1_opy_(self.bstack1l1ll1ll11l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll1l1ll1_opy_(self.bstack1l1ll1ll11l_opy_.percy_build_id)