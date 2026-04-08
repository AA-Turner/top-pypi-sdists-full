# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
bstack111l_opy_ (u"ࠤࠥࠦࠏ࡜ࡡ࡯࡫࡯ࡰࡦࡖࡹࡵࡪࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࠮ࠢࡗࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡸࡤࡲ࡮ࡲ࡬ࡢࠢࡓࡽࡹ࡮࡯࡯ࠢࡷࡩࡸࡺࡳ࠯ࠌࡗ࡬࡮ࡹࠠ࡮ࡱࡧࡹࡱ࡫ࠠࡱࡴࡲࡺ࡮ࡪࡥࡴࠢࡨࡺࡪࡴࡴࠡࡶࡵࡥࡨࡱࡩ࡯ࡩࠣࡥࡳࡪࠠࡴࡶࡤࡸࡪࠦ࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶࠣࡪࡴࡸࠠࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠡࡶࡨࡷࡹࡹࠬࠋࡵ࡬ࡱ࡮ࡲࡡࡳࠢࡷࡳࠥ࡜ࡡ࡯࡫࡯ࡰࡦࡐࡡࡷࡣࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣࡥ࡬࡫࡮ࡵ࠰ࠍࠦࠧࠨᑚ")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.bstack1l1ll111111_opy_ import bstack1l1l1ll1l1l_opy_, bstack1l1lll111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l11ll11l_opy_,
    TestHookState,
    bstack1ll1lll1l1l_opy_,
    bstack11lllllll1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l1ll11l1_opy_ import bstack1l1l11ll111_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1lll1l11l_opy_ import bstack1l1ll1111ll_opy_
