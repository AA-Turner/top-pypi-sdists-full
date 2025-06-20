# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll1ll_opy_,
)
from bstack_utils.helper import  bstack111ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll11111l_opy_, bstack1llll111l11_opy_, bstack1ll1l1lll11_opy_, bstack1lll11lll11_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1111l111l_opy_ import bstack1l11lll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1l1l1_opy_
from bstack_utils.percy import bstack1l1111ll1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1llll11_opy_(bstack1ll1ll1llll_opy_):
    def __init__(self, bstack1l1l1ll1l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1ll1l1l_opy_ = bstack1l1l1ll1l1l_opy_
        self.percy = bstack1l1111ll1_opy_()
        self.bstack1lll1l1111_opy_ = bstack1l11lll1l1_opy_()
        self.bstack1l1l1ll111l_opy_()
        bstack1llll11l111_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1l1l1ll1ll1_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), self.bstack1ll1l111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1ll11l_opy_(self, instance: bstack1llll1ll1ll_opy_, driver: object):
        bstack1l1lllll11l_opy_ = TestFramework.bstack1llllll111l_opy_(instance.context)
        for t in bstack1l1lllll11l_opy_:
            bstack1l1lll11l1l_opy_ = TestFramework.bstack1lllll1l1ll_opy_(t, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll11l1l_opy_) or instance == driver:
                return t
    def bstack1l1l1ll1ll1_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll11l111_opy_.bstack1ll1l11ll1l_opy_(method_name):
                return
            platform_index = f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_, 0)
            bstack1l1lll1l1l1_opy_ = self.bstack1l1ll1ll11l_opy_(instance, driver)
            bstack1l1l1lll1l1_opy_ = TestFramework.bstack1lllll1l1ll_opy_(bstack1l1lll1l1l1_opy_, TestFramework.bstack1l1l1ll11ll_opy_, None)
            if not bstack1l1l1lll1l1_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡥࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡸࡺࡡࡳࡶࡨࡨࠧታ"))
                return
            driver_command = f.bstack1ll11l1ll1l_opy_(*args)
            for command in bstack1lll1l11ll_opy_:
                if command == driver_command:
                    self.bstack111l1l1ll_opy_(driver, platform_index)
            bstack11l111lll1_opy_ = self.percy.bstack1l1l11l1_opy_()
            if driver_command in bstack1l1ll11l1_opy_[bstack11l111lll1_opy_]:
                self.bstack1lll1l1111_opy_.bstack1l1111l111_opy_(bstack1l1l1lll1l1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡧࡵࡶࡴࡸࠢቴ"), e)
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
        bstack1l1lll11l1l_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1lll1l1l1l1_opy_.bstack1l1ll11ll11_opy_, [])
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤት") + str(kwargs) + bstack11ll11_opy_ (u"ࠣࠤቶ"))
            return
        if len(bstack1l1lll11l1l_opy_) > 1:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቷ") + str(kwargs) + bstack11ll11_opy_ (u"ࠥࠦቸ"))
        bstack1l1l1ll11l1_opy_, bstack1l1l1lll111_opy_ = bstack1l1lll11l1l_opy_[0]
        driver = bstack1l1l1ll11l1_opy_()
        if not driver:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቹ") + str(kwargs) + bstack11ll11_opy_ (u"ࠧࠨቺ"))
            return
        bstack1l1l1ll1l11_opy_ = {
            TestFramework.bstack1ll1l111l1l_opy_: bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤቻ"),
            TestFramework.bstack1ll1l11ll11_opy_: bstack11ll11_opy_ (u"ࠢࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥቼ"),
            TestFramework.bstack1l1l1ll11ll_opy_: bstack11ll11_opy_ (u"ࠣࡶࡨࡷࡹࠦࡲࡦࡴࡸࡲࠥࡴࡡ࡮ࡧࠥች")
        }
        bstack1l1l1lll11l_opy_ = { key: f.bstack1lllll1l1ll_opy_(instance, key) for key in bstack1l1l1ll1l11_opy_ }
        bstack1l1l1ll1111_opy_ = [key for key, value in bstack1l1l1lll11l_opy_.items() if not value]
        if bstack1l1l1ll1111_opy_:
            for key in bstack1l1l1ll1111_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠧቾ") + str(key) + bstack11ll11_opy_ (u"ࠥࠦቿ"))
            return
        platform_index = f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_, 0)
        if self.bstack1l1l1ll1l1l_opy_.percy_capture_mode == bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨኀ"):
            bstack1ll1ll1ll1_opy_ = bstack1l1l1lll11l_opy_.get(TestFramework.bstack1l1l1ll11ll_opy_) + bstack11ll11_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣኁ")
            bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1l1l1l1llll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll1ll1ll1_opy_,
                bstack1l1lll11l1_opy_=bstack1l1l1lll11l_opy_[TestFramework.bstack1ll1l111l1l_opy_],
                bstack1l1111111_opy_=bstack1l1l1lll11l_opy_[TestFramework.bstack1ll1l11ll11_opy_],
                bstack11ll1lll1_opy_=platform_index
            )
            bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1l1l1l1llll_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨኂ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧኃ"), True, None, None, None, None, test_name=bstack1ll1ll1ll1_opy_)
    def bstack111l1l1ll_opy_(self, driver, platform_index):
        if self.bstack1lll1l1111_opy_.bstack11l11l1ll1_opy_() is True or self.bstack1lll1l1111_opy_.capturing() is True:
            return
        self.bstack1lll1l1111_opy_.bstack1ll11lll1l_opy_()
        while not self.bstack1lll1l1111_opy_.bstack11l11l1ll1_opy_():
            bstack1l1l1lll1l1_opy_ = self.bstack1lll1l1111_opy_.bstack1l1111ll_opy_()
            self.bstack11111llll_opy_(driver, bstack1l1l1lll1l1_opy_, platform_index)
        self.bstack1lll1l1111_opy_.bstack11l11111_opy_()
    def bstack11111llll_opy_(self, driver, bstack11l1111l_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
        bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1lll1111_opy_.value)
        if test != None:
            bstack1l1lll11l1_opy_ = getattr(test, bstack11ll11_opy_ (u"ࠨࡰࡤࡱࡪ࠭ኄ"), None)
            bstack1l1111111_opy_ = getattr(test, bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧኅ"), None)
            PercySDK.screenshot(driver, bstack11l1111l_opy_, bstack1l1lll11l1_opy_=bstack1l1lll11l1_opy_, bstack1l1111111_opy_=bstack1l1111111_opy_, bstack11ll1lll1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1111l_opy_)
        bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1lll1111_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥኆ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤኇ"), True, None, None, None, None, test_name=bstack11l1111l_opy_)
    def bstack1l1l1ll111l_opy_(self):
        os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪኈ")] = str(self.bstack1l1l1ll1l1l_opy_.success)
        os.environ[bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪ኉")] = str(self.bstack1l1l1ll1l1l_opy_.percy_capture_mode)
        self.percy.bstack1l1l1ll1lll_opy_(self.bstack1l1l1ll1l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1lll1ll_opy_(self.bstack1l1l1ll1l1l_opy_.percy_build_id)