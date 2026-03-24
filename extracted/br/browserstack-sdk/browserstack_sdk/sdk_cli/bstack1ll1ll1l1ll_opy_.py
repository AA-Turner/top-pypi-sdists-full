# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1ll11ll1_opy_ import (
    bstack111l11ll_opy_,
    bstack1lll1ll11_opy_,
    bstack111lll11l_opy_,
    bstack1ll11l1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1l1llll1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111lllll_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1l1llll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll111lll_opy_ import bstack1l1ll1ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1111_opy_ import bstack1l1ll111l11_opy_
from browserstack_sdk.sdk_cli.bstack11llll11l1_opy_ import bstack11ll1l1l_opy_
from bstack_utils.helper import bstack1l11lll1lll_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll1ll11ll1_opy_(bstack1l1llll1l11_opy_):
    bstack1l1l1111lll_opy_ = False
    bstack1l11lllllll_opy_ = bstack1ll1lll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᐾ")
    bstack1l1l11l111l_opy_ = bstack1ll1lll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧ࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᐿ")
    bstack1l11l1ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠤᑀ")
    bstack1l1l11ll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯ࡳࡠࡵࡦࡥࡳࡴࡩ࡯ࡩࠥᑁ")
    bstack1l11lllll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡨࡢࡵࡢࡹࡷࡲࠢᑂ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1ll1l11ll11_opy_ = threading.Event()
    _1ll1l11ll11_opy_.set()
    def __init__(self, bstack1l1llllll11_opy_, bstack1l1lllll1ll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1111ll1_opy_ = False
        self.bstack1l11ll111l1_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l11ll11111_opy_ = False
        self.bstack1l11l1l1lll_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l1l11ll11l_opy_ = bstack1l1lllll1ll_opy_
        bstack1l1llllll11_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack1ll1ll111l1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack1ll1ll1111l_opy_)
        bstack1l1llllll11_opy_.bstack1l11l1lllll_opy_((bstack111l11ll_opy_.bstack11ll1lll1_opy_, bstack1lll1ll11_opy_.PRE), self.bstack1l1l111ll11_opy_)
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11ll1lll1_opy_)
        TestFramework.bstack1l11l1lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll1l1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11ll1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l11llll1ll_opy_(instance, args)
        test_framework = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11lll111l_opy_)
        if self.bstack1l1l1111ll1_opy_:
            self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᑃ")] = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
        if bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᑄ") in instance.bstack1l11ll1l1ll_opy_:
            platform_index = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l11llll111_opy_)
            self.accessibility = self.bstack1l1l111l111_opy_(tags, self.config[bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᑅ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l111111l_opy_)
            self._current_test_uuid = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
            self.save_result_done = False
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡸ࡯ࡣࡱࡷ࠱ࡵࡽࠠࡵࡣࡪࡷ࠲ࡵ࡮࡭ࡻࠣࡧ࡭࡫ࡣ࡬࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࠦᑆ") + str(self.accessibility) + bstack1ll1lll_opy_ (u"ࠦࠧᑇ"))
        else:
            capabilities = self.bstack1l1l11ll11l_opy_.bstack1l11lll1111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᑈ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠨࠢᑉ"))
                return
            self.accessibility = self.bstack1l1l111l111_opy_(tags, capabilities)
        if self.bstack1l1l11ll11l_opy_.pages and self.bstack1l1l11ll11l_opy_.pages.values():
            bstack1l11ll1llll_opy_ = list(self.bstack1l1l11ll11l_opy_.pages.values())
            if bstack1l11ll1llll_opy_ and isinstance(bstack1l11ll1llll_opy_[0], (list, tuple)) and bstack1l11ll1llll_opy_[0]:
                bstack1l11llll1l1_opy_ = bstack1l11ll1llll_opy_[0][0]
                if callable(bstack1l11llll1l1_opy_):
                    page = bstack1l11llll1l1_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᑊ"))
                    def bstack1l11ll1l11l_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᑋ"))
                    setattr(page, bstack1ll1lll_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᑌ"), get_results)
                    setattr(page, bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᑍ"), bstack1l11ll1l11l_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᑎ") + str(self.accessibility) + bstack1ll1lll_opy_ (u"ࠧࠨᑏ"))
    def bstack1l1l111ll11_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡣࡷࠤࡈࡘࡅࡂࡖࡈ࠲ࡕࡘࡅࠡࡣࡩࡸࡪࡸࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡮ࡴࠠࡓࡱࡥࡳࡹ࠳ࡐࡘࠢࡩࡰࡴࡽ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩ࡫࡯࡮ࡦࡵࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡦ࡬ࡪࡩ࡫࠯ࠤࠥࠦᑐ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l1l11ll11l_opy_.bstack1l11lll1111_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡨࡷ࡯ࡶࡦࡴࡢࡧࡷ࡫ࡡࡵࡧ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠤᑑ"))
            return
        bstack1l1l11l1l1l_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1l1l11l1l1l_opy_
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡩࡸࡩࡷࡧࡵࡣࡨࡸࡥࡢࡶࡨ࠾ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡿ࠯ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡁࠧᑒ") + str(self.accessibility) + bstack1ll1lll_opy_ (u"ࠤࠥᑓ"))
    def bstack1ll1ll1111l_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        bstack1ll11l1ll11_opy_: Tuple[bstack111l11ll_opy_, bstack1lll1ll11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l1l111l11l_opy_(method_name, *args):
                bstack1ll1l111l_opy_ = datetime.now()
                self.bstack1l11l1llll1_opy_(f, exec, *args, **kwargs)
                instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᑔ"), datetime.now() - bstack1ll1l111l_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࡲ࡮ࡴࡧࠣᑕ"))
                return
            bstack1ll1l111l_opy_ = datetime.now()
            self.bstack1l11l1llll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᑖ"), datetime.now() - bstack1ll1l111l_opy_)
            bstack1ll11l1llll_opy_ = instance.data.get(bstack1ll1lll_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᑗ"), None)
            if (
                not f.bstack1l1l111l1ll_opy_(method_name)
                or f.bstack1l1l111l1l1_opy_(method_name, *args)
                or f.bstack1l11ll1111l_opy_(method_name, *args)
                or (bstack1ll11l1llll_opy_ and int(bstack1ll11l1llll_opy_)>1)
            ):
                return
            if not f.bstack1ll1lll11ll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11l1ll1l1_opy_, False):
                if not bstack1ll1ll11ll1_opy_.bstack1l1l1111lll_opy_:
                    self.logger.warning(bstack1ll1lll_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᑘ") + str(f.platform_index) + bstack1ll1lll_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᑙ"))
                    bstack1ll1ll11ll1_opy_.bstack1l1l1111lll_opy_ = True
                return
            bstack1l1l11111ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l11111ll_opy_:
                platform_index = f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_, 0)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᑚ") + str(f.framework_name) + bstack1ll1lll_opy_ (u"ࠥࠦᑛ"))
                return
            command_name = f.bstack1l1l1111l1l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᑜ") + str(method_name) + bstack1ll1lll_opy_ (u"ࠧࠨᑝ"))
                return
            if f.framework_name != bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᑞ"):
                bstack1l11lll11ll_opy_ = f.bstack1ll1lll11ll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11lllll1l_opy_, False)
                if command_name == bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࠦᑟ") and not bstack1l11lll11ll_opy_:
                    f.bstack1l1l11lll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11lllll1l_opy_, True)
                    bstack1l11lll11ll_opy_ = True
                if not bstack1l11lll11ll_opy_ and not self.bstack1l1l1111ll1_opy_:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᑠ") + str(command_name) + bstack1ll1lll_opy_ (u"ࠤࠥᑡ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᑢ") + str(command_name) + bstack1ll1lll_opy_ (u"ࠦࠧᑣ"))
                return
            self.logger.info(bstack1ll1lll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᑤ") + str(command_name) + bstack1ll1lll_opy_ (u"ࠨࠢᑥ"))
            scripts = [(s, bstack1l1l11111ll_opy_[s]) for s in scripts_to_run if s in bstack1l1l11111ll_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack1ll1l111l_opy_ = datetime.now()
                    if script_name == bstack1ll1lll_opy_ (u"ࠢࡴࡥࡤࡲࠧᑦ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack1ll1lll_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤᑧ"): {
                                    bstack1ll1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥᑨ"): bstack1ll1lll_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡆࡅࡓࠨᑩ"),
                                    bstack1ll1lll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠣᑪ"): [
                                        {
                                            bstack1ll1lll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᑫ"): command_name
                                        }
                                    ]
                                },
                                bstack1ll1lll_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᑬ"): {
                                    bstack1ll1lll_opy_ (u"ࠢࡣࡱࡧࡽࠧᑭ"): {
                                        bstack1ll1lll_opy_ (u"ࠣ࡯ࡶ࡫ࠧᑮ"): result.get(bstack1ll1lll_opy_ (u"ࠤࡰࡷ࡬ࠨᑯ"), bstack1ll1lll_opy_ (u"ࠥࠦᑰ")) if isinstance(result, dict) else bstack1ll1lll_opy_ (u"ࠦࠧᑱ"),
                                        bstack1ll1lll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᑲ"): result.get(bstack1ll1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᑳ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack1ll1lll_opy_ (u"ࠢ࠭ࠤᑴ"), bstack1ll1lll_opy_ (u"ࠣ࠼ࠥᑵ"))))
                        except Exception as bstack1l1l1ll1l1_opy_:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࠢᑶ") + str(bstack1l1l1ll1l1_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦᑷ"))
                    instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᑸ") + script_name, datetime.now() - bstack1ll1l111l_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll1lll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᑹ"), True):
                        self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᑺ") + str(result) + bstack1ll1lll_opy_ (u"ࠢࠣᑻ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᑼ") + str(e) + bstack1ll1lll_opy_ (u"ࠤࠥᑽ"))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᑾ") + str(e) + bstack1ll1lll_opy_ (u"ࠦࠧᑿ"))
    def bstack1l11lll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll11l1ll11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᒀ") not in instance.bstack1l11ll1l1ll_opy_:
            tags = self._1l11llll1ll_opy_(instance, args)
            capabilities = self.bstack1l1l11ll11l_opy_.bstack1l11lll1111_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l1l111l111_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᒁ"))
            return
        driver = self.bstack1l1l11ll11l_opy_.bstack1l1l11l1l11_opy_(f, instance, bstack1ll11l1ll11_opy_, *args, **kwargs)
        test_name = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l111111l_opy_)
        if not test_name:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᒂ"))
            return
        test_uuid = f.bstack1ll1lll11ll_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᒃ"))
            return
        if isinstance(self.bstack1l1l11ll11l_opy_, bstack1l1ll111l11_opy_):
            framework_name = bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᒄ")
        else:
            framework_name = bstack1ll1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᒅ")
        if not self.save_result_done:
            self.bstack1ll1ll11ll_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack11llll1l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᒆ"))
            return
        bstack1ll1l111l_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack1ll1lll_opy_ (u"ࠧࡹࡣࡢࡰࠥᒇ"), None)
        if not script_code:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᒈ") + str(framework_name) + bstack1ll1lll_opy_ (u"ࠢࠡࠤᒉ"))
            return
        if self.bstack1l1l1111ll1_opy_:
            arg = dict()
            arg[bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᒊ")] = method if method else bstack1ll1lll_opy_ (u"ࠤࠥᒋ")
            arg[bstack1ll1lll_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥᒌ")] = self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᒍ")]
            arg[bstack1ll1lll_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥᒎ")] = self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᒏ")]
            arg[bstack1ll1lll_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᒐ")] = self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨᒑ")]
            arg[bstack1ll1lll_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨᒒ")] = self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᒓ")]
            arg[bstack1ll1lll_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦᒔ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l11ll1ll11_opy_ = self.bstack1l11llllll1_opy_(bstack1ll1lll_opy_ (u"ࠧࡹࡣࡢࡰࠥᒕ"), self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᒖ")])
            if bstack1ll1lll_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥᒗ") in bstack1l11ll1ll11_opy_:
                bstack1l11ll1ll11_opy_ = bstack1l11ll1ll11_opy_.copy()
                bstack1l11ll1ll11_opy_[bstack1ll1lll_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧᒘ")] = bstack1l11ll1ll11_opy_.pop(bstack1ll1lll_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧᒙ"))
            arg = bstack1l11lll1lll_opy_(arg, bstack1l11ll1ll11_opy_)
            bstack1l1l111llll_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l1l111llll_opy_)
            return
        instance = bstack111lll11l_opy_.bstack1ll1l111l1l_opy_(driver)
        if instance:
            if not bstack111lll11l_opy_.bstack1ll1lll11ll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l1l11ll1l1_opy_, False):
                bstack111lll11l_opy_.bstack1l1l11lll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l1l11ll1l1_opy_, True)
            else:
                self.logger.info(bstack1ll1lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᒚ") + str(method) + bstack1ll1lll_opy_ (u"ࠦࠧᒛ"))
                return
        self.logger.info(bstack1ll1lll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᒜ") + str(method) + bstack1ll1lll_opy_ (u"ࠨࠢᒝ"))
        if framework_name == bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᒞ"):
            result = self.bstack1l1l11ll11l_opy_.bstack1l1l11111l1_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᒟ"): method if method else bstack1ll1lll_opy_ (u"ࠤࠥᒠ")})
        bstack1lll1lll11_opy_.end(EVENTS.bstack11llll1l1_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᒡ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᒢ"), True, None, command=method)
        if instance:
            bstack111lll11l_opy_.bstack1l1l11lll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l1l11ll1l1_opy_, False)
            instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤᒣ"), datetime.now() - bstack1ll1l111l_opy_)
        return result
        def bstack1l11l1lll1l_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l11l1ll111_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l11ll11ll1_opy_ = self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᒤ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᒥ"), bstack1ll1lll_opy_ (u"ࠨ࠲ࠪᒦ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᒧ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1ll1l1ll1_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᒨ") + str(r) + bstack1ll1lll_opy_ (u"ࠦࠧᒩ"))
                else:
                    bstack1l1l11l11ll_opy_ = json.loads(r.bstack1l11llll11l_opy_.decode(bstack1ll1lll_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᒪ")))
                    if result_type == bstack1ll1lll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᒫ"):
                        return bstack1l1l11l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠢࡥࡣࡷࡥࠧᒬ"), [])
                    else:
                        return bstack1l1l11l11ll_opy_.get(bstack1ll1lll_opy_ (u"ࠣࡦࡤࡸࡦࠨᒭ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡵࡶ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡩ࡬ࡪ࠼ࠣࠦᒮ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᒯ"))
    @measure(event_name=EVENTS.bstack1l1ll11l1l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l1l1111ll1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l11l1lll1l_opy_(driver, framework_name, bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᒰ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᒱ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᒲ"), framework_name=framework_name)
            bstack1ll1l111l_opy_ = datetime.now()
            if framework_name == bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᒳ"):
                result = self.bstack1l1l11ll11l_opy_.bstack1l1l11111l1_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack111lll11l_opy_.bstack1ll1l111l1l_opy_(driver)
            if instance:
                instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᒴ"), datetime.now() - bstack1ll1l111l_opy_)
            return result
        finally:
            bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.set()
    @measure(event_name=EVENTS.bstack1l1ll1l11l_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᒵ"))
                return
            if self.bstack1l1l1111ll1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l11l1lll1l_opy_(driver, framework_name, bstack1ll1lll_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᒶ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1ll1lll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᒷ"), None)
            if not script_code:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᒸ") + str(framework_name) + bstack1ll1lll_opy_ (u"ࠨࠢᒹ"))
                return
            self.perform_scan(driver, method=bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᒺ"), framework_name=framework_name)
            bstack1ll1l111l_opy_ = datetime.now()
            if framework_name == bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᒻ"):
                result = self.bstack1l1l11ll11l_opy_.bstack1l1l11111l1_opy_(driver, script_code)
                bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack111lll11l_opy_.bstack1ll1l111l1l_opy_(driver)
            if instance:
                instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᒼ"), datetime.now() - bstack1ll1l111l_opy_)
            return result
        finally:
            bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.set()
    @measure(event_name=EVENTS.bstack1l11ll11l11_opy_, stage=STAGE.bstack1ll1llll_opy_)
    def bstack1l1l11l1111_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l11l1ll111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᒽ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1ll1l1ll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᒾ") + str(r) + bstack1ll1lll_opy_ (u"ࠧࠨᒿ"))
            else:
                self.bstack1l1l1111111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᓀ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᓁ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1111111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᓂ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1111ll1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᓃ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l11ll111l1_opy_[bstack1ll1lll_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᓄ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l11ll111l1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l111lll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l1l111lll1_opy_:
                        bstack1l1l111lll1_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l1l111lll1_opy_[command.method]:
                        bstack1l1l111lll1_opy_[command.method][command.name] = list()
                    bstack1l1l111lll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l111lll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l11l1llll1_opy_(
        self,
        f: bstack1l1llll1111_opy_,
        exec: Tuple[bstack1ll11l1l111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l11ll11l_opy_, bstack1l1ll111l11_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack1ll1lll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᓅ"):
                    return
        if f.bstack1ll1lll11ll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11l1ll1l1_opy_, False) == True:
            return
        bstack1l1l11ll1ll_opy_ = False
        desired_capabilities = f.bstack1l11ll11l1l_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack1l11ll111ll_opy_(instance)
            platform_index = f.bstack1ll1lll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l11llll111_opy_, 0)
            bstack1l1l11ll111_opy_ = datetime.now()
            r = self.bstack1l1l11l1111_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1111lll11_opy_(bstack1ll1lll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᓆ"), datetime.now() - bstack1l1l11ll111_opy_)
            bstack1l1l11ll1ll_opy_ = r.success
            f.bstack1l1l11lll_opy_(instance, bstack1ll1ll11ll1_opy_.bstack1l11l1ll1l1_opy_, bstack1l1l11ll1ll_opy_)
        else:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡺ࡭ࡱࡲࠠࡳࡧࡷࡶࡾࠦ࡯࡯ࠢࡱࡩࡽࡺࠠ࡬ࡧࡼࡻࡴࡸࡤࠣᓇ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l1l11l1111_opy_ = self.config.get(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᓈ"))
        if not bstack1l1l11l1111_opy_:
            return True
        try:
            include_tags = bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᓉ")] if bstack1ll1lll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᓊ") in bstack1l1l11l1111_opy_ and isinstance(bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᓋ")], list) else []
            exclude_tags = bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᓌ")] if bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᓍ") in bstack1l1l11l1111_opy_ and isinstance(bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᓎ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᓏ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l1l1111ll1_opy_:
                bstack1l1l111ll1l_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᓐ"))
                if bstack1l1l111ll1l_opy_ is not None and str(bstack1l1l111ll1l_opy_).lower() == bstack1ll1lll_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᓑ"):
                    bstack1l11l1ll11l_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᓒ")) or caps.get(bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᓓ"))
                    if bstack1l11l1ll11l_opy_ is not None and int(bstack1l11l1ll11l_opy_) < 11:
                        self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠥࢁࡽ࠯ࠤᓔ").format(bstack1l11l1ll11l_opy_))
                        return False
                return True
            bstack1l1l11l1lll_opy_ = caps.get(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᓕ"), {}).get(bstack1ll1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᓖ"), caps.get(bstack1ll1lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᓗ"), bstack1ll1lll_opy_ (u"ࠩࠪᓘ")))
            if bstack1l1l11l1lll_opy_:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᓙ"))
                return False
            browser = caps.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᓚ"), bstack1ll1lll_opy_ (u"ࠬ࠭ᓛ")).lower()
            if browser != bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᓜ"):
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᓝ"))
                return False
            bstack1l11lllll11_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᓞ")) or self.config.get(bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᓟ")):
                bstack1l11lllll11_opy_ = bstack1l11lll1ll1_opy_
            browser_version = caps.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᓠ"))
            if not browser_version:
                browser_version = caps.get(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᓡ"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᓢ"), bstack1ll1lll_opy_ (u"࠭ࠧᓣ"))
            bstack1l11lll1l11_opy_ = str(browser_version).lower() if browser_version is not None else bstack1ll1lll_opy_ (u"ࠧࠨᓤ")
            if bstack1l11lll1l11_opy_:
                if bstack1l11lll1l11_opy_.startswith(bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᓥ")):
                    if bstack1l11lll1l11_opy_.startswith(bstack1ll1lll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵ࠯ࠪᓦ")):
                        bstack1l11ll11lll_opy_ = bstack1l11lll1l11_opy_[len(bstack1ll1lll_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᓧ")):]
                        if bstack1l11ll11lll_opy_ and not bstack1l11ll11lll_opy_.isdigit():
                            self.logger.warning(bstack1ll1lll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡧࡱࡵࡱࡦࡺࠠࠨࡽࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࠩ࡯ࡥࡹ࡫ࡳࡵࠩࠣࡳࡷࠦࠧ࡭ࡣࡷࡩࡸࡺ࠭࠽ࡰࡸࡱࡧ࡫ࡲ࠿ࠩ࠱ࠦᓨ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack1l11lll1l11_opy_.split(bstack1ll1lll_opy_ (u"ࠬ࠴ࠧᓩ"))[0]) <= bstack1l11lllll11_opy_:
                            self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼࡿ࠱ࠦᓪ").format(bstack1l11lllll11_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨᓫ").format(browser_version, e))
            bstack1l11l1ll1ll_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᓬ"), {}).get(bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᓭ"))
            if not bstack1l11l1ll1ll_opy_:
                bstack1l11l1ll1ll_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᓮ"), {})
            if not bstack1l11l1ll1ll_opy_:
                bstack1l11l1ll1ll_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᓯ"), {})
            if bstack1l11l1ll1ll_opy_ and any(arg == bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᓰ") or (arg.startswith(bstack1ll1lll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᓱ")) and arg != bstack1ll1lll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᓲ"))
                                     for arg in bstack1l11l1ll1ll_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᓳ"), [])):
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᓴ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᓵ") + str(error))
            return False
    def bstack1l11ll1ll1l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l11l1lll11_opy_ = {
            bstack1ll1lll_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᓶ"): test_uuid,
        }
        bstack1l11lll11l1_opy_ = {}
        if result.success:
            bstack1l11lll11l1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l11lll1lll_opy_(bstack1l11l1lll11_opy_, bstack1l11lll11l1_opy_)
    def bstack1l11llllll1_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡩࡹࡩࡨࠡࡥࡨࡲࡹࡸࡡ࡭ࠢࡤࡹࡹ࡮ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡴࡥࡵ࡭ࡵࡺࠠ࡯ࡣࡰࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡥࡤࡧ࡭࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡬ࡥࡵࡥ࡫ࡩࡩ࠲ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠣࡰࡴࡧࡤࡴࠢࡤࡲࡩࠦࡣࡢࡥ࡫ࡩࡸࠦࡩࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡹࡣࡳ࡫ࡳࡸࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨ࠿ࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠭ࠢࡨࡱࡵࡺࡹࠡࡦ࡬ࡧࡹࠦࡩࡧࠢࡨࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᓷ")
        try:
            if self.bstack1l11ll11111_opy_:
                return self.bstack1l11l1l1lll_opy_
            self.bstack1l11l1ll111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll1lll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᓸ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᓹ"), bstack1ll1lll_opy_ (u"ࠨ࠲ࠪᓺ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᓻ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1ll1l1ll1_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l11l1l1lll_opy_ = self.bstack1l11ll1ll1l_opy_(test_uuid, r)
                self.bstack1l11ll11111_opy_ = True
            else:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠥࡪࡪࡺࡣࡩࡅࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡇ࠱࠲ࡻࡆࡳࡳ࡬ࡩࡨ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡪࡲࡪࡸࡨࡶࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡰࡢࡴࡤࡱࡸࠦࡦࡰࡴࠣࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧᓼ") + str(r.error) + bstack1ll1lll_opy_ (u"ࠦࠧᓽ"))
                self.bstack1l11l1l1lll_opy_ = dict()
            return self.bstack1l11l1l1lll_opy_
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧ࡬ࡥࡵࡥ࡫ࡇࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡂ࠳࠴ࡽࡈࡵ࡮ࡧ࡫ࡪ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡲࡶࠥࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢᓾ") + str(traceback.format_exc()) + bstack1ll1lll_opy_ (u"ࠨࠢᓿ"))
            return dict()
    def bstack1ll1ll11ll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack11ll1ll1l_opy_ = None
        bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.clear()
        try:
            self.bstack1l11l1ll111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll1lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᔀ")
            req.script_name = bstack1ll1lll_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᔁ")
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᔂ"), bstack1ll1lll_opy_ (u"ࠪ࠴ࠬᔃ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᔄ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1ll1l1ll1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᔅ") + str(r.error) + bstack1ll1lll_opy_ (u"ࠨࠢᔆ"))
            else:
                bstack1l11l1lll11_opy_ = self.bstack1l11ll1ll1l_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᔇ") + str(bstack1l11l1lll11_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᔈ") + str(framework_name) + bstack1ll1lll_opy_ (u"ࠤࠣࠦᔉ"))
                return
            bstack11ll1ll1l_opy_ = bstack1lll1lll11_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l1l11l11l1_opy_.value)
            self.bstack1l1l11l1ll1_opy_(driver, script_code, bstack1l11l1lll11_opy_, framework_name)
            try:
                bstack1l11ll1l1l1_opy_ = {
                    bstack1ll1lll_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦᔊ"): {
                        bstack1ll1lll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧᔋ"): bstack1ll1lll_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡆ࡜ࡅࡠࡔࡈࡗ࡚ࡒࡔࡔࠤᔌ"),
                    },
                    bstack1ll1lll_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᔍ"): {
                        bstack1ll1lll_opy_ (u"ࠢࡣࡱࡧࡽࠧᔎ"): {
                            bstack1ll1lll_opy_ (u"ࠣ࡯ࡶ࡫ࠧᔏ"): bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᔐ"),
                            bstack1ll1lll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᔑ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l11ll1l1l1_opy_, separators=(bstack1ll1lll_opy_ (u"ࠫ࠱࠭ᔒ"), bstack1ll1lll_opy_ (u"ࠬࡀࠧᔓ"))))
            except Exception as bstack1l1l1ll1l1_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡢࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡪࡡࡵࡣ࠽ࠤࠧᔔ") + str(bstack1l1l1ll1l1_opy_) + bstack1ll1lll_opy_ (u"ࠢࠣᔕ"))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᔖ"))
            bstack1lll1lll11_opy_.end(EVENTS.bstack1l1l11l11l1_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᔗ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᔘ"), True, None, command=bstack1ll1lll_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᔙ"),test_name=name)
        except Exception as bstack1l11ll1l111_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᔚ") + bstack1ll1lll_opy_ (u"ࠨࡳࡵࡴࠫࡴࡦࡺࡨࠪࠤᔛ") + bstack1ll1lll_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᔜ") + str(bstack1l11ll1l111_opy_))
            bstack1lll1lll11_opy_.end(EVENTS.bstack1l1l11l11l1_opy_.value, bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᔝ"), bstack11ll1ll1l_opy_+bstack1ll1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᔞ"), False, bstack1l11ll1l111_opy_, command=bstack1ll1lll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᔟ"),test_name=name)
        finally:
            bstack1ll1ll11ll1_opy_._1ll1l11ll11_opy_.set()
    def bstack1ll1l1l1l1l_opy_(self):
        bstack1ll1lll_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡦࡳࡱࡰࠤࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡺ࡬ࡪࡴࠠࡢࠢࡦࡰࡴࡹࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢ࡬ࡷࠥࡧࡢࡰࡷࡷࠤࡹࡵࠠࡦࡺࡨࡧࡺࡺࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᔠ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࡣࡧ࡫ࡦࡰࡴࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨ࠾ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠢᔡ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠣࡳࡷࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᔢ"))
            return
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡶࡲࡴࡤࡩࡡࡱࡶࡸࡶࡪࡥࡢࡦࡨࡲࡶࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪࡀࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵࡷࡳࡵࡥࡴࡦࡵࡷࡣࡨࡧࡰࡵࡷࡵࡩࠧᔣ"))
        self.bstack1ll1ll11ll_opy_(None, self._current_test_name, bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᔤ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack1l1l11l1ll1_opy_(self, driver, script_code, bstack1l11l1lll11_opy_, framework_name):
        if framework_name == bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᔥ"):
            self.bstack1l1l11ll11l_opy_.bstack1l1l11111l1_opy_(driver, script_code, bstack1l11l1lll11_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l11l1lll11_opy_))
    def _1l11llll1ll_opy_(self, instance: bstack1ll111lllll_opy_, args: Tuple) -> list:
        bstack1ll1lll_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡩࡶࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢᔦ")
        if bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᔧ") in instance.bstack1l11ll1l1ll_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll1lll_opy_ (u"ࠬࡺࡡࡨࡵࠪᔨ")) else []
        if hasattr(args[0], bstack1ll1lll_opy_ (u"࠭࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠫᔩ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack1ll1lll_opy_ (u"ࠧࡵࡣࡪࡷࠬᔪ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l1l111l111_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)