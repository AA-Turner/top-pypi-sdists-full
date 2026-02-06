# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1l1l11l_opy_,
)
from bstack_utils.helper import  bstack1l1ll1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11111l1l_opy_, bstack1ll11111ll1_opy_, bstack1ll11l1l11l_opy_, bstack1ll1l11ll11_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111l1ll1ll_opy_ import bstack11l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l11l_opy_ import bstack1ll11l1llll_opy_
from bstack_utils.percy import bstack111llll1l1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll111111ll_opy_(bstack1lll1l1l1l1_opy_):
    def __init__(self, bstack1l11l1l1l1l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l11l1l1l1l_opy_ = bstack1l11l1l1l1l_opy_
        self.percy = bstack111llll1l1_opy_()
        self.bstack1lll1llll1_opy_ = bstack11l11l11_opy_()
        self.bstack1l11l11ll1l_opy_()
        bstack1lll11lllll_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l11l1l1l11_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), self.bstack1l1l1l1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lllllll_opy_(self, instance: bstack1lll1l1l11l_opy_, driver: object):
        bstack1l11ll1l1l1_opy_ = TestFramework.bstack1lll11l1111_opy_(instance.context)
        for t in bstack1l11ll1l1l1_opy_:
            bstack1l1l11ll111_opy_ = TestFramework.bstack1lll1l1l111_opy_(t, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
            if any(instance is d[1] for d in bstack1l1l11ll111_opy_) or instance == driver:
                return t
    def bstack1l11l1l1l11_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1lll11lllll_opy_.bstack1l1ll11ll1l_opy_(method_name):
                return
            platform_index = f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_, 0)
            bstack1l1l111l1ll_opy_ = self.bstack1l11lllllll_opy_(instance, driver)
            bstack1l11l1l11ll_opy_ = TestFramework.bstack1lll1l1l111_opy_(bstack1l1l111l1ll_opy_, TestFramework.bstack1l11l1l1111_opy_, None)
            if not bstack1l11l1l11ll_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡶࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡡࡴࠢࡶࡩࡸࡹࡩࡰࡰࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡽࡪࡺࠠࡴࡶࡤࡶࡹ࡫ࡤࠣᏩ"))
                return
            driver_command = f.bstack1l1l1lll11l_opy_(*args)
            for command in bstack11ll1ll1l_opy_:
                if command == driver_command:
                    self.bstack111lll1l1l_opy_(driver, platform_index)
            bstack111l1ll1l1_opy_ = self.percy.bstack1l1111lll1_opy_()
            if driver_command in bstack111lll1ll1_opy_[bstack111l1ll1l1_opy_]:
                self.bstack1lll1llll1_opy_.bstack11l11lll1_opy_(bstack1l11l1l11ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠤࡲࡲࡤࡶࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧ࠽ࠤࡪࡸࡲࡰࡴࠥᏪ"), e)
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
        bstack1l1l11ll111_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1ll11l1llll_opy_.bstack1l1l11l1111_opy_, [])
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᏫ") + str(kwargs) + bstack11lllll_opy_ (u"ࠦࠧᏬ"))
            return
        if len(bstack1l1l11ll111_opy_) > 1:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡻ࡭ࡧࡱࠬࡩࡸࡩࡷࡧࡵࡣ࡮ࡴࡳࡵࡣࡱࡧࡪࡹࠩࡾࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏭ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢᏮ"))
        bstack1l11l1l1lll_opy_, bstack1l11l11l1ll_opy_ = bstack1l1l11ll111_opy_[0]
        driver = bstack1l11l1l1lll_opy_()
        if not driver:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᏯ") + str(kwargs) + bstack11lllll_opy_ (u"ࠣࠤᏰ"))
            return
        bstack1l11l11llll_opy_ = {
            TestFramework.bstack1l1lll11111_opy_: bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᏱ"),
            TestFramework.bstack1l1lll1l111_opy_: bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᏲ"),
            TestFramework.bstack1l11l1l1111_opy_: bstack11lllll_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡵࡩࡷࡻ࡮ࠡࡰࡤࡱࡪࠨᏳ")
        }
        bstack1l11l1l1ll1_opy_ = { key: f.bstack1lll1l1l111_opy_(instance, key) for key in bstack1l11l11llll_opy_ }
        bstack1l11l11ll11_opy_ = [key for key, value in bstack1l11l1l1ll1_opy_.items() if not value]
        if bstack1l11l11ll11_opy_:
            for key in bstack1l11l11ll11_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠣᏴ") + str(key) + bstack11lllll_opy_ (u"ࠨࠢᏵ"))
            return
        platform_index = f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_, 0)
        if self.bstack1l11l1l1l1l_opy_.percy_capture_mode == bstack11lllll_opy_ (u"ࠢࡵࡧࡶࡸࡨࡧࡳࡦࠤ᏶"):
            bstack1lll1111_opy_ = bstack1l11l1l1ll1_opy_.get(TestFramework.bstack1l11l1l1111_opy_) + bstack11lllll_opy_ (u"ࠣ࠯ࡷࡩࡸࡺࡣࡢࡵࡨࠦ᏷")
            bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1l11l1l111l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1lll1111_opy_,
                bstack1l1lll11_opy_=bstack1l11l1l1ll1_opy_[TestFramework.bstack1l1lll11111_opy_],
                bstack1l1llll11_opy_=bstack1l11l1l1ll1_opy_[TestFramework.bstack1l1lll1l111_opy_],
                bstack11l111lll_opy_=platform_index
            )
            bstack1lll11l1ll_opy_.end(EVENTS.bstack1l11l1l111l_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᏸ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᏹ"), True, None, None, None, None, test_name=bstack1lll1111_opy_)
    def bstack111lll1l1l_opy_(self, driver, platform_index):
        if self.bstack1lll1llll1_opy_.bstack11l1l1l11_opy_() is True or self.bstack1lll1llll1_opy_.capturing() is True:
            return
        self.bstack1lll1llll1_opy_.bstack11l111l1_opy_()
        while not self.bstack1lll1llll1_opy_.bstack11l1l1l11_opy_():
            bstack1l11l1l11ll_opy_ = self.bstack1lll1llll1_opy_.bstack1l11llll11_opy_()
            self.bstack11l111ll1_opy_(driver, bstack1l11l1l11ll_opy_, platform_index)
        self.bstack1lll1llll1_opy_.bstack1l1l1l11l_opy_()
    def bstack11l111ll1_opy_(self, driver, bstack1llll1lll_opy_, platform_index, test=None):
        from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
        bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack111l1l11l_opy_.value)
        if test != None:
            bstack1l1lll11_opy_ = getattr(test, bstack11lllll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᏺ"), None)
            bstack1l1llll11_opy_ = getattr(test, bstack11lllll_opy_ (u"ࠬࡻࡵࡪࡦࠪᏻ"), None)
            PercySDK.screenshot(driver, bstack1llll1lll_opy_, bstack1l1lll11_opy_=bstack1l1lll11_opy_, bstack1l1llll11_opy_=bstack1l1llll11_opy_, bstack11l111lll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1llll1lll_opy_)
        bstack1lll11l1ll_opy_.end(EVENTS.bstack111l1l11l_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᏼ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᏽ"), True, None, None, None, None, test_name=bstack1llll1lll_opy_)
    def bstack1l11l11ll1l_opy_(self):
        os.environ[bstack11lllll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞࠭᏾")] = str(self.bstack1l11l1l1l1l_opy_.success)
        os.environ[bstack11lllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡈࡖࡈ࡟࡟ࡄࡃࡓࡘ࡚ࡘࡅࡠࡏࡒࡈࡊ࠭᏿")] = str(self.bstack1l11l1l1l1l_opy_.percy_capture_mode)
        self.percy.bstack1l11l11lll1_opy_(self.bstack1l11l1l1l1l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l11l1l11l1_opy_(self.bstack1l11l1l1l1l_opy_.percy_build_id)