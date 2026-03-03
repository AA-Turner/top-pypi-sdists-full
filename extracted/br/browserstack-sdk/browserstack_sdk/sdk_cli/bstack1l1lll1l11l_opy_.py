# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1lll1111_opy_,
)
from bstack_utils.helper import  bstack1lll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1ll1l111111_opy_, bstack1l1llll1l1l_opy_, bstack1ll1l1l11ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack111l111l1_opy_ import bstack11111l111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11llll_opy_ import bstack1ll11l1ll1l_opy_
from bstack_utils.percy import bstack1ll1111l_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll11ll111l_opy_(bstack1ll1l1l11l1_opy_):
    def __init__(self, bstack1l111ll1111_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l111ll1111_opy_ = bstack1l111ll1111_opy_
        self.percy = bstack1ll1111l_opy_()
        self.bstack1lll1lllll_opy_ = bstack11111l111_opy_()
        self.bstack1l111ll1l11_opy_()
        bstack1ll1111ll11_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l111l1l11l_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11l111l1l_opy_(self, instance: bstack1ll1lll1111_opy_, driver: object):
        bstack1l11ll11l11_opy_ = TestFramework.bstack1lll11l11l1_opy_(instance.context)
        for t in bstack1l11ll11l11_opy_:
            bstack1l11lll111l_opy_ = TestFramework.bstack1ll1lllll11_opy_(t, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
            if any(instance is d[1] for d in bstack1l11lll111l_opy_) or instance == driver:
                return t
    def bstack1l111l1l11l_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1111ll11_opy_.bstack1l1l1l11111_opy_(method_name):
                return
            platform_index = f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_, 0)
            bstack1l11ll11ll1_opy_ = self.bstack1l11l111l1l_opy_(instance, driver)
            bstack1l111ll11ll_opy_ = TestFramework.bstack1ll1lllll11_opy_(bstack1l11ll11ll1_opy_, TestFramework.bstack1l111ll111l_opy_, None)
            if not bstack1l111ll11ll_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢᒉ"))
                return
            driver_command = f.bstack1l1l11ll111_opy_(*args)
            for command in bstack111111l1l_opy_:
                if command == driver_command:
                    self.bstack1l1lllllll_opy_(driver, platform_index)
            bstack1l11l1lll1_opy_ = self.percy.bstack11lllllll_opy_()
            if driver_command in bstack111ll11ll_opy_[bstack1l11l1lll1_opy_]:
                self.bstack1lll1lllll_opy_.bstack111l1ll1l1_opy_(bstack1l111ll11ll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤᒊ"), e)
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
        bstack1l11lll111l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll1l_opy_.bstack1l11l11l111_opy_, [])
        if not bstack1l11lll111l_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᒋ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦᒌ"))
            return
        if len(bstack1l11lll111l_opy_) > 1:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᒍ") + str(kwargs) + bstack11ll111_opy_ (u"ࠧࠨᒎ"))
        bstack1l111l1ll1l_opy_, bstack1l111ll1l1l_opy_ = bstack1l11lll111l_opy_[0]
        driver = bstack1l111l1ll1l_opy_()
        if not driver:
            self.logger.debug(bstack11ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᒏ") + str(kwargs) + bstack11ll111_opy_ (u"ࠢࠣᒐ"))
            return
        bstack1l111l1lll1_opy_ = {
            TestFramework.bstack1l1l1l1111l_opy_: bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᒑ"),
            TestFramework.bstack1l1l11ll1ll_opy_: bstack11ll111_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᒒ"),
            TestFramework.bstack1l111ll111l_opy_: bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧᒓ")
        }
        bstack1l111ll11l1_opy_ = { key: f.bstack1ll1lllll11_opy_(instance, key) for key in bstack1l111l1lll1_opy_ }
        bstack1l111l1l1l1_opy_ = [key for key, value in bstack1l111ll11l1_opy_.items() if not value]
        if bstack1l111l1l1l1_opy_:
            for key in bstack1l111l1l1l1_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢᒔ") + str(key) + bstack11ll111_opy_ (u"ࠧࠨᒕ"))
            return
        platform_index = f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_, 0)
        if self.bstack1l111ll1111_opy_.percy_capture_mode == bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᒖ"):
            bstack1ll1l111l1_opy_ = bstack1l111ll11l1_opy_.get(TestFramework.bstack1l111ll111l_opy_) + bstack11ll111_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥᒗ")
            bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1l111l1ll11_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll1l111l1_opy_,
                bstack11l1ll11l_opy_=bstack1l111ll11l1_opy_[TestFramework.bstack1l1l1l1111l_opy_],
                bstack1ll11ll1l_opy_=bstack1l111ll11l1_opy_[TestFramework.bstack1l1l11ll1ll_opy_],
                bstack11l111l1l_opy_=platform_index
            )
            bstack1111l1l1l_opy_.end(EVENTS.bstack1l111l1ll11_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᒘ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᒙ"), True, None, None, None, None, test_name=bstack1ll1l111l1_opy_)
    def bstack1l1lllllll_opy_(self, driver, platform_index):
        if self.bstack1lll1lllll_opy_.bstack1l11111l1l_opy_() is True or self.bstack1lll1lllll_opy_.capturing() is True:
            return
        self.bstack1lll1lllll_opy_.bstack1l11l1l1l1_opy_()
        while not self.bstack1lll1lllll_opy_.bstack1l11111l1l_opy_():
            bstack1l111ll11ll_opy_ = self.bstack1lll1lllll_opy_.bstack1l1ll11ll1_opy_()
            self.bstack1lll1l1ll1_opy_(driver, bstack1l111ll11ll_opy_, platform_index)
        self.bstack1lll1lllll_opy_.bstack1ll11lllll_opy_()
    def bstack1lll1l1ll1_opy_(self, driver, bstack1l111ll1_opy_, platform_index, test=None):
        from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
        bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1lll11l1ll_opy_.value)
        if test != None:
            bstack11l1ll11l_opy_ = getattr(test, bstack11ll111_opy_ (u"ࠪࡲࡦࡳࡥࠨᒚ"), None)
            bstack1ll11ll1l_opy_ = getattr(test, bstack11ll111_opy_ (u"ࠫࡺࡻࡩࡥࠩᒛ"), None)
            PercySDK.screenshot(driver, bstack1l111ll1_opy_, bstack11l1ll11l_opy_=bstack11l1ll11l_opy_, bstack1ll11ll1l_opy_=bstack1ll11ll1l_opy_, bstack11l111l1l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l111ll1_opy_)
        bstack1111l1l1l_opy_.end(EVENTS.bstack1lll11l1ll_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᒜ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᒝ"), True, None, None, None, None, test_name=bstack1l111ll1_opy_)
    def bstack1l111ll1l11_opy_(self):
        os.environ[bstack11ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᒞ")] = str(self.bstack1l111ll1111_opy_.success)
        os.environ[bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᒟ")] = str(self.bstack1l111ll1111_opy_.percy_capture_mode)
        self.percy.bstack1l111l1l1ll_opy_(self.bstack1l111ll1111_opy_.is_percy_auto_enabled)
        self.percy.bstack1l111l1llll_opy_(self.bstack1l111ll1111_opy_.percy_build_id)