logger = logging.getLogger(__name__)
class bstack1l1ll1l1111_opy_(TestFramework):
    bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࡘࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡳࡰ࡭ࡧࡰࡩࡳࡺࡡࡵ࡫ࡲࡲࠥ࡬࡯ࡳࠢࡹࡥࡳ࡯࡬࡭ࡣࠣࡔࡾࡺࡨࡰࡰࠣࡸࡪࡹࡴࡴࠢࠫࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦ࠭࠳ࠐࠠࠡࠢࠣࡌࡦࡴࡤ࡭ࡧࡶࠤࡪࡼࡥ࡯ࡶࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫࠱ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡ࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸ࠱ࠦࡡ࡯ࡦࠣ࡬ࡴࡵ࡫ࠡࡥࡤࡰࡱࡨࡡࡤ࡭ࡶࠤ࡫ࡵࡲࠋࠢࠣࠤࠥࡺࡥࡴࡶࡶࠤࡹ࡮ࡡࡵࠢࡧࡳࡳ࠭ࡴࠡࡷࡶࡩࠥࡶࡹࡵࡧࡶࡸࠥࡵࡲࠡࡱࡷ࡬ࡪࡸࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡴ࠰ࠍࠤࠥࠦࠠࡕࡪ࡬ࡷࠥ࡯ࡳࠡࡶ࡫ࡩࠥࡖࡹࡵࡪࡲࡲࠥ࡫ࡱࡶ࡫ࡹࡥࡱ࡫࡮ࡵࠢࡲࡪࠥ࡜ࡡ࡯࡫࡯ࡰࡦࡐࡡࡷࡣࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࠡࡶ࡫ࡩࠥࡐࡡࡷࡣࠣࡗࡉࡑ࠮ࠋࠢࠣࠤࠥࠨࠢࠣᑛ")
    FRAMEWORK_NAME = bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠬᑜ")
    bstack1l1l1l1lll1_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l1lll1l111_opy_: Dict[str, str] = None,
        bstack1l1ll1ll11l_opy_: List[str] = None,
        bstack1l1l1ll11l1_opy_: bstack1l1l11ll111_opy_ = None,
        bstack11l11lll11_opy_=None
    ):
        bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡌࡲ࡮ࡺࡩࡢ࡮࡬ࡾࡪࠦࡖࡢࡰ࡬ࡰࡱࡧࡐࡺࡶ࡫ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࡵ࠽ࠤࡉ࡯ࡣࡵࠢࡰࡥࡵࡶࡩ࡯ࡩࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡮ࡢ࡯ࡨࡷࠥࡺ࡯ࠡࡸࡨࡶࡸ࡯࡯࡯ࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵ࠽ࠤࡑ࡯ࡳࡵࠢࡲࡪࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡰࡤࡱࡪࡹࠠࠩࡦࡨࡪࡦࡻ࡬ࡵࡵࠣࡸࡴ࡛ࠦࠣࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠤࡠ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡥࡸࡿ࡮ࡤࡡࡧ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࡀࠠࡂࡵࡼࡲࡨࡊࡩࡴࡲࡤࡸࡨ࡮ࡥࡳࠢࡩࡳࡷࠦࡢࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠣࡳࡵ࡫ࡲࡢࡶ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡩ࡬ࡪࡡࡶࡩࡷࡼࡩࡤࡧ࠽ࠤ࡬ࡘࡐࡄࠢࡆࡐࡎࠦࡳࡦࡴࡹ࡭ࡨ࡫ࠠࡤ࡮࡬ࡩࡳࡺࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᑝ")
        if bstack1l1ll1ll11l_opy_ is None:
            bstack1l1ll1ll11l_opy_ = [self.FRAMEWORK_NAME]
        if bstack1l1lll1l111_opy_ is None:
            bstack1l1lll1l111_opy_ = {self.FRAMEWORK_NAME: self._1l1ll1l111l_opy_()}
        super().__init__(bstack1l1ll1ll11l_opy_, bstack1l1lll1l111_opy_, bstack1l1l1ll11l1_opy_)
        self.bstack11l11lll11_opy_ = bstack11l11lll11_opy_
        self._1l1l1ll11ll_opy_: Dict[str, bstack1l1l11ll11l_opy_] = {}
        self._1l1ll1l11l1_opy_: Dict[int, str] = {}
        logger.info(bstack111l_opy_ (u"ࠨࡖࡢࡰ࡬ࡰࡱࡧࡐࡺࡶ࡫ࡳࡳࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࡩࠦࡷࡪࡶ࡫ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳ࠾ࠤᑞ") + str(bstack1l1ll1ll11l_opy_) + bstack111l_opy_ (u"ࠢࠣᑟ"))
    def _1l1ll1l111l_opy_(self) -> str:
        bstack111l_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡖࡹࡵࡪࡲࡲࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡳࡵࡴ࡬ࡲ࡬࠴ࠢࠣࠤᑠ")
        return bstack111l_opy_ (u"ࠤࡾࢁ࠳ࢁࡽ࠯ࡽࢀࠦᑡ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def bstack1l1l1llll1l_opy_(self) -> bool:
        bstack111l_opy_ (u"ࠥࠦࠧࡘࡥࡵࡷࡵࡲࠥࡌࡡ࡭ࡵࡨࠤࡦࡹࠠࡵࡪ࡬ࡷࠥ࡯ࡳࠡࡰࡲࡸࠥࡧࠠࡱࡻࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᑢ")
        return False
    def bstack1l1lll11111_opy_(self) -> bool:
        bstack111l_opy_ (u"ࠦࠧࠨࡒࡦࡶࡸࡶࡳࠦࡆࡢ࡮ࡶࡩࠥࡧࡳࠡࡶ࡫࡭ࡸࠦࡩࡴࠢࡱࡳࡹࠦࡡࠡࡴࡲࡦࡴࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᑣ")
        return False
    def track_event(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗࡶࡦࡩ࡫ࠡࡣࠣࡸࡪࡹࡴࠡ࡮࡬ࡪࡪࡩࡹࡤ࡮ࡨࠤࡪࡼࡥ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡺࡥࡹࡶ࠽ࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡇࡴࡴࡴࡦࡺࡷࠤࡼ࡯ࡴࡩࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡴࡡ࡮ࡧ࠯ࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠱ࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥ࡯࡮ࡥࡧࡻࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠼ࠣࡘ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡵࡷࡥࡹ࡫ࠠࠩࡋࡑࡍ࡙ࡥࡔࡆࡕࡗ࠰࡚ࠥࡅࡔࡖ࠯ࠤࡪࡺࡣ࠯ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧ࠽ࠤࡕࡸࡥࠡࡱࡵࠤࡕࡵࡳࡵࠢ࡫ࡳࡴࡱࠠࡴࡶࡤࡸࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠯ࡧࡲࡨࡵ࠽ࠤࡆࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࠭ࡺࡹࡱ࡫ࡦࡥࡱࡲࡹࠡࡖࡨࡷࡹࡊࡡࡵࡣࠣࡳࡷࠦࡤࡪࡥࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠮࠯ࡱࡷࡢࡴࡪࡷ࠿ࠦࡁࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᑤ")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack111l_opy_ (u"ࠨࡉࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡳࡵࡣࡷࡩࡂࠨᑥ") + str(test_framework_state) + bstack111l_opy_ (u"ࠢࠣᑦ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack111l_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᑧ") + str(kwargs) + bstack111l_opy_ (u"ࠤࠥᑨ"))
            return
        instance = self._1l1ll11l11l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack111l_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡥࡴࡱ࡯ࡺࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢᑩ") + str(test_hook_state) + bstack111l_opy_ (u"ࠦࠧᑪ"))
            return
        try:
            self._1l1ll1l1ll1_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡥࡷࡧࡱࡸࠥࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀ࠾ࠥࠨᑫ") + str(e) + bstack111l_opy_ (u"ࠨࠢᑬ"))
        self.bstack1l1l1l11lll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _1l1ll1l1ll1_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111l_opy_ (u"ࠢࠣࠤࡋࡥࡳࡪ࡬ࡦࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࠤࡪࡼࡥ࡯ࡶࠣࡸࡾࡶࡥࡴ࠰ࠥࠦࠧᑭ")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1ll111l1l_opy_):
                bstack1llll1ll111_opy_ = self._1l1l1ll1lll_opy_(args, kwargs)
                if bstack1llll1ll111_opy_:
                    instance.data.update(bstack1llll1ll111_opy_)
                    logger.debug(bstack111l_opy_ (u"ࠣࡎࡲࡥࡩ࡫ࡤࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᑮ") + str(instance.ref()) + bstack111l_opy_ (u"ࠤࠥᑯ"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1ll1_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack111l_opy_ (u"ࠥࡗࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᑰ") + str(instance.ref()) + bstack111l_opy_ (u"ࠦࠧᑱ"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.bstack1ll1111ll1l_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_):
                    TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack111l_opy_ (u"࡙ࠧࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᑲ") + str(instance.ref()) + bstack111l_opy_ (u"ࠨࠢᑳ"))
                self._1l1l1l111ll_opy_(instance, *args, **kwargs)
                self.__1l1l1l11l11_opy_(instance)
                self.__1l1l1llllll_opy_(instance)
        elif test_framework_state in bstack1l1ll1l1111_opy_.bstack1l1l1l1lll1_opy_:
            self._1l1lll11l1l_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣᑴ") + str(instance.ref()) + bstack111l_opy_ (u"ࠣࠤᑵ"))
    def _1l1ll11l11l_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[bstack1l1l11ll11l_opy_]:
        bstack111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡵࡲࡰࡻ࡫ࠠࡰࡴࠣࡧࡷ࡫ࡡࡵࡧࠣࡥ࡚ࠥࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡙࡫ࡳࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡍࡓࡏࡔࡠࡖࡈࡗ࡙ࠦࡐࡓࡇ࠯ࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠ࡯ࡧࡺࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡵࡴࡩࡧࡵࠤࡪࡼࡥ࡯ࡶࡶ࠰ࠥࡲ࡯ࡰ࡭ࡶࠤࡺࡶࠠࡵࡪࡨࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᑶ")
        target = self._1l1ll1l1l1l_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._1l1ll111ll1_opy_(context, target)
            self._1l1ll1l11l1_opy_[thread_id] = target
            return instance
        if target and target in self._1l1l1ll11ll_opy_:
            return self._1l1l1ll11ll_opy_[target]
        bstack1l1lll111l1_opy_ = self._1l1ll1l11l1_opy_.get(thread_id)
        if bstack1l1lll111l1_opy_ and bstack1l1lll111l1_opy_ in self._1l1l1ll11ll_opy_:
            return self._1l1l1ll11ll_opy_[bstack1l1lll111l1_opy_]
        instance = TestFramework.bstack1l1l1l1l11l_opy_(target) if target else None
        if instance:
            return instance
        logger.debug(bstack111l_opy_ (u"ࠥࡒࡴࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡴࡩࡴࡨࡥࡩࡥࡩࡥ࠿ࠥᑷ") + str(thread_id) + bstack111l_opy_ (u"ࠦࠧᑸ"))
        return None
    def _1l1ll111ll1_opy_(
        self,
        context: bstack1ll1lll1l1l_opy_,
        target: str
    ) -> bstack1l1l11ll11l_opy_:
        bstack111l_opy_ (u"ࠧࠨࠢࡄࡴࡨࡥࡹ࡫ࠠࡢࠢࡱࡩࡼࠦࡴࡦࡵࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫࠳ࠨࠢࠣᑹ")
        ctx = bstack1l1l1ll1l1l_opy_.create_context(target)
        instance = bstack1l1l11ll11l_opy_(
            ctx,
            self.bstack1l1ll1ll11l_opy_,
            self.bstack1l1lll1l111_opy_,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.bstack1l1l1l1111l_opy_(instance, {
            TestFramework.bstack1l1l1lll11l_opy_: str(uuid4()),
            TestFramework.bstack1l1ll1l1l11_opy_: context.test_framework_name,
            TestFramework.bstack1l1l1lll1l1_opy_: context.test_framework_version,
            TestFramework.bstack1l1l11lllll_opy_: [],
            TestFramework.bstack1l1ll1lll11_opy_: TestFramework.bstack1l1lll11l11_opy_,
        })
        if context.platform_index >= 0:
            TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_, context.platform_index)
        self._1l1l1ll11ll_opy_[target] = instance
        TestFramework.bstack1l111l111_opy_[ctx.id] = instance
        logger.debug(bstack111l_opy_ (u"ࠨࡃࡳࡧࡤࡸࡪࡪࠠ࡯ࡧࡺࠤࡹ࡫ࡳࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡲࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡧࡹࡾ࠮ࡪࡦࡀࠦᑺ") + str(ctx.id) + bstack111l_opy_ (u"ࠢࠣᑻ"))
        return instance
    def _1l1ll1l1l1l_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack111l_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡲࡨࡧࡷࠤ࠭ࡺࡥࡴࡶࠣࡲࡦࡳࡥࠪࠢࡩࡶࡴࡳࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠱ࠦࠧࠨᑼ")
        if args and hasattr(args[0], bstack111l_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᑽ")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᑾ")) or
                    args[0].get(bstack111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡐࡤࡱࡪ࠭ᑿ")) or
                    args[0].get(bstack111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᒀ")) or
                    args[0].get(TestFramework.bstack1l1ll1lll1l_opy_))
        return (kwargs.get(bstack111l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩᒁ")) or
                kwargs.get(bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡓࡧ࡭ࡦࠩᒂ")) or
                kwargs.get(bstack111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᒃ")))
    def _1l1l1ll1lll_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack111l_opy_ (u"ࠤࠥࠦࡕࡧࡲࡴࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡳࡱࡰࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡪࡰࡷࡳࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳ࡯ࡤࡸ࠳ࠨࠢࠣᒄ")
        if not args:
            return None
        data = None
        bstack1l1lll11lll_opy_ = args[0]
        if hasattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠪࡲࡦࡳࡥࠨᒅ")) and hasattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᒆ")):
            bstack1l1ll1l1lll_opy_ = getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᒇ"), [])
            bstack1l1l1l11l1l_opy_ = getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤ࡯ࡤࠨᒈ"), None)
            bstack1l1l11lll1l_opy_ = getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᒉ"), {})
            file_path = getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠨࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠫᒊ"), None)
            test_name = bstack1l1lll11lll_opy_.name
            if not bstack1l1l1l11l1l_opy_ and file_path and test_name:
                bstack1l1l1l11l1l_opy_ = bstack111l_opy_ (u"ࠤࡾࢁ࠿ࡀࡻࡾࠤᒋ").format(file_path, test_name)
            data = {
                TestFramework.bstack1l1l1lll11l_opy_: bstack1l1lll11lll_opy_.uuid,
                TestFramework.bstack1l1ll111l1l_opy_: bstack1l1lll11lll_opy_.uuid,
                TestFramework.bstack1l1ll1lll1l_opy_: test_name,
                TestFramework.bstack1l1ll111lll_opy_: file_path,
                TestFramework.bstack1l1ll111l11_opy_: getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠪࡧࡴࡪࡥࠨᒌ"), None),
                TestFramework.bstack1l1ll1ll1l1_opy_: getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᒍ"), []),
                TestFramework.bstack1l1l1l1ll1l_opy_: bstack1l1ll1l1lll_opy_,
                bstack111l_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬᒎ"): bstack1l1ll1l1lll_opy_,
                TestFramework.bstack1l1lll11ll1_opy_: getattr(bstack1l1lll11lll_opy_, bstack111l_opy_ (u"࠭࡭ࡦࡶࡤࠫᒏ"), {}),
                TestFramework.bstack1l1l1lll1ll_opy_: test_name,
                bstack111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩᒐ"): {},
                TestFramework.bstack1l1ll11ll11_opy_: bstack1l1l1l11l1l_opy_,
                bstack111l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᒑ"): bstack1l1l11lll1l_opy_,
            }
            data[bstack111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᒒ")] = {bstack111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᒓ"): bstack1l1l1l11l1l_opy_}
        elif isinstance(bstack1l1lll11lll_opy_, dict):
            bstack1l1ll1l1lll_opy_ = bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫᒔ")) or bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᒕ"), [])
            bstack1l1l1l11l1l_opy_ = bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤ࡯ࡤࠨᒖ")) or bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡏࡤࠨᒗ"))
            bstack1l1l11lll1l_opy_ = bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᒘ"), {})
            file_path = bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠬᒙ")) or bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠪࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠬᒚ"))
            test_name = bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᒛ")) or bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡑࡥࡲ࡫ࠧᒜ"))
            if not bstack1l1l1l11l1l_opy_ and file_path and test_name:
                bstack1l1l1l11l1l_opy_ = bstack111l_opy_ (u"ࠨࡻࡾ࠼࠽ࡿࢂࠨᒝ").format(file_path, test_name)
            data = {
                TestFramework.bstack1l1l1lll11l_opy_: bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᒞ")) or bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠨࡶࡨࡷࡹࡏࡤࠨᒟ")) or str(uuid4()),
                TestFramework.bstack1l1ll111l1l_opy_: bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠩࡷࡩࡸࡺࡉࡥࠩᒠ")) or bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᒡ")),
                TestFramework.bstack1l1ll1lll1l_opy_: test_name,
                TestFramework.bstack1l1ll111lll_opy_: file_path,
                TestFramework.bstack1l1ll111l11_opy_: bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠫࡨࡵࡤࡦࠩᒢ")),
                TestFramework.bstack1l1ll1ll1l1_opy_: bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠬࡺࡡࡨࡵࠪᒣ"), []),
                TestFramework.bstack1l1l1l1ll1l_opy_: bstack1l1ll1l1lll_opy_,
                bstack111l_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᒤ"): bstack1l1ll1l1lll_opy_,
                TestFramework.bstack1l1lll11ll1_opy_: bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᒥ"), {}),
                TestFramework.bstack1l1l1lll1ll_opy_: bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᒦ")) or test_name,
                bstack111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫᒧ"): bstack1l1lll11lll_opy_.get(bstack111l_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬᒨ"), {}),
                TestFramework.bstack1l1ll11ll11_opy_: bstack1l1l1l11l1l_opy_,
                bstack111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᒩ"): bstack1l1l11lll1l_opy_,
            }
            data[bstack111l_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨᒪ")] = {bstack111l_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪᒫ"): bstack1l1l1l11l1l_opy_}
        return data
    def _1l1l1l111ll_opy_(self, instance: bstack1l1l11ll11l_opy_, *args, **kwargs):
        bstack111l_opy_ (u"ࠢࠣࠤࡏࡳࡦࡪࠠࡵࡧࡶࡸࠥࡸࡥࡴࡷ࡯ࡸࠥ࡬ࡲࡰ࡯ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࡶࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠢࠣࠤᒬ")
        bstack1l1l11ll1ll_opy_ = None
        if args and hasattr(args[0], bstack111l_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᒭ")) and args[0].result:
            bstack1llll1ll111_opy_ = args[0]
            result = bstack1llll1ll111_opy_.result
            bstack1l1l11ll1ll_opy_ = {
                TestFramework.bstack1l1ll1lll11_opy_: getattr(result, bstack111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᒮ"), bstack111l_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᒯ")),
                TestFramework.bstack1l1ll1111l1_opy_: None,
                TestFramework.bstack1l1l1lll111_opy_: None,
            }
            if hasattr(result, bstack111l_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠧᒰ")) and result.exception:
                bstack1l1l11ll1ll_opy_[TestFramework.bstack1l1ll1111l1_opy_] = [{bstack111l_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᒱ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack111l_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠩᒲ")) else None
                bstack1l1l11ll1ll_opy_[TestFramework.bstack1l1l1lll111_opy_] = exc_type or bstack111l_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣᒳ")
            bstack1l1l11lll1l_opy_ = getattr(bstack1llll1ll111_opy_, bstack111l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᒴ"), None)
            if bstack1l1l11lll1l_opy_:
                bstack1l1l11ll1ll_opy_[bstack111l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᒵ")] = bstack1l1l11lll1l_opy_
                logger.debug(bstack111l_opy_ (u"࡙ࠥࡵࡪࡡࡵࡧࡧࠤ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠣࡥࡹࠦࡐࡐࡕࡗࠤࡹ࡯࡭ࡦ࠼ࠣࠦᒶ") + str(list(bstack1l1l11lll1l_opy_.keys()) if bstack1l1l11lll1l_opy_ else []) + bstack111l_opy_ (u"ࠦࠧᒷ"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack1l1l11ll1ll_opy_ = {
                TestFramework.bstack1l1ll1lll11_opy_: data.get(bstack111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᒸ"), TestFramework.bstack1l1lll11l11_opy_),
                TestFramework.bstack1l1ll1111l1_opy_: data.get(bstack111l_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᒹ")),
                TestFramework.bstack1l1l1lll111_opy_: data.get(bstack111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᒺ")),
            }
            bstack1l1l11lll1l_opy_ = data.get(bstack111l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᒻ"))
            if bstack1l1l11lll1l_opy_:
                bstack1l1l11ll1ll_opy_[bstack111l_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᒼ")] = bstack1l1l11lll1l_opy_
                logger.debug(bstack111l_opy_ (u"࡙ࠥࡵࡪࡡࡵࡧࡧࠤ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠣࡥࡹࠦࡐࡐࡕࡗࠤࡹ࡯࡭ࡦ࠼ࠣࠦᒽ") + str(list(bstack1l1l11lll1l_opy_.keys()) if bstack1l1l11lll1l_opy_ else []) + bstack111l_opy_ (u"ࠦࠧᒾ"))
        if bstack1l1l11ll1ll_opy_:
            if bstack1l1l11ll1ll_opy_.get(TestFramework.bstack1l1ll1lll11_opy_) != TestFramework.bstack1l1lll11l11_opy_:
                bstack1l1l11ll1ll_opy_[TestFramework.bstack1l1l1ll1111_opy_] = datetime.now(tz=timezone.utc)
            TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1l11ll1ll_opy_)
            logger.debug(bstack111l_opy_ (u"ࠧࡒ࡯ࡢࡦࡨࡨࠥࡺࡥࡴࡶࠣࡶࡪࡹࡵ࡭ࡶ࠽ࠤࠧᒿ") + str(bstack1l1l11ll1ll_opy_.get(TestFramework.bstack1l1ll1lll11_opy_)) + bstack111l_opy_ (u"ࠨࠢᓀ"))
    def _1l1lll11l1l_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111l_opy_ (u"ࠢࠣࠤࡗࡶࡦࡩ࡫ࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸࠦࠨࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏ࠰ࠥࡇࡆࡕࡇࡕࡣࡆࡒࡌ࠭ࠢࡨࡸࡨ࠴ࠩ࠯ࠤࠥࠦᓁ")
        key = test_framework_state.name
        bstack1l1ll1l11ll_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᓂ"), {})
        if key not in bstack1l1ll1l11ll_opy_:
            bstack1l1ll1l11ll_opy_[key] = []
        bstack1l1l11lll11_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, bstack111l_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠪᓃ"), {})
        if key not in bstack1l1l11lll11_opy_:
            bstack1l1l11lll11_opy_[key] = []
        bstack1l1ll11l1l1_opy_ = {
            bstack111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠪᓄ"): bstack1l1ll1l11ll_opy_,
            bstack111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠬᓅ"): bstack1l1l11lll11_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack111l_opy_ (u"ࠧࡱࡥࡺࠤᓆ"): key,
                TestFramework.bstack1l1ll11llll_opy_: str(uuid4()),
                TestFramework.bstack1l1ll11ll1l_opy_: TestFramework.bstack1l1ll11lll1_opy_,
                TestFramework.bstack1l1l11llll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack1l1ll11l111_opy_: [],
                TestFramework.bstack1l1ll11l1ll_opy_: kwargs.get(bstack111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩᓇ"), key),
            }
            bstack1l1ll1l11ll_opy_[key].append(hook)
            bstack1l1ll11l1l1_opy_[bstack111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠫᓈ")] = key
        elif test_hook_state == TestHookState.POST:
            bstack1l1l1l1llll_opy_ = bstack1l1ll1l11ll_opy_.get(key, [])
            hook = bstack1l1l1l1llll_opy_.pop() if bstack1l1l1l1llll_opy_ else None
            if hook:
                hook[TestFramework.bstack1l1ll1ll1ll_opy_] = datetime.now(tz=timezone.utc)
                bstack1l1l11lll11_opy_[key].append(hook)
                bstack1l1ll11l1l1_opy_[bstack111l_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᓉ")] = key
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
        logger.debug(bstack111l_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡻ࡬ࡧࡼࢁ࠳ࠨᓊ") + str(test_hook_state) + bstack111l_opy_ (u"ࠥࠦᓋ"))
    def bstack1l1lll1111l_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]
    ) -> List[bstack11lllllll1_opy_]:
        bstack111l_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡰࡴ࡭ࠠࡦࡰࡷࡶ࡮࡫ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡪࡲࡳࡰࠦࡳࡵࡣࡷࡩ࠳ࠨࠢࠣᓌ")
        if instance is None:
            return []
        return TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, [])
    def bstack1l1l1l11111_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack111l_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡷࠦ࡬ࡰࡩࠣࡩࡳࡺࡲࡪࡧࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤ࡭ࡵ࡯࡬ࠢࡶࡸࡦࡺࡥ࠯ࠤࠥࠦᓍ")
        if instance is None:
            return
        TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, [])
    def get_current_test_instance(self) -> Optional[bstack1l1l11ll11l_opy_]:
        bstack111l_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡨࡳࡧࡤࡨ࠳ࠨࠢࠣᓎ")
        thread_id = threading.get_ident()
        target = self._1l1ll1l11l1_opy_.get(thread_id)
        if target:
            return self._1l1l1ll11ll_opy_.get(target)
        return None
    def bstack1l1ll1llll1_opy_(
        self,
        instance: bstack1l1l11ll11l_opy_,
        log_entry: bstack11lllllll1_opy_
    ):
        bstack111l_opy_ (u"ࠢࠣࠤࡄࡨࡩࠦࡡࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴࡼࠤࡹࡵࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠢࠣࠤᓏ")
        if instance is None:
            return
        logs = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, [])
        logs.append(log_entry)
        TestFramework.bstack1l11l1ll11_opy_(instance, TestFramework.bstack1l1l11lllll_opy_, logs)
    def __1l1l1l11l11_opy_(self, instance: bstack1l1l11ll11l_opy_) -> None:
        bstack111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᓐ")
        bstack1l1ll11l1l1_opy_ = {bstack111l_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦᓑ"): bstack1l1ll1111ll_opy_.bstack1l1ll11111l_opy_()}
        TestFramework.bstack1l1l1l1111l_opy_(instance, bstack1l1ll11l1l1_opy_)
    def __1l1l1llllll_opy_(self, instance: bstack1l1l11ll11l_opy_) -> None:
        bstack111l_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡻࡰ࡭ࡱࡤࡨࡪࡪࠠࡷ࡫ࡤࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴ࠱ࡹࡵࡲ࡯ࡢࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘࡩࡡ࡯ࡵࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡳࡪࠠࡴࡧࡱࡨࡸࠦ࡬ࡰࡩࡶࠤࡻ࡯ࡡࠡࡩࡕࡔࡈ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᓒ")
        from bstack_utils.helper import bstack1l1ll1lllll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᓓ"), bstack111l_opy_ (u"ࠬ࠶ࠧᓔ"))
            bstack1l1l1l1l1ll_opy_ = os.path.join(
                bstack1l1ll1lllll_opy_(),
                bstack111l_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࢁࡽࠣᓕ").format(platform_index),
                bstack111l_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥᓖ")
            )
            if not os.path.isdir(bstack1l1l1l1l1ll_opy_):
                logger.debug(bstack111l_opy_ (u"ࠣࡐࡲࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࡀࠠࠣᓗ") + str(bstack1l1l1l1l1ll_opy_) + bstack111l_opy_ (u"ࠤࠥᓘ"))
                return
            bstack1l1l1l1l1l1_opy_ = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_, bstack111l_opy_ (u"ࠥࠦᓙ"))
            bstack1l1l1l1ll11_opy_ = []
            for file_name in os.listdir(bstack1l1l1l1l1ll_opy_):
                file_path = os.path.join(bstack1l1l1l1l1ll_opy_, file_name)
                if os.path.isfile(file_path):
                    try:
                        bstack1l1l1ll111l_opy_ = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(bstack1l1l1ll111l_opy_, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = bstack11lllllll1_opy_(
                            kind=bstack111l_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨᓚ"),
                            message=bstack111l_opy_ (u"ࠧࠨᓛ"),
                            level=bstack111l_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤᓜ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            bstack1l1l11ll1l1_opy_=file_size,
                            bstack1l1l1l1l111_opy_=bstack111l_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢᓝ"),
                            bstack1lllllll_opy_=os.path.abspath(file_path),
                            bstack1ll1l1l11l_opy_=bstack1l1l1l1l1l1_opy_
                        )
                        bstack1l1l1l1ll11_opy_.append(log_entry)
                        logger.debug(bstack111l_opy_ (u"ࠣࡃࡧࡨࡪࡪࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡱࡵࡧࠡࡧࡱࡸࡷࡿ࠺ࠡࠤᓞ") + str(file_name) + bstack111l_opy_ (u"ࠤࠥᓟ"))
                    except Exception as bstack1l1ll1ll111_opy_:
                        logger.error(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᓠ") + str(bstack1l1ll1ll111_opy_) + bstack111l_opy_ (u"ࠦࠧᓡ"))
            if bstack1l1l1l1ll11_opy_ and self.bstack11l11lll11_opy_:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack111l_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤᓢ"), bstack111l_opy_ (u"ࠨࠢᓣ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack111l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᓤ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack1l1l1l1ll11_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack111l_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠤᓥ")
                        log_entry.test_framework_version = TestFramework.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_, bstack111l_opy_ (u"ࠤࠥᓦ"))
                        log_entry.uuid = bstack1l1l1l1l1l1_opy_
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack1l1l1l111l1_opy_ (u"ࠥࠦᓧ")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.bstack1l1l11ll1l1_opy_
                        log_entry.file_path = entry.bstack1lllllll_opy_
                    self.bstack11l11lll11_opy_.LogCreatedEvent(req)
                    logger.debug(bstack111l_opy_ (u"ࠦࡘ࡫࡮ࡵࠢࠥᓨ") + str(len(bstack1l1l1l1ll11_opy_)) + bstack111l_opy_ (u"ࠧࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡰࡴ࡭ࡳࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠥᓩ"))
                except Exception as bstack11ll1111ll_opy_:
                    logger.error(bstack111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡰࡴ࡭ࡳࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅ࠽ࠤࠧᓪ") + str(bstack11ll1111ll_opy_) + bstack111l_opy_ (u"ࠢࠣᓫ"))
        except Exception as e:
            logger.error(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵ࠯࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࡀࠠࠣᓬ") + str(e) + bstack111l_opy_ (u"ࠤࠥᓭ"))