# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll11lll1l_opy_,
)
from bstack_utils.helper import  bstack111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11l1l1l1_opy_, bstack1ll1ll111l1_opy_, bstack1ll1111llll_opy_, bstack1ll1lll11ll_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack11llll11l_opy_ import bstack1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l11_opy_ import bstack1ll1l11l11l_opy_
from bstack_utils.percy import bstack111llll11_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll11l11111_opy_(bstack1ll1l11l1ll_opy_):
    def __init__(self, bstack1l11l1l11ll_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l11l1l11ll_opy_ = bstack1l11l1l11ll_opy_
        self.percy = bstack111llll11_opy_()
        self.bstack1ll1lll11l_opy_ = bstack1l1l11l1_opy_()
        self.bstack1l11l11ll11_opy_()
        bstack1ll1ll1lll1_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l11l1l1111_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), self.bstack1l1llll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll111_opy_(self, instance: bstack1lll11lll1l_opy_, driver: object):
        bstack1l11llllll1_opy_ = TestFramework.bstack1lll11l11ll_opy_(instance.context)
        for t in bstack1l11llllll1_opy_:
            bstack1l1l111111l_opy_ = TestFramework.bstack1lll1ll11l1_opy_(t, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
            if any(instance is d[1] for d in bstack1l1l111111l_opy_) or instance == driver:
                return t
    def bstack1l11l1l1111_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1ll1lll1_opy_.bstack1l1ll111111_opy_(method_name):
                return
            platform_index = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_, 0)
            bstack1l11lll1ll1_opy_ = self.bstack1l1l11ll111_opy_(instance, driver)
            bstack1l11l11llll_opy_ = TestFramework.bstack1lll1ll11l1_opy_(bstack1l11lll1ll1_opy_, TestFramework.bstack1l11l1l1l11_opy_, None)
            if not bstack1l11l11llll_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡯࡯ࡡࡳࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫࠺ࠡࡴࡨࡸࡺࡸ࡮ࡪࡰࡪࠤࡦࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡ࡫ࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡹࡴࡢࡴࡷࡩࡩࠨᏙ"))
                return
            driver_command = f.bstack1l1llll11l1_opy_(*args)
            for command in bstack1lll1lllll_opy_:
                if command == driver_command:
                    self.bstack1l1l1l1lll_opy_(driver, platform_index)
            bstack1l1l111l1l_opy_ = self.percy.bstack1l111l11_opy_()
            if driver_command in bstack1111ll1l_opy_[bstack1l1l111l1l_opy_]:
                self.bstack1ll1lll11l_opy_.bstack11l111ll1l_opy_(bstack1l11l11llll_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡨࡶࡷࡵࡲࠣᏚ"), e)
    def bstack1l1llll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
        bstack1l1l111111l_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1l11l11l_opy_.bstack1l1l11l111l_opy_, [])
        if not bstack1l1l111111l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᏛ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠤࠥᏜ"))
            return
        if len(bstack1l1l111111l_opy_) > 1:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷ࠮ࢃࠠࡥࡴ࡬ࡺࡪࡸࡳࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᏝ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠦࠧᏞ"))
        bstack1l11l1l1ll1_opy_, bstack1l11l1l111l_opy_ = bstack1l1l111111l_opy_[0]
        driver = bstack1l11l1l1ll1_opy_()
        if not driver:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡧࡶ࡮ࡼࡥࡳࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏟ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠨࠢᏠ"))
            return
        bstack1l11l1l1lll_opy_ = {
            TestFramework.bstack1l1l1lll11l_opy_: bstack11l1ll1_opy_ (u"ࠢࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥᏡ"),
            TestFramework.bstack1l1llll1l11_opy_: bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦᏢ"),
            TestFramework.bstack1l11l1l1l11_opy_: bstack11l1ll1_opy_ (u"ࠤࡷࡩࡸࡺࠠࡳࡧࡵࡹࡳࠦ࡮ࡢ࡯ࡨࠦᏣ")
        }
        bstack1l11l1l1l1l_opy_ = { key: f.bstack1lll1ll11l1_opy_(instance, key) for key in bstack1l11l1l1lll_opy_ }
        bstack1l11l11lll1_opy_ = [key for key, value in bstack1l11l1l1l1l_opy_.items() if not value]
        if bstack1l11l11lll1_opy_:
            for key in bstack1l11l11lll1_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࠨᏤ") + str(key) + bstack11l1ll1_opy_ (u"ࠦࠧᏥ"))
            return
        platform_index = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_, 0)
        if self.bstack1l11l1l11ll_opy_.percy_capture_mode == bstack11l1ll1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢᏦ"):
            bstack1l11ll1ll_opy_ = bstack1l11l1l1l1l_opy_.get(TestFramework.bstack1l11l1l1l11_opy_) + bstack11l1ll1_opy_ (u"ࠨ࠭ࡵࡧࡶࡸࡨࡧࡳࡦࠤᏧ")
            bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack1l11l1ll111_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1l11ll1ll_opy_,
                bstack11l1ll1l1l_opy_=bstack1l11l1l1l1l_opy_[TestFramework.bstack1l1l1lll11l_opy_],
                bstack11ll1l1l_opy_=bstack1l11l1l1l1l_opy_[TestFramework.bstack1l1llll1l11_opy_],
                bstack1lll1ll1l1_opy_=platform_index
            )
            bstack1ll1111ll_opy_.end(EVENTS.bstack1l11l1ll111_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᏨ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᏩ"), True, None, None, None, None, test_name=bstack1l11ll1ll_opy_)
    def bstack1l1l1l1lll_opy_(self, driver, platform_index):
        if self.bstack1ll1lll11l_opy_.bstack1llll111l1_opy_() is True or self.bstack1ll1lll11l_opy_.capturing() is True:
            return
        self.bstack1ll1lll11l_opy_.bstack1111111l_opy_()
        while not self.bstack1ll1lll11l_opy_.bstack1llll111l1_opy_():
            bstack1l11l11llll_opy_ = self.bstack1ll1lll11l_opy_.bstack111l1l11ll_opy_()
            self.bstack111l1l1l11_opy_(driver, bstack1l11l11llll_opy_, platform_index)
        self.bstack1ll1lll11l_opy_.bstack1l1llllll1_opy_()
    def bstack111l1l1l11_opy_(self, driver, bstack1l1ll111ll_opy_, platform_index, test=None):
        from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
        bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack1ll1l1l11_opy_.value)
        if test != None:
            bstack11l1ll1l1l_opy_ = getattr(test, bstack11l1ll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᏪ"), None)
            bstack11ll1l1l_opy_ = getattr(test, bstack11l1ll1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᏫ"), None)
            PercySDK.screenshot(driver, bstack1l1ll111ll_opy_, bstack11l1ll1l1l_opy_=bstack11l1ll1l1l_opy_, bstack11ll1l1l_opy_=bstack11ll1l1l_opy_, bstack1lll1ll1l1_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack1l1ll111ll_opy_)
        bstack1ll1111ll_opy_.end(EVENTS.bstack1ll1l1l11_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᏬ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᏭ"), True, None, None, None, None, test_name=bstack1l1ll111ll_opy_)
    def bstack1l11l11ll11_opy_(self):
        os.environ[bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡅࡓࡅ࡜ࠫᏮ")] = str(self.bstack1l11l1l11ll_opy_.success)
        os.environ[bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࡤࡉࡁࡑࡖࡘࡖࡊࡥࡍࡐࡆࡈࠫᏯ")] = str(self.bstack1l11l1l11ll_opy_.percy_capture_mode)
        self.percy.bstack1l11l11ll1l_opy_(self.bstack1l11l1l11ll_opy_.is_percy_auto_enabled)
        self.percy.bstack1l11l1l11l1_opy_(self.bstack1l11l1l11ll_opy_.percy_build_id)