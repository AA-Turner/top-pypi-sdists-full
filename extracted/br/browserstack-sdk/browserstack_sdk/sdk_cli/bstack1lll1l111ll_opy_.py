# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llll1ll111_opy_,
)
from bstack_utils.helper import  bstack1111l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1ll11_opy_, bstack1lll11ll1l1_opy_, bstack1ll1lllll11_opy_, bstack1ll1l1l1ll1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l11l111l_opy_ import bstack1l1l111l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1lll1111ll1_opy_
from bstack_utils.percy import bstack11ll1l1111_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llll1111l1_opy_(bstack1ll1l1l11l1_opy_):
    def __init__(self, bstack1l1l1l11111_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1l11111_opy_ = bstack1l1l1l11111_opy_
        self.percy = bstack11ll1l1111_opy_()
        self.bstack11ll1111l_opy_ = bstack1l1l111l_opy_()
        self.bstack1l1l1l11lll_opy_()
        bstack1ll1l1ll111_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1l1l11lll1l_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), self.bstack1ll1l1111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1ll1lll_opy_(self, instance: bstack1llll1ll111_opy_, driver: object):
        bstack1l1lll1l1l1_opy_ = TestFramework.bstack1llllll1l11_opy_(instance.context)
        for t in bstack1l1lll1l1l1_opy_:
            bstack1l1lll111ll_opy_ = TestFramework.bstack1llll1lllll_opy_(t, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
            if any(instance is d[1] for d in bstack1l1lll111ll_opy_) or instance == driver:
                return t
    def bstack1l1l11lll1l_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1l1ll111_opy_.bstack1ll11ll1l1l_opy_(method_name):
                return
            platform_index = f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_, 0)
            bstack1l1ll1ll1l1_opy_ = self.bstack1l1l1ll1lll_opy_(instance, driver)
            bstack1l1l11llll1_opy_ = TestFramework.bstack1llll1lllll_opy_(bstack1l1ll1ll1l1_opy_, TestFramework.bstack1l1l1l11ll1_opy_, None)
            if not bstack1l1l11llll1_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢዞ"))
                return
            driver_command = f.bstack1ll111ll1l1_opy_(*args)
            for command in bstack1111lll1l_opy_:
                if command == driver_command:
                    self.bstack11l1l11l1_opy_(driver, platform_index)
            bstack11l1lll111_opy_ = self.percy.bstack1l11ll1ll1_opy_()
            if driver_command in bstack11111lll1_opy_[bstack11l1lll111_opy_]:
                self.bstack11ll1111l_opy_.bstack1111111ll_opy_(bstack1l1l11llll1_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤዟ"), e)
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
        bstack1l1lll111ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1lll1111ll1_opy_.bstack1l1lll111l1_opy_, [])
        if not bstack1l1lll111ll_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦዠ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠥࠦዡ"))
            return
        if len(bstack1l1lll111ll_opy_) > 1:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨዢ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠧࠨዣ"))
        bstack1l1l11lll11_opy_, bstack1l1l11lllll_opy_ = bstack1l1lll111ll_opy_[0]
        driver = bstack1l1l11lll11_opy_()
        if not driver:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢዤ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠢࠣዥ"))
            return
        bstack1l1l1l111ll_opy_ = {
            TestFramework.bstack1ll11l111l1_opy_: bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦዦ"),
            TestFramework.bstack1ll11l1111l_opy_: bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧዧ"),
            TestFramework.bstack1l1l1l11ll1_opy_: bstack1ll11ll_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧየ")
        }
        bstack1l1l1l11l11_opy_ = { key: f.bstack1llll1lllll_opy_(instance, key) for key in bstack1l1l1l111ll_opy_ }
        bstack1l1l1l111l1_opy_ = [key for key, value in bstack1l1l1l11l11_opy_.items() if not value]
        if bstack1l1l1l111l1_opy_:
            for key in bstack1l1l1l111l1_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢዩ") + str(key) + bstack1ll11ll_opy_ (u"ࠧࠨዪ"))
            return
        platform_index = f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_, 0)
        if self.bstack1l1l1l11111_opy_.percy_capture_mode == bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣያ"):
            bstack11l111l1l1_opy_ = bstack1l1l1l11l11_opy_.get(TestFramework.bstack1l1l1l11ll1_opy_) + bstack1ll11ll_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥዬ")
            bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack1l1l11ll1ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack11l111l1l1_opy_,
                bstack1l1llll1ll_opy_=bstack1l1l1l11l11_opy_[TestFramework.bstack1ll11l111l1_opy_],
                bstack11l1l11l_opy_=bstack1l1l1l11l11_opy_[TestFramework.bstack1ll11l1111l_opy_],
                bstack1ll11l1l11_opy_=platform_index
            )
            bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1l1l11ll1ll_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣይ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢዮ"), True, None, None, None, None, test_name=bstack11l111l1l1_opy_)
    def bstack11l1l11l1_opy_(self, driver, platform_index):
        if self.bstack11ll1111l_opy_.bstack111llll111_opy_() is True or self.bstack11ll1111l_opy_.capturing() is True:
            return
        self.bstack11ll1111l_opy_.bstack1l11l11l_opy_()
        while not self.bstack11ll1111l_opy_.bstack111llll111_opy_():
            bstack1l1l11llll1_opy_ = self.bstack11ll1111l_opy_.bstack1ll1111111_opy_()
            self.bstack1lll1l11ll_opy_(driver, bstack1l1l11llll1_opy_, platform_index)
        self.bstack11ll1111l_opy_.bstack1ll11l1l1_opy_()
    def bstack1lll1l11ll_opy_(self, driver, bstack11lll111l_opy_, platform_index, test=None):
        from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
        bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack1llll1ll11_opy_.value)
        if test != None:
            bstack1l1llll1ll_opy_ = getattr(test, bstack1ll11ll_opy_ (u"ࠪࡲࡦࡳࡥࠨዯ"), None)
            bstack11l1l11l_opy_ = getattr(test, bstack1ll11ll_opy_ (u"ࠫࡺࡻࡩࡥࠩደ"), None)
            PercySDK.screenshot(driver, bstack11lll111l_opy_, bstack1l1llll1ll_opy_=bstack1l1llll1ll_opy_, bstack11l1l11l_opy_=bstack11l1l11l_opy_, bstack1ll11l1l11_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11lll111l_opy_)
        bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1llll1ll11_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧዱ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦዲ"), True, None, None, None, None, test_name=bstack11lll111l_opy_)
    def bstack1l1l1l11lll_opy_(self):
        os.environ[bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬዳ")] = str(self.bstack1l1l1l11111_opy_.success)
        os.environ[bstack1ll11ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬዴ")] = str(self.bstack1l1l1l11111_opy_.percy_capture_mode)
        self.percy.bstack1l1l1l11l1l_opy_(self.bstack1l1l1l11111_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1l1111l_opy_(self.bstack1l1l1l11111_opy_.percy_build_id)