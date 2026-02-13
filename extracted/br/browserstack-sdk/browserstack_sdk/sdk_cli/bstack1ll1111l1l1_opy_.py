# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1l1ll1ll_opy_,
)
from bstack_utils.helper import  bstack11ll11l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1lllllll1_opy_, bstack1ll11l111ll_opy_, bstack1l1lllll1ll_opy_, bstack1l1lll1l11l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1ll1ll11l_opy_ import bstack111lll111_opy_
from browserstack_sdk.sdk_cli.bstack1ll11lllll1_opy_ import bstack1ll1l111l11_opy_
from bstack_utils.percy import bstack11l11ll11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll1l11l1l1_opy_(bstack1l1ll1lll11_opy_):
    def __init__(self, bstack1l111l11ll1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l111l11ll1_opy_ = bstack1l111l11ll1_opy_
        self.percy = bstack11l11ll11_opy_()
        self.bstack1lll11ll_opy_ = bstack111lll111_opy_()
        self.bstack1l111l11l11_opy_()
        bstack1l1llllllll_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l1111lllll_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), self.bstack1l1l1llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll111l1_opy_(self, instance: bstack1ll1l1ll1ll_opy_, driver: object):
        bstack1l111ll1111_opy_ = TestFramework.bstack1ll1ll1l1l1_opy_(instance.context)
        for t in bstack1l111ll1111_opy_:
            bstack1l11l11l1ll_opy_ = TestFramework.bstack1lll111111l_opy_(t, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
            if any(instance is d[1] for d in bstack1l11l11l1ll_opy_) or instance == driver:
                return t
    def bstack1l1111lllll_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1l1llllllll_opy_.bstack1l1l1l1ll1l_opy_(method_name):
                return
            platform_index = f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_, 0)
            bstack1l111l1ll1l_opy_ = self.bstack1l11ll111l1_opy_(instance, driver)
            bstack1l1111lll11_opy_ = TestFramework.bstack1lll111111l_opy_(bstack1l111l1ll1l_opy_, TestFramework.bstack1l111l11111_opy_, None)
            if not bstack1l1111lll11_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢᒂ"))
                return
            driver_command = f.bstack1l1l11ll11l_opy_(*args)
            for command in bstack111lll1lll_opy_:
                if command == driver_command:
                    self.bstack1l1l11l1_opy_(driver, platform_index)
            bstack1llll1ll1_opy_ = self.percy.bstack1lllll11l1_opy_()
            if driver_command in bstack1lll11ll1_opy_[bstack1llll1ll1_opy_]:
                self.bstack1lll11ll_opy_.bstack11l1l1ll1l_opy_(bstack1l1111lll11_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤᒃ"), e)
    def bstack1l1l1llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
        bstack1l11l11l1ll_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1l111l11_opy_.bstack1l11l1l11ll_opy_, [])
        if not bstack1l11l11l1ll_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᒄ") + str(kwargs) + bstack11l11_opy_ (u"ࠥࠦᒅ"))
            return
        if len(bstack1l11l11l1ll_opy_) > 1:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᒆ") + str(kwargs) + bstack11l11_opy_ (u"ࠧࠨᒇ"))
        bstack1l111l111l1_opy_, bstack1l1111llll1_opy_ = bstack1l11l11l1ll_opy_[0]
        driver = bstack1l111l111l1_opy_()
        if not driver:
            self.logger.debug(bstack11l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᒈ") + str(kwargs) + bstack11l11_opy_ (u"ࠢࠣᒉ"))
            return
        bstack1l1111lll1l_opy_ = {
            TestFramework.bstack1l1ll11111l_opy_: bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᒊ"),
            TestFramework.bstack1l1l11l11l1_opy_: bstack11l11_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᒋ"),
            TestFramework.bstack1l111l11111_opy_: bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧᒌ")
        }
        bstack1l111l11lll_opy_ = { key: f.bstack1lll111111l_opy_(instance, key) for key in bstack1l1111lll1l_opy_ }
        bstack1l111l1111l_opy_ = [key for key, value in bstack1l111l11lll_opy_.items() if not value]
        if bstack1l111l1111l_opy_:
            for key in bstack1l111l1111l_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢᒍ") + str(key) + bstack11l11_opy_ (u"ࠧࠨᒎ"))
            return
        platform_index = f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_, 0)
        if self.bstack1l111l11ll1_opy_.percy_capture_mode == bstack11l11_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᒏ"):
            bstack1l1l1l1ll_opy_ = bstack1l111l11lll_opy_.get(TestFramework.bstack1l111l11111_opy_) + bstack11l11_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥᒐ")
            bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1l111l11l1l_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1l1l1ll_opy_,
                bstack11lll1l1ll_opy_=bstack1l111l11lll_opy_[TestFramework.bstack1l1ll11111l_opy_],
                bstack11l1ll11_opy_=bstack1l111l11lll_opy_[TestFramework.bstack1l1l11l11l1_opy_],
                bstack1l11111l1l_opy_=platform_index
            )
            bstack111l1lllll_opy_.end(EVENTS.bstack1l111l11l1l_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᒑ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᒒ"), True, None, None, None, None, test_name=bstack1l1l1l1ll_opy_)
    def bstack1l1l11l1_opy_(self, driver, platform_index):
        if self.bstack1lll11ll_opy_.bstack1111l1l1_opy_() is True or self.bstack1lll11ll_opy_.capturing() is True:
            return
        self.bstack1lll11ll_opy_.bstack11l11l1l1l_opy_()
        while not self.bstack1lll11ll_opy_.bstack1111l1l1_opy_():
            bstack1l1111lll11_opy_ = self.bstack1lll11ll_opy_.bstack1111l11l_opy_()
            self.bstack111lllll11_opy_(driver, bstack1l1111lll11_opy_, platform_index)
        self.bstack1lll11ll_opy_.bstack11111ll1_opy_()
    def bstack111lllll11_opy_(self, driver, bstack111l1lll11_opy_, platform_index, test=None):
        from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
        bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11l11111_opy_.value)
        if test != None:
            bstack11lll1l1ll_opy_ = getattr(test, bstack11l11_opy_ (u"ࠪࡲࡦࡳࡥࠨᒓ"), None)
            bstack11l1ll11_opy_ = getattr(test, bstack11l11_opy_ (u"ࠫࡺࡻࡩࡥࠩᒔ"), None)
            PercySDK.screenshot(driver, bstack111l1lll11_opy_, bstack11lll1l1ll_opy_=bstack11lll1l1ll_opy_, bstack11l1ll11_opy_=bstack11l1ll11_opy_, bstack1l11111l1l_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack111l1lll11_opy_)
        bstack111l1lllll_opy_.end(EVENTS.bstack11l11111_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᒕ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᒖ"), True, None, None, None, None, test_name=bstack111l1lll11_opy_)
    def bstack1l111l11l11_opy_(self):
        os.environ[bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᒗ")] = str(self.bstack1l111l11ll1_opy_.success)
        os.environ[bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᒘ")] = str(self.bstack1l111l11ll1_opy_.percy_capture_mode)
        self.percy.bstack1l111l1l111_opy_(self.bstack1l111l11ll1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l111l111ll_opy_(self.bstack1l111l11ll1_opy_.percy_build_id)