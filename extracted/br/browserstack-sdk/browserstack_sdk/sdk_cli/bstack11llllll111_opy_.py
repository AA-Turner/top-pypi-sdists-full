# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
bstack1l1llll_opy_ (u"ࠣࠤࠥࠎ࡛ࡧ࡮ࡪ࡮࡯ࡥࡕࡿࡴࡩࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰࠦ࠭ࠡࡖࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠢ࡬ࡱࡵࡲࡥ࡮ࡧࡱࡸࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡷࡣࡱ࡭ࡱࡲࡡࠡࡒࡼࡸ࡭ࡵ࡮ࠡࡶࡨࡷࡹࡹ࠮ࠋࡖ࡫࡭ࡸࠦ࡭ࡰࡦࡸࡰࡪࠦࡰࡳࡱࡹ࡭ࡩ࡫ࡳࠡࡧࡹࡩࡳࡺࠠࡵࡴࡤࡧࡰ࡯࡮ࡨࠢࡤࡲࡩࠦࡳࡵࡣࡷࡩࠥࡳࡡ࡯ࡣࡪࡩࡲ࡫࡮ࡵࠢࡩࡳࡷࠦࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠠࡵࡧࡶࡸࡸ࠲ࠊࡴ࡫ࡰ࡭ࡱࡧࡲࠡࡶࡲࠤ࡛ࡧ࡮ࡪ࡮࡯ࡥࡏࡧࡶࡢࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢࡤ࡫ࡪࡴࡴ࠯ࠌࠥࠦࠧḎ")
import logging
import os
import sys
import threading
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple, Optional
from uuid import uuid4
from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance, bstack1l11ll1l1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import (
    TestFramework,
    TestFrameworkState,
    TestFrameworkTest,
    TestHookState,
    TestFrameworkContext,
    LogEntry,
)
from browserstack_sdk.sdk_cli.async_dispatcher import AsyncDispatcher
from browserstack_sdk.sdk_cli.utils.custom_tag_manager import CustomTagManager
logger = logging.getLogger(__name__)
class bstack1l1111lllll_opy_(TestFramework):
    bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࡗࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡲࡶ࡬ࡦ࡯ࡨࡲࡹࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡸࡤࡲ࡮ࡲ࡬ࡢࠢࡓࡽࡹ࡮࡯࡯ࠢࡷࡩࡸࡺࡳࠡࠪࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠬ࠲ࠏࠦࠠࠡࠢࡋࡥࡳࡪ࡬ࡦࡵࠣࡩࡻ࡫࡮ࡵࠢࡷࡶࡦࡩ࡫ࡪࡰࡪ࠰ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠ࡮ࡣࡱࡥ࡬࡫࡭ࡦࡰࡷ࠰ࠥࡧ࡮ࡥࠢ࡫ࡳࡴࡱࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࡵࠣࡪࡴࡸࠊࠡࠢࠣࠤࡹ࡫ࡳࡵࡵࠣࡸ࡭ࡧࡴࠡࡦࡲࡲࠬࡺࠠࡶࡵࡨࠤࡵࡿࡴࡦࡵࡷࠤࡴࡸࠠࡰࡶ࡫ࡩࡷࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡳ࠯ࠌࠣࠤࠥࠦࡔࡩ࡫ࡶࠤ࡮ࡹࠠࡵࡪࡨࠤࡕࡿࡴࡩࡱࡱࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴࠡࡱࡩࠤ࡛ࡧ࡮ࡪ࡮࡯ࡥࡏࡧࡶࡢࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠤ࡮ࡴࠠࡵࡪࡨࠤࡏࡧࡶࡢࠢࡖࡈࡐ࠴ࠊࠡࠢࠣࠤࠧࠨࠢḏ")
    FRAMEWORK_NAME = bstack1l1llll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫḐ")
    hook_events = [
        TestFrameworkState.BEFORE_ALL,
        TestFrameworkState.AFTER_ALL,
        TestFrameworkState.BEFORE_EACH,
        TestFrameworkState.AFTER_EACH,
    ]
    def __init__(
        self,
        test_framework_versions: Dict[str, str] = None,
        test_frameworks: List[str] = None,
        async_dispatcher: AsyncDispatcher = None,
        cli_service=None
    ):
        bstack1l1llll_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡽࡩࠥ࡜ࡡ࡯࡫࡯ࡰࡦࡖࡹࡵࡪࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡄࡶ࡬ࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡴ࠼ࠣࡈ࡮ࡩࡴࠡ࡯ࡤࡴࡵ࡯࡮ࡨࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡴࡡ࡮ࡧࡶࠤࡹࡵࠠࡷࡧࡵࡷ࡮ࡵ࡮ࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡴ࠼ࠣࡐ࡮ࡹࡴࠡࡱࡩࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠠ࡯ࡣࡰࡩࡸࠦࠨࡥࡧࡩࡥࡺࡲࡴࡴࠢࡷࡳࠥࡡࠢࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠣ࡟ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡤࡷࡾࡴࡣࡠࡦ࡬ࡷࡵࡧࡴࡤࡪࡨࡶ࠿ࠦࡁࡴࡻࡱࡧࡉ࡯ࡳࡱࡣࡷࡧ࡭࡫ࡲࠡࡨࡲࡶࠥࡨࡡࡤ࡭ࡪࡶࡴࡻ࡮ࡥࠢࡲࡴࡪࡸࡡࡵ࡫ࡲࡲࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡨࡲࡩࡠࡵࡨࡶࡻ࡯ࡣࡦ࠼ࠣ࡫ࡗࡖࡃࠡࡅࡏࡍࠥࡹࡥࡳࡸ࡬ࡧࡪࠦࡣ࡭࡫ࡨࡲࡹࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥḑ")
        if test_frameworks is None:
            test_frameworks = [self.FRAMEWORK_NAME]
        if test_framework_versions is None:
            test_framework_versions = {self.FRAMEWORK_NAME: self._1111llllll1_opy_()}
        super().__init__(test_frameworks, test_framework_versions, async_dispatcher)
        self.cli_service = cli_service
        self._111l1111ll1_opy_: Dict[str, TestFrameworkTest] = {}
        self._1111lllllll_opy_: Dict[int, str] = {}
        logger.info(bstack1l1llll_opy_ (u"ࠧ࡜ࡡ࡯࡫࡯ࡰࡦࡖࡹࡵࡪࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠠࡪࡰ࡬ࡸ࡮ࡧ࡬ࡪࡼࡨࡨࠥࡽࡩࡵࡪࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡹ࠽ࠣḒ") + str(test_frameworks) + bstack1l1llll_opy_ (u"ࠨࠢḓ"))
    def _1111llllll1_opy_(self) -> str:
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡊࡩࡹࠦࡴࡩࡧࠣࡧࡺࡸࡲࡦࡰࡷࠤࡕࡿࡴࡩࡱࡱࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡹࡴࡳ࡫ࡱ࡫࠳ࠨࠢࠣḔ")
        return bstack1l1llll_opy_ (u"ࠣࡽࢀ࠲ࢀࢃ࠮ࡼࡿࠥḕ").format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro)
    def is_pytest_framework(self) -> bool:
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡗ࡫ࡴࡶࡴࡱࠤࡋࡧ࡬ࡴࡧࠣࡥࡸࠦࡴࡩ࡫ࡶࠤ࡮ࡹࠠ࡯ࡱࡷࠤࡦࠦࡰࡺࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧḖ")
        return False
    def is_robot_framework(self) -> bool:
        bstack1l1llll_opy_ (u"ࠥࠦࠧࡘࡥࡵࡷࡵࡲࠥࡌࡡ࡭ࡵࡨࠤࡦࡹࠠࡵࡪ࡬ࡷࠥ࡯ࡳࠡࡰࡲࡸࠥࡧࠠࡳࡱࡥࡳࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧḗ")
        return False
    def is_behave_framework(self) -> bool:
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡒࡦࡶࡸࡶࡳࠦࡆࡢ࡮ࡶࡩࠥࡧࡳࠡࡶ࡫࡭ࡸࠦࡩࡴࠢࡱࡳࡹࠦࡡࠡࡤࡨ࡬ࡦࡼࡥࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢḘ")
        return False
    def track_event(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡗࡶࡦࡩ࡫ࠡࡣࠣࡸࡪࡹࡴࠡ࡮࡬ࡪࡪࡩࡹࡤ࡮ࡨࠤࡪࡼࡥ࡯ࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡦࡳࡳࡺࡥࡹࡶ࠽ࠤ࡙࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡇࡴࡴࡴࡦࡺࡷࠤࡼ࡯ࡴࡩࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡴࡡ࡮ࡧ࠯ࠤࡻ࡫ࡲࡴ࡫ࡲࡲ࠱ࠦࡡ࡯ࡦࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥ࡯࡮ࡥࡧࡻࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠼ࠣࡘ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠡࡵࡷࡥࡹ࡫ࠠࠩࡋࡑࡍ࡙ࡥࡔࡆࡕࡗ࠰࡚ࠥࡅࡔࡖ࠯ࠤࡪࡺࡣ࠯ࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧ࠽ࠤࡕࡸࡥࠡࡱࡵࠤࡕࡵࡳࡵࠢ࡫ࡳࡴࡱࠠࡴࡶࡤࡸࡪࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࠯ࡧࡲࡨࡵ࠽ࠤࡆࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠤ࠭ࡺࡹࡱ࡫ࡦࡥࡱࡲࡹࠡࡖࡨࡷࡹࡊࡡࡵࡣࠣࡳࡷࠦࡤࡪࡥࡷ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣ࠮࠯ࡱࡷࡢࡴࡪࡷ࠿ࠦࡁࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࠣ࡯ࡪࡿࡷࡰࡴࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦḙ")
        super().track_event(context, test_framework_state, test_hook_state, *args, **kwargs)
        if test_framework_state == TestFrameworkState.NONE:
            logger.warning(bstack1l1llll_opy_ (u"ࠨࡉࡨࡰࡲࡶࡪࡪࠠࡤࡣ࡯ࡰࡧࡧࡣ࡬ࠢࡩࡳࡷࠦࡳࡵࡣࡷࡩࡂࠨḚ") + str(test_framework_state) + bstack1l1llll_opy_ (u"ࠢࠣḛ"))
            return
        if not isinstance(args, tuple) or len(args) == 0:
            logger.warning(bstack1l1llll_opy_ (u"ࠣࡶࡵࡥࡨࡱ࡟ࡦࡸࡨࡲࡹࡀࠠࡶࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥḜ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠤࠥḝ"))
            return
        instance = self._1111llll1ll_opy_(context, test_framework_state, test_hook_state, *args, **kwargs)
        if instance is None:
            logger.debug(bstack1l1llll_opy_ (u"ࠥࡸࡷࡧࡣ࡬ࡡࡨࡺࡪࡴࡴ࠻ࠢࡸࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡸࡥࡴࡱ࡯ࡺࡪࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡁࢀࡺࡥࡴࡶࡢࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂ࠴ࠢḞ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠦࠧḟ"))
            return
        try:
            self._1111llll1l1_opy_(instance, context, test_framework_state, test_hook_state, *args, **kwargs)
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡭ࡧ࡮ࡥ࡮࡬ࡲ࡬ࠦࡥࡷࡧࡱࡸࠥࢁࡴࡦࡵࡷࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃ࠮ࡼࡶࡨࡷࡹࡥࡨࡰࡱ࡮ࡣࡸࡺࡡࡵࡧࢀ࠾ࠥࠨḠ") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢḡ"))
        self.run_hooks(instance, (test_framework_state, test_hook_state), *args, **kwargs)
    def _1111llll1l1_opy_(
        self,
        instance: TestFrameworkTest,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡋࡥࡳࡪ࡬ࡦࠢࡶࡴࡪࡩࡩࡧ࡫ࡦࠤࡪࡼࡥ࡯ࡶࠣࡸࡾࡶࡥࡴ࠰ࠥࠦࠧḢ")
        if test_hook_state == TestHookState.PRE:
            if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ID):
                test_data = self._1111lll1ll1_opy_(args, kwargs)
                if test_data:
                    instance.data.update(test_data)
                    logger.debug(bstack1l1llll_opy_ (u"ࠣࡎࡲࡥࡩ࡫ࡤࠡࡶࡨࡷࡹࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦḣ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠤࠥḤ"))
        if test_framework_state == TestFrameworkState.TEST:
            if test_hook_state == TestHookState.PRE:
                if not TestFramework.has_state(instance, TestFramework.KEY_TEST_STARTED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_STARTED_AT, datetime.now(tz=timezone.utc))
                    logger.debug(bstack1l1llll_opy_ (u"ࠥࡗࡪࡺࠠࡵࡧࡶࡸ࠲ࡹࡴࡢࡴࡷࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦḥ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠦࠧḦ"))
            elif test_hook_state == TestHookState.POST:
                if not TestFramework.has_state(instance, TestFramework.KEY_TEST_ENDED_AT):
                    TestFramework.set_state(instance, TestFramework.KEY_TEST_ENDED_AT, datetime.now(tz=timezone.utc))
                    logger.debug(bstack1l1llll_opy_ (u"࡙ࠧࡥࡵࠢࡷࡩࡸࡺ࠭ࡦࡰࡧࠤ࡫ࡵࡲࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦḧ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠨࠢḨ"))
                self._111l11111l1_opy_(instance, *args, **kwargs)
                self.__load_custom_tags(instance)
                self.__1111lllll1l_opy_(instance)
        elif test_framework_state in bstack1l1111lllll_opy_.hook_events:
            self._111l1111l1l_opy_(instance, test_framework_state, test_hook_state, *args, **kwargs)
        logger.debug(bstack1l1llll_opy_ (u"ࠢࡵࡴࡤࡧࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡨࡢࡰࡧࡰࡪࡪࠠࡦࡸࡨࡲࡹࡃࡻࡵࡧࡶࡸࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽ࠯ࡽࡷࡩࡸࡺ࡟ࡩࡱࡲ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࠣḩ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠣࠤḪ"))
    def _1111llll1ll_opy_(
        self,
        context: TestFrameworkContext,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ) -> Optional[TestFrameworkTest]:
        bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡵࡲࡰࡻ࡫ࠠࡰࡴࠣࡧࡷ࡫ࡡࡵࡧࠣࡥ࡚ࠥࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡙࡫ࡳࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡩࡵࡳࡴࡨࡲࡹࠦࡴࡦࡵࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡰࡴࠣࡍࡓࡏࡔࡠࡖࡈࡗ࡙ࠦࡐࡓࡇ࠯ࠤࡨࡸࡥࡢࡶࡨࡷࠥࡧࠠ࡯ࡧࡺࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡲࡶࠥࡵࡴࡩࡧࡵࠤࡪࡼࡥ࡯ࡶࡶ࠰ࠥࡲ࡯ࡰ࡭ࡶࠤࡺࡶࠠࡵࡪࡨࠤࡪࡾࡩࡴࡶ࡬ࡲ࡬ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨḫ")
        target = self._111l111l111_opy_(args, kwargs)
        thread_id = threading.get_ident()
        if test_framework_state == TestFrameworkState.INIT_TEST and test_hook_state == TestHookState.PRE:
            instance = self._1111lll1lll_opy_(context, target)
            self._1111lllllll_opy_[thread_id] = target
            return instance
        if target and target in self._111l1111ll1_opy_:
            return self._111l1111ll1_opy_[target]
        bstack111l11111ll_opy_ = self._1111lllllll_opy_.get(thread_id)
        if bstack111l11111ll_opy_ and bstack111l11111ll_opy_ in self._111l1111ll1_opy_:
            return self._111l1111ll1_opy_[bstack111l11111ll_opy_]
        instance = TestFramework.get_tracked_instance(target) if target else None
        if instance:
            return instance
        logger.debug(bstack1l1llll_opy_ (u"ࠥࡒࡴࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤࡹࡧࡲࡨࡧࡷࡁࢀࡺࡡࡳࡩࡨࡸࢂࠦࡴࡩࡴࡨࡥࡩࡥࡩࡥ࠿ࠥḬ") + str(thread_id) + bstack1l1llll_opy_ (u"ࠦࠧḭ"))
        return None
    def _1111lll1lll_opy_(
        self,
        context: TestFrameworkContext,
        target: str
    ) -> TestFrameworkTest:
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡄࡴࡨࡥࡹ࡫ࠠࡢࠢࡱࡩࡼࠦࡴࡦࡵࡷࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡦࡰࡴࠣࡸࡷࡧࡣ࡬࡫ࡱ࡫࠳ࠨࠢࠣḮ")
        ctx = TrackedInstance.create_context(target)
        instance = TestFrameworkTest(
            ctx,
            self.test_frameworks,
            self.test_framework_versions,
            TestFrameworkState.INIT_TEST
        )
        TestFramework.set_state_entries(instance, {
            TestFramework.KEY_TEST_UUID: str(uuid4()),
            TestFramework.KEY_TEST_FRAMEWORK_NAME: context.test_framework_name,
            TestFramework.KEY_TEST_FRAMEWORK_VERSION: context.test_framework_version,
            TestFramework.KEY_TEST_LOGS: [],
            TestFramework.KEY_TEST_RESULT: TestFramework.DEFAULT_TEST_RESULT,
        })
        if context.platform_index >= 0:
            TestFramework.set_state(instance, TestFramework.KEY_PLATFORM_INDEX, context.platform_index)
        self._111l1111ll1_opy_[target] = instance
        TestFramework.instances[ctx.id] = instance
        logger.debug(bstack1l1llll_opy_ (u"ࠨࡃࡳࡧࡤࡸࡪࡪࠠ࡯ࡧࡺࠤࡹ࡫ࡳࡵࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠤ࡫ࡵࡲࠡࡶࡤࡶ࡬࡫ࡴ࠾ࡽࡷࡥࡷ࡭ࡥࡵࡿࠣࡧࡹࡾ࠮ࡪࡦࡀࠦḯ") + str(ctx.id) + bstack1l1llll_opy_ (u"ࠢࠣḰ"))
        return instance
    def _111l111l111_opy_(self, args: tuple, kwargs: dict) -> Optional[str]:
        bstack1l1llll_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡲࡨࡧࡷࠤ࠭ࡺࡥࡴࡶࠣࡲࡦࡳࡥࠪࠢࡩࡶࡴࡳࠠࡢࡴࡪࡹࡲ࡫࡮ࡵࡵ࠱ࠦࠧࠨḱ")
        if args and hasattr(args[0], bstack1l1llll_opy_ (u"ࠩࡱࡥࡲ࡫ࠧḲ")):
            return args[0].name
        if args and isinstance(args[0], dict):
            return (args[0].get(bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨḳ")) or
                    args[0].get(bstack1l1llll_opy_ (u"ࠫࡹ࡫ࡳࡵࡐࡤࡱࡪ࠭Ḵ")) or
                    args[0].get(bstack1l1llll_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪḵ")) or
                    args[0].get(TestFramework.KEY_TEST_NAME))
        return (kwargs.get(bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠩḶ")) or
                kwargs.get(bstack1l1llll_opy_ (u"ࠧࡵࡧࡶࡸࡓࡧ࡭ࡦࠩḷ")) or
                kwargs.get(bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭Ḹ")))
    def _1111lll1ll1_opy_(self, args: tuple, kwargs: dict) -> Optional[Dict[str, Any]]:
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡕࡧࡲࡴࡧࠣࡸࡪࡹࡴࠡࡦࡤࡸࡦࠦࡦࡳࡱࡰࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠠࡪࡰࡷࡳࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࠠࡥࡣࡷࡥࠥ࡬࡯ࡳ࡯ࡤࡸ࠳ࠨࠢࠣḹ")
        if not args:
            return None
        data = None
        bstack111l1111lll_opy_ = args[0]
        if hasattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠪࡲࡦࡳࡥࠨḺ")) and hasattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠫࡺࡻࡩࡥࠩḻ")):
            bstack1111llll111_opy_ = getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫḼ"), [])
            bstack1111llll11l_opy_ = getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤ࡯ࡤࠨḽ"), None)
            bstack111l1111111_opy_ = getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠧࡪࡰࡷࡩ࡬ࡸࡡࡵ࡫ࡲࡲࡸ࠭Ḿ"), {})
            file_path = getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠨࡨ࡬ࡰࡪࡥࡰࡢࡶ࡫ࠫḿ"), None)
            test_name = bstack111l1111lll_opy_.name
            if not bstack1111llll11l_opy_ and file_path and test_name:
                bstack1111llll11l_opy_ = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠿ࡀࡻࡾࠤṀ").format(file_path, test_name)
            data = {
                TestFramework.KEY_TEST_UUID: bstack111l1111lll_opy_.uuid,
                TestFramework.KEY_TEST_ID: bstack111l1111lll_opy_.uuid,
                TestFramework.KEY_TEST_NAME: test_name,
                TestFramework.KEY_TEST_FILE_PATH: file_path,
                TestFramework.bstack111l1l1l1ll_opy_: getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠪࡧࡴࡪࡥࠨṁ"), None),
                TestFramework.KEY_TEST_TAGS: getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"ࠫࡹࡧࡧࡴࠩṂ"), []),
                TestFramework.KEY_TEST_SCOPES: bstack1111llll111_opy_,
                bstack1l1llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࡷࠬṃ"): bstack1111llll111_opy_,
                TestFramework.KEY_TEST_META: getattr(bstack111l1111lll_opy_, bstack1l1llll_opy_ (u"࠭࡭ࡦࡶࡤࠫṄ"), {}),
                TestFramework.KEY_AUTOMATE_SESSION_NAME: test_name,
                bstack1l1llll_opy_ (u"ࠧࡤࡷࡶࡸࡴࡳ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩṅ"): {},
                TestFramework.KEY_TEST_RERUN_NAME: bstack1111llll11l_opy_,
                bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧṆ"): bstack111l1111111_opy_,
            }
            data[bstack1l1llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡔࡨࡶࡺࡴࡐࡢࡴࡤࡱࠬṇ")] = {bstack1l1llll_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡡࡱࡥࡲ࡫ࠧṈ"): bstack1111llll11l_opy_}
        elif isinstance(bstack111l1111lll_opy_, dict):
            bstack1111llll111_opy_ = bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠫࡸࡩ࡯ࡱࡧࡶࠫṉ")) or bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫṊ"), [])
            bstack1111llll11l_opy_ = bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤ࡯ࡤࠨṋ")) or bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠧࡳࡧࡵࡹࡳࡏࡤࠨṌ"))
            bstack111l1111111_opy_ = bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧṍ"), {})
            file_path = bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟ࡱࡣࡷ࡬ࠬṎ")) or bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠪࡪ࡮ࡲࡥࡑࡣࡷ࡬ࠬṏ"))
            test_name = bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩṐ")) or bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡑࡥࡲ࡫ࠧṑ"))
            if not bstack1111llll11l_opy_ and file_path and test_name:
                bstack1111llll11l_opy_ = bstack1l1llll_opy_ (u"ࠨࡻࡾ࠼࠽ࡿࢂࠨṒ").format(file_path, test_name)
            data = {
                TestFramework.KEY_TEST_UUID: bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠧࡶࡷ࡬ࡨࠬṓ")) or bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡏࡤࠨṔ")) or str(uuid4()),
                TestFramework.KEY_TEST_ID: bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠩࡷࡩࡸࡺࡉࡥࠩṕ")) or bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠪࡹࡺ࡯ࡤࠨṖ")),
                TestFramework.KEY_TEST_NAME: test_name,
                TestFramework.KEY_TEST_FILE_PATH: file_path,
                TestFramework.bstack111l1l1l1ll_opy_: bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠫࡨࡵࡤࡦࠩṗ")),
                TestFramework.KEY_TEST_TAGS: bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡺࡡࡨࡵࠪṘ"), []),
                TestFramework.KEY_TEST_SCOPES: bstack1111llll111_opy_,
                bstack1l1llll_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ṙ"): bstack1111llll111_opy_,
                TestFramework.KEY_TEST_META: bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠧ࡮ࡧࡷࡥࠬṚ"), {}),
                TestFramework.KEY_AUTOMATE_SESSION_NAME: bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ṛ")) or test_name,
                bstack1l1llll_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠫṜ"): bstack111l1111lll_opy_.get(bstack1l1llll_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡢࡱࡪࡺࡡࡥࡣࡷࡥࠬṝ"), {}),
                TestFramework.KEY_TEST_RERUN_NAME: bstack1111llll11l_opy_,
                bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠪṞ"): bstack111l1111111_opy_,
            }
            data[bstack1l1llll_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡗ࡫ࡲࡶࡰࡓࡥࡷࡧ࡭ࠨṟ")] = {bstack1l1llll_opy_ (u"࠭ࡲࡦࡴࡸࡲࡤࡴࡡ࡮ࡧࠪṠ"): bstack1111llll11l_opy_}
        return data
    def _111l11111l1_opy_(self, instance: TestFrameworkTest, *args, **kwargs):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡏࡳࡦࡪࠠࡵࡧࡶࡸࠥࡸࡥࡴࡷ࡯ࡸࠥ࡬ࡲࡰ࡯ࠣࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠦࡩ࡯ࡶࡲࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠢࠣࠤṡ")
        bstack111l111111l_opy_ = None
        if args and hasattr(args[0], bstack1l1llll_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨṢ")) and args[0].result:
            test_data = args[0]
            result = test_data.result
            bstack111l111111l_opy_ = {
                TestFramework.KEY_TEST_RESULT: getattr(result, bstack1l1llll_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩṣ"), bstack1l1llll_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫṤ")),
                TestFramework.KEY_TEST_FAILURE: None,
                TestFramework.KEY_TEST_FAILURE_TYPE: None,
            }
            if hasattr(result, bstack1l1llll_opy_ (u"ࠫࡪࡾࡣࡦࡲࡷ࡭ࡴࡴࠧṥ")) and result.exception:
                bstack111l111111l_opy_[TestFramework.KEY_TEST_FAILURE] = [{bstack1l1llll_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨṦ"): [str(result.exception)]}]
                exc_type = type(result.exception).__name__ if hasattr(result, bstack1l1llll_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࠩṧ")) else None
                bstack111l111111l_opy_[TestFramework.KEY_TEST_FAILURE_TYPE] = exc_type or bstack1l1llll_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣṨ")
            bstack111l1111111_opy_ = getattr(test_data, bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧṩ"), None)
            if bstack111l1111111_opy_:
                bstack111l111111l_opy_[bstack1l1llll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨṪ")] = bstack111l1111111_opy_
                logger.debug(bstack1l1llll_opy_ (u"࡙ࠥࡵࡪࡡࡵࡧࡧࠤ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠣࡥࡹࠦࡐࡐࡕࡗࠤࡹ࡯࡭ࡦ࠼ࠣࠦṫ") + str(list(bstack111l1111111_opy_.keys()) if bstack111l1111111_opy_ else []) + bstack1l1llll_opy_ (u"ࠦࠧṬ"))
        elif args and isinstance(args[0], dict):
            data = args[0]
            bstack111l111111l_opy_ = {
                TestFramework.KEY_TEST_RESULT: data.get(bstack1l1llll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬṭ"), TestFramework.DEFAULT_TEST_RESULT),
                TestFramework.KEY_TEST_FAILURE: data.get(bstack1l1llll_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧṮ")),
                TestFramework.KEY_TEST_FAILURE_TYPE: data.get(bstack1l1llll_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ṯ")),
            }
            bstack111l1111111_opy_ = data.get(bstack1l1llll_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧṰ"))
            if bstack111l1111111_opy_:
                bstack111l111111l_opy_[bstack1l1llll_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨṱ")] = bstack111l1111111_opy_
                logger.debug(bstack1l1llll_opy_ (u"࡙ࠥࡵࡪࡡࡵࡧࡧࠤ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠣࡥࡹࠦࡐࡐࡕࡗࠤࡹ࡯࡭ࡦ࠼ࠣࠦṲ") + str(list(bstack111l1111111_opy_.keys()) if bstack111l1111111_opy_ else []) + bstack1l1llll_opy_ (u"ࠦࠧṳ"))
        if bstack111l111111l_opy_:
            if bstack111l111111l_opy_.get(TestFramework.KEY_TEST_RESULT) != TestFramework.DEFAULT_TEST_RESULT:
                bstack111l111111l_opy_[TestFramework.KEY_TEST_RESULT_AT] = datetime.now(tz=timezone.utc)
            TestFramework.set_state_entries(instance, bstack111l111111l_opy_)
            logger.debug(bstack1l1llll_opy_ (u"ࠧࡒ࡯ࡢࡦࡨࡨࠥࡺࡥࡴࡶࠣࡶࡪࡹࡵ࡭ࡶ࠽ࠤࠧṴ") + str(bstack111l111111l_opy_.get(TestFramework.KEY_TEST_RESULT)) + bstack1l1llll_opy_ (u"ࠨࠢṵ"))
    def _111l1111l1l_opy_(
        self,
        instance: TestFrameworkTest,
        test_framework_state: TestFrameworkState,
        test_hook_state: TestHookState,
        *args,
        **kwargs,
    ):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡗࡶࡦࡩ࡫ࠡࡪࡲࡳࡰࠦࡥࡷࡧࡱࡸࡸࠦࠨࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏ࠰ࠥࡇࡆࡕࡇࡕࡣࡆࡒࡌ࠭ࠢࡨࡸࡨ࠴ࠩ࠯ࠤࠥࠦṶ")
        key = test_framework_state.name
        hooks_started = TestFramework.get_state(instance, bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡹ࡟ࡴࡶࡤࡶࡹ࡫ࡤࠨṷ"), {})
        if key not in hooks_started:
            hooks_started[key] = []
        hooks_finished = TestFramework.get_state(instance, bstack1l1llll_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࡠࡨ࡬ࡲ࡮ࡹࡨࡦࡦࠪṸ"), {})
        if key not in hooks_finished:
            hooks_finished[key] = []
        updates = {
            bstack1l1llll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࡡࡶࡸࡦࡸࡴࡦࡦࠪṹ"): hooks_started,
            bstack1l1llll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࡢࡪ࡮ࡴࡩࡴࡪࡨࡨࠬṺ"): hooks_finished,
        }
        if test_hook_state == TestHookState.PRE:
            hook = {
                bstack1l1llll_opy_ (u"ࠧࡱࡥࡺࠤṻ"): key,
                TestFramework.KEY_HOOK_ID: str(uuid4()),
                TestFramework.KEY_HOOK_RESULT: TestFramework.DEFAULT_HOOK_RESULT,
                TestFramework.KEY_EVENT_STARTED_AT: datetime.now(tz=timezone.utc),
                TestFramework.KEY_HOOK_LOGS: [],
                TestFramework.KEY_HOOK_NAME: kwargs.get(bstack1l1llll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡳࡧ࡭ࡦࠩṼ"), key),
            }
            hooks_started[key].append(hook)
            updates[bstack1l1llll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡲࡡࡴࡶࡢࡷࡹࡧࡲࡵࡧࡧࠫṽ")] = key
        elif test_hook_state == TestHookState.POST:
            hooks_list = hooks_started.get(key, [])
            hook = hooks_list.pop() if hooks_list else None
            if hook:
                hook[TestFramework.KEY_EVENT_ENDED_AT] = datetime.now(tz=timezone.utc)
                hooks_finished[key].append(hook)
                updates[bstack1l1llll_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡬ࡢࡵࡷࡣ࡫࡯࡮ࡪࡵ࡫ࡩࡩ࠭Ṿ")] = key
        TestFramework.set_state_entries(instance, updates)
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡷࡶࡦࡩ࡫ࡠࡪࡲࡳࡰࡥࡥࡷࡧࡱࡸ࠿ࠦࡻ࡬ࡧࡼࢁ࠳ࠨṿ") + str(test_hook_state) + bstack1l1llll_opy_ (u"ࠥࠦẀ"))
    def get_log_entries(
        self,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState]
    ) -> List[LogEntry]:
        bstack1l1llll_opy_ (u"ࠦࠧࠨࡇࡦࡶࠣࡰࡴ࡭ࠠࡦࡰࡷࡶ࡮࡫ࡳࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡪࡲࡳࡰࠦࡳࡵࡣࡷࡩ࠳ࠨࠢࠣẁ")
        if instance is None:
            return []
        return TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, [])
    def clear_logs(
        self,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState]
    ):
        bstack1l1llll_opy_ (u"ࠧࠨࠢࡄ࡮ࡨࡥࡷࠦ࡬ࡰࡩࠣࡩࡳࡺࡲࡪࡧࡶࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤ࡭ࡵ࡯࡬ࠢࡶࡸࡦࡺࡥ࠯ࠤࠥࠦẂ")
        if instance is None:
            return
        TestFramework.set_state(instance, TestFramework.KEY_TEST_LOGS, [])
    def get_current_test_instance(self) -> Optional[TestFrameworkTest]:
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡉࡨࡸࠥࡺࡨࡦࠢࡦࡹࡷࡸࡥ࡯ࡶࠣࡸࡪࡹࡴࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡨࡳࡧࡤࡨ࠳ࠨࠢࠣẃ")
        thread_id = threading.get_ident()
        target = self._1111lllllll_opy_.get(thread_id)
        if target:
            return self._111l1111ll1_opy_.get(target)
        return None
    def bstack111l1111l11_opy_(
        self,
        instance: TestFrameworkTest,
        log_entry: LogEntry
    ):
        bstack1l1llll_opy_ (u"ࠢࠣࠤࡄࡨࡩࠦࡡࠡ࡮ࡲ࡫ࠥ࡫࡮ࡵࡴࡼࠤࡹࡵࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࠢࠣࠤẄ")
        if instance is None:
            return
        logs = TestFramework.get_state(instance, TestFramework.KEY_TEST_LOGS, [])
        logs.append(log_entry)
        TestFramework.set_state(instance, TestFramework.KEY_TEST_LOGS, logs)
    def __load_custom_tags(self, instance: TestFrameworkTest) -> None:
        bstack1l1llll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡒ࡯ࡢࡦࡶࠤࡨࡻࡳࡵࡱࡰࠤࡹࡧࡧࡴࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡄࡴࡨࡥࡹ࡫ࡳࠡࡣࠣࡨ࡮ࡩࡴࠡࡥࡲࡲࡹࡧࡩ࡯࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡰࡪࡼࡥ࡭ࠢࡦࡹࡸࡺ࡯࡮ࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡷ࡫ࡴࡳ࡫ࡨࡺࡪࡪࠠࡧࡴࡲࡱࠏࠦࠠࠡࠢࠣࠤࠥࠦࡃࡶࡵࡷࡳࡲ࡚ࡡࡨࡏࡤࡲࡦ࡭ࡥࡳࠢࡤࡲࡩࠦࡵࡱࡦࡤࡸࡪࡹࠠࡵࡪࡨࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࠦࡳࡵࡣࡷࡩࠥࡻࡳࡪࡰࡪࠤࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࡟ࡦࡰࡷࡶ࡮࡫ࡳ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨẅ")
        updates = {bstack1l1llll_opy_ (u"ࠤࡦࡹࡸࡺ࡯࡮ࡡࡰࡩࡹࡧࡤࡢࡶࡤࠦẆ"): CustomTagManager.get_test_level_custom_metadata()}
        TestFramework.set_state_entries(instance, updates)
    def __1111lllll1l_opy_(self, instance: TestFrameworkTest) -> None:
        bstack1l1llll_opy_ (u"ࠥࠦࠧࠐࠠࠡࠢࠣࠤࠥࠦࠠࡑࡴࡲࡧࡪࡹࡳࡦࡵࠣࡸࡪࡹࡴ࠮࡮ࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷࠥࡻࡰ࡭ࡱࡤࡨࡪࡪࠠࡷ࡫ࡤࠤࡋ࡯࡬ࡦࡗࡳࡰࡴࡧࡤࡦࡴ࠱ࡹࡵࡲ࡯ࡢࡦࡢࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠨࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡘࡩࡡ࡯ࡵࠣࡸ࡭࡫ࠠࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠣࡥࡹࡺࡡࡤࡪࡰࡩࡳࡺࠠࡥ࡫ࡵࡩࡨࡺ࡯ࡳࡻࠣࡥࡳࡪࠠࡴࡧࡱࡨࡸࠦ࡬ࡰࡩࡶࠤࡻ࡯ࡡࠡࡩࡕࡔࡈ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦẇ")
        from bstack_utils.helper import get_writable_dir
        from browserstack_sdk import sdk_pb2 as structs
        try:
            platform_index = os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫẈ"), bstack1l1llll_opy_ (u"ࠬ࠶ࠧẉ"))
            attachment_dir = os.path.join(
                get_writable_dir(),
                bstack1l1llll_opy_ (u"ࠨࡕࡱ࡮ࡲࡥࡩ࡫ࡤࡂࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࡷ࠲ࢁࡽࠣẊ").format(platform_index),
                bstack1l1llll_opy_ (u"ࠢࡕࡧࡶࡸࡑ࡫ࡶࡦ࡮ࠥẋ")
            )
            if not os.path.isdir(attachment_dir):
                logger.debug(bstack1l1llll_opy_ (u"ࠣࡐࡲࠤ࡙࡫ࡳࡵࡎࡨࡺࡪࡲࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡩ࡯ࡲࡦࡥࡷࡳࡷࡿࠠࡧࡱࡸࡲࡩࡀࠠࠣẌ") + str(attachment_dir) + bstack1l1llll_opy_ (u"ࠤࠥẍ"))
                return
            uuid_str = TestFramework.get_state(instance, TestFramework.KEY_TEST_UUID, bstack1l1llll_opy_ (u"ࠥࠦẎ"))
            bstack1111lllll11_opy_ = []
            for file_name in os.listdir(attachment_dir):
                file_path = os.path.join(attachment_dir, file_name)
                if os.path.isfile(file_path):
                    try:
                        mod_time = os.path.getmtime(file_path)
                        timestamp = datetime.fromtimestamp(mod_time, tz=timezone.utc).isoformat()
                        file_size = os.path.getsize(file_path)
                        log_entry = LogEntry(
                            kind=bstack1l1llll_opy_ (u"࡙ࠦࡋࡓࡕࡡࡄࡘ࡙ࡇࡃࡉࡏࡈࡒ࡙ࠨẏ"),
                            message=bstack1l1llll_opy_ (u"ࠧࠨẐ"),
                            level=bstack1l1llll_opy_ (u"ࠨࡔࡦࡵࡷࡐࡪࡼࡥ࡭ࠤẑ"),
                            timestamp=timestamp,
                            fileName=file_name,
                            fileSize=file_size,
                            attachmentType=bstack1l1llll_opy_ (u"ࠢࡎࡃࡑ࡙ࡆࡒ࡟ࡖࡒࡏࡓࡆࡊࠢẒ"),
                            filePath=os.path.abspath(file_path),
                            test_run_uuid=uuid_str
                        )
                        bstack1111lllll11_opy_.append(log_entry)
                        logger.debug(bstack1l1llll_opy_ (u"ࠣࡃࡧࡨࡪࡪࠠࡢࡶࡷࡥࡨ࡮࡭ࡦࡰࡷࠤࡱࡵࡧࠡࡧࡱࡸࡷࡿ࠺ࠡࠤẓ") + str(file_name) + bstack1l1llll_opy_ (u"ࠤࠥẔ"))
                    except Exception as file_err:
                        logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡳࡶࡴࡩࡥࡴࡵ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡿ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥẕ") + str(file_err) + bstack1l1llll_opy_ (u"ࠦࠧẖ"))
            if bstack1111lllll11_opy_ and self.cli_service:
                try:
                    req = structs.LogCreatedEventRequest()
                    req.bin_session_id = os.environ.get(bstack1l1llll_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡈࡒࡉࡠࡄࡌࡒࡤ࡙ࡅࡔࡕࡌࡓࡓࡥࡉࡅࠤẗ"), bstack1l1llll_opy_ (u"ࠨࠢẘ"))
                    req.platform_index = int(platform_index)
                    req.client_worker_id = bstack1l1llll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨẙ").format(threading.get_ident(), os.getpid())
                    req.execution_context.hash = str(instance.context.hash)
                    req.execution_context.thread_id = str(instance.context.thread_id)
                    req.execution_context.process_id = str(instance.context.process_id)
                    for entry in bstack1111lllll11_opy_:
                        log_entry = req.logs.add()
                        log_entry.test_framework_name = bstack1l1llll_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠤẚ")
                        log_entry.test_framework_version = TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION, bstack1l1llll_opy_ (u"ࠤࠥẛ"))
                        log_entry.uuid = uuid_str
                        log_entry.test_framework_state = instance.state.name
                        log_entry.message = bstack111lll1l1l1_opy_ (u"ࠥࠦẜ")
                        log_entry.kind = entry.kind
                        log_entry.timestamp = entry.timestamp if isinstance(entry.timestamp, str) else datetime.now(tz=timezone.utc).isoformat()
                        if isinstance(entry.level, str) and len(entry.level.strip()) > 0:
                            log_entry.level = entry.level.strip()
                        log_entry.file_name = entry.fileName
                        log_entry.file_size = entry.fileSize
                        log_entry.file_path = entry.filePath
                    self.cli_service.LogCreatedEvent(req)
                    logger.debug(bstack1l1llll_opy_ (u"ࠦࡘ࡫࡮ࡵࠢࠥẝ") + str(len(bstack1111lllll11_opy_)) + bstack1l1llll_opy_ (u"ࠧࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡰࡴ࡭ࡳࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅࠥẞ"))
                except Exception as bstack1l1ll11llll_opy_:
                    logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡹࡥ࡯ࡦ࡬ࡲ࡬ࠦࡡࡵࡶࡤࡧ࡭ࡳࡥ࡯ࡶࠣࡰࡴ࡭ࡳࠡࡸ࡬ࡥࠥ࡭ࡒࡑࡅ࠽ࠤࠧẟ") + str(bstack1l1ll11llll_opy_) + bstack1l1llll_opy_ (u"ࠢࠣẠ"))
        except Exception as e:
            logger.error(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡱࡴࡲࡧࡪࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵ࠯࡯ࡩࡻ࡫࡬ࠡࡣࡷࡸࡦࡩࡨ࡮ࡧࡱࡸࡸࡀࠠࠣạ") + str(e) + bstack1l1llll_opy_ (u"ࠤࠥẢ"))