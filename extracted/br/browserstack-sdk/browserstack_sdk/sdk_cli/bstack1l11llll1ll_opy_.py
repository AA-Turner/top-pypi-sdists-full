# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
bstack1ll_opy_ (u"ࠢࠣࠤࠍ࡚ࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡕࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡑࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠴ࠊࡕࡪ࡬ࡷࠥࡳ࡯ࡥࡷ࡯ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡦࡸࡨࡲࡹࠦࡴࡳࡣࡦ࡯࡮ࡴࡧࠡࡣࡱࡨࠥࡹࡴࡢࡶࡨࠤࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠡࡨࡲࡶࠥࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨࠦࡴࡦࡵࡷࡷ࠱ࠐࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡎࡦࡼࡡࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡࡣࡪࡩࡳࡺ࠮ࠋࠤࠥࠦᬼ")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.bstack1l1ll11111l_opy_ import bstack1l1ll1l1l11_opy_, bstack1l1ll1llll1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11l11ll_opy_,
    TestHookState,
    bstack1ll1ll1ll11_opy_,
    bstack111l1111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll11ll1_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11l111lll_opy_ import bstack1l11lll1lll_opy_
logger = logging.getLogger(__name__)
class bstack1l1l1l11111_opy_(TestFramework):
    bstack1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡷࡣࡱ࡭ࡱࡲࡡࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡶࡨࡷࡹࡹࠠࠩࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠫ࠱ࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡨࡺࡪࡴࡴࠡࡶࡵࡥࡨࡱࡩ࡯ࡩ࠯ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦ࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶ࠯ࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠐࠠࠡࠢࠣࡸࡪࡹࡴࡴࠢࡷ࡬ࡦࡺࠠࡥࡱࡱࠫࡹࠦࡵࡴࡧࠣࡴࡾࡺࡥࡴࡶࠣࡳࡷࠦ࡯ࡵࡪࡨࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣ࡭ࡸࠦࡴࡩࡧࠣࡔࡾࡺࡨࡰࡰࠣࡩࡶࡻࡩࡷࡣ࡯ࡩࡳࡺࠠࡰࡨ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡎࡦࡼࡡࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡࡕࡇࡏ࠳ࠐࠠࠡࠢࠣࠦࠧࠨᬽ")
    FRAMEWORK_NAME = bstack1ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᬾ")
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1ll1l_opy_: Dict[str, str] = None,
        bstack1l1l111111l_opy_: List[str] = None,
        bstack1l1lll11ll1_opy_: bstack1l1lll11l11_opy_ = None,
        bstack1ll11ll11l_opy_=None
    ):
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠤ࡛ࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࡳ࠻ࠢࡇ࡭ࡨࡺࠠ࡮ࡣࡳࡴ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡳࡧ࡭ࡦࡵࠣࡸࡴࠦࡶࡦࡴࡶ࡭ࡴࡴࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡮ࡢ࡯ࡨࡷࠥ࠮ࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡠࠨࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠢ࡞ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡶࡽࡳࡩ࡟ࡥ࡫ࡶࡴࡦࡺࡣࡩࡧࡵ࠾ࠥࡇࡳࡺࡰࡦࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࠠࡧࡱࡵࠤࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥ࠻ࠢࡪࡖࡕࡉࠠࡄࡎࡌࠤࡸ࡫ࡲࡷ࡫ࡦࡩࠥࡩ࡬ࡪࡧࡱࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᬿ")
        if bstack1l1l111111l_opy_ is None:
            bstack1l1l111111l_opy_ = [self.FRAMEWORK_NAME]
        if bstack1l11ll1ll1l_opy_ is None:
            bstack1l11ll1ll1l_opy_ = {self.FRAMEWORK_NAME: self._111l11llll1_opy_()}
        super().__init__(bstack1l1l111111l_opy_, bstack1l11ll1ll1l_opy_, bstack1l1lll11ll1_opy_)
        self.bstack1ll11ll11l_opy_ = bstack1ll11ll11l_opy_
        self._111l1l111l1_opy_: Dict[str, bstack1l1l11l11ll_opy_] = {}
        self._111l11ll1ll_opy_: Dict[int, str] = {}
        logger.info(bstack1ll_opy_ (u"࡛ࠦࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧࠤࡼ࡯ࡴࡩࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸࡃࠢᭀ") + str(bstack1l1l111111l_opy_) + bstack1ll_opy_ (u"ࠧࠨᭁ"))
    def _111l11llll1_opy_(self) -> str:
        bstack1ll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡔࡾࡺࡨࡰࡰࠣࡺࡪࡸࡳࡪࡱࡱࠤࡸࡺࡲࡪࡰࡪ࠲ࠧࠨࠢᭂ")
        return bstack1ll_opy_ (u"ࠢࡼࡿ࠱ࡿࢂ࠴ࡻࡾࠤᭃ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def bstack11ll1l11lll_opy_(self) -> bool:
        bstack1ll_opy_ (u"ࠣࠤࠥࡖࡪࡺࡵࡳࡰࠣࡊࡦࡲࡳࡦࠢࡤࡷࠥࡺࡨࡪࡵࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡥࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤ᭄ࠥࠦ")
        return False
    def bstack11ll1ll1l11_opy_(self) -> bool:
        bstack1ll_opy_ (u"ࠤࠥࠦࡗ࡫ࡴࡶࡴࡱࠤࡋࡧ࡬ࡴࡧࠣࡥࡸࠦࡴࡩ࡫ࡶࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡦࠦࡲࡰࡤࡲࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᭅ")
        return False
    def track_event(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡴࡤࡧࡰࠦࡡࠡࡶࡨࡷࡹࠦ࡬ࡪࡨࡨࡧࡾࡩ࡬ࡦࠢࡨࡺࡪࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡸࡪࡾࡴ࠻ࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡅࡲࡲࡹ࡫ࡸࡵࠢࡺ࡭ࡹ࡮ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡲࡦࡳࡥ࠭ࠢࡹࡩࡷࡹࡩࡰࡰ࠯ࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠺ࠡࡖ࡫ࡩࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡳࡵࡣࡷࡩࠥ࠮ࡉࡏࡋࡗࡣ࡙ࡋࡓࡕ࠮ࠣࡘࡊ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠻ࠢࡓࡶࡪࠦ࡯ࡳࠢࡓࡳࡸࡺࠠࡩࡱࡲ࡯ࠥࡹࡴࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠭ࡥࡷ࡭ࡳ࠻ࠢࡄࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࠫࡸࡾࡶࡩࡤࡣ࡯ࡰࡾࠦࡔࡦࡵࡷࡈࡦࡺࡡࠡࡱࡵࠤࡩ࡯ࡣࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠬ࠭࡯ࡼࡧࡲࡨࡵ࠽ࠤࡆࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᭆ")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack1ll_opy_ (u"ࠦࡎ࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡸࡺࡡࡵࡧࡀࠦᭇ") + str(test_framework_state) + bstack1ll_opy_ (u"ࠧࠨᭈ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack1ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᭉ") + str(kwargs) + bstack1ll_opy_ (u"ࠢࠣᭊ"))
            return
        instance = self._111l1l11l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack1ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡪࡹ࡯࡭ࡸࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧᭋ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠤࠥᭌ"))
            return
        try:
            self._111l1l11111_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤࡪࡼࡥ࡯ࡶࠣࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾ࠼ࠣࠦ᭍") + str(e) + bstack1ll_opy_ (u"ࠦࠧ᭎"))
        self.bstack111ll1ll1l1_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _111l1l11111_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll_opy_ (u"ࠧࠨࠢࡉࡣࡱࡨࡱ࡫ࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࠢࡨࡺࡪࡴࡴࠡࡶࡼࡴࡪࡹ࠮ࠣࠤࠥ᭏")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11l1ll11111_opy_):
                bstack1llll11l111_opy_ = self._111l1l1111l_opy_(args, kwargs)
                if bstack1llll11l111_opy_:
                    instance.data.update(bstack1llll11l111_opy_)
                    logger.debug(bstack1ll_opy_ (u"ࠨࡌࡰࡣࡧࡩࡩࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᭐") + str(instance.ref()) + bstack1ll_opy_ (u"ࠢࠣ᭑"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11ll1l11ll1_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack1ll_opy_ (u"ࠣࡕࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᭒") + str(instance.ref()) + bstack1ll_opy_ (u"ࠤࠥ᭓"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.bstack1ll11111lll_opy_(instance, TestFramework.bstack11lll111111_opy_):
                    TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack11lll111111_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack1ll_opy_ (u"ࠥࡗࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᭔") + str(instance.ref()) + bstack1ll_opy_ (u"ࠦࠧ᭕"))
                self._111l11l1lll_opy_(instance, *args, **kwargs)
                self.__11l11111l11_opy_(instance)
                self.__111l1l11l11_opy_(instance)
        elif test_framework_state in bstack1l1l1l11111_opy_.bstack111ll1l1l1l_opy_:
            self._111l11lll11_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack1ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭖") + str(instance.ref()) + bstack1ll_opy_ (u"ࠨࠢ᭗"))
    def _111l1l11l1l_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[bstack1l1l11l11ll_opy_]:
        bstack1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡳࡰ࡮ࡹࡩࠥࡵࡲࠡࡥࡵࡩࡦࡺࡥࠡࡣࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡗࡩࡸࡺࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡋࡑࡍ࡙ࡥࡔࡆࡕࡗࠤࡕࡘࡅ࠭ࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡴࡥࡸࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡳࡹ࡮ࡥࡳࠢࡨࡺࡪࡴࡴࡴ࠮ࠣࡰࡴࡵ࡫ࡴࠢࡸࡴࠥࡺࡨࡦࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᭘")
        target = self._111l11ll1l1_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._111l1l11ll1_opy_(context, target)
            self._111l11ll1ll_opy_[thread_id] = target
            return instance
        if target and target in self._111l1l111l1_opy_:
            return self._111l1l111l1_opy_[target]
        bstack111l11ll111_opy_ = self._111l11ll1ll_opy_.get(thread_id)
        if bstack111l11ll111_opy_ and bstack111l11ll111_opy_ in self._111l1l111l1_opy_:
            return self._111l1l111l1_opy_[bstack111l11ll111_opy_]
        instance = TestFramework.bstack1l1ll1lll1l_opy_(target) if target else None
        if instance:
            return instance
        logger.debug(bstack1ll_opy_ (u"ࠣࡐࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡹ࡮ࡲࡦࡣࡧࡣ࡮ࡪ࠽ࠣ᭙") + str(thread_id) + bstack1ll_opy_ (u"ࠤࠥ᭚"))
        return None
    def _111l1l11ll1_opy_(
        self,
        context: bstack1ll1ll1ll11_opy_,
        target: str
    ) -> bstack1l1l11l11ll_opy_:
        bstack1ll_opy_ (u"ࠥࠦࠧࡉࡲࡦࡣࡷࡩࠥࡧࠠ࡯ࡧࡺࠤࡹ࡫ࡳࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡲࠡࡶࡵࡥࡨࡱࡩ࡯ࡩ࠱ࠦࠧࠨ᭛")
        ctx = bstack1l1ll1l1l11_opy_.create_context(target)
        instance = bstack1l1l11l11ll_opy_(
            ctx,
            self.bstack1l1l111111l_opy_,
            self.bstack1l11ll1ll1l_opy_,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.bstack111lllllll1_opy_(instance, {
            TestFramework.bstack1l1111ll1l1_opy_: str(uuid4()),
            TestFramework.bstack1l11111111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l11ll_opy_: context.test_framework_version,
            TestFramework.bstack111ll11llll_opy_: [],
            TestFramework.bstack11l1ll11lll_opy_: TestFramework.bstack11l111ll111_opy_,
        })
        if context.platform_index >= 0:
            TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack1l1111l11l1_opy_, context.platform_index)
        self._111l1l111l1_opy_[target] = instance
        TestFramework.bstack1l111l11l_opy_[ctx.id] = instance
        logger.debug(bstack1ll_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨࠥࡴࡥࡸࠢࡷࡩࡸࡺࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡷࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡥࡷࡼ࠳࡯ࡤ࠾ࠤ᭜") + str(ctx.id) + bstack1ll_opy_ (u"ࠧࠨ᭝"))
        return instance
    def _111l11ll1l1_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack1ll_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥࡷ࡭ࡥࡵࠢࠫࡸࡪࡹࡴࠡࡰࡤࡱࡪ࠯ࠠࡧࡴࡲࡱࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࠯ࠤࠥࠦ᭞")
        if args and hasattr(args[0], bstack1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᭟")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭᭠")) or
                    args[0].get(bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡎࡢ࡯ࡨࠫ᭡")) or
                    args[0].get(bstack1ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᭢")) or
                    args[0].get(TestFramework.bstack1l111111lll_opy_))
        return (kwargs.get(bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧ᭣")) or
                kwargs.get(bstack1ll_opy_ (u"ࠬࡺࡥࡴࡶࡑࡥࡲ࡫ࠧ᭤")) or
                kwargs.get(bstack1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᭥")))
    def _111l1l1111l_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack1ll_opy_ (u"ࠢࠣࠤࡓࡥࡷࡹࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮ࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡯࡮ࡵࡱࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡪࡡࡵࡣࠣࡪࡴࡸ࡭ࡢࡶ࠱ࠦࠧࠨ᭦")
        if not args:
            return None
        data = None
        bstack111l1l111ll_opy_ = args[0]
        if hasattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭᭧")) and hasattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧ᭨")):
            bstack111l11l1ll1_opy_ = getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ᭩"), [])
            bstack111l11ll11l_opy_ = getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢ࡭ࡩ࠭᭪"), None)
            bstack111l11lllll_opy_ = getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ᭫"), {})
            file_path = getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡵࡧࡴࡩ᭬ࠩ"), None)
            test_name = bstack111l1l111ll_opy_.name
            if not bstack111l11ll11l_opy_ and file_path and test_name:
                bstack111l11ll11l_opy_ = bstack1ll_opy_ (u"ࠢࡼࡿ࠽࠾ࢀࢃࠢ᭭").format(file_path, test_name)
            data = {
                TestFramework.bstack1l1111ll1l1_opy_: bstack111l1l111ll_opy_.uuid,
                TestFramework.bstack11l1ll11111_opy_: bstack111l1l111ll_opy_.uuid,
                TestFramework.bstack1l111111lll_opy_: test_name,
                TestFramework.bstack111llllllll_opy_: file_path,
                TestFramework.bstack111ll1ll1ll_opy_: getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠨࡥࡲࡨࡪ࠭᭮"), None),
                TestFramework.bstack11l111l1l11_opy_: getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ᭯"), []),
                TestFramework.bstack111ll11l11l_opy_: bstack111l11l1ll1_opy_,
                bstack1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪ᭰"): bstack111l11l1ll1_opy_,
                TestFramework.bstack111ll1l11ll_opy_: getattr(bstack111l1l111ll_opy_, bstack1ll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩ᭱"), {}),
                TestFramework.bstack11l11l1l1ll_opy_: test_name,
                bstack1ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧ᭲"): {},
                TestFramework.bstack11ll111l1ll_opy_: bstack111l11ll11l_opy_,
                bstack1ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ᭳"): bstack111l11lllll_opy_,
            }
            data[bstack1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪ᭴")] = {bstack1ll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬ᭵"): bstack111l11ll11l_opy_}
        elif isinstance(bstack111l1l111ll_opy_, dict):
            bstack111l11l1ll1_opy_ = bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩ᭶")) or bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩ᭷"), [])
            bstack111l11ll11l_opy_ = bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢ࡭ࡩ࠭᭸")) or bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡍࡩ࠭᭹"))
            bstack111l11lllll_opy_ = bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ᭺"), {})
            file_path = bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠪ᭻")) or bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡖࡡࡵࡪࠪ᭼"))
            test_name = bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ᭽")) or bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠪࡸࡪࡹࡴࡏࡣࡰࡩࠬ᭾"))
            if not bstack111l11ll11l_opy_ and file_path and test_name:
                bstack111l11ll11l_opy_ = bstack1ll_opy_ (u"ࠦࢀࢃ࠺࠻ࡽࢀࠦ᭿").format(file_path, test_name)
            data = {
                TestFramework.bstack1l1111ll1l1_opy_: bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠬࡻࡵࡪࡦࠪᮀ")) or bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"࠭ࡴࡦࡵࡷࡍࡩ࠭ᮁ")) or str(uuid4()),
                TestFramework.bstack11l1ll11111_opy_: bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠧࡵࡧࡶࡸࡎࡪࠧᮂ")) or bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᮃ")),
                TestFramework.bstack1l111111lll_opy_: test_name,
                TestFramework.bstack111llllllll_opy_: file_path,
                TestFramework.bstack111ll1ll1ll_opy_: bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᮄ")),
                TestFramework.bstack11l111l1l11_opy_: bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᮅ"), []),
                TestFramework.bstack111ll11l11l_opy_: bstack111l11l1ll1_opy_,
                bstack1ll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᮆ"): bstack111l11l1ll1_opy_,
                TestFramework.bstack111ll1l11ll_opy_: bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠬࡳࡥࡵࡣࠪᮇ"), {}),
                TestFramework.bstack11l11l1l1ll_opy_: bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᮈ")) or test_name,
                bstack1ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩᮉ"): bstack111l1l111ll_opy_.get(bstack1ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪᮊ"), {}),
                TestFramework.bstack11ll111l1ll_opy_: bstack111l11ll11l_opy_,
                bstack1ll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᮋ"): bstack111l11lllll_opy_,
            }
            data[bstack1ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭ᮌ")] = {bstack1ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨᮍ"): bstack111l11ll11l_opy_}
        return data
    def _111l11l1lll_opy_(self, instance: bstack1l1l11l11ll_opy_, *args, **kwargs):
        bstack1ll_opy_ (u"ࠧࠨࠢࡍࡱࡤࡨࠥࡺࡥࡴࡶࠣࡶࡪࡹࡵ࡭ࡶࠣࡪࡷࡵ࡭ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡴࡰࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠧࠨࠢᮎ")
        bstack111l11lll1l_opy_ = None
        if args and hasattr(args[0], bstack1ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᮏ")) and args[0].result:
            bstack1llll11l111_opy_ = args[0]
            result = bstack1llll11l111_opy_.result
            bstack111l11lll1l_opy_ = {
                TestFramework.bstack11l1ll11lll_opy_: getattr(result, bstack1ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᮐ"), bstack1ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᮑ")),
                TestFramework.bstack11l1ll11l11_opy_: None,
                TestFramework.bstack111ll1l1l11_opy_: None,
            }
            if hasattr(result, bstack1ll_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬᮒ")) and result.exception:
                bstack111l11lll1l_opy_[TestFramework.bstack11l1ll11l11_opy_] = [{bstack1ll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᮓ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack1ll_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠧᮔ")) else None
                bstack111l11lll1l_opy_[TestFramework.bstack111ll1l1l11_opy_] = exc_type or bstack1ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᮕ")
            bstack111l11lllll_opy_ = getattr(bstack1llll11l111_opy_, bstack1ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᮖ"), None)
            if bstack111l11lllll_opy_:
                bstack111l11lll1l_opy_[bstack1ll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᮗ")] = bstack111l11lllll_opy_
                logger.debug(bstack1ll_opy_ (u"ࠣࡗࡳࡨࡦࡺࡥࡥࠢ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠡࡣࡷࠤࡕࡕࡓࡕࠢࡷ࡭ࡲ࡫࠺ࠡࠤᮘ") + str(list(bstack111l11lllll_opy_.keys()) if bstack111l11lllll_opy_ else []) + bstack1ll_opy_ (u"ࠤࠥᮙ"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack111l11lll1l_opy_ = {
                TestFramework.bstack11l1ll11lll_opy_: data.get(bstack1ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᮚ"), TestFramework.bstack11l111ll111_opy_),
                TestFramework.bstack11l1ll11l11_opy_: data.get(bstack1ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᮛ")),
                TestFramework.bstack111ll1l1l11_opy_: data.get(bstack1ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᮜ")),
            }
            bstack111l11lllll_opy_ = data.get(bstack1ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᮝ"))
            if bstack111l11lllll_opy_:
                bstack111l11lll1l_opy_[bstack1ll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᮞ")] = bstack111l11lllll_opy_
                logger.debug(bstack1ll_opy_ (u"ࠣࡗࡳࡨࡦࡺࡥࡥࠢ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠡࡣࡷࠤࡕࡕࡓࡕࠢࡷ࡭ࡲ࡫࠺ࠡࠤᮟ") + str(list(bstack111l11lllll_opy_.keys()) if bstack111l11lllll_opy_ else []) + bstack1ll_opy_ (u"ࠤࠥᮠ"))
        if bstack111l11lll1l_opy_:
            if bstack111l11lll1l_opy_.get(TestFramework.bstack11l1ll11lll_opy_) != TestFramework.bstack11l111ll111_opy_:
                bstack111l11lll1l_opy_[TestFramework.bstack11ll1ll1l1l_opy_] = datetime.now(tz=timezone.utc)
            TestFramework.bstack111lllllll1_opy_(instance, bstack111l11lll1l_opy_)
            logger.debug(bstack1ll_opy_ (u"ࠥࡐࡴࡧࡤࡦࡦࠣࡸࡪࡹࡴࠡࡴࡨࡷࡺࡲࡴ࠻ࠢࠥᮡ") + str(bstack111l11lll1l_opy_.get(TestFramework.bstack11l1ll11lll_opy_)) + bstack1ll_opy_ (u"ࠦࠧᮢ"))
    def _111l11lll11_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1ll_opy_ (u"ࠧࠨࠢࡕࡴࡤࡧࡰࠦࡨࡰࡱ࡮ࠤࡪࡼࡥ࡯ࡶࡶࠤ࠭ࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍ࠮ࠣࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠲ࠠࡦࡶࡦ࠲࠮࠴ࠢࠣࠤᮣ")
        key = test_framework_state.name
        bstack11l111111ll_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᮤ"), {})
        if key not in bstack11l111111ll_opy_:
            bstack11l111111ll_opy_[key] = []
        bstack111lll1lll1_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, bstack1ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠨᮥ"), {})
        if key not in bstack111lll1lll1_opy_:
            bstack111lll1lll1_opy_[key] = []
        bstack111lll11111_opy_ = {
            bstack1ll_opy_ (u"ࠨࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᮦ"): bstack11l111111ll_opy_,
            bstack1ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠪᮧ"): bstack111lll1lll1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1ll_opy_ (u"ࠥ࡯ࡪࡿࠢᮨ"): key,
                TestFramework.bstack111lllll111_opy_: str(uuid4()),
                TestFramework.bstack11l1111lll1_opy_: TestFramework.bstack11l1111ll1l_opy_,
                TestFramework.bstack11l11111ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l11ll_opy_: [],
                TestFramework.bstack111ll1llll1_opy_: kwargs.get(bstack1ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᮩ"), key),
            }
            bstack11l111111ll_opy_[key].append(hook)
            bstack111lll11111_opy_[bstack1ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥ᮪ࠩ")] = key
        elif test_hook_state == TestHookState.POST:
            bstack111lll1llll_opy_ = bstack11l111111ll_opy_.get(key, [])
            hook = bstack111lll1llll_opy_.pop() if bstack111lll1llll_opy_ else None
            if hook:
                hook[TestFramework.bstack111lllll1ll_opy_] = datetime.now(tz=timezone.utc)
                bstack111lll1lll1_opy_[key].append(hook)
                bstack111lll11111_opy_[bstack1ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧ᮫ࠫ")] = key
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
        logger.debug(bstack1ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࡱࡥࡺࡿ࠱ࠦᮬ") + str(test_hook_state) + bstack1ll_opy_ (u"ࠣࠤᮭ"))
    def bstack11ll11llll1_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]
    ) -> List[bstack111l1111ll_opy_]:
        bstack1ll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡨࡰࡱ࡮ࠤࡸࡺࡡࡵࡧ࠱ࠦࠧࠨᮮ")
        if instance is None:
            return []
        return TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, [])
    def bstack11ll1l1lll1_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        bstack1l1ll1lll11_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack1ll_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡵࠤࡱࡵࡧࠡࡧࡱࡸࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢ࡫ࡳࡴࡱࠠࡴࡶࡤࡸࡪ࠴ࠢࠣࠤᮯ")
        if instance is None:
            return
        TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack111ll11llll_opy_, [])
    def get_current_test_instance(self) -> Optional[bstack1l1l11l11ll_opy_]:
        bstack1ll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸ࡭ࡸࡥࡢࡦ࠱ࠦࠧࠨ᮰")
        thread_id = threading.get_ident()
        target = self._111l11ll1ll_opy_.get(thread_id)
        if target:
            return self._111l1l111l1_opy_.get(target)
        return None
    def bstack111l1l11lll_opy_(
        self,
        instance: bstack1l1l11l11ll_opy_,
        log_entry: bstack111l1111ll_opy_
    ):
        bstack1ll_opy_ (u"ࠧࠨࠢࡂࡦࡧࠤࡦࠦ࡬ࡰࡩࠣࡩࡳࡺࡲࡺࠢࡷࡳࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠧࠨࠢ᮱")
        if instance is None:
            return
        logs = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack111ll11llll_opy_, [])
        logs.append(log_entry)
        TestFramework.bstack1l1l1l1l_opy_(instance, TestFramework.bstack111ll11llll_opy_, logs)
    def __11l11111l11_opy_(self, instance: bstack1l1l11l11ll_opy_) -> None:
        bstack1ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦ᮲")
        bstack111lll11111_opy_ = {bstack1ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤ᮳"): bstack1l11lll1lll_opy_.bstack11l111111l1_opy_()}
        TestFramework.bstack111lllllll1_opy_(instance, bstack111lll11111_opy_)
    def __111l1l11l11_opy_(self, instance: bstack1l1l11l11ll_opy_) -> None:
        bstack1ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶࡨࡷࡹ࠳࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡹࡵࡲ࡯ࡢࡦࡨࡨࠥࡼࡩࡢࠢࡉ࡭ࡱ࡫ࡕࡱ࡮ࡲࡥࡩ࡫ࡲ࠯ࡷࡳࡰࡴࡧࡤࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸ࠭࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡧࡦࡴࡳࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡱࡨࠥࡹࡥ࡯ࡦࡶࠤࡱࡵࡧࡴࠢࡹ࡭ࡦࠦࡧࡓࡒࡆ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᮴")
        from bstack_utils.helper import bstack11lll1l1111_opy_
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack1ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ᮵"), bstack1ll_opy_ (u"ࠪ࠴ࠬ᮶"))
            bstack11ll11l1ll1_opy_ = os.path.join(
                bstack11lll1l1111_opy_(),
                bstack1ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࡿࢂࠨ᮷").format(platform_index),
                bstack1ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣ᮸")
            )
            if not os.path.isdir(bstack11ll11l1ll1_opy_):
                logger.debug(bstack1ll_opy_ (u"ࠨࡎࡰࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧ࠾ࠥࠨ᮹") + str(bstack11ll11l1ll1_opy_) + bstack1ll_opy_ (u"ࠢࠣᮺ"))
                return
            bstack11ll1l1l11l_opy_ = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack1l1111ll1l1_opy_, bstack1ll_opy_ (u"ࠣࠤᮻ"))
            bstack111l1l1l111_opy_ = []
            for file_name in os.listdir(bstack11ll11l1ll1_opy_):
                file_path = os.path.join(bstack11ll11l1ll1_opy_, file_name)
                if os.path.isfile(file_path):
                    try:
                        bstack11lll11ll11_opy_ = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(bstack11lll11ll11_opy_, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = bstack111l1111ll_opy_(
                            kind=bstack1ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗࠦᮼ"),
                            message=bstack1ll_opy_ (u"ࠥࠦᮽ"),
                            level=bstack1ll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᮾ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            bstack11ll1ll1111_opy_=file_size,
                            bstack11ll11lllll_opy_=bstack1ll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᮿ"),
                            bstack1ll11l1_opy_=os.path.abspath(file_path),
                            bstack11ll11l1ll_opy_=bstack11ll1l1l11l_opy_
                        )
                        bstack111l1l1l111_opy_.append(log_entry)
                        logger.debug(bstack1ll_opy_ (u"ࠨࡁࡥࡦࡨࡨࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡯ࡳ࡬ࠦࡥ࡯ࡶࡵࡽ࠿ࠦࠢᯀ") + str(file_name) + bstack1ll_opy_ (u"ࠢࠣᯁ"))
                    except Exception as bstack11lll1l11ll_opy_:
                        logger.error(bstack1ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࢂࡀࠠࠣᯂ") + str(bstack11lll1l11ll_opy_) + bstack1ll_opy_ (u"ࠤࠥᯃ"))
            if bstack111l1l1l111_opy_ and self.bstack1ll11ll11l_opy_:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack1ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᯄ"), bstack1ll_opy_ (u"ࠦࠧᯅ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack1ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᯆ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack111l1l1l111_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack1ll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠢᯇ")
                        log_entry.test_framework_version = TestFramework.bstack1ll11111l11_opy_(instance, TestFramework.bstack11ll11l11ll_opy_, bstack1ll_opy_ (u"ࠢࠣᯈ"))
                        log_entry.uuid = bstack11ll1l1l11l_opy_
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack11l11l11l11_opy_ (u"ࠣࠤᯉ")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.bstack11ll1ll1111_opy_
                        log_entry.file_path = entry.bstack1ll11l1_opy_
                    self.bstack1ll11ll11l_opy_.LogCreatedEvent(req)
                    logger.debug(bstack1ll_opy_ (u"ࠤࡖࡩࡳࡺࠠࠣᯊ") + str(len(bstack111l1l1l111_opy_)) + bstack1ll_opy_ (u"ࠥࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡮ࡲ࡫ࡸࠦࡶࡪࡣࠣ࡫ࡗࡖࡃࠣᯋ"))
                except Exception as bstack1l1l1l1ll1_opy_:
                    logger.error(bstack1ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡪࡴࡤࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡮ࡲ࡫ࡸࠦࡶࡪࡣࠣ࡫ࡗࡖࡃ࠻ࠢࠥᯌ") + str(bstack1l1l1l1ll1_opy_) + bstack1ll_opy_ (u"ࠧࠨᯍ"))
        except Exception as e:
            logger.error(bstack1ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺ࠭࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠾ࠥࠨᯎ") + str(e) + bstack1ll_opy_ (u"ࠢࠣᯏ"))