# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack1l1ll11l1ll_opy_,
)
from bstack_utils.helper import  bstack11l11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, bstack1l11l1ll111_opy_, TestHookState, bstack11lll1ll1l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11l1111lll_opy_ import bstack1lll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11l11111l_opy_
from bstack_utils.percy import bstack11l111llll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1l1l1111l11_opy_(bstack1l1l1111111_opy_):
    def __init__(self, bstack11l1lllll11_opy_: Dict[str, str]):
        super().__init__()
        self.bstack11l1lllll11_opy_ = bstack11l1lllll11_opy_
        self.percy = bstack11l111llll_opy_()
        self.bstack1l111l11l1_opy_ = bstack1lll1ll1l1_opy_()
        self.bstack11l1llllll1_opy_()
        bstack1l1l111l111_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.PRE), self.bstack11l1llll1ll_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11ll1ll11l1_opy_(self, instance: bstack1l1ll11l1ll_opy_, driver: object):
        bstack11ll1lll1ll_opy_ = TestFramework.bstack1l1ll111111_opy_(instance.context)
        for t in bstack11ll1lll1ll_opy_:
            bstack11ll1l11111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(t, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
            if any(instance is d[1] for d in bstack11ll1l11111_opy_) or instance == driver:
                return t
    def bstack11l1llll1ll_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l1l111l111_opy_.bstack1l1111l111l_opy_(method_name):
                return
            platform_index = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_, 0)
            bstack1l111ll1ll_opy_ = self.bstack11ll1ll11l1_opy_(instance, driver)
            bstack11ll1111l11_opy_ = TestFramework.bstack1ll1111l1l1_opy_(bstack1l111ll1ll_opy_, TestFramework.bstack11ll11111l1_opy_, None)
            if not bstack11ll1111l11_opy_:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡲࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࡀࠠࡳࡧࡷࡹࡷࡴࡩ࡯ࡩࠣࡥࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡪࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡸࡺࡡࡳࡶࡨࡨࠧᝦ"))
                return
            driver_command = f.bstack1l1111l11l1_opy_(*args)
            for command in bstack1ll1l1111_opy_:
                if command == driver_command:
                    self.bstack11l11l1l1_opy_(driver, platform_index)
            bstack1l1ll1lll_opy_ = self.percy.bstack11lll1ll_opy_()
            if driver_command in bstack1l11lll1l_opy_[bstack1l1ll1lll_opy_]:
                self.bstack1l111l11l1_opy_.bstack1l1lllll_opy_(bstack11ll1111l11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡧࡵࡶࡴࡸࠢᝧ"), e)
    def bstack1l1111ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
        bstack11ll1l11111_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11ll1lllll1_opy_, [])
        if not bstack11ll1l11111_opy_:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᝨ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠣࠤᝩ"))
            return
        if len(bstack11ll1l11111_opy_) > 1:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡿࡱ࡫࡮ࠩࡦࡵ࡭ࡻ࡫ࡲࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᝪ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠥࠦᝫ"))
        bstack11ll11111ll_opy_, bstack11ll1111111_opy_ = bstack11ll1l11111_opy_[0]
        driver = bstack11ll11111ll_opy_()
        if not driver:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᝬ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠧࠨ᝭"))
            return
        bstack11l1lllll1l_opy_ = {
            TestFramework.bstack1l111l11l1l_opy_: bstack1l1111l_opy_ (u"ࠨࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᝮ"),
            TestFramework.bstack11llllll111_opy_: bstack1l1111l_opy_ (u"ࠢࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥᝯ"),
            TestFramework.bstack11ll11111l1_opy_: bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹࠦࡲࡦࡴࡸࡲࠥࡴࡡ࡮ࡧࠥᝰ")
        }
        bstack11ll1111lll_opy_ = { key: f.bstack1ll1111l1l1_opy_(instance, key) for key in bstack11l1lllll1l_opy_ }
        bstack11l1lllllll_opy_ = [key for key, value in bstack11ll1111lll_opy_.items() if not value]
        if bstack11l1lllllll_opy_:
            for key in bstack11l1lllllll_opy_:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠧ᝱") + str(key) + bstack1l1111l_opy_ (u"ࠥࠦᝲ"))
            return
        platform_index = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_, 0)
        if self.bstack11l1lllll11_opy_.percy_capture_mode == bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᝳ"):
            bstack11l1ll1l1_opy_ = bstack11ll1111lll_opy_.get(TestFramework.bstack11ll11111l1_opy_) + bstack1l1111l_opy_ (u"ࠧ࠳ࡴࡦࡵࡷࡧࡦࡹࡥࠣ᝴")
            bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack11ll111111l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11l1ll1l1_opy_,
                bstack111ll11ll_opy_=bstack11ll1111lll_opy_[TestFramework.bstack1l111l11l1l_opy_],
                bstack1ll111l1l_opy_=bstack11ll1111lll_opy_[TestFramework.bstack11llllll111_opy_],
                bstack1ll1l1l11l_opy_=platform_index
            )
            bstack11lll1111_opy_.end(EVENTS.bstack11ll111111l_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᝵"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᝶"), True, None, None, None, None, test_name=bstack11l1ll1l1_opy_)
    def bstack11l11l1l1_opy_(self, driver, platform_index):
        if self.bstack1l111l11l1_opy_.bstack11111111_opy_() is True or self.bstack1l111l11l1_opy_.capturing() is True:
            return
        self.bstack1l111l11l1_opy_.bstack111lll1l11_opy_()
        while not self.bstack1l111l11l1_opy_.bstack11111111_opy_():
            bstack11ll1111l11_opy_ = self.bstack1l111l11l1_opy_.bstack1llllll1lll_opy_()
            self.bstack11lll1l11l_opy_(driver, bstack11ll1111l11_opy_, platform_index)
        self.bstack1l111l11l1_opy_.bstack11l1ll11l1_opy_()
    def bstack11lll1l11l_opy_(self, driver, bstack11l1l11l1l_opy_, platform_index, test=None):
        from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
        bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack1lllll11l1_opy_.value)
        if test != None:
            bstack111ll11ll_opy_ = getattr(test, bstack1l1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭᝷"), None)
            bstack1ll111l1l_opy_ = getattr(test, bstack1l1111l_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᝸"), None)
            PercySDK.screenshot(driver, bstack11l1l11l1l_opy_, bstack111ll11ll_opy_=bstack111ll11ll_opy_, bstack1ll111l1l_opy_=bstack1ll111l1l_opy_, bstack1ll1l1l11l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1l11l1l_opy_)
        bstack11lll1111_opy_.end(EVENTS.bstack1lllll11l1_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᝹"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᝺"), True, None, None, None, None, test_name=bstack11l1l11l1l_opy_)
    def bstack11l1llllll1_opy_(self):
        os.environ[bstack1l1111l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡋࡒࡄ࡛ࠪ᝻")] = str(self.bstack11l1lllll11_opy_.success)
        os.environ[bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࡣࡈࡇࡐࡕࡗࡕࡉࡤࡓࡏࡅࡇࠪ᝼")] = str(self.bstack11l1lllll11_opy_.percy_capture_mode)
        self.percy.bstack11ll1111ll1_opy_(self.bstack11l1lllll11_opy_.is_percy_auto_enabled)
        self.percy.bstack11ll1111l1l_opy_(self.bstack11l1lllll11_opy_.percy_build_id)