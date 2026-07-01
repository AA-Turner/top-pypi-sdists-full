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
import json
import time
import os
import threading
import asyncio
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    AutomationFrameworkBrowser,
    bstack1l11ll1l1l1_opy_,
)
from typing import Tuple, Dict, Any, List, Union
from bstack_utils.helper import is_bstack_automation, bstack1llll1l11l1_opy_, is_robot_playwright_installed, cached_raw_robot_pw_binary_flow
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, TestFrameworkTest
from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
from browserstack_sdk.sdk_cli.bstack11l1lll1ll1_opy_ import bstack11l1l1lllll_opy_
from typing import Tuple, List, Any
from bstack_utils.bstack1l1ll1ll1_opy_ import bstack1lll111ll_opy_, bstack1l1lll1ll1l_opy_, bstack1lll1111l1l_opy_
from browserstack_sdk import sdk_pb2 as structs
class _11l111ll1l1_opy_:
    __slots__ = ()
    state = AutomationFrameworkState.bstack1l11lll1l11_opy_
class bstack1l11111llll_opy_(bstack11l1l1lllll_opy_):
    bstack11l11l1ll11_opy_ = bstack1l1llll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡩࡸࡩࡷࡧࡵࡷࠧᨿ")
    KEY_AUTOMATION_SESSIONS = bstack1l1llll_opy_ (u"ࠢࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡸ࡫ࡳࡴ࡫ࡲࡲࡸࠨᩀ")
    KEY_NON_BROWSERSTACK_AUTOMATION_SESSIONS = bstack1l1llll_opy_ (u"ࠣࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࡠࡵࡨࡷࡸ࡯࡯࡯ࡵࠥᩁ")
    bstack11l11l11ll1_opy_ = bstack1l1llll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡴࡧࡶࡷ࡮ࡵ࡮ࡴࠤᩂ")
    bstack11l111ll1ll_opy_ = bstack1l1llll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡡࡵࡩ࡫ࡹࠢᩃ")
    KEY_CBT_SESSION_CREATED = bstack1l1llll_opy_ (u"ࠦࡨࡨࡴࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡦࡶࡪࡧࡴࡦࡦࠥᩄ")
    bstack11l11l111l1_opy_ = bstack1l1llll_opy_ (u"ࠧࡩࡢࡵࡡࡶࡩࡸࡹࡩࡰࡰࡢࡲࡦࡳࡥࠣᩅ")
    bstack11l111llll1_opy_ = bstack1l1llll_opy_ (u"ࠨࡣࡣࡶࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠦᩆ")
    def __init__(self):
        super().__init__(bstack11l1ll11111_opy_=self.bstack11l11l1ll11_opy_, frameworks=[SeleniumFramework.NAME])
        if not self.is_enabled():
            return
        TestFramework.set_hook_callback((TestFrameworkState.BEFORE_EACH, TestHookState.POST), self.bstack11l111ll111_opy_)
        if bstack1llll1l11l1_opy_():
            TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.POST), self.on_before_test)
        else:
            TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.PRE), self.on_before_test)
        TestFramework.set_hook_callback((TestFrameworkState.TEST, TestHookState.POST), self.on_after_test)
    def is_enabled(self) -> bool:
        return True
    def bstack11l111ll111_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        bstack11l111lll1l_opy_ = self.bstack11l11l11lll_opy_(instance.context)
        if not bstack11l111lll1l_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡴࡧࡷࡣࡦࡩࡴࡪࡸࡨࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࠧᩇ") + str(hook_info) + bstack1l1llll_opy_ (u"ࠣࠤᩈ"))
            return
        f.set_state(instance, bstack1l11111llll_opy_.KEY_AUTOMATION_SESSIONS, bstack11l111lll1l_opy_)
    def bstack11l11l11lll_opy_(self, context: bstack1l11ll1l1l1_opy_, bstack11l111l1l1l_opy_= True):
        if bstack11l111l1l1l_opy_:
            bstack11l111lll1l_opy_ = self.bstack11l1lll11ll_opy_(context, reverse=True)
        else:
            bstack11l111lll1l_opy_ = self.bstack11l1lll1l11_opy_(context, reverse=True)
        bstack11l111lll1l_opy_ = [f for f in bstack11l111lll1l_opy_ if f[1].state != AutomationFrameworkState.QUIT]
        if bstack11l111l1l1l_opy_ and not bstack11l111lll1l_opy_:
            fallback = self._11l11l11l11_opy_()
            if fallback is not None:
                bstack11l111lll1l_opy_ = [fallback]
        return bstack11l111lll1l_opy_
    def _11l11l11l11_opy_(self):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࡋ࡯࡮ࡥࠢࡤࠤࡗࡵࡢࡰࡶࠣࡰ࡮ࡨࡲࡢࡴࡼࠤࡼ࡯ࡴࡩࠢࡤࠤࡱ࡯ࡶࡦࠢࡣࡣࡵࡧࡧࡦࡢࠣࡥࡳࡪࠠࡴࡪࡤࡴࡪࠦࡩࡵࠢ࡯࡭ࡰ࡫ࠠࡢࠌࠣࠤࠥࠦࠠࠡࠢࠣࡶࡪࡹ࡯࡭ࡸࡨࡣࡩࡸࡩࡷࡧࡵࡷࠥ࡫࡮ࡵࡴࡼ࠲ࠥࡘࡥࡵࡷࡵࡲࡸࠦࡎࡰࡰࡨࠤࡼ࡮ࡥ࡯ࠢࡱࡳࡹࠦࡩ࡯ࠢࡤࠤࡗࡵࡢࡰࡶࠣࡧࡴࡴࡴࡦࡺࡷ࠰ࠥࡺࡨࡦࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡴࡨ࡯ࡵࠢࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠥࡈࡵࡪ࡮ࡷࡍࡳࠦࡩࡴࡰࠪࡸࠥࡻࡳࡢࡤ࡯ࡩ࠱ࠦ࡯ࡳࠢࡱࡳࠥ࡫࡬ࡪࡩ࡬ࡦࡱ࡫ࠠ࡭࡫ࡥࡶࡦࡸࡹࠡ࡫ࡶࠤࡱࡵࡡࡥࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᩉ")
        try:
            from robot.libraries.BuiltIn import BuiltIn
        except Exception:
            return None
        try:
            bstack11l11l1l1ll_opy_ = BuiltIn().get_library_instance(all=True)
        except Exception as e:
            self.logger.debug(
                bstack1l1llll_opy_ (u"ࠥࡣࡷࡵࡢࡰࡶࡢࡧࡺࡹࡴࡰ࡯ࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࡟ࡱࡣࡪࡩࡤ࡬ࡡ࡭࡮ࡥࡥࡨࡱ࠺ࠡࡄࡸ࡭ࡱࡺࡉ࡯ࠪࠬ࠲࡬࡫ࡴࡠ࡮࡬ࡦࡷࡧࡲࡺࡡ࡬ࡲࡸࡺࡡ࡯ࡥࡨࠬࡦࡲ࡬࠾ࡖࡵࡹࡪ࠯ࠠࡧࡣ࡬ࡰࡪࡪࠠࠩࡽࡨࢁ࠮ࠨᩊ").format(e=e)
            )
            return None
        if not bstack11l11l1l1ll_opy_:
            return None
        iterable = bstack11l11l1l1ll_opy_.values() if hasattr(bstack11l11l1l1ll_opy_, bstack1l1llll_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࡶࠫᩋ")) else bstack11l11l1l1ll_opy_
        for lib in iterable:
            if lib is None:
                continue
            page = getattr(lib, bstack1l1llll_opy_ (u"ࠬࡥࡰࡢࡩࡨࠫᩌ"), None)
            if page is None:
                continue
            if not hasattr(page, bstack1l1llll_opy_ (u"࠭ࡥࡷࡣ࡯ࡹࡦࡺࡥࠨᩍ")):
                continue
            _11l111lllll_opy_ = getattr(type(page), bstack1l1llll_opy_ (u"ࠧࡠࡡࡰࡳࡩࡻ࡬ࡦࡡࡢࠫᩎ"), bstack1l1llll_opy_ (u"ࠨࠩᩏ")) or bstack1l1llll_opy_ (u"ࠩࠪᩐ")
            if not _11l111lllll_opy_.startswith(bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᩑ")):
                continue
            self.logger.debug(
                bstack1l1llll_opy_ (u"ࠦࡤࡸ࡯ࡣࡱࡷࡣࡨࡻࡳࡵࡱࡰࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡠࡲࡤ࡫ࡪࡥࡦࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࡸࡷ࡮ࡴࡧࠡࡽࡦࡰࡸࢃ࠮ࡠࡲࡤ࡫ࡪࠦࡦࡰࡴࠣࡱࡦࡸ࡫ࡪࡰࡪࠦᩒ").format(
                    cls=type(lib).__name__,
                )
            )
            bstack11l111l11ll_opy_ = lambda p=page: p
            return (bstack11l111l11ll_opy_, _11l111ll1l1_opy_())
        return None
    def on_before_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l111ll111_opy_(f, instance, hook_info, *args, **kwargs)
        if not is_bstack_automation:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࡷࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡷࡪࡹࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᩓ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠨࠢᩔ"))
            return
        bstack11l111lll1l_opy_ = f.get_state(instance, bstack1l11111llll_opy_.KEY_AUTOMATION_SESSIONS, [])
        if not bstack11l111lll1l_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᩕ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠣࠤᩖ"))
            return
        if len(bstack11l111lll1l_opy_) > 1:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࢀࡲࡥ࡯ࠪࡳࡥ࡬࡫࡟ࡪࡰࡶࡸࡦࡴࡣࡦࡵࠬࢁࠥࡪࡲࡪࡸࡨࡶࡸࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࡾ࡯ࡼࡧࡲࡨࡵࢀࠦᩗ"))
        bstack11l111l1l11_opy_, bstack11l1l1lll1l_opy_ = bstack11l111lll1l_opy_[0]
        page = bstack11l111l1l11_opy_()
        if not page:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᩘ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠦࠧᩙ"))
            return
        bstack11lllll111_opy_ = getattr(args[0], bstack1l1llll_opy_ (u"ࠧࡴ࡯ࡥࡧ࡬ࡨࠧᩚ"), None) or getattr(args[0], bstack1l1llll_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᩛ"), None)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1llll_opy_ (u"ࠢࡵࡧࡶࡸࡈࡵ࡮ࡵࡧࡻࡸࡔࡶࡴࡪࡱࡱࡷࠧᩜ")).get(bstack1l1llll_opy_ (u"ࠣࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠥᩝ")):
            try:
                page.evaluate(bstack1l1llll_opy_ (u"ࠤࡢࠤࡂࡄࠠࡼࡿࠥᩞ"),
                            bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࢁࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥࢁࠢ࡯ࡣࡰࡩࠧࡀࠧ᩟") + json.dumps(
                                bstack11lllll111_opy_) + bstack1l1llll_opy_ (u"ࠦࢂࢃ᩠ࠢ"))
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧ࡫ࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡼࡿࠥᩡ"), e)
    def on_after_test(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l111ll111_opy_(f, instance, hook_info, *args, **kwargs)
        if not is_bstack_automation:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࡸࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᩢ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠢࠣᩣ"))
            return
        bstack11l111lll1l_opy_ = f.get_state(instance, bstack1l11111llll_opy_.KEY_AUTOMATION_SESSIONS, [])
        if not bstack11l111lll1l_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᩤ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠤࠥᩥ"))
            return
        if len(bstack11l111lll1l_opy_) > 1:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࢁ࡬ࡦࡰࠫࡴࡦ࡭ࡥࡠ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡶ࠭ࢂࠦࡤࡳ࡫ࡹࡩࡷࡹࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧᩦ"))
        bstack11l111l1l11_opy_, bstack11l1l1lll1l_opy_ = bstack11l111lll1l_opy_[0]
        page = bstack11l111l1l11_opy_()
        if not page:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡳࡥ࡬࡫ࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᩧ") + str(kwargs) + bstack1l1llll_opy_ (u"ࠧࠨᩨ"))
            return
        status = f.get_state(instance, TestFramework.KEY_TEST_RESULT, None)
        if not status:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡮ࡰࠢࡶࡸࡦࡺࡵࡴࠢࡩࡳࡷࠦࡴࡦࡵࡷ࠰ࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࠤᩩ") + str(hook_info) + bstack1l1llll_opy_ (u"ࠢࠣᩪ"))
            return
        bstack11l11l1l1l1_opy_ = {bstack1l1llll_opy_ (u"ࠣࡵࡷࡥࡹࡻࡳࠣᩫ"): status.lower()}
        bstack11l1l1l1_opy_ = f.get_state(instance, TestFramework.KEY_TEST_FAILURE, None)
        if status.lower() == bstack1l1llll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᩬ") and bstack11l1l1l1_opy_ is not None:
            bstack11l11l1l1l1_opy_[bstack1l1llll_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪᩭ")] = bstack11l1l1l1_opy_[0][bstack1l1llll_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧᩮ")][0] if isinstance(bstack11l1l1l1_opy_, list) else str(bstack11l1l1l1_opy_)
        from browserstack_sdk.sdk_cli.cli import cli
        if not cli.config.get(bstack1l1llll_opy_ (u"ࠧࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠥᩯ")).get(bstack1l1llll_opy_ (u"ࠨࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠥᩰ")):
            try:
                page.evaluate(
                        bstack1l1llll_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᩱ"),
                        bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦ࠱ࠦࠢࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠥ࠾ࠥ࠭ᩲ")
                        + json.dumps(bstack11l11l1l1l1_opy_)
                        + bstack1l1llll_opy_ (u"ࠤࢀࠦᩳ")
                    )
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹࠠࡼࡿࠥᩴ"), e)
    def mark_o11y_sync(
        self,
        instance: TestFrameworkTest,
        f: TestFramework,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l111ll111_opy_(f, instance, hook_info, *args, **kwargs)
        if not is_bstack_automation:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠦࡲࡧࡲ࡬ࡡࡲ࠵࠶ࡿ࡟ࡴࡻࡱࡧ࠿ࠦ࡮ࡰࡶࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࡿࡰࡽࡡࡳࡩࡶࢁࠧ᩵"))
            return
        bstack11l111lll1l_opy_ = f.get_state(instance, bstack1l11111llll_opy_.KEY_AUTOMATION_SESSIONS, [])
        if not bstack11l111lll1l_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᩶") + str(kwargs) + bstack1l1llll_opy_ (u"ࠨࠢ᩷"))
            return
        if len(bstack11l111lll1l_opy_) > 1:
            self.logger.debug(
                bstack1l11lll11ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡾࡰࡪࡴࠨࡱࡣࡪࡩࡤ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳࠪࡿࠣࡨࡷ࡯ࡶࡦࡴࡶࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࡼ࡭ࡺࡥࡷ࡭ࡳࡾࠤ᩸"))
        bstack11l111l1l11_opy_, bstack11l1l1lll1l_opy_ = bstack11l111lll1l_opy_[0]
        page = bstack11l111l1l11_opy_()
        if not page:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣ࡯ࡤࡶࡰࡥ࡯࠲࠳ࡼࡣࡸࡿ࡮ࡤ࠼ࠣࡲࡴࠦࡰࡢࡩࡨࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣ᩹") + str(kwargs) + bstack1l1llll_opy_ (u"ࠤࠥ᩺"))
            return
        timestamp = int(time.time() * 1000)
        data = bstack1l1llll_opy_ (u"ࠥࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࡖࡽࡳࡩ࠺ࠣ᩻") + str(timestamp)
        try:
            page.evaluate(
                bstack1l1llll_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧ᩼"),
                bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪ᩽").format(
                    json.dumps(
                        {
                            bstack1l1llll_opy_ (u"ࠨࡡࡤࡶ࡬ࡳࡳࠨ᩾"): bstack1l1llll_opy_ (u"ࠢࡢࡰࡱࡳࡹࡧࡴࡦࠤ᩿"),
                            bstack1l1llll_opy_ (u"ࠣࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠦ᪀"): {
                                bstack1l1llll_opy_ (u"ࠤࡷࡽࡵ࡫ࠢ᪁"): bstack1l1llll_opy_ (u"ࠥࡅࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠢ᪂"),
                                bstack1l1llll_opy_ (u"ࠦࡩࡧࡴࡢࠤ᪃"): data,
                                bstack1l1llll_opy_ (u"ࠧࡲࡥࡷࡧ࡯ࠦ᪄"): bstack1l1llll_opy_ (u"ࠨࡤࡦࡤࡸ࡫ࠧ᪅")
                            }
                        }
                    )
                )
            )
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡳ࠶࠷ࡹࠡࡣࡱࡲࡴࡺࡡࡵ࡫ࡲࡲࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡻࡾࠤ᪆"), e)
    def get_cbt_event(
        self,
        instance: TestFrameworkTest,
        f: TestFramework,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        self.bstack11l111ll111_opy_(f, instance, hook_info, *args, **kwargs)
        if f.get_state(instance, bstack1l11111llll_opy_.KEY_CBT_SESSION_CREATED, False):
            return
        self.ensure_bin_session()
        req = structs.TestSessionEventRequest()
        req.bin_session_id = str(self.bin_session_id or bstack1l1llll_opy_ (u"ࠣࠤ᪇"))
        req.platform_index = int(TestFramework.get_state(instance, TestFramework.KEY_PLATFORM_INDEX, 0) or 0)
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ᪈").format(threading.get_ident(), os.getpid())
        req.test_framework_name = str(TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_NAME, bstack1l1llll_opy_ (u"ࠥࠦ᪉")) or bstack1l1llll_opy_ (u"ࠦࠧ᪊"))
        req.test_framework_version = str(TestFramework.get_state(instance, TestFramework.KEY_TEST_FRAMEWORK_VERSION, bstack1l1llll_opy_ (u"ࠧࠨ᪋")) or bstack1l1llll_opy_ (u"ࠨࠢ᪌"))
        req.test_framework_state = str(hook_info[0].name)
        req.test_hook_state = str(hook_info[1].name)
        req.test_uuid = str(TestFramework.get_state(instance, TestFramework.KEY_TEST_UUID, bstack1l1llll_opy_ (u"ࠢࠣ᪍")) or bstack1l1llll_opy_ (u"ࠣࠤ᪎"))
        current_test_id = TestFramework.get_state(instance, TestFramework.KEY_TEST_ID, None)
        is_behave = f.is_behave_framework() if hasattr(f, bstack1l1llll_opy_ (u"ࠩ࡬ࡷࡤࡨࡥࡩࡣࡹࡩࡤ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᪏")) else False
        bstack11l11l1l111_opy_ = 0
        skipped_count = 0
        for bstack11l11l1l11l_opy_, bstack11l11l11111_opy_ in bstack111ll111_opy_.instances.items():
            session_id = bstack111ll111_opy_.get_state(
                bstack11l11l11111_opy_,
                bstack111ll111_opy_.bstack111lllll_opy_,
                bstack1l1llll_opy_ (u"ࠥࠦ᪐")
            )
            try:
                _1l1111l11ll_opy_ = cached_raw_robot_pw_binary_flow()
            except (ImportError, AttributeError) as e:
                self.logger.warning(
                    bstack1l1llll_opy_ (u"ࠦ࡬࡫ࡴࡠࡥࡥࡸࡤ࡫ࡶࡦࡰࡷ࠾ࠥࡩࡡࡤࡪࡨࡨࡤࡸࡡࡸࡡࡵࡳࡧࡵࡴࡠࡲࡺࡣࡧ࡯࡮ࡢࡴࡼࡣ࡫ࡲ࡯ࡸࠢࡸࡲࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠠࡪࡰࠣࡸ࡭࡯ࡳࠡࡕࡇࡏࠥࡨࡵࡪ࡮ࡧࠤ࠲ࠦࡲࡢࡹࠣࡖࡴࡨ࡯ࡵ࠭ࡓ࡛ࠥࡪࡥࡵࡧࡦࡸ࡮ࡵ࡮ࠡࡦ࡬ࡷࡦࡨ࡬ࡦࡦ࠱ࠤ࡚ࡶࡤࡢࡶࡨࠤࡧࡹࡴࡢࡥ࡮ࡣࡺࡺࡩ࡭ࡵ࠽ࠤࢀࢃࠢ᪑").format(e)
                )
                _1l1111l11ll_opy_ = False
            if is_robot_playwright_installed():
                instance_test_id = bstack111ll111_opy_.get_state(bstack11l11l11111_opy_, bstack1l1llll_opy_ (u"ࠬࡺࡥࡴࡶࡢ࡭ࡩ࠭᪒"), None)
                if instance_test_id != current_test_id:
                    skipped_count += 1
                    continue
                if not session_id:
                    skipped_count += 1
                    continue
            elif _1l1111l11ll_opy_:
                if not session_id:
                    skipped_count += 1
                    continue
            elif is_behave:
                bstack11l111l1lll_opy_ = getattr(bstack11l11l11111_opy_.context, bstack1l1llll_opy_ (u"࠭ࡴࡩࡴࡨࡥࡩࡥࡩࡥࠩ᪓"), None)
                bstack11l111l11l1_opy_ = getattr(instance.context, bstack1l1llll_opy_ (u"ࠧࡵࡪࡵࡩࡦࡪ࡟ࡪࡦࠪ᪔"), None)
                if bstack11l111l1lll_opy_ and bstack11l111l11l1_opy_ and str(bstack11l111l1lll_opy_) != str(bstack11l111l11l1_opy_):
                    skipped_count += 1
                    continue
                if not session_id:
                    skipped_count += 1
                    continue
            session = req.automation_sessions.add()
            session.provider = (
                bstack1l1llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠢ᪕")
                if is_bstack_automation
                else bstack1l1llll_opy_ (u"ࠤࡸࡲࡰࡴ࡯ࡸࡰࡢ࡫ࡷ࡯ࡤࠣ᪖")
            )
            session.ref = str(bstack11l11l11111_opy_.ref() or bstack1l1llll_opy_ (u"ࠥࠦ᪗"))
            session.hub_url = str(bstack111ll111_opy_.get_state(
                bstack11l11l11111_opy_,
                bstack111ll111_opy_.bstack11lll111_opy_,
                bstack1l1llll_opy_ (u"ࠦࠧ᪘")
            ) or bstack1l1llll_opy_ (u"ࠧࠨ᪙"))
            session.framework_name = str(bstack11l11l11111_opy_.framework_name or bstack1l1llll_opy_ (u"ࠨࠢ᪚"))
            session.framework_version = str(bstack11l11l11111_opy_.framework_version or bstack1l1llll_opy_ (u"ࠢࠣ᪛"))
            session.framework_session_id = str(session_id)
            bstack11l11l1l111_opy_ += 1
            if is_behave:
                caps = bstack111ll111_opy_.get_state(bstack11l11l11111_opy_, bstack111ll111_opy_.bstack1l111lll_opy_, None)
                if caps:
                    try:
                        req.capabilities = json.dumps(caps).encode(bstack1l1llll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᪜"))
                    except Exception:
                        pass
        req.execution_context.hash = str(instance.context.hash)
        req.execution_context.thread_id = str(instance.context.thread_id)
        req.execution_context.process_id = str(instance.context.process_id)
        try:
            import json as _json
            bstack11l111ll11l_opy_ = None
            wrapper = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ᪝"), None)
            if wrapper is not None and getattr(wrapper, bstack1l1llll_opy_ (u"ࠪࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᪞"), None):
                bstack11l111ll11l_opy_ = wrapper._capabilities
            if not bstack11l111ll11l_opy_:
                for bstack11l11l11111_opy_ in bstack111ll111_opy_.instances.values():
                    bstack11l111ll11l_opy_ = bstack111ll111_opy_.get_state(
                        bstack11l11l11111_opy_, bstack111ll111_opy_.bstack1l111lll_opy_, None)
                    if bstack11l111ll11l_opy_:
                        break
            if bstack11l111ll11l_opy_:
                req.capabilities = _json.dumps(bstack11l111ll11l_opy_).encode(bstack1l1llll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ᪟"))
        except Exception as _e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧ࡭ࡥࡵࡡࡦࡦࡹࡥࡥࡷࡧࡱࡸ࠿ࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡶ࡯ࡱࡷ࡯ࡥࡹ࡯࡯࡯ࠢࡶ࡯࡮ࡶࡰࡦࡦ࠽ࠤࢀࢃࠢ᪠").format(_e))
        return req
    def bstack11ll11lll1l_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        bstack11l111lll1l_opy_ = f.get_state(instance, bstack1l11111llll_opy_.KEY_AUTOMATION_SESSIONS, [])
        if not bstack11l111lll1l_opy_:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࡟ࡥࡴ࡬ࡺࡪࡸ࠺ࠡࡰࡲࠤࡵࡧࡧࡦࡵࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢ᪡") + str(kwargs) + bstack1l1llll_opy_ (u"ࠢࠣ᪢"))
            return
        if len(bstack11l111lll1l_opy_) > 1:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿࡱ࡫࡮ࠩࡲࡤ࡫ࡪࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࡴࠫࢀࠤࡩࡸࡩࡷࡧࡵࡷࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤ᪣") + str(kwargs) + bstack1l1llll_opy_ (u"ࠤࠥ᪤"))
        bstack11l111l1l11_opy_, bstack11l1l1lll1l_opy_ = bstack11l111lll1l_opy_[0]
        page = bstack11l111l1l11_opy_()
        if not page:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࡣࡩࡸࡩࡷࡧࡵ࠾ࠥࡴ࡯ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥ᪥") + str(kwargs) + bstack1l1llll_opy_ (u"ࠦࠧ᪦"))
            return
        return page
    def bstack11ll111ll11_opy_(
        self,
        f: TestFramework,
        instance: TestFrameworkTest,
        hook_info: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs
    ):
        caps = {}
        platform_details = {}
        bstack11l11l1ll1l_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡘ࡫ࡳࡴ࡫ࡲࡲࡉࡸࡩࡷࡧࡵࠫᪧ"), None)
        if bstack11l11l1ll1l_opy_ and hasattr(bstack11l11l1ll1l_opy_, bstack1l1llll_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᪨")) and bstack11l11l1ll1l_opy_.capabilities:
            caps = bstack11l11l1ll1l_opy_.capabilities
        else:
            bstack11l11l111ll_opy_ = threading.get_ident()
            for bstack11l11l11111_opy_ in bstack111ll111_opy_.instances.values():
                if bstack111ll111_opy_.get_state(bstack11l11l11111_opy_, bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡵࡪࡵࡩࡦࡪ࡟ࡪࡦࠪ᪩"), None) == bstack11l11l111ll_opy_:
                    candidate = bstack111ll111_opy_.get_state(bstack11l11l11111_opy_, bstack111ll111_opy_.bstack1l111lll_opy_, {})
                    if candidate:
                        caps = candidate
                        break
            bstack11l11l11l1l_opy_ = f.is_behave_framework() if (f and hasattr(f, bstack1l1llll_opy_ (u"ࠨ࡫ࡶࡣࡧ࡫ࡨࡢࡸࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ᪪"))) else False
            bstack11l111l1ll1_opy_ = (not bstack11l11l11l1l_opy_) or len(self.config.get(bstack1l1llll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ᪫"), [])) <= 1
            if not caps and bstack11l111l1ll1_opy_:
                for bstack11l11l11111_opy_ in bstack111ll111_opy_.instances.values():
                    candidate = bstack111ll111_opy_.get_state(bstack11l11l11111_opy_, bstack111ll111_opy_.bstack1l111lll_opy_, {})
                    if candidate:
                        caps = candidate
                        break
        platform_details[bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ᪬")] = caps.get(bstack1l1llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ᪭"), bstack1l1llll_opy_ (u"ࠧࠨ᪮"))
        platform_details[bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ᪯")] = caps.get(bstack1l1llll_opy_ (u"ࠢࡰࡵࠥ᪰"), bstack1l1llll_opy_ (u"ࠣࠤ᪱"))
        platform_details[bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ᪲")] = caps.get(bstack1l1llll_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢ᪳"), bstack1l1llll_opy_ (u"ࠦࠧ᪴"))
        platform_details[bstack1l1llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳࠨ᪵")] = caps.get(bstack1l1llll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮᪶ࠣ"), bstack1l1llll_opy_ (u"᪷ࠢࠣ"))
        try:
            bstack1ll1l111l1_opy_ = f.get_state(instance, TestFramework.KEY_PLATFORM_INDEX, 0) if (f and instance) else 0
            if not isinstance(bstack1ll1l111l1_opy_, int):
                bstack1ll1l111l1_opy_ = 0
            bstack1ll11ll1_opy_ = self.config.get(bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶ᪸ࠫ"), [])
            bstack1lll1l1l111_opy_ = bstack1ll11ll1_opy_[bstack1ll1l111l1_opy_] if bstack1ll1l111l1_opy_ < len(bstack1ll11ll1_opy_) else self.config
            bstack1l1l11l11_opy_ = (
                bstack1lll1l1l111_opy_.get(bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹ᪹ࠧ"))
                or bstack1lll1l1l111_opy_.get(bstack1l1llll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ᪺ࠪ"))
                or self.config.get(bstack1l1llll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᪻"))
                or self.config.get(bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᪼"))
            )
            if bstack1l1l11l11_opy_:
                platform_details[bstack1l1llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶ᪽ࠫ")] = bstack1l1l11l11_opy_
        except Exception as ex:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡨࡧࡱࡩࡷࡧࡴࡦࡡࡳࡰࡦࡺࡦࡰࡴࡰࡣࡩ࡫ࡴࡢ࡫࡯ࡷ࠿ࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡤࡸࡹࡧࡣࡩࠢࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦ᪾") + str(ex) + bstack1l1llll_opy_ (u"ࠣࠤᪿ"))
        return platform_details
    def bstack11ll111l1l1_opy_(self, page: object, script_code, args={}):
        if page is None and not is_robot_playwright_installed():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡤ࠵࠶ࡿ࡟ࡴࡥࡵ࡭ࡵࡺ࡟ࡦࡺࡨࡧࡺࡺࡥ࠻ࠢࡳࡥ࡬࡫ࠠࡪࡵࠣࡒࡴࡴࡥ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࠩ࡮࡬࡯ࡪࡲࡹࠡࡦࡨࡪࡪࡸࡲࡦࡦࠣࡧࡱࡵࡳࡦᫀࠫࠥ"))
            return None
        try:
            script_code = script_code.replace(bstack1l1llll_opy_ (u"ࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ᫁"), bstack1l1llll_opy_ (u"ࠦࡧࡹࡴࡢࡥ࡮ࡗࡩࡱࡁࡳࡩࡶࠦ᫂"))
            if is_robot_playwright_installed():
                bstack11l111lll11_opy_ = script_code.replace(bstack1l1llll_opy_ (u"ࠧࡽࡩ࡯ࡦࡲࡻ࠳ࠨ᫃"), bstack1l1llll_opy_ (u"ࠨࡧ࡭ࡱࡥࡥࡱ࡚ࡨࡪࡵ࠱᫄ࠦ"))
                bstack11l111lll11_opy_ = bstack11l111lll11_opy_.replace(bstack1l1llll_opy_ (u"ࠢࡸ࡫ࡱࡨࡴࡽ࡛ࠣ᫅"), bstack1l1llll_opy_ (u"ࠣࡩ࡯ࡳࡧࡧ࡬ࡕࡪ࡬ࡷࡠࠨ᫆"))
                bstack11l11l1111l_opy_ = bstack1l1llll_opy_ (u"ࠤࠥࠦ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࠦࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࠫ࠭ࠥࢁࡻࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡼࡡࡳࠢࡥࡷࡹࡧࡣ࡬ࡕࡧ࡯ࡆࡸࡧࡴࠢࡀࠤࡠࢁࡡࡳࡩࡢ࡮ࡸࡵ࡮ࡾ࡟࠾ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠡࡰࡨࡻࠥࡖࡲࡰ࡯࡬ࡷࡪ࠮ࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࢀࢁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡤࡶࡸࡦࡩ࡫ࡔࡦ࡮ࡅࡷ࡭ࡳ࠯ࡲࡸࡷ࡭࠮ࡲࡦࡵࡲࡰࡻ࡫ࠩ࠼ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࢁࢂ࠯࠻ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡿࢀࠦࠧࠨ᫇").format(fn_body=bstack11l111lll11_opy_, arg_json=json.dumps(args))
                from robot.libraries.BuiltIn import BuiltIn
                builtin = BuiltIn()
                return builtin.run_keyword(
                    bstack1l1llll_opy_ (u"ࠪࡆࡷࡵࡷࡴࡧࡵ࠲ࡊࡼࡡ࡭ࡷࡤࡸࡪࠦࡊࡢࡸࡤࡗࡨࡸࡩࡱࡶࠪ᫈"),
                    None,
                    bstack11l11l1111l_opy_
                )
            else:
                script_template = bstack1l1llll_opy_ (u"ࠦࠧࠨࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࠢࠫ࠲࠳࠴ࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠯ࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡩࡹࡻࡲ࡯ࠢࡱࡩࡼࠦࡐࡳࡱࡰ࡭ࡸ࡫ࠨࠩࡴࡨࡷࡴࡲࡶࡦ࠮ࠣࡶࡪࡰࡥࡤࡶࠬࠤࡂࡄࠠࡼࡽࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡢࡴࡶࡤࡧࡰ࡙ࡤ࡬ࡃࡵ࡫ࡸ࠴ࡰࡶࡵ࡫ࠬࡷ࡫ࡳࡰ࡮ࡹࡩ࠮ࡁࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡿ࡫ࡴ࡟ࡣࡱࡧࡽࢂࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪ࠽ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃࡽࠪࠪࡾࡥࡷ࡭࡟࡫ࡵࡲࡲࢂ࠯ࠢࠣࠤ᫉")
                script = script_template.format(fn_body=script_code, arg_json=json.dumps(args))
                return page.evaluate(script)
        except Exception as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠧࡧ࠱࠲ࡻࡢࡷࡨࡸࡩࡱࡶࡢࡩࡽ࡫ࡣࡶࡶࡨ࠾ࠥࡋࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵ࠮᫊ࠣࠦ") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢ᫋"))