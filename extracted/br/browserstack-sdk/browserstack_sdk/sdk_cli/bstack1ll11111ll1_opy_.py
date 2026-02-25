# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1ll1llll111_opy_,
)
from bstack_utils.helper import  bstack11llll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1llllll1l_opy_, bstack1l1llll111l_opy_, bstack1ll11lll1ll_opy_, bstack1ll11l111l1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111111l1_opy_ import bstack11llllll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll111lll1l_opy_
from bstack_utils.percy import bstack11l1llll1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll111111l1_opy_(bstack1ll11llll11_opy_):
    def __init__(self, bstack1l111l1ll11_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l111l1ll11_opy_ = bstack1l111l1ll11_opy_
        self.percy = bstack11l1llll1_opy_()
        self.bstack1l11l1l1l_opy_ = bstack11llllll11_opy_()
        self.bstack1l111ll1ll1_opy_()
        bstack1l1lllll1l1_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l111l1lll1_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), self.bstack1l1l1ll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1ll11_opy_(self, instance: bstack1ll1llll111_opy_, driver: object):
        bstack1l11l111ll1_opy_ = TestFramework.bstack1ll1ll1ll11_opy_(instance.context)
        for t in bstack1l11l111ll1_opy_:
            bstack1l11llll111_opy_ = TestFramework.bstack1ll1lll111l_opy_(t, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
            if any(instance is d[1] for d in bstack1l11llll111_opy_) or instance == driver:
                return t
    def bstack1l111l1lll1_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l1lllll1l1_opy_.bstack1l1ll1ll1ll_opy_(method_name):
                return
            platform_index = f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_, 0)
            bstack1l111llllll_opy_ = self.bstack1l11ll1ll11_opy_(instance, driver)
            bstack1l111ll1l11_opy_ = TestFramework.bstack1ll1lll111l_opy_(bstack1l111llllll_opy_, TestFramework.bstack1l111ll1111_opy_, None)
            if not bstack1l111ll1l11_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡳࡳࡥࡰࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡸࡥࡵࡷࡵࡲ࡮ࡴࡧࠡࡣࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡯ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡶࡸࡦࡸࡴࡦࡦࠥᒌ"))
                return
            driver_command = f.bstack1l1l1l11lll_opy_(*args)
            for command in bstack1ll1111111_opy_:
                if command == driver_command:
                    self.bstack11lll11l_opy_(driver, platform_index)
            bstack1111111ll_opy_ = self.percy.bstack11l1ll111l_opy_()
            if driver_command in bstack1l1l1l11ll_opy_[bstack1111111ll_opy_]:
                self.bstack1l11l1l1l_opy_.bstack1l111lll11_opy_(bstack1l111ll1l11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡱࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩ࠿ࠦࡥࡳࡴࡲࡶࠧᒍ"), e)
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
        bstack1l11llll111_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll111lll1l_opy_.bstack1l11lll11l1_opy_, [])
        if not bstack1l11llll111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᒎ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠨࠢᒏ"))
            return
        if len(bstack1l11llll111_opy_) > 1:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡽ࡯ࡩࡳ࠮ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᒐ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠣࠤᒑ"))
        bstack1l111ll1l1l_opy_, bstack1l111l1ll1l_opy_ = bstack1l11llll111_opy_[0]
        driver = bstack1l111ll1l1l_opy_()
        if not driver:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᒒ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠥࠦᒓ"))
            return
        bstack1l111ll1lll_opy_ = {
            TestFramework.bstack1l1ll11llll_opy_: bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᒔ"),
            TestFramework.bstack1l1l11lll11_opy_: bstack11l1l11_opy_ (u"ࠧࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᒕ"),
            TestFramework.bstack1l111ll1111_opy_: bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࠤࡷ࡫ࡲࡶࡰࠣࡲࡦࡳࡥࠣᒖ")
        }
        bstack1l111ll111l_opy_ = { key: f.bstack1ll1lll111l_opy_(instance, key) for key in bstack1l111ll1lll_opy_ }
        bstack1l111ll11ll_opy_ = [key for key, value in bstack1l111ll111l_opy_.items() if not value]
        if bstack1l111ll11ll_opy_:
            for key in bstack1l111ll11ll_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠥᒗ") + str(key) + bstack11l1l11_opy_ (u"ࠣࠤᒘ"))
            return
        platform_index = f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_, 0)
        if self.bstack1l111l1ll11_opy_.percy_capture_mode == bstack11l1l11_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦᒙ"):
            bstack1l1111l11l_opy_ = bstack1l111ll111l_opy_.get(TestFramework.bstack1l111ll1111_opy_) + bstack11l1l11_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᒚ")
            bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1l111l1l1ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1111l11l_opy_,
                bstack1ll1l1ll1l_opy_=bstack1l111ll111l_opy_[TestFramework.bstack1l1ll11llll_opy_],
                bstack111l1l1ll1_opy_=bstack1l111ll111l_opy_[TestFramework.bstack1l1l11lll11_opy_],
                bstack111l1111l1_opy_=platform_index
            )
            bstack11ll1l1l1_opy_.end(EVENTS.bstack1l111l1l1ll_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᒛ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᒜ"), True, None, None, None, None, test_name=bstack1l1111l11l_opy_)
    def bstack11lll11l_opy_(self, driver, platform_index):
        if self.bstack1l11l1l1l_opy_.bstack11ll1ll1l1_opy_() is True or self.bstack1l11l1l1l_opy_.capturing() is True:
            return
        self.bstack1l11l1l1l_opy_.bstack111ll111l1_opy_()
        while not self.bstack1l11l1l1l_opy_.bstack11ll1ll1l1_opy_():
            bstack1l111ll1l11_opy_ = self.bstack1l11l1l1l_opy_.bstack1l1l1lll1l_opy_()
            self.bstack111ll1l1l1_opy_(driver, bstack1l111ll1l11_opy_, platform_index)
        self.bstack1l11l1l1l_opy_.bstack1111l1111_opy_()
    def bstack111ll1l1l1_opy_(self, driver, bstack1ll11lll1_opy_, platform_index, test=None):
        from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
        bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack111lll1111_opy_.value)
        if test != None:
            bstack1ll1l1ll1l_opy_ = getattr(test, bstack11l1l11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᒝ"), None)
            bstack111l1l1ll1_opy_ = getattr(test, bstack11l1l11_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᒞ"), None)
            PercySDK.screenshot(driver, bstack1ll11lll1_opy_, bstack1ll1l1ll1l_opy_=bstack1ll1l1ll1l_opy_, bstack111l1l1ll1_opy_=bstack111l1l1ll1_opy_, bstack111l1111l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1ll11lll1_opy_)
        bstack11ll1l1l1_opy_.end(EVENTS.bstack111lll1111_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᒟ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᒠ"), True, None, None, None, None, test_name=bstack1ll11lll1_opy_)
    def bstack1l111ll1ll1_opy_(self):
        os.environ[bstack11l1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡉࡗࡉ࡙ࠨᒡ")] = str(self.bstack1l111l1ll11_opy_.success)
        os.environ[bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡊࡘࡃ࡚ࡡࡆࡅࡕ࡚ࡕࡓࡇࡢࡑࡔࡊࡅࠨᒢ")] = str(self.bstack1l111l1ll11_opy_.percy_capture_mode)
        self.percy.bstack1l111ll11l1_opy_(self.bstack1l111l1ll11_opy_.is_percy_auto_enabled)
        self.percy.bstack1l111l1llll_opy_(self.bstack1l111l1ll11_opy_.percy_build_id)