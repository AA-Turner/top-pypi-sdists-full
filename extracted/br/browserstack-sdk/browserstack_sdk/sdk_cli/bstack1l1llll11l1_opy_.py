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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack11l111l1l_opy_ import (
    bstack1ll1l1111l_opy_,
    bstack1l1l111lll_opy_,
    bstack11l1l1l1_opy_,
    bstack1l1ll111lll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l11llll_opy_ import bstack1l11lll111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1ll11l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l111l111_opy_ import bstack1l11l1l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l11l111l1l_opy_ import bstack1l1l1111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack111l11ll_opy_ import bstack11ll1l1ll_opy_
from bstack_utils.helper import bstack11lllll11ll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.accessibility import (
    is_browser_supported_for_accessibility,
    get_browser_display_name,
    get_min_version_for_browser,
    requires_chrome_options_validation,
    is_version_supported
)
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll111111ll_opy_(bstack1l11l1l11ll_opy_):
    bstack1l1111ll11l_opy_ = False
    bstack1l111l111ll_opy_ = bstack111ll_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦᖼ")
    bstack1l111l1l1ll_opy_ = bstack111ll_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᖽ")
    bstack1l11111lll1_opy_ = bstack111ll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨᖾ")
    bstack1l1111l11l1_opy_ = bstack111ll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᖿ")
    bstack11llll1ll1l_opy_ = bstack111ll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦᗀ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1l1lllll1ll_opy_ = threading.Event()
    _1l1lllll1ll_opy_.set()
    def __init__(self, bstack1l11l1111ll_opy_, bstack1l11l1l1l1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1111lll1l_opy_ = False
        self.bstack11lllll1lll_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l111l11ll1_opy_ = False
        self.bstack1l11111l1l1_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack11llll1lll1_opy_ = bstack1l11l1l1l1l_opy_
        bstack1l11l1111ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack1ll1111l111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack1l1llllll1l_opy_)
        bstack1l11l1111ll_opy_.bstack1l111l1111l_opy_((bstack1ll1l1111l_opy_.bstack111l1ll111_opy_, bstack1l1l111lll_opy_.PRE), self.bstack1l111l11l11_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111l11ll_opy_)
        TestFramework.bstack1l111l1111l_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l111l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l111l1l11l_opy_(instance, args)
        test_framework = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l1111l111l_opy_)
        if self.bstack1l1111lll1l_opy_:
            self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᗁ")] = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_)
        if bstack111ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᗂ") in instance.bstack1l1l11l1111_opy_:
            platform_index = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111111111_opy_)
            self.accessibility = self.bstack11lllll11l1_opy_(tags, self.config[bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᗃ")][platform_index])
        elif test_framework == bstack111ll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨᗄ"):
            platform_index = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l111111111_opy_)
            self.accessibility = self.bstack11lllll11l1_opy_(tags, self.config[bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᗅ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l1111lll11_opy_)
            self._current_test_uuid = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_)
            self.save_result_done = False
            self.logger.debug(bstack111ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡷࡵࡢࡰࡶ࠰ࡴࡼࠦࡴࡢࡩࡶ࠱ࡴࡴ࡬ࡺࠢࡦ࡬ࡪࡩ࡫࠭ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠿ࠥᗆ") + str(self.accessibility) + bstack111ll_opy_ (u"ࠥࠦᗇ"))
        else:
            capabilities = self.bstack11llll1lll1_opy_.bstack11llllllll1_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack111ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᗈ") + str(kwargs) + bstack111ll_opy_ (u"ࠧࠨᗉ"))
                return
            self.accessibility = self.bstack11lllll11l1_opy_(tags, capabilities)
        if self.bstack11llll1lll1_opy_.pages and self.bstack11llll1lll1_opy_.pages.values():
            bstack1l111l11lll_opy_ = list(self.bstack11llll1lll1_opy_.pages.values())
            if bstack1l111l11lll_opy_ and isinstance(bstack1l111l11lll_opy_[0], (list, tuple)) and bstack1l111l11lll_opy_[0]:
                bstack11lllllll11_opy_ = bstack1l111l11lll_opy_[0][0]
                if callable(bstack11lllllll11_opy_):
                    page = bstack11lllllll11_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack111ll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᗊ"))
                    def bstack1l11111l11l_opy_():
                        self.get_accessibility_results_summary(page, bstack111ll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᗋ"))
                    setattr(page, bstack111ll_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᗌ"), get_results)
                    setattr(page, bstack111ll_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᗍ"), bstack1l11111l11l_opy_)
        self.logger.debug(bstack111ll_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᗎ") + str(self.accessibility) + bstack111ll_opy_ (u"ࠦࠧᗏ"))
    def bstack1l111l11l11_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack111ll_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡢࡶࠣࡇࡗࡋࡁࡕࡇ࠱ࡔࡗࡋࠠࡢࡨࡷࡩࡷࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣ࡭ࡳࠦࡒࡰࡤࡲࡸ࠲ࡖࡗࠡࡨ࡯ࡳࡼ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡪ࡮ࡴࡥࡴࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡰࡦ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡥ࡫ࡩࡨࡱ࠮ࠣࠤࠥᗐ")
        if not self.accessibility:
            return
        capabilities = self.bstack11llll1lll1_opy_.bstack11llllllll1_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡧࡶ࡮ࡼࡥࡳࡡࡦࡶࡪࡧࡴࡦ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠣᗑ"))
            return
        bstack1ll1l1l1111_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1ll1l1l1111_opy_
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡨࡷ࡯ࡶࡦࡴࡢࡧࡷ࡫ࡡࡵࡧ࠽ࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡾ࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࠦᗒ") + str(self.accessibility) + bstack111ll_opy_ (u"ࠣࠤᗓ"))
    def bstack1l1llllll1l_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        bstack1l1l1lll11l_opy_: Tuple[bstack1ll1l1111l_opy_, bstack1l1l111lll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack11lllll111l_opy_(method_name, *args):
                bstack1l11111lll_opy_ = datetime.now()
                self.bstack1l11111ll1l_opy_(f, exec, *args, **kwargs)
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᗔ"), datetime.now() - bstack1l11111lll_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᗕ"))
                return
            bstack1l11111lll_opy_ = datetime.now()
            self.bstack1l11111ll1l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᗖ"), datetime.now() - bstack1l11111lll_opy_)
            bstack1l1ll1l11l1_opy_ = instance.data.get(bstack111ll_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᗗ"), None)
            if (
                not f.bstack1l1111llll1_opy_(method_name)
                or f.bstack11llll1ll11_opy_(method_name, *args)
                or f.bstack1l1111l1ll1_opy_(method_name, *args)
                or (bstack1l1ll1l11l1_opy_ and int(bstack1l1ll1l11l1_opy_)>1)
            ):
                return
            if not f.bstack1l1llll1111_opy_(instance, bstack1ll111111ll_opy_.bstack1l11111lll1_opy_, False):
                if not bstack1ll111111ll_opy_.bstack1l1111ll11l_opy_:
                    self.logger.warning(bstack111ll_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᗘ") + str(f.platform_index) + bstack111ll_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᗙ"))
                    bstack1ll111111ll_opy_.bstack1l1111ll11l_opy_ = True
                return
            bstack1l1111l1lll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1111l1lll_opy_:
                platform_index = f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_, 0)
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᗚ") + str(f.framework_name) + bstack111ll_opy_ (u"ࠤࠥᗛ"))
                return
            command_name = f.bstack1l111l1l1l1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧᗜ") + str(method_name) + bstack111ll_opy_ (u"ࠦࠧᗝ"))
                return
            if f.framework_name != bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᗞ"):
                bstack1l111l1lll1_opy_ = f.bstack1l1llll1111_opy_(instance, bstack1ll111111ll_opy_.bstack11llll1ll1l_opy_, False)
                if command_name == bstack111ll_opy_ (u"ࠨࡧࡦࡶࠥᗟ") and not bstack1l111l1lll1_opy_:
                    f.bstack11ll11l1_opy_(instance, bstack1ll111111ll_opy_.bstack11llll1ll1l_opy_, True)
                    bstack1l111l1lll1_opy_ = True
                if not bstack1l111l1lll1_opy_ and not self.bstack1l1111lll1l_opy_:
                    self.logger.debug(bstack111ll_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᗠ") + str(command_name) + bstack111ll_opy_ (u"ࠣࠤᗡ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack111ll_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᗢ") + str(command_name) + bstack111ll_opy_ (u"ࠥࠦᗣ"))
                return
            self.logger.info(bstack111ll_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᗤ") + str(command_name) + bstack111ll_opy_ (u"ࠧࠨᗥ"))
            scripts = [(s, bstack1l1111l1lll_opy_[s]) for s in scripts_to_run if s in bstack1l1111l1lll_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack1l11111lll_opy_ = datetime.now()
                    if script_name == bstack111ll_opy_ (u"ࠨࡳࡤࡣࡱࠦᗦ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack111ll_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᗧ"): {
                                    bstack111ll_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᗨ"): bstack111ll_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧᗩ"),
                                    bstack111ll_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢᗪ"): [
                                        {
                                            bstack111ll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᗫ"): command_name
                                        }
                                    ]
                                },
                                bstack111ll_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᗬ"): {
                                    bstack111ll_opy_ (u"ࠨࡢࡰࡦࡼࠦᗭ"): {
                                        bstack111ll_opy_ (u"ࠢ࡮ࡵࡪࠦᗮ"): result.get(bstack111ll_opy_ (u"ࠣ࡯ࡶ࡫ࠧᗯ"), bstack111ll_opy_ (u"ࠤࠥᗰ")) if isinstance(result, dict) else bstack111ll_opy_ (u"ࠥࠦᗱ"),
                                        bstack111ll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᗲ"): result.get(bstack111ll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᗳ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack111ll_opy_ (u"ࠨࠬࠣᗴ"), bstack111ll_opy_ (u"ࠢ࠻ࠤᗵ"))))
                        except Exception as bstack1111l1llll_opy_:
                            self.logger.debug(bstack111ll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨᗶ") + str(bstack1111l1llll_opy_) + bstack111ll_opy_ (u"ࠤࠥᗷ"))
                    instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᗸ") + script_name, datetime.now() - bstack1l11111lll_opy_)
                    if isinstance(result, dict) and not result.get(bstack111ll_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᗹ"), True):
                        self.logger.warning(bstack111ll_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᗺ") + str(result) + bstack111ll_opy_ (u"ࠨࠢᗻ"))
                        break
                except Exception as e:
                    self.logger.error(bstack111ll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᗼ") + str(e) + bstack111ll_opy_ (u"ࠣࠤᗽ"))
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᗾ") + str(e) + bstack111ll_opy_ (u"ࠥࠦᗿ"))
    def bstack1l111l111l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1ll11l1_opy_,
        bstack1l1l1lll11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᘀ") not in instance.bstack1l1l11l1111_opy_:
            tags = self._1l111l1l11l_opy_(instance, args)
            capabilities = self.bstack11llll1lll1_opy_.bstack11llllllll1_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
            self.accessibility = self.bstack11lllll11l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᘁ"))
            return
        driver = self.bstack11llll1lll1_opy_.bstack1l111l11111_opy_(f, instance, bstack1l1l1lll11l_opy_, *args, **kwargs)
        test_name = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l1111lll11_opy_)
        if not test_name:
            self.logger.debug(bstack111ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᘂ"))
            return
        test_uuid = f.bstack1l1llll1111_opy_(instance, TestFramework.bstack1l11111111l_opy_)
        if not test_uuid:
            self.logger.debug(bstack111ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᘃ"))
            return
        if isinstance(self.bstack11llll1lll1_opy_, bstack1l11l1ll111_opy_):
            framework_name = bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᘄ")
        else:
            framework_name = bstack111ll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᘅ")
        if not self.save_result_done:
            self.bstack11l1ll11l_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack1lll1ll1ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᘆ"))
            return
        bstack1l11111lll_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack111ll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘇ"), None)
        if not script_code:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᘈ") + str(framework_name) + bstack111ll_opy_ (u"ࠨࠠࠣᘉ"))
            return
        if self.bstack1l1111lll1l_opy_:
            arg = dict()
            arg[bstack111ll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᘊ")] = method if method else bstack111ll_opy_ (u"ࠣࠤᘋ")
            arg[bstack111ll_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᘌ")] = self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᘍ")]
            arg[bstack111ll_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᘎ")] = self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᘏ")]
            arg[bstack111ll_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᘐ")] = self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᘑ")]
            arg[bstack111ll_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᘒ")] = self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᘓ")]
            arg[bstack111ll_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᘔ")] = str(int(datetime.now().timestamp() * 1000))
            bstack11lllllll1l_opy_ = self.bstack1l111111lll_opy_(bstack111ll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘕ"), self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᘖ")])
            if bstack111ll_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᘗ") in bstack11lllllll1l_opy_:
                bstack11lllllll1l_opy_ = bstack11lllllll1l_opy_.copy()
                bstack11lllllll1l_opy_[bstack111ll_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᘘ")] = bstack11lllllll1l_opy_.pop(bstack111ll_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᘙ"))
            arg = bstack11lllll11ll_opy_(arg, bstack11lllllll1l_opy_)
            bstack11llllll1l1_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack11llllll1l1_opy_)
            return
        instance = bstack11l1l1l1_opy_.bstack1l1l1llllll_opy_(driver)
        if instance:
            if not bstack11l1l1l1_opy_.bstack1l1llll1111_opy_(instance, bstack1ll111111ll_opy_.bstack1l1111l11l1_opy_, False):
                bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, bstack1ll111111ll_opy_.bstack1l1111l11l1_opy_, True)
            else:
                self.logger.info(bstack111ll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᘚ") + str(method) + bstack111ll_opy_ (u"ࠥࠦᘛ"))
                return
        self.logger.info(bstack111ll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᘜ") + str(method) + bstack111ll_opy_ (u"ࠧࠨᘝ"))
        if framework_name == bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᘞ"):
            result = self.bstack11llll1lll1_opy_.bstack1l111111ll1_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack111ll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᘟ"): method if method else bstack111ll_opy_ (u"ࠣࠤᘠ")})
        bstack111l1l1l_opy_.end(EVENTS.bstack1lll1ll1ll_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘡ"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘢ"), True, None, command=method)
        if instance:
            bstack11l1l1l1_opy_.bstack11ll11l1_opy_(instance, bstack1ll111111ll_opy_.bstack1l1111l11l1_opy_, False)
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᘣ"), datetime.now() - bstack1l11111lll_opy_)
        return result
        def bstack1l1111l1l1l_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack11llllll111_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1111ll1ll_opy_ = self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᘤ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᘥ"), bstack111ll_opy_ (u"ࠧ࠱ࠩᘦ")))
            req.client_worker_id = bstack111ll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᘧ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack111111ll1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack111ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᘨ") + str(r) + bstack111ll_opy_ (u"ࠥࠦᘩ"))
                else:
                    bstack1l111l1ll11_opy_ = json.loads(r.bstack1l11111ll11_opy_.decode(bstack111ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᘪ")))
                    if result_type == bstack111ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᘫ"):
                        return bstack1l111l1ll11_opy_.get(bstack111ll_opy_ (u"ࠨࡤࡢࡶࡤࠦᘬ"), [])
                    else:
                        return bstack1l111l1ll11_opy_.get(bstack111ll_opy_ (u"ࠢࡥࡣࡷࡥࠧᘭ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack111ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᘮ") + str(e) + bstack111ll_opy_ (u"ࠤࠥᘯ"))
    @measure(event_name=EVENTS.bstack11l11ll1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1ll111111ll_opy_._1l1lllll1ll_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l1111lll1l_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l1111l1l1l_opy_(driver, framework_name, bstack111ll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᘰ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack111ll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᘱ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack111ll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᘲ"), framework_name=framework_name)
            bstack1l11111lll_opy_ = datetime.now()
            if framework_name == bstack111ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᘳ"):
                result = self.bstack11llll1lll1_opy_.bstack1l111111ll1_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11l1l1l1_opy_.bstack1l1l1llllll_opy_(driver)
            if instance:
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᘴ"), datetime.now() - bstack1l11111lll_opy_)
            return result
        finally:
            bstack1ll111111ll_opy_._1l1lllll1ll_opy_.set()
    @measure(event_name=EVENTS.bstack1llllll1ll_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1ll111111ll_opy_._1l1lllll1ll_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᘵ"))
                return
            if self.bstack1l1111lll1l_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l1111l1l1l_opy_(driver, framework_name, bstack111ll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᘶ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack111ll_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᘷ"), None)
            if not script_code:
                self.logger.debug(bstack111ll_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᘸ") + str(framework_name) + bstack111ll_opy_ (u"ࠧࠨᘹ"))
                return
            self.perform_scan(driver, method=bstack111ll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᘺ"), framework_name=framework_name)
            bstack1l11111lll_opy_ = datetime.now()
            if framework_name == bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᘻ"):
                result = self.bstack11llll1lll1_opy_.bstack1l111111ll1_opy_(driver, script_code)
                bstack1ll111111ll_opy_._1l1lllll1ll_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11l1l1l1_opy_.bstack1l1l1llllll_opy_(driver)
            if instance:
                instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᘼ"), datetime.now() - bstack1l11111lll_opy_)
            return result
        finally:
            bstack1ll111111ll_opy_._1l1lllll1ll_opy_.set()
    @measure(event_name=EVENTS.bstack1l1111111l1_opy_, stage=STAGE.bstack1l1l11l1l_opy_)
    def bstack1l111111l11_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack11llllll111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᘽ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack111111ll1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᘾ") + str(r) + bstack111ll_opy_ (u"ࠦࠧᘿ"))
            else:
                self.bstack1l1111l1111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᙀ") + str(e) + bstack111ll_opy_ (u"ࠨࠢᙁ"))
            traceback.print_exc()
            raise e
    def bstack1l1111l1111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack111ll_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᙂ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1111lll1l_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨᙃ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack11lllll1lll_opy_[bstack111ll_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᙄ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack11lllll1lll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack11lllll1ll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack11lllll1ll1_opy_:
                        bstack11lllll1ll1_opy_[command.method] = dict()
                    if command.name and not command.name in bstack11lllll1ll1_opy_[command.method]:
                        bstack11lllll1ll1_opy_[command.method][command.name] = list()
                    bstack11lllll1ll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack11lllll1ll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l11111ll1l_opy_(
        self,
        f: bstack1l11lll111l_opy_,
        exec: Tuple[bstack1l1ll111lll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack11llll1lll1_opy_, bstack1l11l1ll111_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack111ll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᙅ"):
                    return
        if f.bstack1l1llll1111_opy_(instance, bstack1ll111111ll_opy_.bstack1l11111lll1_opy_, False) == True:
            return
        bstack11lllll1l11_opy_ = False
        desired_capabilities = f.bstack1l1111ll1l1_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack1l11111l111_opy_(instance)
            platform_index = f.bstack1l1llll1111_opy_(instance, bstack1l11lll111l_opy_.bstack1l111111111_opy_, 0)
            bstack1l1111ll111_opy_ = datetime.now()
            r = self.bstack1l111111l11_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1ll11111l_opy_(bstack111ll_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᙆ"), datetime.now() - bstack1l1111ll111_opy_)
            bstack11lllll1l11_opy_ = r.success
            f.bstack11ll11l1_opy_(instance, bstack1ll111111ll_opy_.bstack1l11111lll1_opy_, bstack11lllll1l11_opy_)
        else:
            self.logger.debug(bstack111ll_opy_ (u"ࠧ࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡹ࡬ࡰࡱࠦࡲࡦࡶࡵࡽࠥࡵ࡮ࠡࡰࡨࡼࡹࠦ࡫ࡦࡻࡺࡳࡷࡪࠢᙇ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l111111l11_opy_ = self.config.get(bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙈ"))
        if not bstack1l111111l11_opy_:
            return True
        try:
            include_tags = bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᙉ")] if bstack111ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᙊ") in bstack1l111111l11_opy_ and isinstance(bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᙋ")], list) else []
            exclude_tags = bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᙌ")] if bstack111ll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᙍ") in bstack1l111111l11_opy_ and isinstance(bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᙎ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᙏ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l1111lll1l_opy_:
                bstack11llllll11l_opy_ = caps.get(bstack111ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᙐ"))
                if bstack11llllll11l_opy_ is not None and str(bstack11llllll11l_opy_).lower() == bstack111ll_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᙑ"):
                    bstack11lllllllll_opy_ = caps.get(bstack111ll_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᙒ")) or caps.get(bstack111ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᙓ"))
                    if bstack11lllllllll_opy_ is not None and int(bstack11lllllllll_opy_) < 11:
                        self.logger.warning(bstack111ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡆࡴࡤࡳࡱ࡬ࡨࠥ࠷࠱ࠡࡣࡱࡨࠥࡧࡢࡰࡸࡨ࠲ࠥࡉࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡀࠤࢀࢃ࠮ࠣᙔ").format(bstack11lllllllll_opy_))
                        return False
                return True
            bstack1l1111l1l11_opy_ = caps.get(bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙕ"), {}).get(bstack111ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᙖ"), caps.get(bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᙗ"), bstack111ll_opy_ (u"ࠨࠩᙘ")))
            if bstack1l1111l1l11_opy_:
                self.logger.warning(bstack111ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᙙ"))
                return False
            browser = caps.get(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᙚ"), bstack111ll_opy_ (u"ࠫࠬᙛ")).lower()
            if not is_browser_supported_for_accessibility(browser):
                bstack11lllll1111_opy_ = bstack111ll_opy_ (u"ࠬ࠲ࠠࠨᙜ").join([get_browser_display_name(b) for b in ACCESSIBILITY_SUPPORTED_BROWSERS.keys()])
                self.logger.warning(bstack111ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࠢᙝ") + str(bstack11lllll1111_opy_) + bstack111ll_opy_ (u"ࠢࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᙞ"))
                return False
            bstack1ll1lll1111_opy_ = self.config.get(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᙟ"), True)
            bstack1l1111111ll_opy_ = self.config.get(bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᙠ"), False)
            min_version = get_min_version_for_browser(browser, bstack1ll1lll1111_opy_, bstack1l1111111ll_opy_)
            if not min_version:
                self.logger.warning(bstack111ll_opy_ (u"ࠥࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡰ࡭ࡳ࡯࡭ࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࠤᙡ") + str(browser) + bstack111ll_opy_ (u"ࠦࠧᙢ"))
                return False
            browser_version = caps.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙣ"))
            if not browser_version:
                browser_version = caps.get(bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᙤ"), {}).get(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙥ"), bstack111ll_opy_ (u"ࠨࠩᙦ"))
            bstack1l111l1l111_opy_ = str(browser_version).lower() if browser_version is not None else bstack111ll_opy_ (u"ࠩࠪᙧ")
            if bstack1l111l1l111_opy_:
                if bstack1l111l1l111_opy_.startswith(bstack111ll_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᙨ")):
                    if bstack1l111l1l111_opy_.startswith(bstack111ll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬᙩ")):
                        bstack11llll1llll_opy_ = bstack1l111l1l111_opy_[len(bstack111ll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ᙪ")):]
                        if bstack11llll1llll_opy_ and not bstack11llll1llll_opy_.isdigit():
                            self.logger.warning(bstack111ll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡩࡳࡷࡳࡡࡵࠢࠪࡿࢂ࠭࠻ࠡࡧࡻࡴࡪࡩࡴࡦࡦࠣࠫࡱࡧࡴࡦࡵࡷࠫࠥࡵࡲࠡࠩ࡯ࡥࡹ࡫ࡳࡵ࠯࠿ࡲࡺࡳࡢࡦࡴࡁࠫ࠳ࠨᙫ").format(browser_version))
                            return False
                else:
                    if not is_version_supported(bstack1l111l1l111_opy_, min_version):
                        display_name = get_browser_display_name(browser)
                        self.logger.warning(bstack111ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡼࡿࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡽࠡࡱࡵࠤ࡭࡯ࡧࡩࡧࡵ࠲ࠧᙬ").format(display_name, min_version))
                        return False
            if requires_chrome_options_validation(browser):
                bstack1l111l1ll1l_opy_ = caps.get(bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᙭"), {}).get(bstack111ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᙮"))
                if not bstack1l111l1ll1l_opy_:
                    bstack1l111l1ll1l_opy_ = caps.get(bstack111ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᙯ"), {})
                if not bstack1l111l1ll1l_opy_:
                    bstack1l111l1ll1l_opy_ = caps.get(bstack111ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᙰ"), {})
                if bstack1l111l1ll1l_opy_ and any(arg == bstack111ll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᙱ") or (arg.startswith(bstack111ll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᙲ")) and arg != bstack111ll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᙳ"))
                                         for arg in bstack1l111l1ll1l_opy_.get(bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᙴ"), [])):
                    self.logger.warning(bstack111ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᙵ"))
                    return False
            return True
        except Exception as error:
            self.logger.debug(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᙶ") + str(error))
            return False
    def bstack11llllll1ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l111l11l1l_opy_ = {
            bstack111ll_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᙷ"): test_uuid,
        }
        bstack1l11111llll_opy_ = {}
        if result.success:
            bstack1l11111llll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack11lllll11ll_opy_(bstack1l111l11l1l_opy_, bstack1l11111llll_opy_)
    def bstack1l111111lll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack111ll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡩࡹࡩࡨࠡࡥࡨࡲࡹࡸࡡ࡭ࠢࡤࡹࡹ࡮ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡴࡥࡵ࡭ࡵࡺࠠ࡯ࡣࡰࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡥࡤࡧ࡭࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡬ࡥࡵࡥ࡫ࡩࡩ࠲ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠣࡰࡴࡧࡤࡴࠢࡤࡲࡩࠦࡣࡢࡥ࡫ࡩࡸࠦࡩࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡹࡣࡳ࡫ࡳࡸࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨ࠿ࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠭ࠢࡨࡱࡵࡺࡹࠡࡦ࡬ࡧࡹࠦࡩࡧࠢࡨࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᙸ")
        try:
            if self.bstack1l111l11ll1_opy_:
                return self.bstack1l11111l1l1_opy_
            self.bstack11llllll111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111ll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᙹ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᙺ"), bstack111ll_opy_ (u"ࠨ࠲ࠪᙻ")))
            req.client_worker_id = bstack111ll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᙼ").format(threading.get_ident(), os.getpid())
            r = self.bstack111111ll1l_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l11111l1l1_opy_ = self.bstack11llllll1ll_opy_(test_uuid, r)
                self.bstack1l111l11ll1_opy_ = True
            else:
                self.logger.error(bstack111ll_opy_ (u"ࠥࡪࡪࡺࡣࡩࡅࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡇ࠱࠲ࡻࡆࡳࡳ࡬ࡩࡨ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡪࡲࡪࡸࡨࡶࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡰࡢࡴࡤࡱࡸࠦࡦࡰࡴࠣࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧᙽ") + str(r.error) + bstack111ll_opy_ (u"ࠦࠧᙾ"))
                self.bstack1l11111l1l1_opy_ = dict()
            return self.bstack1l11111l1l1_opy_
        except Exception as e:
            self.logger.error(bstack111ll_opy_ (u"ࠧ࡬ࡥࡵࡥ࡫ࡇࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡂ࠳࠴ࡽࡈࡵ࡮ࡧ࡫ࡪ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡲࡶࠥࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢᙿ") + str(traceback.format_exc()) + bstack111ll_opy_ (u"ࠨࠢ "))
            return dict()
    def bstack11l1ll11l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack11111l11l_opy_ = None
        bstack1ll111111ll_opy_._1l1lllll1ll_opy_.clear()
        try:
            self.bstack11llllll111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111ll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᚁ")
            req.script_name = bstack111ll_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᚂ")
            req.platform_index = str(os.environ.get(bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᚃ"), bstack111ll_opy_ (u"ࠪ࠴ࠬᚄ")))
            req.client_worker_id = bstack111ll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᚅ").format(threading.get_ident(), os.getpid())
            r = self.bstack111111ll1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack111ll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᚆ") + str(r.error) + bstack111ll_opy_ (u"ࠨࠢᚇ"))
            else:
                bstack1l111l11l1l_opy_ = self.bstack11llllll1ll_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᚈ") + str(bstack1l111l11l1l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack111ll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᚉ") + str(framework_name) + bstack111ll_opy_ (u"ࠤࠣࠦᚊ"))
                return
            bstack11111l11l_opy_ = bstack111l1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack1l1111lllll_opy_.value)
            self.bstack1l11111l1ll_opy_(driver, script_code, bstack1l111l11l1l_opy_, framework_name)
            try:
                bstack11lllll1l1l_opy_ = {
                    bstack111ll_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦᚋ"): {
                        bstack111ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧᚌ"): bstack111ll_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡆ࡜ࡅࡠࡔࡈࡗ࡚ࡒࡔࡔࠤᚍ"),
                    },
                    bstack111ll_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᚎ"): {
                        bstack111ll_opy_ (u"ࠢࡣࡱࡧࡽࠧᚏ"): {
                            bstack111ll_opy_ (u"ࠣ࡯ࡶ࡫ࠧᚐ"): bstack111ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᚑ"),
                            bstack111ll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᚒ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack11lllll1l1l_opy_, separators=(bstack111ll_opy_ (u"ࠫ࠱࠭ᚓ"), bstack111ll_opy_ (u"ࠬࡀࠧᚔ"))))
            except Exception as bstack1111l1llll_opy_:
                self.logger.debug(bstack111ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡢࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡪࡡࡵࡣ࠽ࠤࠧᚕ") + str(bstack1111l1llll_opy_) + bstack111ll_opy_ (u"ࠢࠣᚖ"))
            self.logger.info(bstack111ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᚗ"))
            bstack111l1l1l_opy_.end(EVENTS.bstack1l1111lllll_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᚘ"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᚙ"), True, None, command=bstack111ll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᚚ"),test_name=name)
        except Exception as bstack1l111111l1l_opy_:
            self.logger.error(bstack111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢ᚛") + bstack111ll_opy_ (u"ࠨࡳࡵࡴࠫࡴࡦࡺࡨࠪࠤ᚜") + bstack111ll_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤ᚝") + str(bstack1l111111l1l_opy_))
            bstack111l1l1l_opy_.end(EVENTS.bstack1l1111lllll_opy_.value, bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᚞"), bstack11111l11l_opy_+bstack111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᚟"), False, bstack1l111111l1l_opy_, command=bstack111ll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᚠ"),test_name=name)
        finally:
            bstack1ll111111ll_opy_._1l1lllll1ll_opy_.set()
    def bstack1l1lllll11l_opy_(self):
        bstack111ll_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡦࡳࡱࡰࠤࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡺ࡬ࡪࡴࠠࡢࠢࡦࡰࡴࡹࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢ࡬ࡷࠥࡧࡢࡰࡷࡷࠤࡹࡵࠠࡦࡺࡨࡧࡺࡺࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᚡ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack111ll_opy_ (u"ࠧࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࡣࡧ࡫ࡦࡰࡴࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨ࠾ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠢᚢ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack111ll_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠣࡳࡷࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᚣ"))
            return
        self.logger.debug(bstack111ll_opy_ (u"ࠢࡴࡶࡲࡴࡤࡩࡡࡱࡶࡸࡶࡪࡥࡢࡦࡨࡲࡶࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪࡀࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵࡷࡳࡵࡥࡴࡦࡵࡷࡣࡨࡧࡰࡵࡷࡵࡩࠧᚤ"))
        self.bstack11l1ll11l_opy_(None, self._current_test_name, bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᚥ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack1l11111l1ll_opy_(self, driver, script_code, bstack1l111l11l1l_opy_, framework_name):
        if framework_name == bstack111ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᚦ"):
            self.bstack11llll1lll1_opy_.bstack1l111111ll1_opy_(driver, script_code, bstack1l111l11l1l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l111l11l1l_opy_))
    def _1l111l1l11l_opy_(self, instance: bstack1l1l1ll11l1_opy_, args: Tuple) -> list:
        bstack111ll_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡩࡶࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢᚧ")
        if bstack111ll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᚨ") in instance.bstack1l1l11l1111_opy_:
            return args[2].tags if hasattr(args[2], bstack111ll_opy_ (u"ࠬࡺࡡࡨࡵࠪᚩ")) else []
        if hasattr(args[0], bstack111ll_opy_ (u"࠭࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠫᚪ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack111ll_opy_ (u"ࠧࡵࡣࡪࡷࠬᚫ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack11lllll11l1_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)