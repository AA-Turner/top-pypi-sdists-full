# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1111111111_opy_,
)
from bstack_utils.helper import  bstack111l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l11_opy_, bstack1lll1l1l1l1_opy_, bstack1lll1lll111_opy_, bstack1lll111l1l1_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1l1l1lll1_opy_ import bstack111111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.percy import bstack11lllll1_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1llll1l1l1l_opy_(bstack1llll11l1ll_opy_):
    def __init__(self, bstack1l1l1lll1l1_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l1l1lll1l1_opy_ = bstack1l1l1lll1l1_opy_
        self.percy = bstack11lllll1_opy_()
        self.bstack1l11111lll_opy_ = bstack111111l1_opy_()
        self.bstack1l1l1ll1111_opy_()
        bstack1llll111lll_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1l1l1l1llll_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), self.bstack1ll1l11ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llll1111_opy_(self, instance: bstack1111111111_opy_, driver: object):
        bstack1l1llllll11_opy_ = TestFramework.bstack1llll1lll11_opy_(instance.context)
        for t in bstack1l1llllll11_opy_:
            bstack1l1lllll1ll_opy_ = TestFramework.bstack1lllll1ll11_opy_(t, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1lllll1ll_opy_) or instance == driver:
                return t
    def bstack1l1l1l1llll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1llll111lll_opy_.bstack1ll11l111ll_opy_(method_name):
                return
            platform_index = f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_, 0)
            bstack1l1lll111ll_opy_ = self.bstack1l1llll1111_opy_(instance, driver)
            bstack1l1l1lll11l_opy_ = TestFramework.bstack1lllll1ll11_opy_(bstack1l1lll111ll_opy_, TestFramework.bstack1l1l1lll1ll_opy_, None)
            if not bstack1l1l1lll11l_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨቴ"))
                return
            driver_command = f.bstack1ll11l1ll11_opy_(*args)
            for command in bstack11lll1ll1l_opy_:
                if command == driver_command:
                    self.bstack11ll11ll1_opy_(driver, platform_index)
            bstack11llllll11_opy_ = self.percy.bstack111l1ll11_opy_()
            if driver_command in bstack1l111l1ll1_opy_[bstack11llllll11_opy_]:
                self.bstack1l11111lll_opy_.bstack1l11l11l1_opy_(bstack1l1l1lll11l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣት"), e)
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
        bstack1l1lllll1ll_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1lll1llll1l_opy_.bstack1l1ll1l111l_opy_, [])
        if not bstack1l1lllll1ll_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥቶ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠤࠥቷ"))
            return
        if len(bstack1l1lllll1ll_opy_) > 1:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቸ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠦࠧቹ"))
        bstack1l1l1ll111l_opy_, bstack1l1l1ll1l11_opy_ = bstack1l1lllll1ll_opy_[0]
        driver = bstack1l1l1ll111l_opy_()
        if not driver:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨቺ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠨࠢቻ"))
            return
        bstack1l1l1ll1lll_opy_ = {
            TestFramework.bstack1ll111llll1_opy_: bstack1l1l1l1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥቼ"),
            TestFramework.bstack1ll1l11lll1_opy_: bstack1l1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦች"),
            TestFramework.bstack1l1l1lll1ll_opy_: bstack1l1l1l1_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦቾ")
        }
        bstack1l1l1ll11ll_opy_ = { key: f.bstack1lllll1ll11_opy_(instance, key) for key in bstack1l1l1ll1lll_opy_ }
        bstack1l1l1ll11l1_opy_ = [key for key, value in bstack1l1l1ll11ll_opy_.items() if not value]
        if bstack1l1l1ll11l1_opy_:
            for key in bstack1l1l1ll11l1_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨቿ") + str(key) + bstack1l1l1l1_opy_ (u"ࠦࠧኀ"))
            return
        platform_index = f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_, 0)
        if self.bstack1l1l1lll1l1_opy_.percy_capture_mode == bstack1l1l1l1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢኁ"):
            bstack1l1ll111ll_opy_ = bstack1l1l1ll11ll_opy_.get(TestFramework.bstack1l1l1lll1ll_opy_) + bstack1l1l1l1_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤኂ")
            bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1l1l1lll111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l1ll111ll_opy_,
                bstack11l1111l_opy_=bstack1l1l1ll11ll_opy_[TestFramework.bstack1ll111llll1_opy_],
                bstack1ll1l1l11l_opy_=bstack1l1l1ll11ll_opy_[TestFramework.bstack1ll1l11lll1_opy_],
                bstack1l111l1lll_opy_=platform_index
            )
            bstack1lll1ll11l1_opy_.end(EVENTS.bstack1l1l1lll111_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢኃ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨኄ"), True, None, None, None, None, test_name=bstack1l1ll111ll_opy_)
    def bstack11ll11ll1_opy_(self, driver, platform_index):
        if self.bstack1l11111lll_opy_.bstack11l111ll_opy_() is True or self.bstack1l11111lll_opy_.capturing() is True:
            return
        self.bstack1l11111lll_opy_.bstack1l1l1l1l11_opy_()
        while not self.bstack1l11111lll_opy_.bstack11l111ll_opy_():
            bstack1l1l1lll11l_opy_ = self.bstack1l11111lll_opy_.bstack11ll1l1lll_opy_()
            self.bstack1ll1l11111_opy_(driver, bstack1l1l1lll11l_opy_, platform_index)
        self.bstack1l11111lll_opy_.bstack11111l1ll_opy_()
    def bstack1ll1l11111_opy_(self, driver, bstack11l1111lll_opy_, platform_index, test=None):
        from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
        bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1l11ll11_opy_.value)
        if test != None:
            bstack11l1111l_opy_ = getattr(test, bstack1l1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧኅ"), None)
            bstack1ll1l1l11l_opy_ = getattr(test, bstack1l1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨኆ"), None)
            PercySDK.screenshot(driver, bstack11l1111lll_opy_, bstack11l1111l_opy_=bstack11l1111l_opy_, bstack1ll1l1l11l_opy_=bstack1ll1l1l11l_opy_, bstack1l111l1lll_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack11l1111lll_opy_)
        bstack1lll1ll11l1_opy_.end(EVENTS.bstack1l11ll11_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦኇ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥኈ"), True, None, None, None, None, test_name=bstack11l1111lll_opy_)
    def bstack1l1l1ll1111_opy_(self):
        os.environ[bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫ኉")] = str(self.bstack1l1l1lll1l1_opy_.success)
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫኊ")] = str(self.bstack1l1l1lll1l1_opy_.percy_capture_mode)
        self.percy.bstack1l1l1ll1l1l_opy_(self.bstack1l1l1lll1l1_opy_.is_percy_auto_enabled)
        self.percy.bstack1l1l1ll1ll1_opy_(self.bstack1l1l1lll1l1_opy_.percy_build_id)