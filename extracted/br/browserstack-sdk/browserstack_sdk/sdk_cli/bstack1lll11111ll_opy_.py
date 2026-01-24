# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from typing import Dict, List, Any, Callable, Tuple, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1l1111l_opy_,
)
from bstack_utils.helper import  bstack111111lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll111ll_opy_, bstack1ll111l1lll_opy_, bstack1ll1l111111_opy_, bstack1ll11l1l11l_opy_
from typing import Tuple, Any
import threading
from bstack_utils.bstack1lll1l111l_opy_ import bstack11lll1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11lll_opy_ import bstack1ll11l1l1l1_opy_
from bstack_utils.percy import bstack1l1l11l1ll_opy_
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.constants import *
import re
class bstack1ll1l11111l_opy_(bstack1ll1ll111l1_opy_):
    def __init__(self, bstack1l11l1l111l_opy_: Dict[str, str]):
        super().__init__()
        self.bstack1l11l1l111l_opy_ = bstack1l11l1l111l_opy_
        self.percy = bstack1l1l11l1ll_opy_()
        self.bstack1ll1l11l1_opy_ = bstack11lll1ll11_opy_()
        self.bstack1l11l1l1ll1_opy_()
        bstack1ll1l111l1l_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l11l1ll111_opy_)
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.POST), self.bstack1l1ll1ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11111ll_opy_(self, instance: bstack1lll1l1111l_opy_, driver: object):
        bstack1l11lllll1l_opy_ = TestFramework.bstack1lll11l1l11_opy_(instance.context)
        for t in bstack1l11lllll1l_opy_:
            bstack1l1l111l1l1_opy_ = TestFramework.bstack1lll1l11lll_opy_(t, bstack1ll11l1l1l1_opy_.bstack1l11llll1ll_opy_, [])
            if any(instance is d[1] for d in bstack1l1l111l1l1_opy_) or instance == driver:
                return t
    def bstack1l11l1ll111_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if not bstack1ll1l111l1l_opy_.bstack1l1llll111l_opy_(method_name):
                return
            platform_index = f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_, 0)
            bstack1l11l1lll11_opy_ = self.bstack1l1l11111ll_opy_(instance, driver)
            bstack1l11l1l1l1l_opy_ = TestFramework.bstack1lll1l11lll_opy_(bstack1l11l1lll11_opy_, TestFramework.bstack1l11l1l1111_opy_, None)
            if not bstack1l11l1l1l1l_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡰࡰࡢࡴࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡵࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥࡧࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡳࡵࡣࡵࡸࡪࡪࠢᏓ"))
                return
            driver_command = f.bstack1l1ll111ll1_opy_(*args)
            for command in bstack111ll1l1l1_opy_:
                if command == driver_command:
                    self.bstack111l1l1l1l_opy_(driver, platform_index)
            bstack1l11llll1l_opy_ = self.percy.bstack11llllll11_opy_()
            if driver_command in bstack1l11lllll_opy_[bstack1l11llll1l_opy_]:
                self.bstack1ll1l11l1_opy_.bstack111l1llll_opy_(bstack1l11l1l1l1l_opy_, driver_command)
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠣࡱࡱࡣࡵࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦ࠼ࠣࡩࡷࡸ࡯ࡳࠤᏔ"), e)
    def bstack1l1ll1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
        bstack1l1l111l1l1_opy_ = f.bstack1lll1l11lll_opy_(instance, bstack1ll11l1l1l1_opy_.bstack1l11llll1ll_opy_, [])
        if not bstack1l1l111l1l1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᏕ") + str(kwargs) + bstack1l1111_opy_ (u"ࠥࠦᏖ"))
            return
        if len(bstack1l1l111l1l1_opy_) > 1:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡨࡷ࡯ࡶࡦࡴࡢ࡭ࡳࡹࡴࡢࡰࡦࡩࡸ࠯ࡽࠡࡦࡵ࡭ࡻ࡫ࡲࡴࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᏗ") + str(kwargs) + bstack1l1111_opy_ (u"ࠧࠨᏘ"))
        bstack1l11l1l1l11_opy_, bstack1l11l1l11l1_opy_ = bstack1l1l111l1l1_opy_[0]
        driver = bstack1l11l1l1l11_opy_()
        if not driver:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᏙ") + str(kwargs) + bstack1l1111_opy_ (u"ࠢࠣᏚ"))
            return
        bstack1l11l1ll11l_opy_ = {
            TestFramework.bstack1l1ll11111l_opy_: bstack1l1111_opy_ (u"ࠣࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᏛ"),
            TestFramework.bstack1l1lll111ll_opy_: bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᏜ"),
            TestFramework.bstack1l11l1l1111_opy_: bstack1l1111_opy_ (u"ࠥࡸࡪࡹࡴࠡࡴࡨࡶࡺࡴࠠ࡯ࡣࡰࡩࠧᏝ")
        }
        bstack1l11l11llll_opy_ = { key: f.bstack1lll1l11lll_opy_(instance, key) for key in bstack1l11l1ll11l_opy_ }
        bstack1l11l1ll1ll_opy_ = [key for key, value in bstack1l11l11llll_opy_.items() if not value]
        if bstack1l11l1ll1ll_opy_:
            for key in bstack1l11l1ll1ll_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠢᏞ") + str(key) + bstack1l1111_opy_ (u"ࠧࠨᏟ"))
            return
        platform_index = f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_, 0)
        if self.bstack1l11l1l111l_opy_.percy_capture_mode == bstack1l1111_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣᏠ"):
            bstack1ll1l1lll_opy_ = bstack1l11l11llll_opy_.get(TestFramework.bstack1l11l1l1111_opy_) + bstack1l1111_opy_ (u"ࠢ࠮ࡶࡨࡷࡹࡩࡡࡴࡧࠥᏡ")
            bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1l11l1l11ll_opy_.value)
            PercySDK.screenshot(
                driver,
                bstack1ll1l1lll_opy_,
                bstack1ll11l11l_opy_=bstack1l11l11llll_opy_[TestFramework.bstack1l1ll11111l_opy_],
                bstack1111l1ll1_opy_=bstack1l11l11llll_opy_[TestFramework.bstack1l1lll111ll_opy_],
                bstack1lll111111_opy_=platform_index
            )
            bstack11ll111lll_opy_.end(EVENTS.bstack1l11l1l11ll_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᏢ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᏣ"), True, None, None, None, None, test_name=bstack1ll1l1lll_opy_)
    def bstack111l1l1l1l_opy_(self, driver, platform_index):
        if self.bstack1ll1l11l1_opy_.bstack11l111ll_opy_() is True or self.bstack1ll1l11l1_opy_.capturing() is True:
            return
        self.bstack1ll1l11l1_opy_.bstack1l1ll111ll_opy_()
        while not self.bstack1ll1l11l1_opy_.bstack11l111ll_opy_():
            bstack1l11l1l1l1l_opy_ = self.bstack1ll1l11l1_opy_.bstack1l111lllll_opy_()
            self.bstack1l1lllllll_opy_(driver, bstack1l11l1l1l1l_opy_, platform_index)
        self.bstack1ll1l11l1_opy_.bstack1ll111lll_opy_()
    def bstack1l1lllllll_opy_(self, driver, bstack111l11lll_opy_, platform_index, test=None):
        from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
        bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1l11111ll_opy_.value)
        if test != None:
            bstack1ll11l11l_opy_ = getattr(test, bstack1l1111_opy_ (u"ࠪࡲࡦࡳࡥࠨᏤ"), None)
            bstack1111l1ll1_opy_ = getattr(test, bstack1l1111_opy_ (u"ࠫࡺࡻࡩࡥࠩᏥ"), None)
            PercySDK.screenshot(driver, bstack111l11lll_opy_, bstack1ll11l11l_opy_=bstack1ll11l11l_opy_, bstack1111l1ll1_opy_=bstack1111l1ll1_opy_, bstack1lll111111_opy_=platform_index)
        else:
            PercySDK.screenshot(driver, bstack111l11lll_opy_)
        bstack11ll111lll_opy_.end(EVENTS.bstack1l11111ll_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏦ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏧ"), True, None, None, None, None, test_name=bstack111l11lll_opy_)
    def bstack1l11l1l1ll1_opy_(self):
        os.environ[bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡆࡔࡆ࡝ࠬᏨ")] = str(self.bstack1l11l1l111l_opy_.success)
        os.environ[bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡇࡕࡇ࡞ࡥࡃࡂࡒࡗ࡙ࡗࡋ࡟ࡎࡑࡇࡉࠬᏩ")] = str(self.bstack1l11l1l111l_opy_.percy_capture_mode)
        self.percy.bstack1l11l1l1lll_opy_(self.bstack1l11l1l111l_opy_.is_percy_auto_enabled)
        self.percy.bstack1l11l1ll1l1_opy_(self.bstack1l11l1l111l_opy_.percy_build_id)