# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
bstack111ll_opy_ (u"ࠢࠣࠤࠍ࡚ࡦࡴࡩ࡭࡮ࡤࡔࡾࡺࡨࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥ࠳ࠠࡕࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡰࡴࡱ࡫࡭ࡦࡰࡷࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡶࡢࡰ࡬ࡰࡱࡧࠠࡑࡻࡷ࡬ࡴࡴࠠࡵࡧࡶࡸࡸ࠴ࠊࡕࡪ࡬ࡷࠥࡳ࡯ࡥࡷ࡯ࡩࠥࡶࡲࡰࡸ࡬ࡨࡪࡹࠠࡦࡸࡨࡲࡹࠦࡴࡳࡣࡦ࡯࡮ࡴࡧࠡࡣࡱࡨࠥࡹࡴࡢࡶࡨࠤࡲࡧ࡮ࡢࡩࡨࡱࡪࡴࡴࠡࡨࡲࡶࠥࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨࠦࡴࡦࡵࡷࡷ࠱ࠐࡳࡪ࡯࡬ࡰࡦࡸࠠࡵࡱ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡎࡦࡼࡡࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡࡣࡪࡩࡳࡺ࠮ࠋࠤࠥࠦ᭦")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.bstack1l1ll1l1lll_opy_ import bstack1l1ll1l1l1l_opy_, bstack1l1ll1111l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    bstack1l1l1ll11l1_opy_,
    TestHookState,
    bstack1ll1lllll1l_opy_,
    bstack11l1l1l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll1llll1_opy_ import bstack1l1lll1111l_opy_
