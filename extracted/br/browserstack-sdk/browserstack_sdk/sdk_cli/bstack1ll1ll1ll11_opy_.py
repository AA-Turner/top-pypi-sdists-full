# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1llllll111l_opy_,
)
from bstack_utils.helper import  bstack1ll11l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11lllll_opy_, bstack1lll1111l1l_opy_, bstack1lllll1111l_opy_, bstack1lll11111l1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1ll1lll1l_opy_ import bstack1llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1111_opy_
from bstack_utils.percy import bstack11l1ll1l11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1lll1ll111l_opy_(bstack1lll1l11ll1_opy_):
    def __init__(self, bstack1l1ll11111l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1ll11111l_opy_ = bstack1l1ll11111l_opy_
        self.percy = bstack11l1ll1l11_opy_()
        self.bstack1l1ll1ll1_opy_ = bstack1llll11l_opy_()
        self.bstack1l1l1llllll_opy_()
        bstack1llll111lll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1l1ll111l1l_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), self.bstack1ll11ll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll111ll_opy_(self, instance: bstack1llllll111l_opy_, driver: object):
        bstack1l1ll1l111l_opy_ = TestFramework.bstack1llllll1l11_opy_(instance.context)
        for t in bstack1l1ll1l111l_opy_:
            bstack1ll1111l11l_opy_ = TestFramework.bstack1llllll1l1l_opy_(t, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
            if any(instance is d[1] for d in bstack1ll1111l11l_opy_) or instance == driver:
                return t
    def bstack1l1ll111l1l_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll111lll_opy_.bstack1ll11l1l1l1_opy_(method_name):
                return
            platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_, 0)
            bstack1l1lllll1l1_opy_ = self.bstack1l1lll111ll_opy_(instance, driver)
            bstack1l1ll11l11l_opy_ = TestFramework.bstack1llllll1l1l_opy_(bstack1l1lllll1l1_opy_, TestFramework.bstack1l1ll111ll1_opy_, None)
            if not bstack1l1ll11l11l_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡥࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡸࡺࡡࡳࡶࡨࡨࠧብ"))
                return
            driver_command = f.bstack1ll1l111lll_opy_(*args)
            for command in bstack1llll111l_opy_:
                if command == driver_command:
                    self.bstack1l1llll11_opy_(driver, platform_index)
            bstack1l11llll_opy_ = self.percy.bstack1ll111ll11_opy_()
            if driver_command in bstack1l11111lll_opy_[bstack1l11llll_opy_]:
                self.bstack1l1ll1ll1_opy_.bstack1l1lllll1_opy_(bstack1l1ll11l11l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡧࡵࡶࡴࡸࠢቦ"), e)
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
        bstack1ll1111l11l_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1111_opy_.bstack1ll1111lll1_opy_, [])
        if not bstack1ll1111l11l_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤቧ") + str(kwargs) + bstack111lll_opy_ (u"ࠣࠤቨ"))
            return
        if len(bstack1ll1111l11l_opy_) > 1:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቩ") + str(kwargs) + bstack111lll_opy_ (u"ࠥࠦቪ"))
        bstack1l1ll111111_opy_, bstack1l1l1lllll1_opy_ = bstack1ll1111l11l_opy_[0]
        driver = bstack1l1ll111111_opy_()
        if not driver:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቫ") + str(kwargs) + bstack111lll_opy_ (u"ࠧࠨቬ"))
            return
        bstack1l1ll1111ll_opy_ = {
            TestFramework.bstack1ll11l1l1ll_opy_: bstack111lll_opy_ (u"ࠨࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤቭ"),
            TestFramework.bstack1ll11lll11l_opy_: bstack111lll_opy_ (u"ࠢࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥቮ"),
            TestFramework.bstack1l1ll111ll1_opy_: bstack111lll_opy_ (u"ࠣࡶࡨࡷࡹࠦࡲࡦࡴࡸࡲࠥࡴࡡ࡮ࡧࠥቯ")
        }
        bstack1l1ll11l1l1_opy_ = { key: f.bstack1llllll1l1l_opy_(instance, key) for key in bstack1l1ll1111ll_opy_ }
        bstack1l1ll1111l1_opy_ = [key for key, value in bstack1l1ll11l1l1_opy_.items() if not value]
        if bstack1l1ll1111l1_opy_:
            for key in bstack1l1ll1111l1_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠧተ") + str(key) + bstack111lll_opy_ (u"ࠥࠦቱ"))
            return
        platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_, 0)
        if self.bstack1l1ll11111l_opy_.percy_capture_mode == bstack111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨቲ"):
            bstack1l1ll111l1_opy_ = bstack1l1ll11l1l1_opy_.get(TestFramework.bstack1l1ll111ll1_opy_) + bstack111lll_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣታ")
            bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1l1ll111lll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1ll111l1_opy_,
                bstack1lllllll11_opy_=bstack1l1ll11l1l1_opy_[TestFramework.bstack1ll11l1l1ll_opy_],
                bstack111111ll_opy_=bstack1l1ll11l1l1_opy_[TestFramework.bstack1ll11lll11l_opy_],
                bstack1lll1l1lll_opy_=platform_index
            )
            bstack1llll1l1l11_opy_.end(EVENTS.bstack1l1ll111lll_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨቴ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧት"), True, None, None, None, None, test_name=bstack1l1ll111l1_opy_)
    def bstack1l1llll11_opy_(self, driver, platform_index):
        if self.bstack1l1ll1ll1_opy_.bstack1l11l1ll11_opy_() is True or self.bstack1l1ll1ll1_opy_.capturing() is True:
            return
        self.bstack1l1ll1ll1_opy_.bstack1l1l1111l_opy_()
        while not self.bstack1l1ll1ll1_opy_.bstack1l11l1ll11_opy_():
            bstack1l1ll11l11l_opy_ = self.bstack1l1ll1ll1_opy_.bstack11ll111lll_opy_()
            self.bstack1l1111l11l_opy_(driver, bstack1l1ll11l11l_opy_, platform_index)
        self.bstack1l1ll1ll1_opy_.bstack11lll1l1_opy_()
    def bstack1l1111l11l_opy_(self, driver, bstack11l1lll1l_opy_, platform_index, test=None):
        from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
        bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1ll111l11l_opy_.value)
        if test != None:
            bstack1lllllll11_opy_ = getattr(test, bstack111lll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ቶ"), None)
            bstack111111ll_opy_ = getattr(test, bstack111lll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧቷ"), None)
            PercySDK.screenshot(driver, bstack11l1lll1l_opy_, bstack1lllllll11_opy_=bstack1lllllll11_opy_, bstack111111ll_opy_=bstack111111ll_opy_, bstack1lll1l1lll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1lll1l_opy_)
        bstack1llll1l1l11_opy_.end(EVENTS.bstack1ll111l11l_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥቸ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤቹ"), True, None, None, None, None, test_name=bstack11l1lll1l_opy_)
    def bstack1l1l1llllll_opy_(self):
        os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪቺ")] = str(self.bstack1l1ll11111l_opy_.success)
        os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪቻ")] = str(self.bstack1l1ll11111l_opy_.percy_capture_mode)
        self.percy.bstack1l1ll11l111_opy_(self.bstack1l1ll11111l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1ll111l11_opy_(self.bstack1l1ll11111l_opy_.percy_build_id)