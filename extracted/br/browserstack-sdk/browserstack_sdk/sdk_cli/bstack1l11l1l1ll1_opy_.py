# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
bstack1l1111l_opy_ (u"ࠨࠢࠣࠌ࡙ࡥࡳ࡯࡬࡭ࡣࡓࡽࡹ࡮࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࠲ࠦࡔࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪ࡯ࡳࡰࡪࡳࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡼࡡ࡯࡫࡯ࡰࡦࠦࡐࡺࡶ࡫ࡳࡳࠦࡴࡦࡵࡷࡷ࠳ࠐࡔࡩ࡫ࡶࠤࡲࡵࡤࡶ࡮ࡨࠤࡵࡸ࡯ࡷ࡫ࡧࡩࡸࠦࡥࡷࡧࡱࡸࠥࡺࡲࡢࡥ࡮࡭ࡳ࡭ࠠࡢࡰࡧࠤࡸࡺࡡࡵࡧࠣࡱࡦࡴࡡࡨࡧࡰࡩࡳࡺࠠࡧࡱࡵࠤࡵࡿࡴࡩࡱࡱ࠱࡬࡫࡮ࡦࡴ࡬ࡧࠥࡺࡥࡴࡶࡶ࠰ࠏࡹࡩ࡮࡫࡯ࡥࡷࠦࡴࡰ࡙ࠢࡥࡳ࡯࡬࡭ࡣࡍࡥࡻࡧࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡢࡩࡨࡲࡹ࠴ࠊࠣࠤࠥ᭗")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1ll11lll1_opy_, bstack1l1ll1ll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l11l1ll111_opy_,
    TestHookState,
    bstack1ll1lll111l_opy_,
    bstack11lll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll11l1l_opy_ import bstack1l1lll111l1_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l1l11ll1_opy_ import bstack1l1l1l1lll1_opy_