from browserstack_sdk.sdk_cli.utils.bstack1l1l11ll1l1_opy_ import bstack1l11ll1111l_opy_
logger = logging.getLogger(__name__)
class bstack1l11l11ll11_opy_(TestFramework):
    bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࡖࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡷࡣࡱ࡭ࡱࡲࡡࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡶࡨࡷࡹࡹࠠࠩࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠫ࠱ࠎࠥࠦࠠࠡࡊࡤࡲࡩࡲࡥࡴࠢࡨࡺࡪࡴࡴࠡࡶࡵࡥࡨࡱࡩ࡯ࡩ࠯ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦ࡭ࡢࡰࡤ࡫ࡪࡳࡥ࡯ࡶ࠯ࠤࡦࡴࡤࠡࡪࡲࡳࡰࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫ࡴࠢࡩࡳࡷࠐࠠࠡࠢࠣࡸࡪࡹࡴࡴࠢࡷ࡬ࡦࡺࠠࡥࡱࡱࠫࡹࠦࡵࡴࡧࠣࡴࡾࡺࡥࡴࡶࠣࡳࡷࠦ࡯ࡵࡪࡨࡶࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹ࠮ࠋࠢࠣࠤ࡚ࠥࡨࡪࡵࠣ࡭ࡸࠦࡴࡩࡧࠣࡔࡾࡺࡨࡰࡰࠣࡩࡶࡻࡩࡷࡣ࡯ࡩࡳࡺࠠࡰࡨ࡚ࠣࡦࡴࡩ࡭࡮ࡤࡎࡦࡼࡡࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࠦࡴࡩࡧࠣࡎࡦࡼࡡࠡࡕࡇࡏ࠳ࠐࠠࠡࠢࠣࠦࠧࠨ᭧")
    FRAMEWORK_NAME = bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ᭨")
    bstack111llll111l_opy_ = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        bstack1l11llll11l_opy_: Dict[str, str] = None,
        bstack1l1l11l1111_opy_: List[str] = None,
        bstack1l1ll1llll1_opy_: bstack1l1lll1111l_opy_ = None,
        bstack111111ll1l_opy_=None
    ):
        bstack111ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࠤ࡛ࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࡳ࠻ࠢࡇ࡭ࡨࡺࠠ࡮ࡣࡳࡴ࡮ࡴࡧࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤࡳࡧ࡭ࡦࡵࠣࡸࡴࠦࡶࡦࡴࡶ࡭ࡴࡴࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳ࠻ࠢࡏ࡭ࡸࡺࠠࡰࡨࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࡮ࡢ࡯ࡨࡷࠥ࠮ࡤࡦࡨࡤࡹࡱࡺࡳࠡࡶࡲࠤࡠࠨࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠢ࡞ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡣࡶࡽࡳࡩ࡟ࡥ࡫ࡶࡴࡦࡺࡣࡩࡧࡵ࠾ࠥࡇࡳࡺࡰࡦࡈ࡮ࡹࡰࡢࡶࡦ࡬ࡪࡸࠠࡧࡱࡵࠤࡧࡧࡣ࡬ࡩࡵࡳࡺࡴࡤࠡࡱࡳࡩࡷࡧࡴࡪࡱࡱࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡧࡱ࡯࡟ࡴࡧࡵࡺ࡮ࡩࡥ࠻ࠢࡪࡖࡕࡉࠠࡄࡎࡌࠤࡸ࡫ࡲࡷ࡫ࡦࡩࠥࡩ࡬ࡪࡧࡱࡸࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᭩")
        if bstack1l1l11l1111_opy_ is None:
            bstack1l1l11l1111_opy_ = [self.FRAMEWORK_NAME]
        if bstack1l11llll11l_opy_ is None:
            bstack1l11llll11l_opy_ = {self.FRAMEWORK_NAME: self._111l11lll11_opy_()}
        super().__init__(bstack1l1l11l1111_opy_, bstack1l11llll11l_opy_, bstack1l1ll1llll1_opy_)
        self.bstack111111ll1l_opy_ = bstack111111ll1l_opy_
        self._111l111llll_opy_: Dict[str, bstack1l1l1ll11l1_opy_] = {}
        self._111l11l11l1_opy_: Dict[int, str] = {}
        logger.info(bstack111ll_opy_ (u"࡛ࠦࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧࡧࠤࡼ࡯ࡴࡩࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡸࡃࠢ᭪") + str(bstack1l1l11l1111_opy_) + bstack111ll_opy_ (u"ࠧࠨ᭫"))
    def _111l11lll11_opy_(self) -> str:
        bstack111ll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡔࡾࡺࡨࡰࡰࠣࡺࡪࡸࡳࡪࡱࡱࠤࡸࡺࡲࡪࡰࡪ࠲ࠧࠨ᭬ࠢ")
        return bstack111ll_opy_ (u"ࠢࡼࡿ࠱ࡿࢂ࠴ࡻࡾࠤ᭭").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def bstack11ll1l111ll_opy_(self) -> bool:
        bstack111ll_opy_ (u"ࠣࠤࠥࡖࡪࡺࡵࡳࡰࠣࡊࡦࡲࡳࡦࠢࡤࡷࠥࡺࡨࡪࡵࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡥࠥࡶࡹࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦ᭮")
        return False
    def bstack11ll1ll1l1l_opy_(self) -> bool:
        bstack111ll_opy_ (u"ࠤࠥࠦࡗ࡫ࡴࡶࡴࡱࠤࡋࡧ࡬ࡴࡧࠣࡥࡸࠦࡴࡩ࡫ࡶࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡦࠦࡲࡰࡤࡲࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦ᭯")
        return False
    def track_event(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡴࡤࡧࡰࠦࡡࠡࡶࡨࡷࡹࠦ࡬ࡪࡨࡨࡧࡾࡩ࡬ࡦࠢࡨࡺࡪࡴࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡤࡱࡱࡸࡪࡾࡴ࠻ࠢࡗࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡅࡲࡲࡹ࡫ࡸࡵࠢࡺ࡭ࡹ࡮ࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣࡲࡦࡳࡥ࠭ࠢࡹࡩࡷࡹࡩࡰࡰ࠯ࠤࡦࡴࡤࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣ࡭ࡳࡪࡥࡹࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠺ࠡࡖ࡫ࡩࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࠦࡳࡵࡣࡷࡩࠥ࠮ࡉࡏࡋࡗࡣ࡙ࡋࡓࡕ࠮ࠣࡘࡊ࡙ࡔ࠭ࠢࡨࡸࡨ࠴ࠩࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥ࠻ࠢࡓࡶࡪࠦ࡯ࡳࠢࡓࡳࡸࡺࠠࡩࡱࡲ࡯ࠥࡹࡴࡢࡶࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠭ࡥࡷ࡭ࡳ࠻ࠢࡄࡨࡩ࡯ࡴࡪࡱࡱࡥࡱࠦࡡࡳࡩࡸࡱࡪࡴࡴࡴࠢࠫࡸࡾࡶࡩࡤࡣ࡯ࡰࡾࠦࡔࡦࡵࡷࡈࡦࡺࡡࠡࡱࡵࠤࡩ࡯ࡣࡵࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠬ࠭࡯ࡼࡧࡲࡨࡵ࠽ࠤࡆࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࠡ࡭ࡨࡽࡼࡵࡲࡥࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᭰")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack111ll_opy_ (u"ࠦࡎ࡭࡮ࡰࡴࡨࡨࠥࡩࡡ࡭࡮ࡥࡥࡨࡱࠠࡧࡱࡵࠤࡸࡺࡡࡵࡧࡀࠦ᭱") + str(test_framework_state) + bstack111ll_opy_ (u"ࠧࠨ᭲"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack111ll_opy_ (u"ࠨࡴࡳࡣࡦ࡯ࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡻ࡮ࡦࡺࡳࡩࡨࡺࡥࡥࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᭳") + str(kwargs) + bstack111ll_opy_ (u"ࠢࠣ᭴"))
            return
        instance = self._111l11l1l1l_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack111ll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡶࡪࡹ࡯࡭ࡸࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡩࡻ࡫࡮ࡵ࠿ࡾࡸࡪࡹࡴࡠࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀ࠲ࠧ᭵") + str(test_hook_state) + bstack111ll_opy_ (u"ࠤࠥ᭶"))
            return
        try:
            self._111l11lll1l_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡫ࡥࡳࡪ࡬ࡪࡰࡪࠤࡪࡼࡥ࡯ࡶࠣࡿࡹ࡫ࡳࡵࡡࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁ࠳ࢁࡴࡦࡵࡷࡣ࡭ࡵ࡯࡬ࡡࡶࡸࡦࡺࡥࡾ࠼ࠣࠦ᭷") + str(e) + bstack111ll_opy_ (u"ࠦࠧ᭸"))
        self.bstack111ll1l1l11_opy_(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _111l11lll1l_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll_opy_ (u"ࠧࠨࠢࡉࡣࡱࡨࡱ࡫ࠠࡴࡲࡨࡧ࡮࡬ࡩࡤࠢࡨࡺࡪࡴࡴࠡࡶࡼࡴࡪࡹ࠮ࠣࠤࠥ᭹")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11l1l1ll11l_opy_):
                bstack1lll1lllll1_opy_ = self._111l11ll111_opy_(args, kwargs)
                if bstack1lll1lllll1_opy_:
                    instance.data.update(bstack1lll1lllll1_opy_)
                    logger.debug(bstack111ll_opy_ (u"ࠨࡌࡰࡣࡧࡩࡩࠦࡴࡦࡵࡷࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᭺") + str(instance.ref()) + bstack111ll_opy_ (u"ࠢࠣ᭻"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11ll1l1lll1_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack111ll_opy_ (u"ࠣࡕࡨࡸࠥࡺࡥࡴࡶ࠰ࡷࡹࡧࡲࡵࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᭼") + str(instance.ref()) + bstack111ll_opy_ (u"ࠤࠥ᭽"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11lll11llll_opy_):
                    TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack11lll11llll_opy_, datetime.now(tz=timezone.utc))
                    logger.debug(bstack111ll_opy_ (u"ࠥࡗࡪࡺࠠࡵࡧࡶࡸ࠲࡫࡮ࡥࠢࡩࡳࡷࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤ᭾") + str(instance.ref()) + bstack111ll_opy_ (u"ࠦࠧ᭿"))
                self._111l11l111l_opy_(instance, *args, **kwargs)
                self.__111llll11l1_opy_(instance)
                self.__111l11l1ll1_opy_(instance)
        elif test_framework_state in bstack1l11l11ll11_opy_.bstack111llll111l_opy_:
            self._111l11l1111_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack111ll_opy_ (u"ࠧࡺࡲࡢࡥ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤ࡭ࡧ࡮ࡥ࡮ࡨࡨࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࡻࡵࡧࡶࡸࡤ࡮࡯ࡰ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᮀ") + str(instance.ref()) + bstack111ll_opy_ (u"ࠨࠢᮁ"))
    def _111l11l1l1l_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[bstack1l1l1ll11l1_opy_]:
        bstack111ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡳࡰ࡮ࡹࡩࠥࡵࡲࠡࡥࡵࡩࡦࡺࡥࠡࡣࠣࡘࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡗࡩࡸࡺࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡷࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡹ࡫ࡳࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋࡵࡲࠡࡋࡑࡍ࡙ࡥࡔࡆࡕࡗࠤࡕࡘࡅ࠭ࠢࡦࡶࡪࡧࡴࡦࡵࠣࡥࠥࡴࡥࡸࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡳࡹ࡮ࡥࡳࠢࡨࡺࡪࡴࡴࡴ࠮ࠣࡰࡴࡵ࡫ࡴࠢࡸࡴࠥࡺࡨࡦࠢࡨࡼ࡮ࡹࡴࡪࡰࡪࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᮂ")
        target = self._111l11lllll_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._111l11ll11l_opy_(context, target)
            self._111l11l11l1_opy_[thread_id] = target
            return instance
        if target and target in self._111l111llll_opy_:
            return self._111l111llll_opy_[target]
        bstack111l1l1111l_opy_ = self._111l11l11l1_opy_.get(thread_id)
        if bstack111l1l1111l_opy_ and bstack111l1l1111l_opy_ in self._111l111llll_opy_:
            return self._111l111llll_opy_[bstack111l1l1111l_opy_]
        instance = TestFramework.bstack1l1l1llllll_opy_(target) if target else None
        if instance:
            return instance
        logger.debug(bstack111ll_opy_ (u"ࠣࡐࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢࡷࡥࡷ࡭ࡥࡵ࠿ࡾࡸࡦࡸࡧࡦࡶࢀࠤࡹ࡮ࡲࡦࡣࡧࡣ࡮ࡪ࠽ࠣᮃ") + str(thread_id) + bstack111ll_opy_ (u"ࠤࠥᮄ"))
        return None
    def _111l11ll11l_opy_(
        self,
        context: bstack1ll1lllll1l_opy_,
        target: str
    ) -> bstack1l1l1ll11l1_opy_:
        bstack111ll_opy_ (u"ࠥࠦࠧࡉࡲࡦࡣࡷࡩࠥࡧࠠ࡯ࡧࡺࠤࡹ࡫ࡳࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡲࠡࡶࡵࡥࡨࡱࡩ࡯ࡩ࠱ࠦࠧࠨᮅ")
        ctx = bstack1l1ll1l1l1l_opy_.create_context(target)
        instance = bstack1l1l1ll11l1_opy_(
            ctx,
            self.bstack1l1l11l1111_opy_,
            self.bstack1l11llll11l_opy_,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.bstack11l11111l11_opy_(instance, {
            TestFramework.bstack1l11111111l_opy_: str(uuid4()),
            TestFramework.bstack1l1111l111l_opy_: context.test_framework_name,
            TestFramework.bstack11ll1l11l1l_opy_: context.test_framework_version,
            TestFramework.bstack111lll1ll1l_opy_: [],
            TestFramework.bstack11l1ll11l11_opy_: TestFramework.bstack11l11111111_opy_,
        })
        if context.platform_index >= 0:
            TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack1l111111111_opy_, context.platform_index)
        self._111l111llll_opy_[target] = instance
        TestFramework.bstack111l11l1l1_opy_[ctx.id] = instance
        logger.debug(bstack111ll_opy_ (u"ࠦࡈࡸࡥࡢࡶࡨࡨࠥࡴࡥࡸࠢࡷࡩࡸࡺࠠࡪࡰࡶࡸࡦࡴࡣࡦࠢࡩࡳࡷࠦࡴࡢࡴࡪࡩࡹࡃࡻࡵࡣࡵ࡫ࡪࡺࡽࠡࡥࡷࡼ࠳࡯ࡤ࠾ࠤᮆ") + str(ctx.id) + bstack111ll_opy_ (u"ࠧࠨᮇ"))
        return instance
    def _111l11lllll_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack111ll_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥࡷ࡭ࡥࡵࠢࠫࡸࡪࡹࡴࠡࡰࡤࡱࡪ࠯ࠠࡧࡴࡲࡱࠥࡧࡲࡨࡷࡰࡩࡳࡺࡳ࠯ࠤࠥࠦᮈ")
        if args and hasattr(args[0], bstack111ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᮉ")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᮊ")) or
                    args[0].get(bstack111ll_opy_ (u"ࠩࡷࡩࡸࡺࡎࡢ࡯ࡨࠫᮋ")) or
                    args[0].get(bstack111ll_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨᮌ")) or
                    args[0].get(TestFramework.bstack1l1111lll11_opy_))
        return (kwargs.get(bstack111ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠧᮍ")) or
                kwargs.get(bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡑࡥࡲ࡫ࠧᮎ")) or
                kwargs.get(bstack111ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᮏ")))
    def _111l11ll111_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack111ll_opy_ (u"ࠢࠣࠤࡓࡥࡷࡹࡥࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡸ࡯࡮ࠢࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠥ࡯࡮ࡵࡱࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡪࡡࡵࡣࠣࡪࡴࡸ࡭ࡢࡶ࠱ࠦࠧࠨᮐ")
        if not args:
            return None
        data = None
        bstack111l11l1lll_opy_ = args[0]
        if hasattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᮑ")) and hasattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᮒ")):
            bstack111l11ll1ll_opy_ = getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᮓ"), [])
            bstack111l1l11111_opy_ = getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢ࡭ࡩ࠭ᮔ"), None)
            bstack111l11l1l11_opy_ = getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᮕ"), {})
            file_path = getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡵࡧࡴࡩࠩᮖ"), None)
            test_name = bstack111l11l1lll_opy_.name
            if not bstack111l1l11111_opy_ and file_path and test_name:
                bstack111l1l11111_opy_ = bstack111ll_opy_ (u"ࠢࡼࡿ࠽࠾ࢀࢃࠢᮗ").format(file_path, test_name)
            data = {
                TestFramework.bstack1l11111111l_opy_: bstack111l11l1lll_opy_.uuid,
                TestFramework.bstack11l1l1ll11l_opy_: bstack111l11l1lll_opy_.uuid,
                TestFramework.bstack1l1111lll11_opy_: test_name,
                TestFramework.bstack11l1111l1ll_opy_: file_path,
                TestFramework.bstack111ll11l1ll_opy_: getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠨࡥࡲࡨࡪ࠭ᮘ"), None),
                TestFramework.bstack111ll1llll1_opy_: getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᮙ"), []),
                TestFramework.bstack111ll111111_opy_: bstack111l11ll1ll_opy_,
                bstack111ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᮚ"): bstack111l11ll1ll_opy_,
                TestFramework.bstack111ll111ll1_opy_: getattr(bstack111l11l1lll_opy_, bstack111ll_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᮛ"), {}),
                TestFramework.bstack11l11l1111l_opy_: test_name,
                bstack111ll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧᮜ"): {},
                TestFramework.bstack11l1llll111_opy_: bstack111l1l11111_opy_,
                bstack111ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᮝ"): bstack111l11l1l11_opy_,
            }
            data[bstack111ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳࡒࡦࡴࡸࡲࡕࡧࡲࡢ࡯ࠪᮞ")] = {bstack111ll_opy_ (u"ࠨࡴࡨࡶࡺࡴ࡟࡯ࡣࡰࡩࠬᮟ"): bstack111l1l11111_opy_}
        elif isinstance(bstack111l11l1lll_opy_, dict):
            bstack111l11ll1ll_opy_ = bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠩࡶࡧࡴࡶࡥࡴࠩᮠ")) or bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠪࡷࡨࡵࡰࡦࠩᮡ"), [])
            bstack111l1l11111_opy_ = bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢ࡭ࡩ࠭ᮢ")) or bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠬࡸࡥࡳࡷࡱࡍࡩ࠭ᮣ"))
            bstack111l11l1l11_opy_ = bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᮤ"), {})
            file_path = bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡶࡡࡵࡪࠪᮥ")) or bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠨࡨ࡬ࡰࡪࡖࡡࡵࡪࠪᮦ"))
            test_name = bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᮧ")) or bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡏࡣࡰࡩࠬᮨ"))
            if not bstack111l1l11111_opy_ and file_path and test_name:
                bstack111l1l11111_opy_ = bstack111ll_opy_ (u"ࠦࢀࢃ࠺࠻ࡽࢀࠦᮩ").format(file_path, test_name)
            data = {
                TestFramework.bstack1l11111111l_opy_: bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠬࡻࡵࡪࡦ᮪ࠪ")) or bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"࠭ࡴࡦࡵࡷࡍࡩ᮫࠭")) or str(uuid4()),
                TestFramework.bstack11l1l1ll11l_opy_: bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠧࡵࡧࡶࡸࡎࡪࠧᮬ")) or bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᮭ")),
                TestFramework.bstack1l1111lll11_opy_: test_name,
                TestFramework.bstack11l1111l1ll_opy_: file_path,
                TestFramework.bstack111ll11l1ll_opy_: bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᮮ")),
                TestFramework.bstack111ll1llll1_opy_: bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᮯ"), []),
                TestFramework.bstack111ll111111_opy_: bstack111l11ll1ll_opy_,
                bstack111ll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫ᮰"): bstack111l11ll1ll_opy_,
                TestFramework.bstack111ll111ll1_opy_: bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠬࡳࡥࡵࡣࠪ᮱"), {}),
                TestFramework.bstack11l11l1111l_opy_: bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫ᮲")) or test_name,
                bstack111ll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ᮳"): bstack111l11l1lll_opy_.get(bstack111ll_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪ᮴"), {}),
                TestFramework.bstack11l1llll111_opy_: bstack111l1l11111_opy_,
                bstack111ll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨ᮵"): bstack111l11l1l11_opy_,
            }
            data[bstack111ll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡕࡩࡷࡻ࡮ࡑࡣࡵࡥࡲ࠭᮶")] = {bstack111ll_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡢࡲࡦࡳࡥࠨ᮷"): bstack111l1l11111_opy_}
        return data
    def _111l11l111l_opy_(self, instance: bstack1l1l1ll11l1_opy_, *args, **kwargs):
        bstack111ll_opy_ (u"ࠧࠨࠢࡍࡱࡤࡨࠥࡺࡥࡴࡶࠣࡶࡪࡹࡵ࡭ࡶࠣࡪࡷࡵ࡭ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࡮ࡴࡴࡰࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠧࠨࠢ᮸")
        bstack111l11llll1_opy_ = None
        if args and hasattr(args[0], bstack111ll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭᮹")) and args[0].result:
            bstack1lll1lllll1_opy_ = args[0]
            result = bstack1lll1lllll1_opy_.result
            bstack111l11llll1_opy_ = {
                TestFramework.bstack11l1ll11l11_opy_: getattr(result, bstack111ll_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᮺ"), bstack111ll_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩᮻ")),
                TestFramework.bstack11l1l1ll1ll_opy_: None,
                TestFramework.bstack111lll1l1l1_opy_: None,
            }
            if hasattr(result, bstack111ll_opy_ (u"ࠩࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠬᮼ")) and result.exception:
                bstack111l11llll1_opy_[TestFramework.bstack11l1l1ll1ll_opy_] = [{bstack111ll_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᮽ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack111ll_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠧᮾ")) else None
                bstack111l11llll1_opy_[TestFramework.bstack111lll1l1l1_opy_] = exc_type or bstack111ll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᮿ")
            bstack111l11l1l11_opy_ = getattr(bstack1lll1lllll1_opy_, bstack111ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᯀ"), None)
            if bstack111l11l1l11_opy_:
                bstack111l11llll1_opy_[bstack111ll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᯁ")] = bstack111l11l1l11_opy_
                logger.debug(bstack111ll_opy_ (u"ࠣࡗࡳࡨࡦࡺࡥࡥࠢ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠡࡣࡷࠤࡕࡕࡓࡕࠢࡷ࡭ࡲ࡫࠺ࠡࠤᯂ") + str(list(bstack111l11l1l11_opy_.keys()) if bstack111l11l1l11_opy_ else []) + bstack111ll_opy_ (u"ࠤࠥᯃ"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack111l11llll1_opy_ = {
                TestFramework.bstack11l1ll11l11_opy_: data.get(bstack111ll_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᯄ"), TestFramework.bstack11l11111111_opy_),
                TestFramework.bstack11l1l1ll1ll_opy_: data.get(bstack111ll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᯅ")),
                TestFramework.bstack111lll1l1l1_opy_: data.get(bstack111ll_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪࡥࡴࡺࡲࡨࠫᯆ")),
            }
            bstack111l11l1l11_opy_ = data.get(bstack111ll_opy_ (u"࠭ࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠬᯇ"))
            if bstack111l11l1l11_opy_:
                bstack111l11llll1_opy_[bstack111ll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭ᯈ")] = bstack111l11l1l11_opy_
                logger.debug(bstack111ll_opy_ (u"ࠣࡗࡳࡨࡦࡺࡥࡥࠢ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠡࡣࡷࠤࡕࡕࡓࡕࠢࡷ࡭ࡲ࡫࠺ࠡࠤᯉ") + str(list(bstack111l11l1l11_opy_.keys()) if bstack111l11l1l11_opy_ else []) + bstack111ll_opy_ (u"ࠤࠥᯊ"))
        if bstack111l11llll1_opy_:
            if bstack111l11llll1_opy_.get(TestFramework.bstack11l1ll11l11_opy_) != TestFramework.bstack11l11111111_opy_:
                bstack111l11llll1_opy_[TestFramework.bstack11lll11111l_opy_] = datetime.now(tz=timezone.utc)
            TestFramework.bstack11l11111l11_opy_(instance, bstack111l11llll1_opy_)
            logger.debug(bstack111ll_opy_ (u"ࠥࡐࡴࡧࡤࡦࡦࠣࡸࡪࡹࡴࠡࡴࡨࡷࡺࡲࡴ࠻ࠢࠥᯋ") + str(bstack111l11llll1_opy_.get(TestFramework.bstack11l1ll11l11_opy_)) + bstack111ll_opy_ (u"ࠦࠧᯌ"))
    def _111l11l1111_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack111ll_opy_ (u"ࠧࠨࠢࡕࡴࡤࡧࡰࠦࡨࡰࡱ࡮ࠤࡪࡼࡥ࡯ࡶࡶࠤ࠭ࡈࡅࡇࡑࡕࡉࡤࡇࡌࡍ࠮ࠣࡅࡋ࡚ࡅࡓࡡࡄࡐࡑ࠲ࠠࡦࡶࡦ࠲࠮࠴ࠢࠣࠤᯍ")
        key = test_framework_state.name
        bstack111ll1l1lll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࡤࡹࡴࡢࡴࡷࡩࡩ࠭ᯎ"), {})
        if key not in bstack111ll1l1lll_opy_:
            bstack111ll1l1lll_opy_[key] = []
        bstack111lll111l1_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, bstack111ll_opy_ (u"ࠧࡩࡱࡲ࡯ࡸࡥࡦࡪࡰ࡬ࡷ࡭࡫ࡤࠨᯏ"), {})
        if key not in bstack111lll111l1_opy_:
            bstack111lll111l1_opy_[key] = []
        bstack111llllllll_opy_ = {
            bstack111ll_opy_ (u"ࠨࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨᯐ"): bstack111ll1l1lll_opy_,
            bstack111ll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠪᯑ"): bstack111lll111l1_opy_,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack111ll_opy_ (u"ࠥ࡯ࡪࡿࠢᯒ"): key,
                TestFramework.bstack111llll1111_opy_: str(uuid4()),
                TestFramework.bstack111ll1l11l1_opy_: TestFramework.bstack111lll1lll1_opy_,
                TestFramework.bstack111lll1llll_opy_: datetime.now(tz=timezone.utc),
                TestFramework.bstack111ll11l111_opy_: [],
                TestFramework.bstack111ll11ll1l_opy_: kwargs.get(bstack111ll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᯓ"), key),
            }
            bstack111ll1l1lll_opy_[key].append(hook)
            bstack111llllllll_opy_[bstack111ll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡰࡦࡹࡴࡠࡵࡷࡥࡷࡺࡥࡥࠩᯔ")] = key
        elif test_hook_state == TestHookState.POST:
            bstack11l111l111l_opy_ = bstack111ll1l1lll_opy_.get(key, [])
            hook = bstack11l111l111l_opy_.pop() if bstack11l111l111l_opy_ else None
            if hook:
                hook[TestFramework.bstack111llll1l11_opy_] = datetime.now(tz=timezone.utc)
                bstack111lll111l1_opy_[key].append(hook)
                bstack111llllllll_opy_[bstack111ll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡱࡧࡳࡵࡡࡩ࡭ࡳ࡯ࡳࡩࡧࡧࠫᯕ")] = key
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
        logger.debug(bstack111ll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡨࡰࡱ࡮ࡣࡪࡼࡥ࡯ࡶ࠽ࠤࢀࡱࡥࡺࡿ࠱ࠦᯖ") + str(test_hook_state) + bstack111ll_opy_ (u"ࠣࠤᯗ"))
    def bstack11lll111l1l_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]
    ) -> List[bstack11l1l1l1ll_opy_]:
        bstack111ll_opy_ (u"ࠤࠥࠦࡌ࡫ࡴࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴ࡬ࡩࡸࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡨࡰࡱ࡮ࠤࡸࡺࡡࡵࡧ࠱ࠦࠧࠨᯘ")
        if instance is None:
            return []
        return TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, [])
    def bstack11lll11l1ll_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack111ll_opy_ (u"ࠥࠦࠧࡉ࡬ࡦࡣࡵࠤࡱࡵࡧࠡࡧࡱࡸࡷ࡯ࡥࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢ࡫ࡳࡴࡱࠠࡴࡶࡤࡸࡪ࠴ࠢࠣࠤᯙ")
        if instance is None:
            return
        TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, [])
    def get_current_test_instance(self) -> Optional[bstack1l1l1ll11l1_opy_]:
        bstack111ll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡸ࡭࡫ࠠࡤࡷࡵࡶࡪࡴࡴࠡࡶࡨࡷࡹࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸ࡭ࡸࡥࡢࡦ࠱ࠦࠧࠨᯚ")
        thread_id = threading.get_ident()
        target = self._111l11l11l1_opy_.get(thread_id)
        if target:
            return self._111l111llll_opy_.get(target)
        return None
    def bstack111l11l11ll_opy_(
        self,
        instance: bstack1l1l1ll11l1_opy_,
        log_entry: bstack11l1l1l1ll_opy_
    ):
        bstack111ll_opy_ (u"ࠧࠨࠢࡂࡦࡧࠤࡦࠦ࡬ࡰࡩࠣࡩࡳࡺࡲࡺࠢࡷࡳࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࠧࠨࠢᯛ")
        if instance is None:
            return
        logs = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, [])
        logs.append(log_entry)
        TestFramework.bstack11ll11l1_opy_(instance, TestFramework.bstack111lll1ll1l_opy_, logs)
    def __111llll11l1_opy_(self, instance: bstack1l1l1ll11l1_opy_) -> None:
        bstack111ll_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡐࡴࡧࡤࡴࠢࡦࡹࡸࡺ࡯࡮ࠢࡷࡥ࡬ࡹࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡉࡲࡦࡣࡷࡩࡸࠦࡡࠡࡦ࡬ࡧࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࡩ࡯ࡩࠣࡸࡪࡹࡴࠡ࡮ࡨࡺࡪࡲࠠࡤࡷࡶࡸࡴࡳࠠ࡮ࡧࡷࡥࡩࡧࡴࡢࠢࡵࡩࡹࡸࡩࡦࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡈࡻࡳࡵࡱࡰࡘࡦ࡭ࡍࡢࡰࡤ࡫ࡪࡸࠠࡢࡰࡧࠤࡺࡶࡤࡢࡶࡨࡷࠥࡺࡨࡦࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤࡸࡺࡡࡵࡧࠣࡹࡸ࡯࡮ࡨࠢࡶࡩࡹࡥࡳࡵࡣࡷࡩࡤ࡫࡮ࡵࡴ࡬ࡩࡸ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᯜ")
        bstack111llllllll_opy_ = {bstack111ll_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠤᯝ"): bstack1l11ll1111l_opy_.bstack11l11111ll1_opy_()}
        TestFramework.bstack11l11111l11_opy_(instance, bstack111llllllll_opy_)
    def __111l11l1ll1_opy_(self, instance: bstack1l1l1ll11l1_opy_) -> None:
        bstack111ll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡖࡲࡰࡥࡨࡷࡸ࡫ࡳࠡࡶࡨࡷࡹ࠳࡬ࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵࠣࡹࡵࡲ࡯ࡢࡦࡨࡨࠥࡼࡩࡢࠢࡉ࡭ࡱ࡫ࡕࡱ࡮ࡲࡥࡩ࡫ࡲ࠯ࡷࡳࡰࡴࡧࡤࡠࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸ࠭࠯࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡖࡧࡦࡴࡳࠡࡶ࡫ࡩ࡚ࠥࡥࡴࡶࡏࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࠥࡪࡩࡳࡧࡦࡸࡴࡸࡹࠡࡣࡱࡨࠥࡹࡥ࡯ࡦࡶࠤࡱࡵࡧࡴࠢࡹ࡭ࡦࠦࡧࡓࡒࡆ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᯞ")
        from bstack_utils.helper import bstack11ll11l1lll_opy_
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᯟ"), bstack111ll_opy_ (u"ࠪ࠴ࠬᯠ"))
            bstack11ll11lllll_opy_ = os.path.join(
                bstack11ll11l1lll_opy_(),
                bstack111ll_opy_ (u"࡚ࠦࡶ࡬ࡰࡣࡧࡩࡩࡇࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࡵ࠰ࡿࢂࠨᯡ").format(platform_index),
                bstack111ll_opy_ (u"࡚ࠧࡥࡴࡶࡏࡩࡻ࡫࡬ࠣᯢ")
            )
            if not os.path.isdir(bstack11ll11lllll_opy_):
                logger.debug(bstack111ll_opy_ (u"ࠨࡎࡰࠢࡗࡩࡸࡺࡌࡦࡸࡨࡰࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢࡧ࡭ࡷ࡫ࡣࡵࡱࡵࡽࠥ࡬࡯ࡶࡰࡧ࠾ࠥࠨᯣ") + str(bstack11ll11lllll_opy_) + bstack111ll_opy_ (u"ࠢࠣᯤ"))
                return
            bstack11ll1ll1lll_opy_ = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_, bstack111ll_opy_ (u"ࠣࠤᯥ"))
            bstack111l11ll1l1_opy_ = []
            for file_name in os.listdir(bstack11ll11lllll_opy_):
                file_path = os.path.join(bstack11ll11lllll_opy_, file_name)
                if os.path.isfile(file_path):
                    try:
                        bstack11ll1ll1111_opy_ = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(bstack11ll1ll1111_opy_, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = bstack11l1l1l1ll_opy_(
                            kind=bstack111ll_opy_ (u"ࠤࡗࡉࡘ࡚࡟ࡂࡖࡗࡅࡈࡎࡍࡆࡐࡗ᯦ࠦ"),
                            message=bstack111ll_opy_ (u"ࠥࠦᯧ"),
                            level=bstack111ll_opy_ (u"࡙ࠦ࡫ࡳࡵࡎࡨࡺࡪࡲࠢᯨ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            bstack11ll1lll111_opy_=file_size,
                            bstack11ll11ll111_opy_=bstack111ll_opy_ (u"ࠧࡓࡁࡏࡗࡄࡐࡤ࡛ࡐࡍࡑࡄࡈࠧᯩ"),
                            bstack111l1_opy_=os.path.abspath(file_path),
                            bstack1lllllllll_opy_=bstack11ll1ll1lll_opy_
                        )
                        bstack111l11ll1l1_opy_.append(log_entry)
                        logger.debug(bstack111ll_opy_ (u"ࠨࡁࡥࡦࡨࡨࠥࡧࡴࡵࡣࡦ࡬ࡲ࡫࡮ࡵࠢ࡯ࡳ࡬ࠦࡥ࡯ࡶࡵࡽ࠿ࠦࠢᯪ") + str(file_name) + bstack111ll_opy_ (u"ࠢࠣᯫ"))
                    except Exception as bstack11ll11llll1_opy_:
                        logger.error(bstack111ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡࡽࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࢂࡀࠠࠣᯬ") + str(bstack11ll11llll1_opy_) + bstack111ll_opy_ (u"ࠤࠥᯭ"))
            if bstack111l11ll1l1_opy_ and self.bstack111111ll1l_opy_:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack111ll_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡐࡎࡥࡂࡊࡐࡢࡗࡊ࡙ࡓࡊࡑࡑࡣࡎࡊࠢᯮ"), bstack111ll_opy_ (u"ࠦࠧᯯ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack111ll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᯰ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack111l11ll1l1_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack111ll_opy_ (u"ࠨࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠢᯱ")
                        log_entry.test_framework_version = TestFramework.bstack1l1llll1111_opy_(instance, TestFramework.bstack11ll1l11l1l_opy_, bstack111ll_opy_ (u"᯲ࠢࠣ"))
                        log_entry.uuid = bstack11ll1ll1lll_opy_
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack11l11l1l111_opy_ (u"ࠣࠤ᯳")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.bstack11ll1lll111_opy_
                        log_entry.file_path = entry.bstack111l1_opy_
                    self.bstack111111ll1l_opy_.LogCreatedEvent(req)
                    logger.debug(bstack111ll_opy_ (u"ࠤࡖࡩࡳࡺࠠࠣ᯴") + str(len(bstack111l11ll1l1_opy_)) + bstack111ll_opy_ (u"ࠥࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡮ࡲ࡫ࡸࠦࡶࡪࡣࠣ࡫ࡗࡖࡃࠣ᯵"))
                except Exception as bstack11ll1l1l1l_opy_:
                    logger.error(bstack111ll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡷࡪࡴࡤࡪࡰࡪࠤࡦࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࠡ࡮ࡲ࡫ࡸࠦࡶࡪࡣࠣ࡫ࡗࡖࡃ࠻ࠢࠥ᯶") + str(bstack11ll1l1l1l_opy_) + bstack111ll_opy_ (u"ࠧࠨ᯷"))
        except Exception as e:
            logger.error(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡶࡲࡰࡥࡨࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺ࠭࡭ࡧࡹࡩࡱࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࡶ࠾ࠥࠨ᯸") + str(e) + bstack111ll_opy_ (u"ࠢࠣ᯹"))