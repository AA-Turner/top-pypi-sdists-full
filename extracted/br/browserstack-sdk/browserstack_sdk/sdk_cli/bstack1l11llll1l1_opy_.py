# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
bstack11ll11_opy_ (u"ࠦࠧࠨࠊࡗࡣࡱ࡭ࡱࡲࡡࡑࡻࡷ࡬ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤ࡙࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡕࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠎ࡙࡮ࡩࡴࠢࡰࡳࡩࡻ࡬ࡦࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤࡪࡼࡥ࡯ࡶࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫ࠥࡧ࡮ࡥࠢࡶࡸࡦࡺࡥࠡ࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠣࡸࡪࡹࡴࡴ࠮ࠍࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡗࡣࡱ࡭ࡱࡲࡡࡋࡣࡹࡥࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥࡧࡧࡦࡰࡷ࠲ࠏࠨࠢࠣᬹ")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1l1ll11111l_opy_, bstack1l1ll1l1l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l111ll1l_opy_,
    TestHookState,
    bstack1ll1ll1ll1l_opy_,
    bstack1111lll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll1l11l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l1l1l1l_opy_ import bstack1l1l1lll1l1_opy_
logger = logging.getLogger(__name__)
class bstack1l11l11l1ll_opy_(TestFramework):
    bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡻࡧ࡮ࡪ࡮࡯ࡥࠥࡖࡹࡵࡪࡲࡲࠥࡺࡥࡴࡶࡶࠤ࠭ࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠯࠮ࠋࠢࠣࠤࠥࡎࡡ࡯ࡦ࡯ࡩࡸࠦࡥࡷࡧࡱࡸࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭ࠬࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠬࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠍࠤࠥࠦࠠࡵࡧࡶࡸࡸࠦࡴࡩࡣࡷࠤࡩࡵ࡮ࠨࡶࠣࡹࡸ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡰࡴࠣࡳࡹ࡮ࡥࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡪࡵࠣࡸ࡭࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡦࡳࡸ࡭ࡻࡧ࡬ࡦࡰࡷࠤࡴ࡬ࠠࡗࡣࡱ࡭ࡱࡲࡡࡋࡣࡹࡥࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࠣࡸ࡭࡫ࠠࡋࡣࡹࡥ࡙ࠥࡄࡌ࠰ࠍࠤࠥࠦࠠࠣࠤࠥᬺ")
    FRAMEWORK_NAME = bstack11ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧᬻ")
    bstack11l111ll1ll_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1l1ll111l_opy_: Dict[str, str] = None,
        bstack1l1l11l1l11_opy_: List[str] = None,
        bstack1l1lll11ll1_opy_: bstack1l1lll1l11l_opy_ = None,
        bstack1l1l111l1_opy_=None
    ):
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠡࡘࡤࡲ࡮ࡲ࡬ࡢࡒࡼࡸ࡭ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࡷ࠿ࠦࡄࡪࡥࡷࠤࡲࡧࡰࡱ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡰࡤࡱࡪࡹࠠࡵࡱࠣࡺࡪࡸࡳࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡲࡦࡳࡥࡴࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡ࡝ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦࡢ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡳࡺࡰࡦࡣࡩ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲ࠻ࠢࡄࡷࡾࡴࡣࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࠤ࡫ࡵࡲࠡࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤ࡮࡬ࡣࡸ࡫ࡲࡷ࡫ࡦࡩ࠿ࠦࡧࡓࡒࡆࠤࡈࡒࡉࠡࡵࡨࡶࡻ࡯ࡣࡦࠢࡦࡰ࡮࡫࡮ࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᬼ")
        if bstack1l1l11l1l11_opy_ is None:
            bstack1l1l11l1l11_opy_ = [self.FRAMEWORK_NAME]
        if bstack1l1l1ll111l_opy_ is None:
            bstack1l1l1ll111l_opy_ = {self.FRAMEWORK_NAME: self._111l1l1ll11_opy_()}
        super().__init__(bstack1l1l11l1l11_opy_, bstack1l1l1ll111l_opy_, bstack1l1lll11ll1_opy_)
        self.bstack1l1l111l1_opy_ = bstack1l1l111l1_opy_
        self._111l1l1l111_opy_: Dict[str, bstack1l1l111ll1l_opy_] = {}
        self._111l1l11lll_opy_: Dict[int, str] = {}
        logger.info(bstack11ll11_opy_ (u"ࠣࡘࡤࡲ࡮ࡲ࡬ࡢࡒࡼࡸ࡭ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵࡀࠦᬽ") + str(bstack1l1l11l1l11_opy_) + bstack11ll11_opy_ (u"ࠤࠥᬾ"))
    def _111l1l1ll11_opy_(self) -> str:
        bstack11ll11_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡑࡻࡷ࡬ࡴࡴࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡵࡷࡶ࡮ࡴࡧ࠯ࠤࠥࠦᬿ")
        return bstack11ll11_opy_ (u"ࠦࢀࢃ࠮ࡼࡿ࠱ࡿࢂࠨᭀ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def bstack11ll11l11l1_opy_(self) -> bool:
        bstack11ll11_opy_ (u"ࠧࠨࠢࡓࡧࡷࡹࡷࡴࠠࡇࡣ࡯ࡷࡪࠦࡡࡴࠢࡷ࡬࡮ࡹࠠࡪࡵࠣࡲࡴࡺࠠࡢࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣᭁ")
        return False
    def bstack11ll1lll11l_opy_(self) -> bool:
        bstack11ll11_opy_ (u"ࠨࠢࠣࡔࡨࡸࡺࡸ࡮ࠡࡈࡤࡰࡸ࡫ࠠࡢࡵࠣࡸ࡭࡯ࡳࠡ࡫ࡶࠤࡳࡵࡴࠡࡣࠣࡶࡴࡨ࡯ࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣᭂ")
        return False
    def track_event(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack11ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࡸࡡࡤ࡭ࠣࡥࠥࡺࡥࡴࡶࠣࡰ࡮࡬ࡥࡤࡻࡦࡰࡪࠦࡥࡷࡧࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡵࡧࡻࡸ࠿ࠦࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࡉ࡯࡯ࡶࡨࡼࡹࠦࡷࡪࡶ࡫ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡯ࡣࡰࡩ࠱ࠦࡶࡦࡴࡶ࡭ࡴࡴࠬࠡࡣࡱࡨࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡰࡧࡩࡽࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠾࡚ࠥࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡷࡹࡧࡴࡦࠢࠫࡍࡓࡏࡔࡠࡖࡈࡗ࡙࠲ࠠࡕࡇࡖࡘ࠱ࠦࡥࡵࡥ࠱࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩ࠿ࠦࡐࡳࡧࠣࡳࡷࠦࡐࡰࡵࡷࠤ࡭ࡵ࡯࡬ࠢࡶࡸࡦࡺࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠪࡢࡴࡪࡷ࠿ࠦࡁࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࠨࡵࡻࡳ࡭ࡨࡧ࡬࡭ࡻࠣࡘࡪࡹࡴࡅࡣࡷࡥࠥࡵࡲࠡࡦ࡬ࡧࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠰ࠪ࡬ࡹࡤࡶ࡬ࡹ࠺ࠡࡃࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࠥࡱࡥࡺࡹࡲࡶࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᭃ")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack11ll11_opy_ (u"ࠣࡋࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡵࡷࡥࡹ࡫࠽᭄ࠣ") + str(test_framework_state) + bstack11ll11_opy_ (u"ࠤࠥᭅ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack11ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᭆ") + str(kwargs) + bstack11ll11_opy_ (u"ࠦࠧᭇ"))
            return
        instance = self._111l1l111ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack11ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡧࡶࡳࡱࡼࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤᭈ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠨࠢᭉ"))
            return
        try:
            self._111l1l1l1l1_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡࡧࡹࡩࡳࡺࠠࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࡀࠠࠣᭊ") + str(e) + bstack11ll11_opy_ (u"ࠣࠤᭋ"))
        self.bstack11l111ll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _111l1l1l1l1_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack11ll11_opy_ (u"ࠤࠥࠦࡍࡧ࡮ࡥ࡮ࡨࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦࡥࡷࡧࡱࡸࠥࡺࡹࡱࡧࡶ࠲ࠧࠨࠢᭌ")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.bstack1l1llll1l1l_opy_(instance, TestFramework.bstack11l1ll1llll_opy_):
                bstack1llll11llll_opy_ = self._111l1l11ll1_opy_(args, kwargs)
                if bstack1llll11llll_opy_:
                    instance.data.update(bstack1llll11llll_opy_)
                    logger.debug(bstack11ll11_opy_ (u"ࠥࡐࡴࡧࡤࡦࡦࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭍") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠦࠧ᭎"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.bstack1l1llll1l1l_opy_(instance, TestFramework.bstack11ll11lll1l_opy_):
                    TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11ll11lll1l_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack11ll11_opy_ (u"࡙ࠧࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭏") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠨࠢ᭐"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.bstack1l1llll1l1l_opy_(instance, TestFramework.bstack11ll1l1111l_opy_):
                    TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11ll1l1111l_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack11ll11_opy_ (u"ࠢࡔࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭑") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠣࠤ᭒"))
                self._111l1l1l11l_opy_(instance, *args, **kwargs)
                self.__111llll111l_opy_(instance)
                self.__111l1l11111_opy_(instance)
        elif test_framework_state in bstack1l11l11l1ll_opy_.bstack11l111ll1ll_opy_:
            self._111l1l11l1l_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack11ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ᭓") + str(instance.ref()) + bstack11ll11_opy_ (u"ࠥࠦ᭔"))
    def _111l1l111ll_opy_(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[bstack1l1l111ll1l_opy_]:
        bstack11ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡷࡴࡲࡶࡦࠢࡲࡶࠥࡩࡲࡦࡣࡷࡩࠥࡧࠠࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡔࡦࡵࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡏࡎࡊࡖࡢࡘࡊ࡙ࡔࠡࡒࡕࡉ࠱ࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡱࡩࡼࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡰࡶ࡫ࡩࡷࠦࡥࡷࡧࡱࡸࡸ࠲ࠠ࡭ࡱࡲ࡯ࡸࠦࡵࡱࠢࡷ࡬ࡪࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᭕")
        target = self._111l1l1l1ll_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._111l11ll1ll_opy_(context, target)
            self._111l1l11lll_opy_[thread_id] = target
            return instance
        if target and target in self._111l1l1l111_opy_:
            return self._111l1l1l111_opy_[target]
        bstack111l1l111l1_opy_ = self._111l1l11lll_opy_.get(thread_id)
        if bstack111l1l111l1_opy_ and bstack111l1l111l1_opy_ in self._111l1l1l111_opy_:
            return self._111l1l1l111_opy_[bstack111l1l111l1_opy_]
        instance = TestFramework.bstack1l1ll1ll111_opy_(target) if target else None
        if instance:
            return instance
        logger.debug(bstack11ll11_opy_ (u"ࠧࡔ࡯ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡶ࡫ࡶࡪࡧࡤࡠ࡫ࡧࡁࠧ᭖") + str(thread_id) + bstack11ll11_opy_ (u"ࠨࠢ᭗"))
        return None
    def _111l11ll1ll_opy_(
        self,
        context: bstack1ll1ll1ll1l_opy_,
        target: str
    ) -> bstack1l1l111ll1l_opy_:
        bstack11ll11_opy_ (u"ࠢࠣࠤࡆࡶࡪࡧࡴࡦࠢࡤࠤࡳ࡫ࡷࠡࡶࡨࡷࡹࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭࠮ࠣࠤࠥ᭘")
        ctx = bstack1l1ll11111l_opy_.create_context(target)
        instance = bstack1l1l111ll1l_opy_(
            ctx,
            self.bstack1l1l11l1l11_opy_,
            self.bstack1l1l1ll111l_opy_,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.bstack11l1111llll_opy_(instance, {
            TestFramework.bstack1l111l11l1l_opy_: str(uuid4()),
            TestFramework.bstack1l111ll1111_opy_: context.test_framework_name,
            TestFramework.bstack11lll1l111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1111lll1_opy_: [],
            TestFramework.bstack11l1l1lll1l_opy_: TestFramework.bstack11l111l1ll1_opy_,
        })
        if context.platform_index >= 0:
            TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack1l111l1lll1_opy_, context.platform_index)
        self._111l1l1l111_opy_[target] = instance
        TestFramework.bstack11111l111l_opy_[ctx.id] = instance
        logger.debug(bstack11ll11_opy_ (u"ࠣࡅࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡴࡦࡵࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡩࡴࡹ࠰࡬ࡨࡂࠨ᭙") + str(ctx.id) + bstack11ll11_opy_ (u"ࠤࠥ᭚"))
        return instance
    def _111l1l1l1ll_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack11ll11_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡴࡪࡩࡹࠦࠨࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠬࠤ࡫ࡸ࡯࡮ࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠳ࠨࠢࠣ᭛")
        if args and hasattr(args[0], bstack11ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᭜")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᭝")) or
                    args[0].get(bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡒࡦࡳࡥࠨ᭞")) or
                    args[0].get(bstack11ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᭟")) or
                    args[0].get(TestFramework.bstack1l11111l111_opy_))
        return (kwargs.get(bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫ᭠")) or
                kwargs.get(bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺࡎࡢ࡯ࡨࠫ᭡")) or
                kwargs.get(bstack11ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᭢")))
    def _111l1l11ll1_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack11ll11_opy_ (u"ࠦࠧࠨࡐࡢࡴࡶࡩࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢ࡬ࡲࡹࡵࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡧࡥࡹࡧࠠࡧࡱࡵࡱࡦࡺ࠮ࠣࠤࠥ᭣")
        if not args:
            return None
        data = None
        bstack111l1l11l11_opy_ = args[0]
        if hasattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᭤")) and hasattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫ᭥")):
            bstack111l11lllll_opy_ = getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭᭦"), [])
            bstack111l11lll11_opy_ = getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡪࡦࠪ᭧"), None)
            bstack111l1l1ll1l_opy_ = getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ᭨"), {})
            file_path = getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭࠭᭩"), None)
            test_name = bstack111l1l11l11_opy_.name
            if not bstack111l11lll11_opy_ and file_path and test_name:
                bstack111l11lll11_opy_ = bstack11ll11_opy_ (u"ࠦࢀࢃ࠺࠻ࡽࢀࠦ᭪").format(file_path, test_name)
            data = {
                TestFramework.bstack1l111l11l1l_opy_: bstack111l1l11l11_opy_.uuid,
                TestFramework.bstack11l1ll1llll_opy_: bstack111l1l11l11_opy_.uuid,
                TestFramework.bstack1l11111l111_opy_: test_name,
                TestFramework.bstack111ll1llll1_opy_: file_path,
                TestFramework.bstack11l111l1l1l_opy_: getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪ᭫"), None),
                TestFramework.bstack111llll1ll1_opy_: getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"࠭ࡴࡢࡩࡶ᭬ࠫ"), []),
                TestFramework.bstack111ll11ll1l_opy_: bstack111l11lllll_opy_,
                bstack11ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧ᭭"): bstack111l11lllll_opy_,
                TestFramework.bstack111llllll1l_opy_: getattr(bstack111l1l11l11_opy_, bstack11ll11_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭᭮"), {}),
                TestFramework.bstack11l11ll111l_opy_: test_name,
                bstack11ll11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫ᭯"): {},
                TestFramework.bstack11ll111ll11_opy_: bstack111l11lll11_opy_,
                bstack11ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ᭰"): bstack111l1l1ll1l_opy_,
            }
            data[bstack11ll11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧ᭱")] = {bstack11ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩ᭲"): bstack111l11lll11_opy_}
        elif isinstance(bstack111l1l11l11_opy_, dict):
            bstack111l11lllll_opy_ = bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭᭳")) or bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭᭴"), [])
            bstack111l11lll11_opy_ = bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡪࡦࠪ᭵")) or bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡊࡦࠪ᭶"))
            bstack111l1l1ll1l_opy_ = bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ᭷"), {})
            file_path = bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠧ᭸")) or bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠧ᭹"))
            test_name = bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᭺")) or bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠧࡵࡧࡶࡸࡓࡧ࡭ࡦࠩ᭻"))
            if not bstack111l11lll11_opy_ and file_path and test_name:
                bstack111l11lll11_opy_ = bstack11ll11_opy_ (u"ࠣࡽࢀ࠾࠿ࢁࡽࠣ᭼").format(file_path, test_name)
            data = {
                TestFramework.bstack1l111l11l1l_opy_: bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᭽")) or bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡊࡦࠪ᭾")) or str(uuid4()),
                TestFramework.bstack11l1ll1llll_opy_: bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡋࡧࠫ᭿")) or bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪᮀ")),
                TestFramework.bstack1l11111l111_opy_: test_name,
                TestFramework.bstack111ll1llll1_opy_: file_path,
                TestFramework.bstack11l111l1l1l_opy_: bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"࠭ࡣࡰࡦࡨࠫᮁ")),
                TestFramework.bstack111llll1ll1_opy_: bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᮂ"), []),
                TestFramework.bstack111ll11ll1l_opy_: bstack111l11lllll_opy_,
                bstack11ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᮃ"): bstack111l11lllll_opy_,
                TestFramework.bstack111llllll1l_opy_: bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠩࡰࡩࡹࡧࠧᮄ"), {}),
                TestFramework.bstack11l11ll111l_opy_: bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᮅ")) or test_name,
                bstack11ll11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ᮆ"): bstack111l1l11l11_opy_.get(bstack11ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧᮇ"), {}),
                TestFramework.bstack11ll111ll11_opy_: bstack111l11lll11_opy_,
                bstack11ll11_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᮈ"): bstack111l1l1ll1l_opy_,
            }
            data[bstack11ll11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᮉ")] = {bstack11ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᮊ"): bstack111l11lll11_opy_}
        return data
    def _111l1l1l11l_opy_(self, instance: bstack1l1l111ll1l_opy_, *args, **kwargs):
        bstack11ll11_opy_ (u"ࠤࠥࠦࡑࡵࡡࡥࠢࡷࡩࡸࡺࠠࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡ࡫ࡱࡸࡴࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠤࠥࠦᮋ")
        bstack111l11llll1_opy_ = None
        if args and hasattr(args[0], bstack11ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᮌ")) and args[0].result:
            bstack1llll11llll_opy_ = args[0]
            result = bstack1llll11llll_opy_.result
            bstack111l11llll1_opy_ = {
                TestFramework.bstack11l1l1lll1l_opy_: getattr(result, bstack11ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᮍ"), bstack11ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬࠭ᮎ")),
                TestFramework.bstack11l1ll1lll1_opy_: None,
                TestFramework.bstack11l111l111l_opy_: None,
            }
            if hasattr(result, bstack11ll11_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠩᮏ")) and result.exception:
                bstack111l11llll1_opy_[TestFramework.bstack11l1ll1lll1_opy_] = [{bstack11ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᮐ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack11ll11_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࠫᮑ")) else None
                bstack111l11llll1_opy_[TestFramework.bstack11l111l111l_opy_] = exc_type or bstack11ll11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᮒ")
            bstack111l1l1ll1l_opy_ = getattr(bstack1llll11llll_opy_, bstack11ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᮓ"), None)
            if bstack111l1l1ll1l_opy_:
                bstack111l11llll1_opy_[bstack11ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᮔ")] = bstack111l1l1ll1l_opy_
                logger.debug(bstack11ll11_opy_ (u"࡛ࠧࡰࡥࡣࡷࡩࡩࠦࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠥࡧࡴࠡࡒࡒࡗ࡙ࠦࡴࡪ࡯ࡨ࠾ࠥࠨᮕ") + str(list(bstack111l1l1ll1l_opy_.keys()) if bstack111l1l1ll1l_opy_ else []) + bstack11ll11_opy_ (u"ࠨࠢᮖ"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack111l11llll1_opy_ = {
                TestFramework.bstack11l1l1lll1l_opy_: data.get(bstack11ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᮗ"), TestFramework.bstack11l111l1ll1_opy_),
                TestFramework.bstack11l1ll1lll1_opy_: data.get(bstack11ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᮘ")),
                TestFramework.bstack11l111l111l_opy_: data.get(bstack11ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨᮙ")),
            }
            bstack111l1l1ll1l_opy_ = data.get(bstack11ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᮚ"))
            if bstack111l1l1ll1l_opy_:
                bstack111l11llll1_opy_[bstack11ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᮛ")] = bstack111l1l1ll1l_opy_
                logger.debug(bstack11ll11_opy_ (u"࡛ࠧࡰࡥࡣࡷࡩࡩࠦࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠥࡧࡴࠡࡒࡒࡗ࡙ࠦࡴࡪ࡯ࡨ࠾ࠥࠨᮜ") + str(list(bstack111l1l1ll1l_opy_.keys()) if bstack111l1l1ll1l_opy_ else []) + bstack11ll11_opy_ (u"ࠨࠢᮝ"))
        if bstack111l11llll1_opy_:
            if bstack111l11llll1_opy_.get(TestFramework.bstack11l1l1lll1l_opy_) != TestFramework.bstack11l111l1ll1_opy_:
                bstack111l11llll1_opy_[TestFramework.bstack11ll1l11111_opy_] = datetime.now(tz=timezone.utc)
            TestFramework.bstack11l1111llll_opy_(instance, bstack111l11llll1_opy_)
            logger.debug(bstack11ll11_opy_ (u"ࠢࡍࡱࡤࡨࡪࡪࠠࡵࡧࡶࡸࠥࡸࡥࡴࡷ࡯ࡸ࠿ࠦࠢᮞ") + str(bstack111l11llll1_opy_.get(TestFramework.bstack11l1l1lll1l_opy_)) + bstack11ll11_opy_ (u"ࠣࠤᮟ"))
    def _111l1l11l1l_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack11ll11_opy_ (u"ࠤ࡙ࠥࠦࡸࡡࡤ࡭ࠣ࡬ࡴࡵ࡫ࠡࡧࡹࡩࡳࡺࡳࠡࠪࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠲ࠠࡂࡈࡗࡉࡗࡥࡁࡍࡎ࠯ࠤࡪࡺࡣ࠯ࠫ࠱ࠦࠧࠨᮠ")
        key = test_framework_state.name
        bstack111lll11l11_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠪᮡ"), {})
        if key not in bstack111lll11l11_opy_:
            bstack111lll11l11_opy_[key] = []
        bstack11l11111lll_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, bstack11ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠬᮢ"), {})
        if key not in bstack11l11111lll_opy_:
            bstack11l11111lll_opy_[key] = []
        bstack11l111lll1l_opy_ = {
            bstack11ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠬᮣ"): bstack111lll11l11_opy_,
            bstack11ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠧᮤ"): bstack11l11111lll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack11ll11_opy_ (u"ࠢ࡬ࡧࡼࠦᮥ"): key,
                TestFramework.bstack111ll1lll1l_opy_: str(uuid4()),
                TestFramework.bstack111lll1l111_opy_: TestFramework.bstack111lll1111l_opy_,
                TestFramework.bstack111llllll11_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll1lll11_opy_: [],
                TestFramework.bstack11l111ll1l1_opy_: kwargs.get(bstack11ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᮦ"), key),
            }
            bstack111lll11l11_opy_[key].append(hook)
            bstack11l111lll1l_opy_[bstack11ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᮧ")] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l11111l1l_opy_ = bstack111lll11l11_opy_.get(key, [])
            hook = bstack11l11111l1l_opy_.pop() if bstack11l11111l1l_opy_ else None
            if hook:
                hook[TestFramework.bstack111lll11ll1_opy_] = datetime.now(tz=timezone.utc)
                bstack11l11111lll_opy_[key].append(hook)
                bstack11l111lll1l_opy_[bstack11ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠨᮨ")] = key
        TestFramework.bstack11l1111llll_opy_(instance, bstack11l111lll1l_opy_)
        logger.debug(bstack11ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡽ࡮ࡩࡾࢃ࠮ࠣᮩ") + str(test_hook_state) + bstack11ll11_opy_ (u"ࠧࠨ᮪"))
    def bstack11lll1ll11l_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState]
    ) -> List[bstack1111lll111_opy_]:
        bstack11ll11_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡲ࡯ࡨࠢࡨࡲࡹࡸࡩࡦࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣ࡬ࡴࡵ࡫ࠡࡵࡷࡥࡹ࡫࠮ࠣࠤ᮫ࠥ")
        if instance is None:
            return []
        return TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1111lll1_opy_, [])
    def bstack11ll11llll1_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack11ll11_opy_ (u"ࠢࠣࠤࡆࡰࡪࡧࡲࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡨࡰࡱ࡮ࠤࡸࡺࡡࡵࡧ࠱ࠦࠧࠨᮬ")
        if instance is None:
            return
        TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11l1111lll1_opy_, [])
    def get_current_test_instance(self) -> Optional[bstack1l1l111ll1l_opy_]:
        bstack11ll11_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡪࡵࡩࡦࡪ࠮ࠣࠤࠥᮭ")
        thread_id = threading.get_ident()
        target = self._111l1l11lll_opy_.get(thread_id)
        if target:
            return self._111l1l1l111_opy_.get(target)
        return None
    def bstack111l1l1111l_opy_(
        self,
        instance: bstack1l1l111ll1l_opy_,
        log_entry: bstack1111lll111_opy_
    ):
        bstack11ll11_opy_ (u"ࠤࠥࠦࡆࡪࡤࠡࡣࠣࡰࡴ࡭ࠠࡦࡰࡷࡶࡾࠦࡴࡰࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠤࠥࠦᮮ")
        if instance is None:
            return
        logs = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11l1111lll1_opy_, [])
        logs.append(log_entry)
        TestFramework.bstack1l1l1111l1_opy_(instance, TestFramework.bstack11l1111lll1_opy_, logs)
    def __111llll111l_opy_(self, instance: bstack1l1l111ll1l_opy_) -> None:
        bstack11ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᮯ")
        bstack11l111lll1l_opy_ = {bstack11ll11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨ᮰"): bstack1l1l1lll1l1_opy_.bstack111ll1l111l_opy_()}
        TestFramework.bstack11l1111llll_opy_(instance, bstack11l111lll1l_opy_)
    def __111l1l11111_opy_(self, instance: bstack1l1l111ll1l_opy_) -> None:
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡥࡴࡶ࠰ࡰࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡶࡲ࡯ࡳࡦࡪࡥࡥࠢࡹ࡭ࡦࠦࡆࡪ࡮ࡨ࡙ࡵࡲ࡯ࡢࡦࡨࡶ࠳ࡻࡰ࡭ࡱࡤࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠪࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡤࡣࡱࡷࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧ࡮ࡥࠢࡶࡩࡳࡪࡳࠡ࡮ࡲ࡫ࡸࠦࡶࡪࡣࠣ࡫ࡗࡖࡃ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᮱")
        from bstack_utils.helper import bstack11ll1ll11ll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭᮲"), bstack11ll11_opy_ (u"ࠧ࠱ࠩ᮳"))
            bstack11lll11ll11_opy_ = os.path.join(
                bstack11ll1ll11ll_opy_(),
                bstack11ll11_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࡼࡿࠥ᮴").format(platform_index),
                bstack11ll11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧ᮵")
            )
            if not os.path.isdir(bstack11lll11ll11_opy_):
                logger.debug(bstack11ll11_opy_ (u"ࠥࡒࡴࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤ࠻ࠢࠥ᮶") + str(bstack11lll11ll11_opy_) + bstack11ll11_opy_ (u"ࠦࠧ᮷"))
                return
            bstack11ll11ll1ll_opy_ = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l11l1l_opy_, bstack11ll11_opy_ (u"ࠧࠨ᮸"))
            bstack111l11lll1l_opy_ = []
            for file_name in os.listdir(bstack11lll11ll11_opy_):
                file_path = os.path.join(bstack11lll11ll11_opy_, file_name)
                if os.path.isfile(file_path):
                    try:
                        bstack11ll1ll1lll_opy_ = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(bstack11ll1ll1lll_opy_, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = bstack1111lll111_opy_(
                            kind=bstack11ll11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣ᮹"),
                            message=bstack11ll11_opy_ (u"ࠢࠣᮺ"),
                            level=bstack11ll11_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᮻ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            bstack11lll1111l1_opy_=file_size,
                            bstack11ll1llllll_opy_=bstack11ll11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᮼ"),
                            bstack1l1l1l1_opy_=os.path.abspath(file_path),
                            bstack111l1l11_opy_=bstack11ll11ll1ll_opy_
                        )
                        bstack111l11lll1l_opy_.append(log_entry)
                        logger.debug(bstack11ll11_opy_ (u"ࠥࡅࡩࡪࡥࡥࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦ࡬ࡰࡩࠣࡩࡳࡺࡲࡺ࠼ࠣࠦᮽ") + str(file_name) + bstack11ll11_opy_ (u"ࠦࠧᮾ"))
                    except Exception as bstack11lll11l1ll_opy_:
                        logger.error(bstack11ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧᮿ") + str(bstack11lll11l1ll_opy_) + bstack11ll11_opy_ (u"ࠨࠢᯀ"))
            if bstack111l11lll1l_opy_ and self.bstack1l1l111l1_opy_:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack11ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᯁ"), bstack11ll11_opy_ (u"ࠣࠤᯂ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᯃ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack111l11lll1l_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack11ll11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦᯄ")
                        log_entry.test_framework_version = TestFramework.bstack1ll111l1111_opy_(instance, TestFramework.bstack11lll1l111l_opy_, bstack11ll11_opy_ (u"ࠦࠧᯅ"))
                        log_entry.uuid = bstack11ll11ll1ll_opy_
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack11l11l1llll_opy_ (u"ࠧࠨᯆ")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.bstack11lll1111l1_opy_
                        log_entry.file_path = entry.bstack1l1l1l1_opy_
                    self.bstack1l1l111l1_opy_.LogCreatedEvent(req)
                    logger.debug(bstack11ll11_opy_ (u"ࠨࡓࡦࡰࡷࠤࠧᯇ") + str(len(bstack111l11lll1l_opy_)) + bstack11ll11_opy_ (u"ࠢࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡲ࡯ࡨࡵࠣࡺ࡮ࡧࠠࡨࡔࡓࡇࠧᯈ"))
                except Exception as bstack111l1l11l_opy_:
                    logger.error(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡲ࡯ࡨࡵࠣࡺ࡮ࡧࠠࡨࡔࡓࡇ࠿ࠦࠢᯉ") + str(bstack111l1l11l_opy_) + bstack11ll11_opy_ (u"ࠤࠥᯊ"))
        except Exception as e:
            logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷ࠱ࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠻ࠢࠥᯋ") + str(e) + bstack11ll11_opy_ (u"ࠦࠧᯌ"))