logger = logging.getLogger(__name__)
class bstack1l1l11lll11_opy_(TestFramework):
    bstack1l1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࡕࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡑࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸࠦࠨࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠪ࠰ࠍࠤࠥࠦࠠࡉࡣࡱࡨࡱ࡫ࡳࠡࡧࡹࡩࡳࡺࠠࡵࡴࡤࡧࡰ࡯࡮ࡨ࠮ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵ࠮ࠣࡥࡳࡪࠠࡩࡱࡲ࡯ࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࡳࠡࡨࡲࡶࠏࠦࠠࠡࠢࡷࡩࡸࡺࡳࠡࡶ࡫ࡥࡹࠦࡤࡰࡰࠪࡸࠥࡻࡳࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡲࡶࠥࡵࡴࡩࡧࡵࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸ࠴ࠊࠡࠢࠣࠤ࡙࡮ࡩࡴࠢ࡬ࡷࠥࡺࡨࡦࠢࡓࡽࡹ࡮࡯࡯ࠢࡨࡵࡺ࡯ࡶࡢ࡮ࡨࡲࡹࠦ࡯ࡧ࡙ࠢࡥࡳ࡯࡬࡭ࡣࡍࡥࡻࡧࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡲࠥࡺࡨࡦࠢࡍࡥࡻࡧࠠࡔࡆࡎ࠲ࠏࠦࠠࠡࠢࠥࠦࠧ᭘")
    FRAMEWORK_NAME = bstack1l1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩ᭙")
    bstack111ll11ll11_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l111lllll1_opy_: Dict[str, str] = None,
        bstack1l1l1lll111_opy_: List[str] = None,
        bstack1l1lll11l1l_opy_: bstack1l1lll111l1_opy_ = None,
        bstack11l1ll1lll_opy_=None
    ):
        bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳࡹ࠺ࠡࡆ࡬ࡧࡹࠦ࡭ࡢࡲࡳ࡭ࡳ࡭ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡲࡦࡳࡥࡴࠢࡷࡳࠥࡼࡥࡳࡵ࡬ࡳࡳࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹ࠺ࠡࡎ࡬ࡷࡹࠦ࡯ࡧࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡴࡡ࡮ࡧࡶࠤ࠭ࡪࡥࡧࡣࡸࡰࡹࡹࠠࡵࡱࠣ࡟ࠧࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨࠨ࡝ࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡢࡵࡼࡲࡨࡥࡤࡪࡵࡳࡥࡹࡩࡨࡦࡴ࠽ࠤࡆࡹࡹ࡯ࡥࡇ࡭ࡸࡶࡡࡵࡥ࡫ࡩࡷࠦࡦࡰࡴࠣࡦࡦࡩ࡫ࡨࡴࡲࡹࡳࡪࠠࡰࡲࡨࡶࡦࡺࡩࡰࡰࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡰ࡮ࡥࡳࡦࡴࡹ࡭ࡨ࡫࠺ࠡࡩࡕࡔࡈࠦࡃࡍࡋࠣࡷࡪࡸࡶࡪࡥࡨࠤࡨࡲࡩࡦࡰࡷࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᭚")
        if bstack1l1l1lll111_opy_ is None:
            bstack1l1l1lll111_opy_ = [self.FRAMEWORK_NAME]
        if bstack1l111lllll1_opy_ is None:
            bstack1l111lllll1_opy_ = {self.FRAMEWORK_NAME: self._111l1l111l1_opy_()}
        super().__init__(bstack1l1l1lll111_opy_, bstack1l111lllll1_opy_, bstack1l1lll11l1l_opy_)
        self.bstack11l1ll1lll_opy_ = bstack11l1ll1lll_opy_
        self._111l11l1l1l_opy_: Dict[str, bstack1l11l1ll111_opy_] = {}
        self._111l1l1111l_opy_: Dict[int, str] = {}
        logger.info(bstack1l1111l_opy_ (u"࡚ࠥࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࡯࡮ࡪࡶ࡬ࡥࡱ࡯ࡺࡦࡦࠣࡻ࡮ࡺࡨࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡷࡂࠨ᭛") + str(bstack1l1l1lll111_opy_) + bstack1l1111l_opy_ (u"ࠦࠧ᭜"))
    def _111l1l111l1_opy_(self) -> str:
        bstack1l1111l_opy_ (u"ࠧࠨࠢࡈࡧࡷࠤࡹ࡮ࡥࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡓࡽࡹ࡮࡯࡯ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡷࡹࡸࡩ࡯ࡩ࠱ࠦࠧࠨ᭝")
        return bstack1l1111l_opy_ (u"ࠨࡻࡾ࠰ࡾࢁ࠳ࢁࡽࠣ᭞").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def bstack11ll11l111l_opy_(self) -> bool:
        bstack1l1111l_opy_ (u"ࠢࠣࠤࡕࡩࡹࡻࡲ࡯ࠢࡉࡥࡱࡹࡥࠡࡣࡶࠤࡹ࡮ࡩࡴࠢ࡬ࡷࠥࡴ࡯ࡵࠢࡤࠤࡵࡿࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥ᭟")
        return False
    def bstack11ll1l11l1l_opy_(self) -> bool:
        bstack1l1111l_opy_ (u"ࠣࠤࠥࡖࡪࡺࡵࡳࡰࠣࡊࡦࡲࡳࡦࠢࡤࡷࠥࡺࡨࡪࡵࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡥࠥࡸ࡯ࡣࡱࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥ᭠")
        return False
    def track_event(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1111l_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡔࡳࡣࡦ࡯ࠥࡧࠠࡵࡧࡶࡸࠥࡲࡩࡧࡧࡦࡽࡨࡲࡥࠡࡧࡹࡩࡳࡺ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡣࡰࡰࡷࡩࡽࡺ࠺ࠡࡖࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡄࡱࡱࡸࡪࡾࡴࠡࡹ࡬ࡸ࡭ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢࡱࡥࡲ࡫ࠬࠡࡸࡨࡶࡸ࡯࡯࡯࠮ࠣࡥࡳࡪࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢ࡬ࡲࡩ࡫ࡸࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡀࠠࡕࡪࡨࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡹࡴࡢࡶࡨࠤ࠭ࡏࡎࡊࡖࡢࡘࡊ࡙ࡔ࠭ࠢࡗࡉࡘ࡚ࠬࠡࡧࡷࡧ࠳࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠺ࠡࡒࡵࡩࠥࡵࡲࠡࡒࡲࡷࡹࠦࡨࡰࡱ࡮ࠤࡸࡺࡡࡵࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠬࡤࡶ࡬ࡹ࠺ࠡࡃࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳࠡࠪࡷࡽࡵ࡯ࡣࡢ࡮࡯ࡽ࡚ࠥࡥࡴࡶࡇࡥࡹࡧࠠࡰࡴࠣࡨ࡮ࡩࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠫࠬ࡮ࡻࡦࡸࡧࡴ࠼ࠣࡅࡩࡪࡩࡵ࡫ࡲࡲࡦࡲࠠ࡬ࡧࡼࡻࡴࡸࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣ᭡")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack1l1111l_opy_ (u"ࠥࡍ࡬ࡴ࡯ࡳࡧࡧࠤࡨࡧ࡬࡭ࡤࡤࡧࡰࠦࡦࡰࡴࠣࡷࡹࡧࡴࡦ࠿ࠥ᭢") + str(test_framework_state) + bstack1l1111l_opy_ (u"ࠦࠧ᭣"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack1l1111l_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࡺࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ᭤") + str(kwargs) + bstack1l1111l_opy_ (u"ࠨࠢ᭥"))
            return
        instance = self._111l1l11l11_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack1l1111l_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡵ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡵࡩࡸࡵ࡬ࡷࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡳࠢࡨࡺࡪࡴࡴ࠾ࡽࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿ࠱ࠦ᭦") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠣࠤ᭧"))
            return
        try:
            self._111l11l1lll_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡪࡤࡲࡩࡲࡩ࡯ࡩࠣࡩࡻ࡫࡮ࡵࠢࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࢀࡺࡥࡴࡶࡢ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠻ࠢࠥ᭨") + str(e) + bstack1l1111l_opy_ (u"ࠥࠦ᭩"))
        self.bstack111lllll11l_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _111l11l1lll_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1111l_opy_ (u"ࠦࠧࠨࡈࡢࡰࡧࡰࡪࠦࡳࡱࡧࡦ࡭࡫࡯ࡣࠡࡧࡹࡩࡳࡺࠠࡵࡻࡳࡩࡸ࠴ࠢࠣࠤ᭪")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11l1ll11111_opy_):
                bstack1llll1l1ll1_opy_ = self._111l11ll11l_opy_(args, kwargs)
                if bstack1llll1l1ll1_opy_:
                    instance.data.update(bstack1llll1l1ll1_opy_)
                    logger.debug(bstack1l1111l_opy_ (u"ࠧࡒ࡯ࡢࡦࡨࡨࠥࡺࡥࡴࡶࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣ᭫") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠨ᭬ࠢ"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11lll1111ll_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11lll1111ll_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack1l1111l_opy_ (u"ࠢࡔࡧࡷࠤࡹ࡫ࡳࡵ࠯ࡶࡸࡦࡸࡴࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣ᭭") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠣࠤ᭮"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.bstack1l1lll1l111_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_):
                    TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack11ll1ll1l11_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack1l1111l_opy_ (u"ࠤࡖࡩࡹࠦࡴࡦࡵࡷ࠱ࡪࡴࡤࠡࡨࡲࡶࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣ᭯") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠥࠦ᭰"))
                self._111l11lll1l_opy_(instance, *args, **kwargs)
                self.__11l1111llll_opy_(instance)
                self.__111l11l11l1_opy_(instance)
        elif test_framework_state in bstack1l1l11lll11_opy_.bstack111ll11ll11_opy_:
            self._111l11lll11_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack1l1111l_opy_ (u"ࠦࡹࡸࡡࡤ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣ࡬ࡦࡴࡤ࡭ࡧࡧࠤࡪࡼࡥ࡯ࡶࡀࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࠧ᭱") + str(instance.ref()) + bstack1l1111l_opy_ (u"ࠧࠨ᭲"))
    def _111l1l11l11_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[bstack1l11l1ll111_opy_]:
        bstack1l1111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡹ࡯࡭ࡸࡨࠤࡴࡸࠠࡤࡴࡨࡥࡹ࡫ࠠࡢࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡖࡨࡷࡹࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡴࡸࠠࡊࡐࡌࡘࡤ࡚ࡅࡔࡖࠣࡔࡗࡋࠬࠡࡥࡵࡩࡦࡺࡥࡴࠢࡤࠤࡳ࡫ࡷࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌ࡯ࡳࠢࡲࡸ࡭࡫ࡲࠡࡧࡹࡩࡳࡺࡳ࠭ࠢ࡯ࡳࡴࡱࡳࠡࡷࡳࠤࡹ࡮ࡥࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥ᭳")
        target = self._111l11l1l11_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._111l11l11ll_opy_(context, target)
            self._111l1l1111l_opy_[thread_id] = target
            return instance
        if target and target in self._111l11l1l1l_opy_:
            return self._111l11l1l1l_opy_[target]
        bstack111l11l1ll1_opy_ = self._111l1l1111l_opy_.get(thread_id)
        if bstack111l11l1ll1_opy_ and bstack111l11l1ll1_opy_ in self._111l11l1l1l_opy_:
            return self._111l11l1l1l_opy_[bstack111l11l1ll1_opy_]
        instance = TestFramework.bstack1l1ll1ll1ll_opy_(target) if target else None
        if instance:
            return instance
        logger.debug(bstack1l1111l_opy_ (u"ࠢࡏࡱࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡸ࡭ࡸࡥࡢࡦࡢ࡭ࡩࡃࠢ᭴") + str(thread_id) + bstack1l1111l_opy_ (u"ࠣࠤ᭵"))
        return None
    def _111l11l11ll_opy_(
        self,
        context: bstack1ll1lll111l_opy_,
        target: str
    ) -> bstack1l11l1ll111_opy_:
        bstack1l1111l_opy_ (u"ࠤࠥࠦࡈࡸࡥࡢࡶࡨࠤࡦࠦ࡮ࡦࡹࠣࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡸࠠࡵࡴࡤࡧࡰ࡯࡮ࡨ࠰ࠥࠦࠧ᭶")
        ctx = bstack1l1ll11lll1_opy_.create_context(target)
        instance = bstack1l11l1ll111_opy_(
            ctx,
            self.bstack1l1l1lll111_opy_,
            self.bstack1l111lllll1_opy_,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.bstack111ll1lllll_opy_(instance, {
            TestFramework.bstack11llllll111_opy_: str(uuid4()),
            TestFramework.bstack1l11111l11l_opy_: context.test_framework_name,
            TestFramework.bstack11ll11l1lll_opy_: context.test_framework_version,
            TestFramework.bstack111lll1lll1_opy_: [],
            TestFramework.bstack11l1ll1111l_opy_: TestFramework.bstack111lll1l1ll_opy_,
        })
        if context.platform_index >= 0:
            TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack1l111l1l111_opy_, context.platform_index)
        self._111l11l1l1l_opy_[target] = instance
        TestFramework.bstack1lllll1ll1_opy_[ctx.id] = instance
        logger.debug(bstack1l1111l_opy_ (u"ࠥࡇࡷ࡫ࡡࡵࡧࡧࠤࡳ࡫ࡷࠡࡶࡨࡷࡹࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥࡺࡡࡳࡩࡨࡸࡂࢁࡴࡢࡴࡪࡩࡹࢃࠠࡤࡶࡻ࠲࡮ࡪ࠽ࠣ᭷") + str(ctx.id) + bstack1l1111l_opy_ (u"ࠦࠧ᭸"))
        return instance
    def _111l11l1l11_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack1l1111l_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡶࡤࡶ࡬࡫ࡴࠡࠪࡷࡩࡸࡺࠠ࡯ࡣࡰࡩ࠮ࠦࡦࡳࡱࡰࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹ࠮ࠣࠤࠥ᭹")
        if args and hasattr(args[0], bstack1l1111l_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ᭺")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack1l1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ᭻")) or
                    args[0].get(bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡔࡡ࡮ࡧࠪ᭼")) or
                    args[0].get(bstack1l1111l_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧ᭽")) or
                    args[0].get(TestFramework.bstack1l111l11l1l_opy_))
        return (kwargs.get(bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭᭾")) or
                kwargs.get(bstack1l1111l_opy_ (u"ࠫࡹ࡫ࡳࡵࡐࡤࡱࡪ࠭᭿")) or
                kwargs.get(bstack1l1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᮀ")))
    def _111l11ll11l_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack1l1111l_opy_ (u"ࠨࠢࠣࡒࡤࡶࡸ࡫ࠠࡵࡧࡶࡸࠥࡪࡡࡵࡣࠣࡪࡷࡵ࡭ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡴࡰࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡩࡧࡴࡢࠢࡩࡳࡷࡳࡡࡵ࠰ࠥࠦࠧᮁ")
        if not args:
            return None
        data = None
        bstack111l11ll1ll_opy_ = args[0]
        if hasattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᮂ")) and hasattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᮃ")):
            bstack111l11ll111_opy_ = getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᮄ"), [])
            bstack111l11lllll_opy_ = getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡ࡬ࡨࠬᮅ"), None)
            bstack111l11ll1l1_opy_ = getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪᮆ"), {})
            file_path = getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡴࡦࡺࡨࠨᮇ"), None)
            test_name = bstack111l11ll1ll_opy_.name
            if not bstack111l11lllll_opy_ and file_path and test_name:
                bstack111l11lllll_opy_ = bstack1l1111l_opy_ (u"ࠨࡻࡾ࠼࠽ࡿࢂࠨᮈ").format(file_path, test_name)
            data = {
                TestFramework.bstack11llllll111_opy_: bstack111l11ll1ll_opy_.uuid,
                TestFramework.bstack11l1ll11111_opy_: bstack111l11ll1ll_opy_.uuid,
                TestFramework.bstack1l111l11l1l_opy_: test_name,
                TestFramework.bstack11l1111ll11_opy_: file_path,
                TestFramework.bstack11l1111111l_opy_: getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠧࡤࡱࡧࡩࠬᮉ"), None),
                TestFramework.bstack11l11111ll1_opy_: getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᮊ"), []),
                TestFramework.bstack111ll11111l_opy_: bstack111l11ll111_opy_,
                bstack1l1111l_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᮋ"): bstack111l11ll111_opy_,
                TestFramework.bstack111ll11l11l_opy_: getattr(bstack111l11ll1ll_opy_, bstack1l1111l_opy_ (u"ࠪࡱࡪࡺࡡࠨᮌ"), {}),
                TestFramework.bstack11l11l11l1l_opy_: test_name,
                bstack1l1111l_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭ᮍ"): {},
                TestFramework.bstack11ll11111l1_opy_: bstack111l11lllll_opy_,
                bstack1l1111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᮎ"): bstack111l11ll1l1_opy_,
            }
            data[bstack1l1111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᮏ")] = {bstack1l1111l_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᮐ"): bstack111l11lllll_opy_}
        elif isinstance(bstack111l11ll1ll_opy_, dict):
            bstack111l11ll111_opy_ = bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠨࡵࡦࡳࡵ࡫ࡳࠨᮑ")) or bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᮒ"), [])
            bstack111l11lllll_opy_ = bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡ࡬ࡨࠬᮓ")) or bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡌࡨࠬᮔ"))
            bstack111l11ll1l1_opy_ = bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᮕ"), {})
            file_path = bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠩᮖ")) or bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠧࡧ࡫࡯ࡩࡕࡧࡴࡩࠩᮗ"))
            test_name = bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᮘ")) or bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡎࡢ࡯ࡨࠫᮙ"))
            if not bstack111l11lllll_opy_ and file_path and test_name:
                bstack111l11lllll_opy_ = bstack1l1111l_opy_ (u"ࠥࡿࢂࡀ࠺ࡼࡿࠥᮚ").format(file_path, test_name)
            data = {
                TestFramework.bstack11llllll111_opy_: bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠫࡺࡻࡩࡥࠩᮛ")) or bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡌࡨࠬᮜ")) or str(uuid4()),
                TestFramework.bstack11l1ll11111_opy_: bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"࠭ࡴࡦࡵࡷࡍࡩ࠭ᮝ")) or bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᮞ")),
                TestFramework.bstack1l111l11l1l_opy_: test_name,
                TestFramework.bstack11l1111ll11_opy_: file_path,
                TestFramework.bstack11l1111111l_opy_: bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᮟ")),
                TestFramework.bstack11l11111ll1_opy_: bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᮠ"), []),
                TestFramework.bstack111ll11111l_opy_: bstack111l11ll111_opy_,
                bstack1l1111l_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᮡ"): bstack111l11ll111_opy_,
                TestFramework.bstack111ll11l11l_opy_: bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᮢ"), {}),
                TestFramework.bstack11l11l11l1l_opy_: bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᮣ")) or test_name,
                bstack1l1111l_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᮤ"): bstack111l11ll1ll_opy_.get(bstack1l1111l_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩᮥ"), {}),
                TestFramework.bstack11ll11111l1_opy_: bstack111l11lllll_opy_,
                bstack1l1111l_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᮦ"): bstack111l11ll1l1_opy_,
            }
            data[bstack1l1111l_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬᮧ")] = {bstack1l1111l_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧᮨ"): bstack111l11lllll_opy_}
        return data
    def _111l11lll1l_opy_(self, instance: bstack1l11l1ll111_opy_, *args, **kwargs):
        bstack1l1111l_opy_ (u"ࠦࠧࠨࡌࡰࡣࡧࠤࡹ࡫ࡳࡵࠢࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠣ࡭ࡳࡺ࡯ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠦࠧࠨᮩ")
        bstack111l1l11111_opy_ = None
        if args and hasattr(args[0], bstack1l1111l_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸ᮪ࠬ")) and args[0].result:
            bstack1llll1l1ll1_opy_ = args[0]
            result = bstack1llll1l1ll1_opy_.result
            bstack111l1l11111_opy_ = {
                TestFramework.bstack11l1ll1111l_opy_: getattr(result, bstack1l1111l_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ᮫࠭"), bstack1l1111l_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᮬ")),
                TestFramework.bstack11l1l1ll11l_opy_: None,
                TestFramework.bstack111ll11l1ll_opy_: None,
            }
            if hasattr(result, bstack1l1111l_opy_ (u"ࠨࡧࡻࡧࡪࡶࡴࡪࡱࡱࠫᮭ")) and result.exception:
                bstack111l1l11111_opy_[TestFramework.bstack11l1l1ll11l_opy_] = [{bstack1l1111l_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᮮ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack1l1111l_opy_ (u"ࠪࡩࡽࡩࡥࡱࡶ࡬ࡳࡳ࠭ᮯ")) else None
                bstack111l1l11111_opy_[TestFramework.bstack111ll11l1ll_opy_] = exc_type or bstack1l1111l_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ᮰")
            bstack111l11ll1l1_opy_ = getattr(bstack1llll1l1ll1_opy_, bstack1l1111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ᮱"), None)
            if bstack111l11ll1l1_opy_:
                bstack111l1l11111_opy_[bstack1l1111l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ᮲")] = bstack111l11ll1l1_opy_
                logger.debug(bstack1l1111l_opy_ (u"ࠢࡖࡲࡧࡥࡹ࡫ࡤࠡ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠠࡢࡶࠣࡔࡔ࡙ࡔࠡࡶ࡬ࡱࡪࡀࠠࠣ᮳") + str(list(bstack111l11ll1l1_opy_.keys()) if bstack111l11ll1l1_opy_ else []) + bstack1l1111l_opy_ (u"ࠣࠤ᮴"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack111l1l11111_opy_ = {
                TestFramework.bstack11l1ll1111l_opy_: data.get(bstack1l1111l_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩ᮵"), TestFramework.bstack111lll1l1ll_opy_),
                TestFramework.bstack11l1l1ll11l_opy_: data.get(bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࠫ᮶")),
                TestFramework.bstack111ll11l1ll_opy_: data.get(bstack1l1111l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪ᮷")),
            }
            bstack111l11ll1l1_opy_ = data.get(bstack1l1111l_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫ᮸"))
            if bstack111l11ll1l1_opy_:
                bstack111l1l11111_opy_[bstack1l1111l_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬ᮹")] = bstack111l11ll1l1_opy_
                logger.debug(bstack1l1111l_opy_ (u"ࠢࡖࡲࡧࡥࡹ࡫ࡤࠡ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠠࡢࡶࠣࡔࡔ࡙ࡔࠡࡶ࡬ࡱࡪࡀࠠࠣᮺ") + str(list(bstack111l11ll1l1_opy_.keys()) if bstack111l11ll1l1_opy_ else []) + bstack1l1111l_opy_ (u"ࠣࠤᮻ"))
        if bstack111l1l11111_opy_:
            if bstack111l1l11111_opy_.get(TestFramework.bstack11l1ll1111l_opy_) != TestFramework.bstack111lll1l1ll_opy_:
                bstack111l1l11111_opy_[TestFramework.bstack11ll111l11l_opy_] = datetime.now(tz=timezone.utc)
            TestFramework.bstack111ll1lllll_opy_(instance, bstack111l1l11111_opy_)
            logger.debug(bstack1l1111l_opy_ (u"ࠤࡏࡳࡦࡪࡥࡥࠢࡷࡩࡸࡺࠠࡳࡧࡶࡹࡱࡺ࠺ࠡࠤᮼ") + str(bstack111l1l11111_opy_.get(TestFramework.bstack11l1ll1111l_opy_)) + bstack1l1111l_opy_ (u"ࠥࠦᮽ"))
    def _111l11lll11_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1111l_opy_ (u"ࠦࠧࠨࡔࡳࡣࡦ࡯ࠥ࡮࡯ࡰ࡭ࠣࡩࡻ࡫࡮ࡵࡵࠣࠬࡇࡋࡆࡐࡔࡈࡣࡆࡒࡌ࠭ࠢࡄࡊ࡙ࡋࡒࡠࡃࡏࡐ࠱ࠦࡥࡵࡥ࠱࠭࠳ࠨࠢࠣᮾ")
        key = test_framework_state.name
        bstack111lll1l111_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࡣࡸࡺࡡࡳࡶࡨࡨࠬᮿ"), {})
        if key not in bstack111lll1l111_opy_:
            bstack111lll1l111_opy_[key] = []
        bstack111llllllll_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, bstack1l1111l_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࡤ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪࠧᯀ"), {})
        if key not in bstack111llllllll_opy_:
            bstack111llllllll_opy_[key] = []
        bstack111llllll11_opy_ = {
            bstack1l1111l_opy_ (u"ࠧࡩࡱࡲ࡯ࡸࡥࡳࡵࡣࡵࡸࡪࡪࠧᯁ"): bstack111lll1l111_opy_,
            bstack1l1111l_opy_ (u"ࠨࡪࡲࡳࡰࡹ࡟ࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᯂ"): bstack111llllllll_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1l1111l_opy_ (u"ࠤ࡮ࡩࡾࠨᯃ"): key,
                TestFramework.bstack11l1111l111_opy_: str(uuid4()),
                TestFramework.bstack111lll111ll_opy_: TestFramework.bstack111ll1lll11_opy_,
                TestFramework.bstack111ll11lll1_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll111lll_opy_: [],
                TestFramework.bstack11l1111ll1l_opy_: kwargs.get(bstack1l1111l_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡰࡤࡱࡪ࠭ᯄ"), key),
            }
            bstack111lll1l111_opy_[key].append(hook)
            bstack111llllll11_opy_[bstack1l1111l_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡ࡯ࡥࡸࡺ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᯅ")] = key
        elif test_hook_state == TestHookState.POST:
            bstack111llll1lll_opy_ = bstack111lll1l111_opy_.get(key, [])
            hook = bstack111llll1lll_opy_.pop() if bstack111llll1lll_opy_ else None
            if hook:
                hook[TestFramework.bstack11l111111ll_opy_] = datetime.now(tz=timezone.utc)
                bstack111llllllll_opy_[key].append(hook)
                bstack111llllll11_opy_[bstack1l1111l_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠪᯆ")] = key
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
        logger.debug(bstack1l1111l_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡮࡯ࡰ࡭ࡢࡩࡻ࡫࡮ࡵ࠼ࠣࡿࡰ࡫ࡹࡾ࠰ࠥᯇ") + str(test_hook_state) + bstack1l1111l_opy_ (u"ࠢࠣᯈ"))
    def bstack11lll1l111l_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]
    ) -> List[bstack11lll1ll1l_opy_]:
        bstack1l1111l_opy_ (u"ࠣࠤࠥࡋࡪࡺࠠ࡭ࡱࡪࠤࡪࡴࡴࡳ࡫ࡨࡷࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡧࡪࡸࡨࡲࠥ࡮࡯ࡰ࡭ࠣࡷࡹࡧࡴࡦ࠰ࠥࠦࠧᯉ")
        if instance is None:
            return []
        return TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, [])
    def bstack11ll1llll1l_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack1l1111l_opy_ (u"ࠤࠥࠦࡈࡲࡥࡢࡴࠣࡰࡴ࡭ࠠࡦࡰࡷࡶ࡮࡫ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡪࡲࡳࡰࠦࡳࡵࡣࡷࡩ࠳ࠨࠢࠣᯊ")
        if instance is None:
            return
        TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, [])
    def get_current_test_instance(self) -> Optional[bstack1l11l1ll111_opy_]:
        bstack1l1111l_opy_ (u"ࠥࠦࠧࡍࡥࡵࠢࡷ࡬ࡪࠦࡣࡶࡴࡵࡩࡳࡺࠠࡵࡧࡶࡸࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷ࡬ࡷ࡫ࡡࡥ࠰ࠥࠦࠧᯋ")
        thread_id = threading.get_ident()
        target = self._111l1l1111l_opy_.get(thread_id)
        if target:
            return self._111l11l1l1l_opy_.get(target)
        return None
    def bstack111l1l111ll_opy_(
        self,
        instance: bstack1l11l1ll111_opy_,
        log_entry: bstack11lll1ll1l_opy_
    ):
        bstack1l1111l_opy_ (u"ࠦࠧࠨࡁࡥࡦࠣࡥࠥࡲ࡯ࡨࠢࡨࡲࡹࡸࡹࠡࡶࡲࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠦࠧࠨᯌ")
        if instance is None:
            return
        logs = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, [])
        logs.append(log_entry)
        TestFramework.bstack111l1llll1_opy_(instance, TestFramework.bstack111lll1lll1_opy_, logs)
    def __11l1111llll_opy_(self, instance: bstack1l11l1ll111_opy_) -> None:
        bstack1l1111l_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡏࡳࡦࡪࡳࠡࡥࡸࡷࡹࡵ࡭ࠡࡶࡤ࡫ࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡸࡥࡢࡶࡨࡷࠥࡧࠠࡥ࡫ࡦࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡭ࡧࡹࡩࡱࠦࡣࡶࡵࡷࡳࡲࠦ࡭ࡦࡶࡤࡨࡦࡺࡡࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡇࡺࡹࡴࡰ࡯ࡗࡥ࡬ࡓࡡ࡯ࡣࡪࡩࡷࠦࡡ࡯ࡦࠣࡹࡵࡪࡡࡵࡧࡶࠤࡹ࡮ࡥࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡷࡹࡧࡴࡦࠢࡸࡷ࡮ࡴࡧࠡࡵࡨࡸࡤࡹࡴࡢࡶࡨࡣࡪࡴࡴࡳ࡫ࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᯍ")
        bstack111llllll11_opy_ = {bstack1l1111l_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠣᯎ"): bstack1l1l1l1lll1_opy_.bstack111ll1ll11l_opy_()}
        TestFramework.bstack111ll1lllll_opy_(instance, bstack111llllll11_opy_)
    def __111l11l11l1_opy_(self, instance: bstack1l11l1ll111_opy_) -> None:
        bstack1l1111l_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡕࡸ࡯ࡤࡧࡶࡷࡪࡹࠠࡵࡧࡶࡸ࠲ࡲࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠢࡸࡴࡱࡵࡡࡥࡧࡧࠤࡻ࡯ࡡࠡࡈ࡬ࡰࡪ࡛ࡰ࡭ࡱࡤࡨࡪࡸ࠮ࡶࡲ࡯ࡳࡦࡪ࡟ࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠬ࠮࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡕࡦࡥࡳࡹࠠࡵࡪࡨࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡢࡰࡧࠤࡸ࡫࡮ࡥࡵࠣࡰࡴ࡭ࡳࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᯏ")
        from bstack_utils.helper import bstack11lll11111l_opy_
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack1l1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᯐ"), bstack1l1111l_opy_ (u"ࠩ࠳ࠫᯑ"))
            bstack11lll11l111_opy_ = os.path.join(
                bstack11lll11111l_opy_(),
                bstack1l1111l_opy_ (u"࡙ࠥࡵࡲ࡯ࡢࡦࡨࡨࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴ࠯ࡾࢁࠧᯒ").format(platform_index),
                bstack1l1111l_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᯓ")
            )
            if not os.path.isdir(bstack11lll11l111_opy_):
                logger.debug(bstack1l1111l_opy_ (u"ࠧࡔ࡯ࠡࡖࡨࡷࡹࡒࡥࡷࡧ࡯ࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡦ࡬ࡶࡪࡩࡴࡰࡴࡼࠤ࡫ࡵࡵ࡯ࡦ࠽ࠤࠧᯔ") + str(bstack11lll11l111_opy_) + bstack1l1111l_opy_ (u"ࠨࠢᯕ"))
                return
            bstack11lll11l1l1_opy_ = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_, bstack1l1111l_opy_ (u"ࠢࠣᯖ"))
            bstack111l11llll1_opy_ = []
            for file_name in os.listdir(bstack11lll11l111_opy_):
                file_path = os.path.join(bstack11lll11l111_opy_, file_name)
                if os.path.isfile(file_path):
                    try:
                        bstack11ll1ll1lll_opy_ = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(bstack11ll1ll1lll_opy_, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = bstack11lll1ll1l_opy_(
                            kind=bstack1l1111l_opy_ (u"ࠣࡖࡈࡗ࡙ࡥࡁࡕࡖࡄࡇࡍࡓࡅࡏࡖࠥᯗ"),
                            message=bstack1l1111l_opy_ (u"ࠤࠥᯘ"),
                            level=bstack1l1111l_opy_ (u"ࠥࡘࡪࡹࡴࡍࡧࡹࡩࡱࠨᯙ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            bstack11ll11l1111_opy_=file_size,
                            bstack11ll11ll1ll_opy_=bstack1l1111l_opy_ (u"ࠦࡒࡇࡎࡖࡃࡏࡣ࡚ࡖࡌࡐࡃࡇࠦᯚ"),
                            bstack111111_opy_=os.path.abspath(file_path),
                            bstack11l1l111ll_opy_=bstack11lll11l1l1_opy_
                        )
                        bstack111l11llll1_opy_.append(log_entry)
                        logger.debug(bstack1l1111l_opy_ (u"ࠧࡇࡤࡥࡧࡧࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴࡼ࠾ࠥࠨᯛ") + str(file_name) + bstack1l1111l_opy_ (u"ࠨࠢᯜ"))
                    except Exception as bstack11lll1l1111_opy_:
                        logger.error(bstack1l1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡰࡳࡱࡦࡩࡸࡹࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡼࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢᯝ") + str(bstack11lll1l1111_opy_) + bstack1l1111l_opy_ (u"ࠣࠤᯞ"))
            if bstack111l11llll1_opy_ and self.bstack11l1ll1lll_opy_:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack1l1111l_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡅࡏࡍࡤࡈࡉࡏࡡࡖࡉࡘ࡙ࡉࡐࡐࡢࡍࡉࠨᯟ"), bstack1l1111l_opy_ (u"ࠥࠦᯠ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack1l1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᯡ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack111l11llll1_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack1l1111l_opy_ (u"ࠧࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨࠨᯢ")
                        log_entry.test_framework_version = TestFramework.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11ll11l1lll_opy_, bstack1l1111l_opy_ (u"ࠨࠢᯣ"))
                        log_entry.uuid = bstack11lll11l1l1_opy_
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack11l11l11111_opy_ (u"ࠢࠣᯤ")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.bstack11ll11l1111_opy_
                        log_entry.file_path = entry.bstack111111_opy_
                    self.bstack11l1ll1lll_opy_.LogCreatedEvent(req)
                    logger.debug(bstack1l1111l_opy_ (u"ࠣࡕࡨࡲࡹࠦࠢᯥ") + str(len(bstack111l11llll1_opy_)) + bstack1l1111l_opy_ (u"ࠤࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠ࡭ࡱࡪࡷࠥࡼࡩࡢࠢࡪࡖࡕࡉ᯦ࠢ"))
                except Exception as bstack1lll1ll111_opy_:
                    logger.error(bstack1l1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡶࡩࡳࡪࡩ࡯ࡩࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠ࡭ࡱࡪࡷࠥࡼࡩࡢࠢࡪࡖࡕࡉ࠺ࠡࠤᯧ") + str(bstack1lll1ll111_opy_) + bstack1l1111l_opy_ (u"ࠦࠧᯨ"))
        except Exception as e:
            logger.error(bstack1l1111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡵࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹ࠳࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠽ࠤࠧᯩ") + str(e) + bstack1l1111l_opy_ (u"ࠨࠢᯪ"))