# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
bstack111ll11_opy_ (u"ࠦࠧࠨࠊࡗࡣࡱ࡭ࡱࡲࡡࡑࡻࡷ࡬ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࠰ࠤ࡙࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡭ࡱ࡮ࡨࡱࡪࡴࡴࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡺࡦࡴࡩ࡭࡮ࡤࠤࡕࡿࡴࡩࡱࡱࠤࡹ࡫ࡳࡵࡵ࠱ࠎ࡙࡮ࡩࡴࠢࡰࡳࡩࡻ࡬ࡦࠢࡳࡶࡴࡼࡩࡥࡧࡶࠤࡪࡼࡥ࡯ࡶࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫ࠥࡧ࡮ࡥࠢࡶࡸࡦࡺࡥࠡ࡯ࡤࡲࡦ࡭ࡥ࡮ࡧࡱࡸࠥ࡬࡯ࡳࠢࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠣࡸࡪࡹࡴࡴ࠮ࠍࡷ࡮ࡳࡩ࡭ࡣࡵࠤࡹࡵࠠࡗࡣࡱ࡭ࡱࡲࡡࡋࡣࡹࡥࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࠣࡸ࡭࡫ࠠࡋࡣࡹࡥࠥࡧࡧࡦࡰࡷ࠲ࠏࠨࠢࠣ᭕")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1l1ll1l1l1l_opy_, bstack1l1lll11111_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l111llll11_opy_,
    TestHookState,
    bstack1lll111l1l1_opy_,
    bstack1llll111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll11l11_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l11lllllll_opy_ import bstack1l1l111111l_opy_
