# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1llll1ll1l_opy_ import (
    bstack111ll1lll1_opy_,
    bstack11lllll11l_opy_,
    bstack1l1lll1111_opy_,
    bstack1ll11llllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll1lllll_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111l1111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1ll1l11ll_opy_ import bstack1l1lllllll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1lll111_opy_ import bstack1l1ll111111_opy_
from browserstack_sdk.sdk_cli.bstack1l1lll11lll_opy_ import bstack1l1ll1ll11l_opy_
from browserstack_sdk.sdk_cli.bstack11l1l1ll1_opy_ import bstack1l1l11ll1l_opy_
from bstack_utils.helper import bstack1l11ll1111l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll1lll1lll_opy_(bstack1l1lllllll1_opy_):
    bstack1l11l1ll111_opy_ = False
    bstack1l11ll11111_opy_ = bstack11lll1_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᐾ")
    bstack1l1l111l11l_opy_ = bstack11lll1_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧ࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᐿ")
    bstack1l11l1lllll_opy_ = bstack11lll1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠤᑀ")
    bstack1l1l11l11ll_opy_ = bstack11lll1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯ࡳࡠࡵࡦࡥࡳࡴࡩ࡯ࡩࠥᑁ")
    bstack1l11llll111_opy_ = bstack11lll1_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡨࡢࡵࡢࡹࡷࡲࠢᑂ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1ll1l1l11l1_opy_ = threading.Event()
    _1ll1l1l11l1_opy_.set()
    def __init__(self, bstack1l1llll1lll_opy_, bstack1l1l1l1l11l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l111l111_opy_ = False
        self.bstack1l11ll1ll1l_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l11ll111ll_opy_ = False
        self.bstack1l11ll111l1_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l1l1111111_opy_ = bstack1l1l1l1l11l_opy_
        bstack1l1llll1lll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_, bstack11lllll11l_opy_.PRE), self.bstack1ll1lll11l1_opy_)
        bstack1l1llll1lll_opy_.bstack1l1l111lll1_opy_((bstack111ll1lll1_opy_.bstack1l1111ll11_opy_, bstack11lllll11l_opy_.PRE), self.bstack1l11l1l1lll_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l111111l_opy_)
        TestFramework.bstack1l1l111lll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l11l1111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l111111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l11lllll1l_opy_(instance, args)
        test_framework = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll111l_opy_)
        if self.bstack1l1l111l111_opy_:
            self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᑃ")] = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
        if bstack11lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᑄ") in instance.bstack1l11ll1l11l_opy_:
            platform_index = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11lll1ll1_opy_)
            self.accessibility = self.bstack1l11lll1l11_opy_(tags, self.config[bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᑅ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11ll1llll_opy_)
            self._current_test_uuid = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
            self.save_result_done = False
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡸ࡯ࡣࡱࡷ࠱ࡵࡽࠠࡵࡣࡪࡷ࠲ࡵ࡮࡭ࡻࠣࡧ࡭࡫ࡣ࡬࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࠦᑆ") + str(self.accessibility) + bstack11lll1_opy_ (u"ࠦࠧᑇ"))
        else:
            capabilities = self.bstack1l1l1111111_opy_.bstack1l11llll1ll_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑈ") + str(kwargs) + bstack11lll1_opy_ (u"ࠨࠢᑉ"))
                return
            self.accessibility = self.bstack1l11lll1l11_opy_(tags, capabilities)
        if self.bstack1l1l1111111_opy_.pages and self.bstack1l1l1111111_opy_.pages.values():
            bstack1l1l11l1l1l_opy_ = list(self.bstack1l1l1111111_opy_.pages.values())
            if bstack1l1l11l1l1l_opy_ and isinstance(bstack1l1l11l1l1l_opy_[0], (list, tuple)) and bstack1l1l11l1l1l_opy_[0]:
                bstack1l11l1ll11l_opy_ = bstack1l1l11l1l1l_opy_[0][0]
                if callable(bstack1l11l1ll11l_opy_):
                    page = bstack1l11l1ll11l_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack11lll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᑊ"))
                    def bstack1l1l1111l11_opy_():
                        self.get_accessibility_results_summary(page, bstack11lll1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᑋ"))
                    setattr(page, bstack11lll1_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᑌ"), get_results)
                    setattr(page, bstack11lll1_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᑍ"), bstack1l1l1111l11_opy_)
        self.logger.debug(bstack11lll1_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᑎ") + str(self.accessibility) + bstack11lll1_opy_ (u"ࠧࠨᑏ"))
    def bstack1l11l1l1lll_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack11lll1_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡣࡷࠤࡈࡘࡅࡂࡖࡈ࠲ࡕࡘࡅࠡࡣࡩࡸࡪࡸࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡮ࡴࠠࡓࡱࡥࡳࡹ࠳ࡐࡘࠢࡩࡰࡴࡽ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩ࡫࡯࡮ࡦࡵࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡦ࡬ࡪࡩ࡫࠯ࠤࠥࠦᑐ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l1l1111111_opy_.bstack1l11llll1ll_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡨࡷ࡯ࡶࡦࡴࡢࡧࡷ࡫ࡡࡵࡧ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠤᑑ"))
            return
        bstack1l11lll11ll_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1l11lll11ll_opy_
        self.logger.debug(bstack11lll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡩࡸࡩࡷࡧࡵࡣࡨࡸࡥࡢࡶࡨ࠾ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡿ࠯ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡁࠧᑒ") + str(self.accessibility) + bstack11lll1_opy_ (u"ࠤࠥᑓ"))
    def bstack1ll1lll11l1_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l11lll11l1_opy_(method_name, *args):
                bstack111ll1l1_opy_ = datetime.now()
                self.bstack1l11l1ll1ll_opy_(f, exec, *args, **kwargs)
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᑔ"), datetime.now() - bstack111ll1l1_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࡲ࡮ࡴࡧࠣᑕ"))
                return
            bstack111ll1l1_opy_ = datetime.now()
            self.bstack1l11l1ll1ll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᑖ"), datetime.now() - bstack111ll1l1_opy_)
            bstack1ll11l11ll1_opy_ = instance.data.get(bstack11lll1_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᑗ"), None)
            if (
                not f.bstack1l11ll1ll11_opy_(method_name)
                or f.bstack1l11ll1l111_opy_(method_name, *args)
                or f.bstack1l11ll11l1l_opy_(method_name, *args)
                or (bstack1ll11l11ll1_opy_ and int(bstack1ll11l11ll1_opy_)>1)
            ):
                return
            if not f.bstack1ll1l1l1111_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l11l1lllll_opy_, False):
                if not bstack1ll1lll1lll_opy_.bstack1l11l1ll111_opy_:
                    self.logger.warning(bstack11lll1_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᑘ") + str(f.platform_index) + bstack11lll1_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᑙ"))
                    bstack1ll1lll1lll_opy_.bstack1l11l1ll111_opy_ = True
                return
            bstack1l11lll1lll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l11lll1lll_opy_:
                platform_index = f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_, 0)
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᑚ") + str(f.framework_name) + bstack11lll1_opy_ (u"ࠥࠦᑛ"))
                return
            command_name = f.bstack1l11l1lll11_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᑜ") + str(method_name) + bstack11lll1_opy_ (u"ࠧࠨᑝ"))
                return
            if f.framework_name != bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᑞ"):
                bstack1l1l111l1l1_opy_ = f.bstack1ll1l1l1111_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l11llll111_opy_, False)
                if command_name == bstack11lll1_opy_ (u"ࠢࡨࡧࡷࠦᑟ") and not bstack1l1l111l1l1_opy_:
                    f.bstack1ll1ll1l1l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l11llll111_opy_, True)
                    bstack1l1l111l1l1_opy_ = True
                if not bstack1l1l111l1l1_opy_ and not self.bstack1l1l111l111_opy_:
                    self.logger.debug(bstack11lll1_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᑠ") + str(command_name) + bstack11lll1_opy_ (u"ࠤࠥᑡ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11lll1_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᑢ") + str(command_name) + bstack11lll1_opy_ (u"ࠦࠧᑣ"))
                return
            self.logger.info(bstack11lll1_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᑤ") + str(command_name) + bstack11lll1_opy_ (u"ࠨࠢᑥ"))
            scripts = [(s, bstack1l11lll1lll_opy_[s]) for s in scripts_to_run if s in bstack1l11lll1lll_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack111ll1l1_opy_ = datetime.now()
                    if script_name == bstack11lll1_opy_ (u"ࠢࡴࡥࡤࡲࠧᑦ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack11lll1_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤᑧ"): {
                                    bstack11lll1_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥᑨ"): bstack11lll1_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡆࡅࡓࠨᑩ"),
                                    bstack11lll1_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠣᑪ"): [
                                        {
                                            bstack11lll1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᑫ"): command_name
                                        }
                                    ]
                                },
                                bstack11lll1_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᑬ"): {
                                    bstack11lll1_opy_ (u"ࠢࡣࡱࡧࡽࠧᑭ"): {
                                        bstack11lll1_opy_ (u"ࠣ࡯ࡶ࡫ࠧᑮ"): result.get(bstack11lll1_opy_ (u"ࠤࡰࡷ࡬ࠨᑯ"), bstack11lll1_opy_ (u"ࠥࠦᑰ")) if isinstance(result, dict) else bstack11lll1_opy_ (u"ࠦࠧᑱ"),
                                        bstack11lll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᑲ"): result.get(bstack11lll1_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᑳ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack11lll1_opy_ (u"ࠢ࠭ࠤᑴ"), bstack11lll1_opy_ (u"ࠣ࠼ࠥᑵ"))))
                        except Exception as bstack1l1l1l1l1l_opy_:
                            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࠢᑶ") + str(bstack1l1l1l1l1l_opy_) + bstack11lll1_opy_ (u"ࠥࠦᑷ"))
                    instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᑸ") + script_name, datetime.now() - bstack111ll1l1_opy_)
                    if isinstance(result, dict) and not result.get(bstack11lll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᑹ"), True):
                        self.logger.warning(bstack11lll1_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᑺ") + str(result) + bstack11lll1_opy_ (u"ࠢࠣᑻ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11lll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᑼ") + str(e) + bstack11lll1_opy_ (u"ࠤࠥᑽ"))
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᑾ") + str(e) + bstack11lll1_opy_ (u"ࠦࠧᑿ"))
    def bstack1l1l11l1111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1111_opy_,
        bstack1ll1l111111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack11lll1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᒀ") not in instance.bstack1l11ll1l11l_opy_:
            tags = self._1l11lllll1l_opy_(instance, args)
            capabilities = self.bstack1l1l1111111_opy_.bstack1l11llll1ll_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l11lll1l11_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᒁ"))
            return
        driver = self.bstack1l1l1111111_opy_.bstack1l1l11l11l1_opy_(f, instance, bstack1ll1l111111_opy_, *args, **kwargs)
        test_name = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11ll1llll_opy_)
        if not test_name:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᒂ"))
            return
        test_uuid = f.bstack1ll1l1l1111_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
        if not test_uuid:
            self.logger.debug(bstack11lll1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᒃ"))
            return
        if isinstance(self.bstack1l1l1111111_opy_, bstack1l1ll1ll11l_opy_):
            framework_name = bstack11lll1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᒄ")
        else:
            framework_name = bstack11lll1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᒅ")
        if not self.save_result_done:
            self.bstack111lll1l1_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1ll11ll1l_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11lll1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᒆ"))
            return
        bstack111ll1l1_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack11lll1_opy_ (u"ࠧࡹࡣࡢࡰࠥᒇ"), None)
        if not script_code:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᒈ") + str(framework_name) + bstack11lll1_opy_ (u"ࠢࠡࠤᒉ"))
            return
        if self.bstack1l1l111l111_opy_:
            arg = dict()
            arg[bstack11lll1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᒊ")] = method if method else bstack11lll1_opy_ (u"ࠤࠥᒋ")
            arg[bstack11lll1_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥᒌ")] = self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᒍ")]
            arg[bstack11lll1_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥᒎ")] = self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᒏ")]
            arg[bstack11lll1_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᒐ")] = self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨᒑ")]
            arg[bstack11lll1_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨᒒ")] = self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᒓ")]
            arg[bstack11lll1_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦᒔ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l11l1lll1l_opy_ = self.bstack1l1l11ll1ll_opy_(bstack11lll1_opy_ (u"ࠧࡹࡣࡢࡰࠥᒕ"), self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᒖ")])
            if bstack11lll1_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥᒗ") in bstack1l11l1lll1l_opy_:
                bstack1l11l1lll1l_opy_ = bstack1l11l1lll1l_opy_.copy()
                bstack1l11l1lll1l_opy_[bstack11lll1_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧᒘ")] = bstack1l11l1lll1l_opy_.pop(bstack11lll1_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧᒙ"))
            arg = bstack1l11ll1111l_opy_(arg, bstack1l11l1lll1l_opy_)
            bstack1l11ll1l1l1_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l11ll1l1l1_opy_)
            return
        instance = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(driver)
        if instance:
            if not bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l11l11ll_opy_, False):
                bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l11l11ll_opy_, True)
            else:
                self.logger.info(bstack11lll1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᒚ") + str(method) + bstack11lll1_opy_ (u"ࠦࠧᒛ"))
                return
        self.logger.info(bstack11lll1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᒜ") + str(method) + bstack11lll1_opy_ (u"ࠨࠢᒝ"))
        if framework_name == bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᒞ"):
            result = self.bstack1l1l1111111_opy_.bstack1l1l11ll1l1_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack11lll1_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᒟ"): method if method else bstack11lll1_opy_ (u"ࠤࠥᒠ")})
        bstack1llll11l_opy_.end(EVENTS.bstack1ll11ll1l_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᒡ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᒢ"), True, None, command=method)
        if instance:
            bstack1l1lll1111_opy_.bstack1ll1ll1l1l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l1l11l11ll_opy_, False)
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤᒣ"), datetime.now() - bstack111ll1l1_opy_)
        return result
        def bstack1l1l11111ll_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l1111l1l_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l11l111l_opy_ = self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᒤ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11lll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᒥ"), bstack11lll1_opy_ (u"ࠨ࠲ࠪᒦ")))
            req.client_worker_id = bstack11lll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᒧ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1lll11l11_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11lll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᒨ") + str(r) + bstack11lll1_opy_ (u"ࠦࠧᒩ"))
                else:
                    bstack1l11lllll11_opy_ = json.loads(r.bstack1l11ll11ll1_opy_.decode(bstack11lll1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᒪ")))
                    if result_type == bstack11lll1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᒫ"):
                        return bstack1l11lllll11_opy_.get(bstack11lll1_opy_ (u"ࠢࡥࡣࡷࡥࠧᒬ"), [])
                    else:
                        return bstack1l11lllll11_opy_.get(bstack11lll1_opy_ (u"ࠣࡦࡤࡸࡦࠨᒭ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11lll1_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡵࡶ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡩ࡬ࡪ࠼ࠣࠦᒮ") + str(e) + bstack11lll1_opy_ (u"ࠥࠦᒯ"))
    @measure(event_name=EVENTS.bstack11l1l1l1l1_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l1l111l111_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l1l11111ll_opy_(driver, framework_name, bstack11lll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᒰ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack11lll1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᒱ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack11lll1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᒲ"), framework_name=framework_name)
            bstack111ll1l1_opy_ = datetime.now()
            if framework_name == bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᒳ"):
                result = self.bstack1l1l1111111_opy_.bstack1l1l11ll1l1_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(driver)
            if instance:
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᒴ"), datetime.now() - bstack111ll1l1_opy_)
            return result
        finally:
            bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.set()
    @measure(event_name=EVENTS.bstack1l1lll1l1l_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᒵ"))
                return
            if self.bstack1l1l111l111_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l1l11111ll_opy_(driver, framework_name, bstack11lll1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᒶ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack11lll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᒷ"), None)
            if not script_code:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᒸ") + str(framework_name) + bstack11lll1_opy_ (u"ࠨࠢᒹ"))
                return
            self.perform_scan(driver, method=bstack11lll1_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᒺ"), framework_name=framework_name)
            bstack111ll1l1_opy_ = datetime.now()
            if framework_name == bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᒻ"):
                result = self.bstack1l1l1111111_opy_.bstack1l1l11ll1l1_opy_(driver, script_code)
                bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(driver)
            if instance:
                instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᒼ"), datetime.now() - bstack111ll1l1_opy_)
            return result
        finally:
            bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.set()
    @measure(event_name=EVENTS.bstack1l11l1llll1_opy_, stage=STAGE.bstack1lllllll11_opy_)
    def bstack1l11lll1l1l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l1111l1l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11lll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒽ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1lll11l11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᒾ") + str(r) + bstack11lll1_opy_ (u"ࠧࠨᒿ"))
            else:
                self.bstack1l11llll1l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᓀ") + str(e) + bstack11lll1_opy_ (u"ࠢࠣᓁ"))
            traceback.print_exc()
            raise e
    def bstack1l11llll1l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11lll1_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᓂ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l111l111_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᓃ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l11ll1ll1l_opy_[bstack11lll1_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᓄ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l11ll1ll1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l11ll1l1ll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l11ll1l1ll_opy_:
                        bstack1l11ll1l1ll_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l11ll1l1ll_opy_[command.method]:
                        bstack1l11ll1l1ll_opy_[command.method][command.name] = list()
                    bstack1l11ll1l1ll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l11ll1l1ll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l11l1ll1ll_opy_(
        self,
        f: bstack1ll111l11ll_opy_,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l1111111_opy_, bstack1l1ll1ll11l_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack11lll1_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᓅ"):
                    return
        if f.bstack1ll1l1l1111_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l11l1lllll_opy_, False) == True:
            return
        bstack1l11ll1lll1_opy_ = False
        desired_capabilities = f.bstack1l1l1111lll_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack1l1l111ll11_opy_(instance)
            platform_index = f.bstack1ll1l1l1111_opy_(instance, bstack1ll111l11ll_opy_.bstack1l11lll1ll1_opy_, 0)
            bstack1l11ll11l11_opy_ = datetime.now()
            r = self.bstack1l11lll1l1l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack11l111ll1l_opy_(bstack11lll1_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᓆ"), datetime.now() - bstack1l11ll11l11_opy_)
            bstack1l11ll1lll1_opy_ = r.success
            f.bstack1ll1ll1l1l_opy_(instance, bstack1ll1lll1lll_opy_.bstack1l11l1lllll_opy_, bstack1l11ll1lll1_opy_)
        else:
            self.logger.debug(bstack11lll1_opy_ (u"ࠨࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡺ࡭ࡱࡲࠠࡳࡧࡷࡶࡾࠦ࡯࡯ࠢࡱࡩࡽࡺࠠ࡬ࡧࡼࡻࡴࡸࡤࠣᓇ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l11lll1l1l_opy_ = self.config.get(bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᓈ"))
        if not bstack1l11lll1l1l_opy_:
            return True
        try:
            include_tags = bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᓉ")] if bstack11lll1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᓊ") in bstack1l11lll1l1l_opy_ and isinstance(bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᓋ")], list) else []
            exclude_tags = bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᓌ")] if bstack11lll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᓍ") in bstack1l11lll1l1l_opy_ and isinstance(bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᓎ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᓏ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l1l111l111_opy_:
                bstack1l1l111l1ll_opy_ = caps.get(bstack11lll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᓐ"))
                if bstack1l1l111l1ll_opy_ is not None and str(bstack1l1l111l1ll_opy_).lower() == bstack11lll1_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᓑ"):
                    bstack1l1l111ll1l_opy_ = caps.get(bstack11lll1_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᓒ")) or caps.get(bstack11lll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᓓ"))
                    if bstack1l1l111ll1l_opy_ is not None and int(bstack1l1l111ll1l_opy_) < 11:
                        self.logger.warning(bstack11lll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠧᓔ") + str(bstack1l1l111ll1l_opy_) + bstack11lll1_opy_ (u"ࠨࠢᓕ"))
                        return False
                return True
            bstack1l1l111llll_opy_ = caps.get(bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓖ"), {}).get(bstack11lll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᓗ"), caps.get(bstack11lll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᓘ"), bstack11lll1_opy_ (u"ࠪࠫᓙ")))
            if bstack1l1l111llll_opy_:
                self.logger.warning(bstack11lll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᓚ"))
                return False
            browser = caps.get(bstack11lll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᓛ"), bstack11lll1_opy_ (u"࠭ࠧᓜ")).lower()
            if browser != bstack11lll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᓝ"):
                self.logger.warning(bstack11lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᓞ"))
                return False
            bstack1l11llllll1_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᓟ")) or self.config.get(bstack11lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᓠ")):
                bstack1l11llllll1_opy_ = bstack1l1l11l1lll_opy_
            browser_version = caps.get(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᓡ"))
            if not browser_version:
                browser_version = caps.get(bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᓢ"), {}).get(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᓣ"), bstack11lll1_opy_ (u"ࠧࠨᓤ"))
            bstack1l1l1111ll1_opy_ = str(browser_version).lower() if browser_version is not None else bstack11lll1_opy_ (u"ࠨࠩᓥ")
            if bstack1l1l1111ll1_opy_:
                if bstack1l1l1111ll1_opy_.startswith(bstack11lll1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᓦ")):
                    if bstack1l1l1111ll1_opy_.startswith(bstack11lll1_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᓧ")):
                        bstack1l1l11ll111_opy_ = bstack1l1l1111ll1_opy_[len(bstack11lll1_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬᓨ")):]
                        if bstack1l1l11ll111_opy_ and not bstack1l1l11ll111_opy_.isdigit():
                            self.logger.warning(bstack11lll1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡨࡲࡶࡲࡧࡴࠡࠩࠥᓩ") + str(browser_version) + bstack11lll1_opy_ (u"ࠨࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࠬࡲࡡࡵࡧࡶࡸࠬࠦ࡯ࡳࠢࠪࡰࡦࡺࡥࡴࡶ࠰ࡀࡳࡻ࡭ࡣࡧࡵࡂࠬ࠴ࠢᓪ"))
                            return False
                else:
                    try:
                        if int(bstack1l1l1111ll1_opy_.split(bstack11lll1_opy_ (u"ࠧ࠯ࠩᓫ"))[0]) <= bstack1l11llllll1_opy_:
                            self.logger.warning(bstack11lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥᓬ") + str(bstack1l11llllll1_opy_) + bstack11lll1_opy_ (u"ࠤ࠱ࠦᓭ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11lll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠨࡽࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࢁࠬࡀࠠࠣᓮ") + str(e) + bstack11lll1_opy_ (u"ࠦࠧᓯ"))
            bstack1l11ll11lll_opy_ = caps.get(bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᓰ"), {}).get(bstack11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᓱ"))
            if not bstack1l11ll11lll_opy_:
                bstack1l11ll11lll_opy_ = caps.get(bstack11lll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᓲ"), {})
            if not bstack1l11ll11lll_opy_:
                bstack1l11ll11lll_opy_ = caps.get(bstack11lll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᓳ"), {})
            if bstack1l11ll11lll_opy_ and any(arg == bstack11lll1_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᓴ") or (arg.startswith(bstack11lll1_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽ࠨᓵ")) and arg != bstack11lll1_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࡰࡨࡻࠬᓶ"))
                                     for arg in bstack1l11ll11lll_opy_.get(bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡵࠪᓷ"), [])):
                self.logger.warning(bstack11lll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᓸ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᓹ") + str(error))
            return False
    def bstack1l11lll1111_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1l11l1ll1_opy_ = {
            bstack11lll1_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᓺ"): test_uuid,
        }
        bstack1l1l11l1l11_opy_ = {}
        if result.success:
            bstack1l1l11l1l11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l11ll1111l_opy_(bstack1l1l11l1ll1_opy_, bstack1l1l11l1l11_opy_)
    def bstack1l1l11ll1ll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11lll1_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡦࡶࡦ࡬ࠥࡩࡥ࡯ࡶࡵࡥࡱࠦࡡࡶࡶ࡫ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡸࡩࡲࡪࡲࡷࠤࡳࡧ࡭ࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡩࡡࡤࡪࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯ࡦࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡩࡩࡹࡩࡨࡦࡦ࠯ࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠠ࡭ࡱࡤࡨࡸࠦࡡ࡯ࡦࠣࡧࡦࡩࡨࡦࡵࠣ࡭ࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧ࠽ࠤࡓࡧ࡭ࡦࠢࡲࡪࠥࡺࡨࡦࠢࡶࡧࡷ࡯ࡰࡵࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡲࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠼࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠱ࠦࡥ࡮ࡲࡷࡽࠥࡪࡩࡤࡶࠣ࡭࡫ࠦࡥࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᓻ")
        try:
            if self.bstack1l11ll111ll_opy_:
                return self.bstack1l11ll111l1_opy_
            self.bstack1l1l1111l1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11lll1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᓼ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᓽ"), bstack11lll1_opy_ (u"ࠬ࠶ࠧᓾ")))
            req.client_worker_id = bstack11lll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᓿ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1lll11l11_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l11ll111l1_opy_ = self.bstack1l11lll1111_opy_(test_uuid, r)
                self.bstack1l11ll111ll_opy_ = True
            else:
                self.logger.error(bstack11lll1_opy_ (u"ࠢࡧࡧࡷࡧ࡭ࡉࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡄ࠵࠶ࡿࡃࡰࡰࡩ࡭࡬ࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡴࡸࠠࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃ࠺ࠡࠤᔀ") + str(r.error) + bstack11lll1_opy_ (u"ࠣࠤᔁ"))
                self.bstack1l11ll111l1_opy_ = dict()
            return self.bstack1l11ll111l1_opy_
        except Exception as e:
            self.logger.error(bstack11lll1_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦᔂ") + str(traceback.format_exc()) + bstack11lll1_opy_ (u"ࠥࠦᔃ"))
            return dict()
    def bstack111lll1l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack11lllll1_opy_ = None
        bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.clear()
        try:
            self.bstack1l1l1111l1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11lll1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᔄ")
            req.script_name = bstack11lll1_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᔅ")
            req.platform_index = str(os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᔆ"), bstack11lll1_opy_ (u"ࠧ࠱ࠩᔇ")))
            req.client_worker_id = bstack11lll1_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᔈ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1lll11l11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11lll1_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᔉ") + str(r.error) + bstack11lll1_opy_ (u"ࠥࠦᔊ"))
            else:
                bstack1l1l11l1ll1_opy_ = self.bstack1l11lll1111_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack11lll1_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᔋ") + str(bstack1l1l11l1ll1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᔌ") + str(framework_name) + bstack11lll1_opy_ (u"ࠨࠠࠣᔍ"))
                return
            bstack11lllll1_opy_ = bstack1llll11l_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1l1l11111l1_opy_.value)
            self.bstack1l1l11ll11l_opy_(driver, script_code, bstack1l1l11l1ll1_opy_, framework_name)
            try:
                bstack1l11l1ll1l1_opy_ = {
                    bstack11lll1_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᔎ"): {
                        bstack11lll1_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᔏ"): bstack11lll1_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᔐ"),
                    },
                    bstack11lll1_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᔑ"): {
                        bstack11lll1_opy_ (u"ࠦࡧࡵࡤࡺࠤᔒ"): {
                            bstack11lll1_opy_ (u"ࠧࡳࡳࡨࠤᔓ"): bstack11lll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᔔ"),
                            bstack11lll1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᔕ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l11l1ll1l1_opy_, separators=(bstack11lll1_opy_ (u"ࠨ࠮ࠪᔖ"), bstack11lll1_opy_ (u"ࠩ࠽ࠫᔗ"))))
            except Exception as bstack1l1l1l1l1l_opy_:
                self.logger.debug(bstack11lll1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᔘ") + str(bstack1l1l1l1l1l_opy_) + bstack11lll1_opy_ (u"ࠦࠧᔙ"))
            self.logger.info(bstack11lll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᔚ"))
            bstack1llll11l_opy_.end(EVENTS.bstack1l1l11111l1_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᔛ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᔜ"), True, None, command=bstack11lll1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᔝ"),test_name=name)
        except Exception as bstack1l11lllllll_opy_:
            self.logger.error(bstack11lll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᔞ") + bstack11lll1_opy_ (u"ࠥࡷࡹࡸࠨࡱࡣࡷ࡬࠮ࠨᔟ") + bstack11lll1_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᔠ") + str(bstack1l11lllllll_opy_))
            bstack1llll11l_opy_.end(EVENTS.bstack1l1l11111l1_opy_.value, bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔡ"), bstack11lllll1_opy_+bstack11lll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔢ"), False, bstack1l11lllllll_opy_, command=bstack11lll1_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᔣ"),test_name=name)
        finally:
            bstack1ll1lll1lll_opy_._1ll1l1l11l1_opy_.set()
    def bstack1ll1lll11ll_opy_(self):
        bstack11lll1_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡪࡷࡵ࡭ࠡࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡷࡩࡧࡱࠤࡦࠦࡣ࡭ࡱࡶࡩࠥࡱࡥࡺࡹࡲࡶࡩࠦࡩࡴࠢࡤࡦࡴࡻࡴࠡࡶࡲࠤࡪࡾࡥࡤࡷࡷࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᔤ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack11lll1_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡤࡣࡳࡸࡺࡸࡥࡠࡤࡨࡪࡴࡸࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥ࠻ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦᔥ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack11lll1_opy_ (u"ࠥࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࡡࡥࡩ࡫ࡵࡲࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠠࡰࡴࠣࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠤᔦ"))
            return
        self.logger.debug(bstack11lll1_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡦࡥࡵࡺࡵࡳࡧࡢࡦࡪ࡬࡯ࡳࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧ࠽ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡴࡰࡲࡢࡸࡪࡹࡴࡠࡥࡤࡴࡹࡻࡲࡦࠤᔧ"))
        self.bstack111lll1l1_opy_(None, self._current_test_name, bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᔨ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack1l1l11ll11l_opy_(self, driver, script_code, bstack1l1l11l1ll1_opy_, framework_name):
        if framework_name == bstack11lll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᔩ"):
            self.bstack1l1l1111111_opy_.bstack1l1l11ll1l1_opy_(driver, script_code, bstack1l1l11l1ll1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l1l11l1ll1_opy_))
    def _1l11lllll1l_opy_(self, instance: bstack1ll111l1111_opy_, args: Tuple) -> list:
        bstack11lll1_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᔪ")
        if bstack11lll1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᔫ") in instance.bstack1l11ll1l11l_opy_:
            return args[2].tags if hasattr(args[2], bstack11lll1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᔬ")) else []
        if hasattr(args[0], bstack11lll1_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨᔭ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack11lll1_opy_ (u"ࠫࡹࡧࡧࡴࠩᔮ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l11lll1l11_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)