logger = logging.getLogger(__name__)
class bstack1l11l11ll1l_opy_(TestFramework):
    bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤ࡚ࠥࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡮ࡲ࡯ࡩࡲ࡫࡮ࡵࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡻࡧ࡮ࡪ࡮࡯ࡥࠥࡖࡹࡵࡪࡲࡲࠥࡺࡥࡴࡶࡶࠤ࠭ࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠯࠮ࠋࠢࠣࠤࠥࡎࡡ࡯ࡦ࡯ࡩࡸࠦࡥࡷࡧࡱࡸࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭ࠬࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠬࠡࡣࡱࡨࠥ࡮࡯ࡰ࡭ࠣࡧࡦࡲ࡬ࡣࡣࡦ࡯ࡸࠦࡦࡰࡴࠍࠤࠥࠦࠠࡵࡧࡶࡸࡸࠦࡴࡩࡣࡷࠤࡩࡵ࡮ࠨࡶࠣࡹࡸ࡫ࠠࡱࡻࡷࡩࡸࡺࠠࡰࡴࠣࡳࡹ࡮ࡥࡳࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡶ࠲ࠏࠦࠠࠡࠢࡗ࡬࡮ࡹࠠࡪࡵࠣࡸ࡭࡫ࠠࡑࡻࡷ࡬ࡴࡴࠠࡦࡳࡸ࡭ࡻࡧ࡬ࡦࡰࡷࠤࡴ࡬ࠠࡗࡣࡱ࡭ࡱࡲࡡࡋࡣࡹࡥࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࠣࡸ࡭࡫ࠠࡋࡣࡹࡥ࡙ࠥࡄࡌ࠰ࠍࠤࠥࠦࠠࠣࠤࠥ᭖")
    FRAMEWORK_NAME = bstack111ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ᭗")
    bstack111ll1l1l1l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11ll1111l_opy_: Dict[str, str] = None,
        bstack1l11lll1ll1_opy_: List[str] = None,
        bstack1l1lll11l1l_opy_: bstack1l1lll11l11_opy_ = None,
        bstack1l1l1l1l1l_opy_=None
    ):
        bstack111ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡥࠡࡘࡤࡲ࡮ࡲ࡬ࡢࡒࡼࡸ࡭ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࡷ࠿ࠦࡄࡪࡥࡷࠤࡲࡧࡰࡱ࡫ࡱ࡫ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡰࡤࡱࡪࡹࠠࡵࡱࠣࡺࡪࡸࡳࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷ࠿ࠦࡌࡪࡵࡷࠤࡴ࡬ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡲࡦࡳࡥࡴࠢࠫࡨࡪ࡬ࡡࡶ࡮ࡷࡷࠥࡺ࡯ࠡ࡝ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦࡢ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡧࡳࡺࡰࡦࡣࡩ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲ࠻ࠢࡄࡷࡾࡴࡣࡅ࡫ࡶࡴࡦࡺࡣࡩࡧࡵࠤ࡫ࡵࡲࠡࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨࠥࡵࡰࡦࡴࡤࡸ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤ࡮࡬ࡣࡸ࡫ࡲࡷ࡫ࡦࡩ࠿ࠦࡧࡓࡒࡆࠤࡈࡒࡉࠡࡵࡨࡶࡻ࡯ࡣࡦࠢࡦࡰ࡮࡫࡮ࡵࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᭘")
        if bstack1l11lll1ll1_opy_ is None:
            bstack1l11lll1ll1_opy_ = [self.FRAMEWORK_NAME]
        if bstack1l11ll1111l_opy_ is None:
            bstack1l11ll1111l_opy_ = {self.FRAMEWORK_NAME: self._111l11ll1l1_opy_()}
        super().__init__(bstack1l11lll1ll1_opy_, bstack1l11ll1111l_opy_, bstack1l1lll11l1l_opy_)
        self.bstack1l1l1l1l1l_opy_ = bstack1l1l1l1l1l_opy_
        self._111l1l111ll_opy_: Dict[str, bstack1l111llll11_opy_] = {}
        self._111l11lllll_opy_: Dict[int, str] = {}
        logger.info(bstack111ll11_opy_ (u"ࠣࡘࡤࡲ࡮ࡲ࡬ࡢࡒࡼࡸ࡭ࡵ࡮ࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡵࡀࠦ᭙") + str(bstack1l11lll1ll1_opy_) + bstack111ll11_opy_ (u"ࠤࠥ᭚"))
    def _111l11ll1l1_opy_(self) -> str:
        bstack111ll11_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡑࡻࡷ࡬ࡴࡴࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡵࡷࡶ࡮ࡴࡧ࠯ࠤࠥࠦ᭛")
        return bstack111ll11_opy_ (u"ࠦࢀࢃ࠮ࡼࡿ࠱ࡿࢂࠨ᭜").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def bstack11ll1lll111_opy_(self) -> bool:
        bstack111ll11_opy_ (u"ࠧࠨࠢࡓࡧࡷࡹࡷࡴࠠࡇࡣ࡯ࡷࡪࠦࡡࡴࠢࡷ࡬࡮ࡹࠠࡪࡵࠣࡲࡴࡺࠠࡢࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣ᭝")
        return False
    def bstack11ll111llll_opy_(self) -> bool:
        bstack111ll11_opy_ (u"ࠨࠢࠣࡔࡨࡸࡺࡸ࡮ࠡࡈࡤࡰࡸ࡫ࠠࡢࡵࠣࡸ࡭࡯ࡳࠡ࡫ࡶࠤࡳࡵࡴࠡࡣࠣࡶࡴࡨ࡯ࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣ᭞")
        return False
    def track_event(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll11_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡙ࡸࡡࡤ࡭ࠣࡥࠥࡺࡥࡴࡶࠣࡰ࡮࡬ࡥࡤࡻࡦࡰࡪࠦࡥࡷࡧࡱࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡵ࡮ࡵࡧࡻࡸ࠿ࠦࡔࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࡉ࡯࡯ࡶࡨࡼࡹࠦࡷࡪࡶ࡫ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡯ࡣࡰࡩ࠱ࠦࡶࡦࡴࡶ࡭ࡴࡴࠬࠡࡣࡱࡨࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡪࡰࡧࡩࡽࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨ࠾࡚ࠥࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡷࡹࡧࡴࡦࠢࠫࡍࡓࡏࡔࡠࡖࡈࡗ࡙࠲ࠠࡕࡇࡖࡘ࠱ࠦࡥࡵࡥ࠱࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩ࠿ࠦࡐࡳࡧࠣࡳࡷࠦࡐࡰࡵࡷࠤ࡭ࡵ࡯࡬ࠢࡶࡸࡦࡺࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠪࡢࡴࡪࡷ࠿ࠦࡁࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࠨࡵࡻࡳ࡭ࡨࡧ࡬࡭ࡻࠣࡘࡪࡹࡴࡅࡣࡷࡥࠥࡵࡲࠡࡦ࡬ࡧࡹ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࠰ࠪ࡬ࡹࡤࡶ࡬ࡹ࠺ࠡࡃࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࠥࡱࡥࡺࡹࡲࡶࡩࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᭟")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack111ll11_opy_ (u"ࠣࡋࡪࡲࡴࡸࡥࡥࠢࡦࡥࡱࡲࡢࡢࡥ࡮ࠤ࡫ࡵࡲࠡࡵࡷࡥࡹ࡫࠽ࠣ᭠") + str(test_framework_state) + bstack111ll11_opy_ (u"ࠤࠥ᭡"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack111ll11_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡪࡾࡰࡦࡥࡷࡩࡩࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ᭢") + str(kwargs) + bstack111ll11_opy_ (u"ࠦࠧ᭣"))
            return
        instance = self._111l1l11l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack111ll11_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡧࡶࡳࡱࡼࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࠤ᭤") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠨࠢ᭥"))
            return
        try:
            self._111l11llll1_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack111ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡨࡢࡰࡧࡰ࡮ࡴࡧࠡࡧࡹࡩࡳࡺࠠࡼࡶࡨࡷࡹࡥࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾ࠰ࡾࡸࡪࡹࡴࡠࡪࡲࡳࡰࡥࡳࡵࡣࡷࡩࢂࡀࠠࠣ᭦") + str(e) + bstack111ll11_opy_ (u"ࠣࠤ᭧"))
        self.bstack11l1111llll_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _111l11llll1_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll11_opy_ (u"ࠤࠥࠦࡍࡧ࡮ࡥ࡮ࡨࠤࡸࡶࡥࡤ࡫ࡩ࡭ࡨࠦࡥࡷࡧࡱࡸࠥࡺࡹࡱࡧࡶ࠲ࠧࠨࠢ᭨")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11l1l1l1l1l_opy_):
                bstack1llll1l11ll_opy_ = self._111l1l1111l_opy_(args, kwargs)
                if bstack1llll1l11ll_opy_:
                    instance.data.update(bstack1llll1l11ll_opy_)
                    logger.debug(bstack111ll11_opy_ (u"ࠥࡐࡴࡧࡤࡦࡦࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭩") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠦࠧ᭪"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11ll1l111l1_opy_):
                    TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11ll1l111l1_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack111ll11_opy_ (u"࡙ࠧࡥࡵࠢࡷࡩࡸࡺ࠭ࡴࡶࡤࡶࡹࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭫") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠨ᭬ࠢ"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.bstack1l1llll1l11_opy_(instance, TestFramework.bstack11ll1l11l11_opy_):
                    TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11ll1l11l11_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack111ll11_opy_ (u"ࠢࡔࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡨࡲࡩࠦࡦࡰࡴࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨ᭭") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠣࠤ᭮"))
                self._111l1l11111_opy_(instance, *args, **kwargs)
                self.__111llll1l11_opy_(instance)
                self.__111l11ll1ll_opy_(instance)
        elif test_framework_state in bstack1l11l11ll1l_opy_.bstack111ll1l1l1l_opy_:
            self._111l11lll1l_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack111ll11_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡪࡤࡲࡩࡲࡥࡥࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࡿࡹ࡫ࡳࡵࡡ࡫ࡳࡴࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥ᭯") + str(instance.ref()) + bstack111ll11_opy_ (u"ࠥࠦ᭰"))
    def _111l1l11l11_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[bstack1l111llll11_opy_]:
        bstack111ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡷࡴࡲࡶࡦࠢࡲࡶࠥࡩࡲࡦࡣࡷࡩࠥࡧࠠࡕࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡔࡦࡵࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡏࡎࡊࡖࡢࡘࡊ࡙ࡔࠡࡒࡕࡉ࠱ࠦࡣࡳࡧࡤࡸࡪࡹࠠࡢࠢࡱࡩࡼࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡰࡶ࡫ࡩࡷࠦࡥࡷࡧࡱࡸࡸ࠲ࠠ࡭ࡱࡲ࡯ࡸࠦࡵࡱࠢࡷ࡬ࡪࠦࡥࡹ࡫ࡶࡸ࡮ࡴࡧࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᭱")
        target = self._111l11l1l1l_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._111l11l1l11_opy_(context, target)
            self._111l11lllll_opy_[thread_id] = target
            return instance
        if target and target in self._111l1l111ll_opy_:
            return self._111l1l111ll_opy_[target]
        bstack111l11l1ll1_opy_ = self._111l11lllll_opy_.get(thread_id)
        if bstack111l11l1ll1_opy_ and bstack111l11l1ll1_opy_ in self._111l1l111ll_opy_:
            return self._111l1l111ll_opy_[bstack111l11l1ll1_opy_]
        instance = TestFramework.bstack1l1ll111l11_opy_(target) if target else None
        if instance:
            return instance
        logger.debug(bstack111ll11_opy_ (u"ࠧࡔ࡯ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡶ࡫ࡶࡪࡧࡤࡠ࡫ࡧࡁࠧ᭲") + str(thread_id) + bstack111ll11_opy_ (u"ࠨࠢ᭳"))
        return None
    def _111l11l1l11_opy_(
        self,
        context: bstack1lll111l1l1_opy_,
        target: str
    ) -> bstack1l111llll11_opy_:
        bstack111ll11_opy_ (u"ࠢࠣࠤࡆࡶࡪࡧࡴࡦࠢࡤࠤࡳ࡫ࡷࠡࡶࡨࡷࡹࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭࠮ࠣࠤࠥ᭴")
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        instance = bstack1l111llll11_opy_(
            ctx,
            self.bstack1l11lll1ll1_opy_,
            self.bstack1l11ll1111l_opy_,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.bstack11l111l11ll_opy_(instance, {
            TestFramework.bstack1l111l1ll1l_opy_: str(uuid4()),
            TestFramework.bstack1l111ll11ll_opy_: context.test_framework_name,
            TestFramework.bstack11lll11111l_opy_: context.test_framework_version,
            TestFramework.bstack11l1111ll1l_opy_: [],
            TestFramework.bstack11l1ll11111_opy_: TestFramework.bstack111ll11llll_opy_,
        })
        if context.platform_index >= 0:
            TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11llllll1ll_opy_, context.platform_index)
        self._111l1l111ll_opy_[target] = instance
        TestFramework.bstack1111l11ll_opy_[ctx.id] = instance
        logger.debug(bstack111ll11_opy_ (u"ࠣࡅࡵࡩࡦࡺࡥࡥࠢࡱࡩࡼࠦࡴࡦࡵࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡸࡦࡸࡧࡦࡶࡀࡿࡹࡧࡲࡨࡧࡷࢁࠥࡩࡴࡹ࠰࡬ࡨࡂࠨ᭵") + str(ctx.id) + bstack111ll11_opy_ (u"ࠤࠥ᭶"))
        return instance
    def _111l11l1l1l_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack111ll11_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡴࡪࡩࡹࠦࠨࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠬࠤ࡫ࡸ࡯࡮ࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷ࠳ࠨࠢࠣ᭷")
        if args and hasattr(args[0], bstack111ll11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ᭸")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᭹")) or
                    args[0].get(bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡒࡦࡳࡥࠨ᭺")) or
                    args[0].get(bstack111ll11_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ᭻")) or
                    args[0].get(TestFramework.bstack1l111l1lll1_opy_))
        return (kwargs.get(bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠫ᭼")) or
                kwargs.get(bstack111ll11_opy_ (u"ࠩࡷࡩࡸࡺࡎࡢ࡯ࡨࠫ᭽")) or
                kwargs.get(bstack111ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ᭾")))
    def _111l1l1111l_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack111ll11_opy_ (u"ࠦࠧࠨࡐࡢࡴࡶࡩࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡵࡳࡲࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢ࡬ࡲࡹࡵࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡧࡥࡹࡧࠠࡧࡱࡵࡱࡦࡺ࠮ࠣࠤࠥ᭿")
        if not args:
            return None
        data = None
        bstack111l1l111l1_opy_ = args[0]
        if hasattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᮀ")) and hasattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᮁ")):
            bstack111l1l11ll1_opy_ = getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᮂ"), [])
            bstack111l11l1lll_opy_ = getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡪࡦࠪᮃ"), None)
            bstack111l1l11l1l_opy_ = getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᮄ"), {})
            file_path = getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡲࡤࡸ࡭࠭ᮅ"), None)
            test_name = bstack111l1l111l1_opy_.name
            if not bstack111l11l1lll_opy_ and file_path and test_name:
                bstack111l11l1lll_opy_ = bstack111ll11_opy_ (u"ࠦࢀࢃ࠺࠻ࡽࢀࠦᮆ").format(file_path, test_name)
            data = {
                TestFramework.bstack1l111l1ll1l_opy_: bstack111l1l111l1_opy_.uuid,
                TestFramework.bstack11l1l1l1l1l_opy_: bstack111l1l111l1_opy_.uuid,
                TestFramework.bstack1l111l1lll1_opy_: test_name,
                TestFramework.bstack11l1111l1ll_opy_: file_path,
                TestFramework.bstack111lll111ll_opy_: getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᮇ"), None),
                TestFramework.bstack111ll1l1l11_opy_: getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᮈ"), []),
                TestFramework.bstack111ll111ll1_opy_: bstack111l1l11ll1_opy_,
                bstack111ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪࡹࠧᮉ"): bstack111l1l11ll1_opy_,
                TestFramework.bstack11l111l1ll1_opy_: getattr(bstack111l1l111l1_opy_, bstack111ll11_opy_ (u"ࠨ࡯ࡨࡸࡦ࠭ᮊ"), {}),
                TestFramework.bstack11l11l1l1ll_opy_: test_name,
                bstack111ll11_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫᮋ"): {},
                TestFramework.bstack11ll111111l_opy_: bstack111l11l1lll_opy_,
                bstack111ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᮌ"): bstack111l1l11l1l_opy_,
            }
            data[bstack111ll11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᮍ")] = {bstack111ll11_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᮎ"): bstack111l11l1lll_opy_}
        elif isinstance(bstack111l1l111l1_opy_, dict):
            bstack111l1l11ll1_opy_ = bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᮏ")) or bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠧࡴࡥࡲࡴࡪ࠭ᮐ"), [])
            bstack111l11l1lll_opy_ = bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟ࡪࡦࠪᮑ")) or bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡊࡦࠪᮒ"))
            bstack111l1l11l1l_opy_ = bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᮓ"), {})
            file_path = bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡳࡥࡹ࡮ࠧᮔ")) or bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡓࡥࡹ࡮ࠧᮕ"))
            test_name = bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᮖ")) or bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡓࡧ࡭ࡦࠩᮗ"))
            if not bstack111l11l1lll_opy_ and file_path and test_name:
                bstack111l11l1lll_opy_ = bstack111ll11_opy_ (u"ࠣࡽࢀ࠾࠿ࢁࡽࠣᮘ").format(file_path, test_name)
            data = {
                TestFramework.bstack1l111l1ll1l_opy_: bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᮙ")) or bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡊࡦࠪᮚ")) or str(uuid4()),
                TestFramework.bstack11l1l1l1l1l_opy_: bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡋࡧࠫᮛ")) or bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠬࡻࡵࡪࡦࠪᮜ")),
                TestFramework.bstack1l111l1lll1_opy_: test_name,
                TestFramework.bstack11l1111l1ll_opy_: file_path,
                TestFramework.bstack111lll111ll_opy_: bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"࠭ࡣࡰࡦࡨࠫᮝ")),
                TestFramework.bstack111ll1l1l11_opy_: bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᮞ"), []),
                TestFramework.bstack111ll111ll1_opy_: bstack111l1l11ll1_opy_,
                bstack111ll11_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᮟ"): bstack111l1l11ll1_opy_,
                TestFramework.bstack11l111l1ll1_opy_: bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠩࡰࡩࡹࡧࠧᮠ"), {}),
                TestFramework.bstack11l11l1l1ll_opy_: bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᮡ")) or test_name,
                bstack111ll11_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ᮢ"): bstack111l1l111l1_opy_.get(bstack111ll11_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧᮣ"), {}),
                TestFramework.bstack11ll111111l_opy_: bstack111l11l1lll_opy_,
                bstack111ll11_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᮤ"): bstack111l1l11l1l_opy_,
            }
            data[bstack111ll11_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᮥ")] = {bstack111ll11_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᮦ"): bstack111l11l1lll_opy_}
        return data
    def _111l1l11111_opy_(self, instance: bstack1l111llll11_opy_, *args, **kwargs):
        bstack111ll11_opy_ (u"ࠤࠥࠦࡑࡵࡡࡥࠢࡷࡩࡸࡺࠠࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡ࡫ࡱࡸࡴࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠤࠥࠦᮧ")
        bstack111l11ll11l_opy_ = None
        if args and hasattr(args[0], bstack111ll11_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᮨ")) and args[0].result:
            bstack1llll1l11ll_opy_ = args[0]
            result = bstack1llll1l11ll_opy_.result
            bstack111l11ll11l_opy_ = {
                TestFramework.bstack11l1ll11111_opy_: getattr(result, bstack111ll11_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᮩ"), bstack111ll11_opy_ (u"ࠬࡶࡥ࡯ࡦ࡬ࡲ࡬᮪࠭")),
                TestFramework.bstack11l1ll111ll_opy_: None,
                TestFramework.bstack111lll1llll_opy_: None,
            }
            if hasattr(result, bstack111ll11_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯᮫ࠩ")) and result.exception:
                bstack111l11ll11l_opy_[TestFramework.bstack11l1ll111ll_opy_] = [{bstack111ll11_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᮬ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack111ll11_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࠫᮭ")) else None
                bstack111l11ll11l_opy_[TestFramework.bstack111lll1llll_opy_] = exc_type or bstack111ll11_opy_ (u"ࠤࡘࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡊࡸࡲࡰࡴࠥᮮ")
            bstack111l1l11l1l_opy_ = getattr(bstack1llll1l11ll_opy_, bstack111ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩᮯ"), None)
            if bstack111l1l11l1l_opy_:
                bstack111l11ll11l_opy_[bstack111ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ᮰")] = bstack111l1l11l1l_opy_
                logger.debug(bstack111ll11_opy_ (u"࡛ࠧࡰࡥࡣࡷࡩࡩࠦࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠥࡧࡴࠡࡒࡒࡗ࡙ࠦࡴࡪ࡯ࡨ࠾ࠥࠨ᮱") + str(list(bstack111l1l11l1l_opy_.keys()) if bstack111l1l11l1l_opy_ else []) + bstack111ll11_opy_ (u"ࠨࠢ᮲"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack111l11ll11l_opy_ = {
                TestFramework.bstack11l1ll11111_opy_: data.get(bstack111ll11_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ᮳"), TestFramework.bstack111ll11llll_opy_),
                TestFramework.bstack11l1ll111ll_opy_: data.get(bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩ᮴")),
                TestFramework.bstack111lll1llll_opy_: data.get(bstack111ll11_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࡢࡸࡾࡶࡥࠨ᮵")),
            }
            bstack111l1l11l1l_opy_ = data.get(bstack111ll11_opy_ (u"ࠪ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠩ᮶"))
            if bstack111l1l11l1l_opy_:
                bstack111l11ll11l_opy_[bstack111ll11_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪ᮷")] = bstack111l1l11l1l_opy_
                logger.debug(bstack111ll11_opy_ (u"࡛ࠧࡰࡥࡣࡷࡩࡩࠦࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠥࡧࡴࠡࡒࡒࡗ࡙ࠦࡴࡪ࡯ࡨ࠾ࠥࠨ᮸") + str(list(bstack111l1l11l1l_opy_.keys()) if bstack111l1l11l1l_opy_ else []) + bstack111ll11_opy_ (u"ࠨࠢ᮹"))
        if bstack111l11ll11l_opy_:
            if bstack111l11ll11l_opy_.get(TestFramework.bstack11l1ll11111_opy_) != TestFramework.bstack111ll11llll_opy_:
                bstack111l11ll11l_opy_[TestFramework.bstack11lll1l11l1_opy_] = datetime.now(tz=timezone.utc)
            TestFramework.bstack11l111l11ll_opy_(instance, bstack111l11ll11l_opy_)
            logger.debug(bstack111ll11_opy_ (u"ࠢࡍࡱࡤࡨࡪࡪࠠࡵࡧࡶࡸࠥࡸࡥࡴࡷ࡯ࡸ࠿ࠦࠢᮺ") + str(bstack111l11ll11l_opy_.get(TestFramework.bstack11l1ll11111_opy_)) + bstack111ll11_opy_ (u"ࠣࠤᮻ"))
    def _111l11lll1l_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll11_opy_ (u"ࠤ࡙ࠥࠦࡸࡡࡤ࡭ࠣ࡬ࡴࡵ࡫ࠡࡧࡹࡩࡳࡺࡳࠡࠪࡅࡉࡋࡕࡒࡆࡡࡄࡐࡑ࠲ࠠࡂࡈࡗࡉࡗࡥࡁࡍࡎ࠯ࠤࡪࡺࡣ࠯ࠫ࠱ࠦࠧࠨᮼ")
        key = test_framework_state.name
        bstack11l11111l1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠪᮽ"), {})
        if key not in bstack11l11111l1l_opy_:
            bstack11l11111l1l_opy_[key] = []
        bstack111ll1lll1l_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, bstack111ll11_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠬᮾ"), {})
        if key not in bstack111ll1lll1l_opy_:
            bstack111ll1lll1l_opy_[key] = []
        bstack111lll1ll1l_opy_ = {
            bstack111ll11_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠬᮿ"): bstack11l11111l1l_opy_,
            bstack111ll11_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠧᯀ"): bstack111ll1lll1l_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack111ll11_opy_ (u"ࠢ࡬ࡧࡼࠦᯁ"): key,
                TestFramework.bstack11l11111l11_opy_: str(uuid4()),
                TestFramework.bstack111lll11ll1_opy_: TestFramework.bstack111ll11l1ll_opy_,
                TestFramework.bstack111ll1l1ll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack11l111l1111_opy_: [],
                TestFramework.bstack11l11111ll1_opy_: kwargs.get(bstack111ll11_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᯂ"), key),
            }
            bstack11l11111l1l_opy_[key].append(hook)
            bstack111lll1ll1l_opy_[bstack111ll11_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟࡭ࡣࡶࡸࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᯃ")] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llllll1l_opy_ = bstack11l11111l1l_opy_.get(key, [])
            hook = bstack111llllll1l_opy_.pop() if bstack111llllll1l_opy_ else None
            if hook:
                hook[TestFramework.bstack111llll1lll_opy_] = datetime.now(tz=timezone.utc)
                bstack111ll1lll1l_opy_[key].append(hook)
                bstack111lll1ll1l_opy_[bstack111ll11_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠ࡮ࡤࡷࡹࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠨᯄ")] = key
        TestFramework.bstack11l111l11ll_opy_(instance, bstack111lll1ll1l_opy_)
        logger.debug(bstack111ll11_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢ࡬ࡴࡵ࡫ࡠࡧࡹࡩࡳࡺ࠺ࠡࡽ࡮ࡩࡾࢃ࠮ࠣᯅ") + str(test_hook_state) + bstack111ll11_opy_ (u"ࠧࠨᯆ"))
    def bstack11ll1ll11l1_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]
    ) -> List[bstack1llll111ll_opy_]:
        bstack111ll11_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡲ࡯ࡨࠢࡨࡲࡹࡸࡩࡦࡵࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣ࡬ࡴࡵ࡫ࠡࡵࡷࡥࡹ࡫࠮ࠣࠤࠥᯇ")
        if instance is None:
            return []
        return TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, [])
    def bstack11lll1l111l_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack111ll11_opy_ (u"ࠢࠣࠤࡆࡰࡪࡧࡲࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡨࡰࡱ࡮ࠤࡸࡺࡡࡵࡧ࠱ࠦࠧࠨᯈ")
        if instance is None:
            return
        TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, [])
    def get_current_test_instance(self) -> Optional[bstack1l111llll11_opy_]:
        bstack111ll11_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠࡵࡪࡨࠤࡨࡻࡲࡳࡧࡱࡸࠥࡺࡥࡴࡶࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡪࡵࡩࡦࡪ࠮ࠣࠤࠥᯉ")
        thread_id = threading.get_ident()
        target = self._111l11lllll_opy_.get(thread_id)
        if target:
            return self._111l1l111ll_opy_.get(target)
        return None
    def bstack111l11lll11_opy_(
        self,
        instance: bstack1l111llll11_opy_,
        log_entry: bstack1llll111ll_opy_
    ):
        bstack111ll11_opy_ (u"ࠤࠥࠦࡆࡪࡤࠡࡣࠣࡰࡴ࡭ࠠࡦࡰࡷࡶࡾࠦࡴࡰࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠤࠥࠦᯊ")
        if instance is None:
            return
        logs = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, [])
        logs.append(log_entry)
        TestFramework.bstack11l1ll11ll_opy_(instance, TestFramework.bstack11l1111ll1l_opy_, logs)
    def __111llll1l11_opy_(self, instance: bstack1l111llll11_opy_) -> None:
        bstack111ll11_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡍࡱࡤࡨࡸࠦࡣࡶࡵࡷࡳࡲࠦࡴࡢࡩࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡆࡶࡪࡧࡴࡦࡵࠣࡥࠥࡪࡩࡤࡶࠣࡧࡴࡴࡴࡢ࡫ࡱ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡲࡥࡷࡧ࡯ࠤࡨࡻࡳࡵࡱࡰࠤࡲ࡫ࡴࡢࡦࡤࡸࡦࠦࡲࡦࡶࡵ࡭ࡪࡼࡥࡥࠢࡩࡶࡴࡳࠊࠡࠢࠣࠤࠥࠦࠠࠡࡅࡸࡷࡹࡵ࡭ࡕࡣࡪࡑࡦࡴࡡࡨࡧࡵࠤࡦࡴࡤࠡࡷࡳࡨࡦࡺࡥࡴࠢࡷ࡬ࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡵࡷࡥࡹ࡫ࠠࡶࡵ࡬ࡲ࡬ࠦࡳࡦࡶࡢࡷࡹࡧࡴࡦࡡࡨࡲࡹࡸࡩࡦࡵ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᯋ")
        bstack111lll1ll1l_opy_ = {bstack111ll11_opy_ (u"ࠦࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦࠨᯌ"): bstack1l1l111111l_opy_.bstack111ll1ll1ll_opy_()}
        TestFramework.bstack11l111l11ll_opy_(instance, bstack111lll1ll1l_opy_)
    def __111l11ll1ll_opy_(self, instance: bstack1l111llll11_opy_) -> None:
        bstack111ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡓࡶࡴࡩࡥࡴࡵࡨࡷࠥࡺࡥࡴࡶ࠰ࡰࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹࠠࡶࡲ࡯ࡳࡦࡪࡥࡥࠢࡹ࡭ࡦࠦࡆࡪ࡮ࡨ࡙ࡵࡲ࡯ࡢࡦࡨࡶ࠳ࡻࡰ࡭ࡱࡤࡨࡤࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠪࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡓࡤࡣࡱࡷࠥࡺࡨࡦࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥࡧ࡮ࡥࠢࡶࡩࡳࡪࡳࠡ࡮ࡲ࡫ࡸࠦࡶࡪࡣࠣ࡫ࡗࡖࡃ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᯍ")
        from bstack_utils.helper import bstack11ll1lll1ll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᯎ"), bstack111ll11_opy_ (u"ࠧ࠱ࠩᯏ"))
            bstack11lll11l1ll_opy_ = os.path.join(
                bstack11ll1lll1ll_opy_(),
                bstack111ll11_opy_ (u"ࠣࡗࡳࡰࡴࡧࡤࡦࡦࡄࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࡹ࠭ࡼࡿࠥᯐ").format(platform_index),
                bstack111ll11_opy_ (u"ࠤࡗࡩࡸࡺࡌࡦࡸࡨࡰࠧᯑ")
            )
            if not os.path.isdir(bstack11lll11l1ll_opy_):
                logger.debug(bstack111ll11_opy_ (u"ࠥࡒࡴࠦࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦࡤࡪࡴࡨࡧࡹࡵࡲࡺࠢࡩࡳࡺࡴࡤ࠻ࠢࠥᯒ") + str(bstack11lll11l1ll_opy_) + bstack111ll11_opy_ (u"ࠦࠧᯓ"))
                return
            bstack11lll1l1lll_opy_ = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_, bstack111ll11_opy_ (u"ࠧࠨᯔ"))
            bstack111l11ll111_opy_ = []
            for file_name in os.listdir(bstack11lll11l1ll_opy_):
                file_path = os.path.join(bstack11lll11l1ll_opy_, file_name)
                if os.path.isfile(file_path):
                    try:
                        bstack11lll1l1l11_opy_ = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(bstack11lll1l1l11_opy_, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = bstack1llll111ll_opy_(
                            kind=bstack111ll11_opy_ (u"ࠨࡔࡆࡕࡗࡣࡆ࡚ࡔࡂࡅࡋࡑࡊࡔࡔࠣᯕ"),
                            message=bstack111ll11_opy_ (u"ࠢࠣᯖ"),
                            level=bstack111ll11_opy_ (u"ࠣࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠦᯗ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            bstack11ll1l1l1ll_opy_=file_size,
                            bstack11ll1ll1l1l_opy_=bstack111ll11_opy_ (u"ࠤࡐࡅࡓ࡛ࡁࡍࡡࡘࡔࡑࡕࡁࡅࠤᯘ"),
                            bstack1l11l11_opy_=os.path.abspath(file_path),
                            bstack1lllllll11_opy_=bstack11lll1l1lll_opy_
                        )
                        bstack111l11ll111_opy_.append(log_entry)
                        logger.debug(bstack111ll11_opy_ (u"ࠥࡅࡩࡪࡥࡥࠢࡤࡸࡹࡧࡣࡩ࡯ࡨࡲࡹࠦ࡬ࡰࡩࠣࡩࡳࡺࡲࡺ࠼ࠣࠦᯙ") + str(file_name) + bstack111ll11_opy_ (u"ࠦࠧᯚ"))
                    except Exception as bstack11ll1l11l1l_opy_:
                        logger.error(bstack111ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࢁࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧᯛ") + str(bstack11ll1l11l1l_opy_) + bstack111ll11_opy_ (u"ࠨࠢᯜ"))
            if bstack111l11ll111_opy_ and self.bstack1l1l1l1l1l_opy_:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack111ll11_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡍࡋࡢࡆࡎࡔ࡟ࡔࡇࡖࡗࡎࡕࡎࡠࡋࡇࠦᯝ"), bstack111ll11_opy_ (u"ࠣࠤᯞ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack111ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᯟ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack111l11ll111_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack111ll11_opy_ (u"ࠥࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠦᯠ")
                        log_entry.test_framework_version = TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11111l_opy_, bstack111ll11_opy_ (u"ࠦࠧᯡ"))
                        log_entry.uuid = bstack11lll1l1lll_opy_
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack11l11l1lll1_opy_ (u"ࠧࠨᯢ")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.bstack11ll1l1l1ll_opy_
                        log_entry.file_path = entry.bstack1l11l11_opy_
                    self.bstack1l1l1l1l1l_opy_.LogCreatedEvent(req)
                    logger.debug(bstack111ll11_opy_ (u"ࠨࡓࡦࡰࡷࠤࠧᯣ") + str(len(bstack111l11ll111_opy_)) + bstack111ll11_opy_ (u"ࠢࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡲ࡯ࡨࡵࠣࡺ࡮ࡧࠠࡨࡔࡓࡇࠧᯤ"))
                except Exception as bstack11llll1lll_opy_:
                    logger.error(bstack111ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡴࡧࡱࡨ࡮ࡴࡧࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡲ࡯ࡨࡵࠣࡺ࡮ࡧࠠࡨࡔࡓࡇ࠿ࠦࠢᯥ") + str(bstack11llll1lll_opy_) + bstack111ll11_opy_ (u"ࠤ᯦ࠥ"))
        except Exception as e:
            logger.error(bstack111ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷ࠱ࡱ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࡳ࠻ࠢࠥᯧ") + str(e) + bstack111ll11_opy_ (u"ࠦࠧᯨ"))