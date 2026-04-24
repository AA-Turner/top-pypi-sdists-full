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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1ll111l111_opy_ import (
    bstack11l111l1l_opy_,
    bstack1111111ll_opy_,
    bstack11ll11l1l1_opy_,
    bstack1l1ll1ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111l1l1_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l111llll11_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1l1ll1l_opy_ import bstack1l11llll11l_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll111ll_opy_ import bstack1l11l1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l11l1111l1_opy_ import bstack1l11lll1l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll_opy_ import bstack111ll11111_opy_
from bstack_utils.helper import bstack1l11111ll1l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1l1llll1111_opy_(bstack1l11llll11l_opy_):
    bstack1l111111111_opy_ = False
    bstack11lllll1l1l_opy_ = bstack111ll11_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᖬ")
    bstack1l1111lll1l_opy_ = bstack111ll11_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᖭ")
    bstack1l111l11lll_opy_ = bstack111ll11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᖮ")
    bstack11llllll11l_opy_ = bstack111ll11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᖯ")
    bstack1l1111ll11l_opy_ = bstack111ll11_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᖰ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1l1llllll1l_opy_ = threading.Event()
    _1l1llllll1l_opy_.set()
    def __init__(self, bstack1l1l1ll11ll_opy_, bstack1l11l1l111l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l111l11l11_opy_ = False
        self.bstack1l111l111l1_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l1111l1l11_opy_ = False
        self.bstack1l1111ll1ll_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l1111l11l1_opy_ = bstack1l11l1l111l_opy_
        bstack1l1l1ll11ll_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1111lll1_opy_, bstack1111111ll_opy_.PRE), self.bstack1ll1111111l_opy_)
        bstack1l1l1ll11ll_opy_.bstack1l1111111ll_opy_((bstack11l111l1l_opy_.bstack1ll1l11ll1_opy_, bstack1111111ll_opy_.PRE), self.bstack1l111111l11_opy_)
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11llllll1l1_opy_)
        TestFramework.bstack1l1111111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l111l1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11llllll1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l11111ll11_opy_(instance, args)
        test_framework = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111ll11ll_opy_)
        if self.bstack1l111l11l11_opy_:
            self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᖱ")] = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_)
        if bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᖲ") in instance.bstack1l11lll1ll1_opy_:
            platform_index = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11llllll1ll_opy_)
            self.accessibility = self.bstack1l111l11ll1_opy_(tags, self.config[bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᖳ")][platform_index])
        elif test_framework == bstack111ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᖴ"):
            platform_index = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack11llllll1ll_opy_)
            self.accessibility = self.bstack1l111l11ll1_opy_(tags, self.config[bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᖵ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
            self._current_test_uuid = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_)
            self.save_result_done = False
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡵࡳࡧࡵࡴ࠮ࡲࡺࠤࡹࡧࡧࡴ࠯ࡲࡲࡱࡿࠠࡤࡪࡨࡧࡰ࠲ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠽ࠣᖶ") + str(self.accessibility) + bstack111ll11_opy_ (u"ࠣࠤᖷ"))
        else:
            capabilities = self.bstack1l1111l11l1_opy_.bstack1l11111l1l1_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack111ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᖸ") + str(kwargs) + bstack111ll11_opy_ (u"ࠥࠦᖹ"))
                return
            self.accessibility = self.bstack1l111l11ll1_opy_(tags, capabilities)
        if self.bstack1l1111l11l1_opy_.pages and self.bstack1l1111l11l1_opy_.pages.values():
            bstack1l11111l111_opy_ = list(self.bstack1l1111l11l1_opy_.pages.values())
            if bstack1l11111l111_opy_ and isinstance(bstack1l11111l111_opy_[0], (list, tuple)) and bstack1l11111l111_opy_[0]:
                bstack11llllll111_opy_ = bstack1l11111l111_opy_[0][0]
                if callable(bstack11llllll111_opy_):
                    page = bstack11llllll111_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᖺ"))
                    def bstack1l111111l1l_opy_():
                        self.get_accessibility_results_summary(page, bstack111ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᖻ"))
                    setattr(page, bstack111ll11_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡴࠤᖼ"), get_results)
                    setattr(page, bstack111ll11_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤᖽ"), bstack1l111111l1l_opy_)
        self.logger.debug(bstack111ll11_opy_ (u"ࠣࡵ࡫ࡳࡺࡲࡤࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭ࡷࡨࡁࠧᖾ") + str(self.accessibility) + bstack111ll11_opy_ (u"ࠤࠥᖿ"))
    def bstack1l111111l11_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack111ll11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥࡧࡴࠡࡅࡕࡉࡆ࡚ࡅ࠯ࡒࡕࡉࠥࡧࡦࡵࡧࡵࠤࡉࡸࡩࡷࡧࡵࡍࡳ࡯ࡴࠡ࡫ࡱࠤࡗࡵࡢࡰࡶ࠰ࡔ࡜ࠦࡦ࡭ࡱࡺ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡨ࡬ࡲࡪࡹࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡧ࡮ࡤ࡫ࠥࡽࡩࡵࡪࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡵࡱࡲࡲࡶࡹࠦࡣࡩࡧࡦ࡯࠳ࠨࠢࠣᗀ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l1111l11l1_opy_.bstack1l11111l1l1_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡴࡨࡥࡹ࡫࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠨᗁ"))
            return
        bstack1ll1lllll1l_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1ll1lllll1l_opy_
        self.logger.debug(bstack111ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡦࡵ࡭ࡻ࡫ࡲࡠࡥࡵࡩࡦࡺࡥ࠻ࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣࡸࡻࡰࡱࡱࡵࡸࡪࡪ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡷࡺࡶࡰࡰࡴࡷࡩࡩࢃࠬࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠾ࠤᗂ") + str(self.accessibility) + bstack111ll11_opy_ (u"ࠨࠢᗃ"))
    def bstack1ll1111111l_opy_(
        self,
        f: bstack1l11l11111l_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        bstack1l1ll11l11l_opy_: Tuple[bstack11l111l1l_opy_, bstack1111111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l1111111l1_opy_(method_name, *args):
                bstack111l1lllll_opy_ = datetime.now()
                self.bstack1l1111llll1_opy_(f, exec, *args, **kwargs)
                instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᗄ"), datetime.now() - bstack111l1lllll_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack111ll11_opy_ (u"ࠣࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᗅ"))
                return
            bstack111l1lllll_opy_ = datetime.now()
            self.bstack1l1111llll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᗆ"), datetime.now() - bstack111l1lllll_opy_)
            bstack1l1lll1111l_opy_ = instance.data.get(bstack111ll11_opy_ (u"ࠪࡶࡦࡴ࡫ࠨᗇ"), None)
            if (
                not f.bstack1l11111111l_opy_(method_name)
                or f.bstack1l111l111ll_opy_(method_name, *args)
                or f.bstack11lllll11l1_opy_(method_name, *args)
                or (bstack1l1lll1111l_opy_ and int(bstack1l1lll1111l_opy_)>1)
            ):
                return
            if not f.bstack1l1lllll1l1_opy_(instance, bstack1l1llll1111_opy_.bstack1l111l11lll_opy_, False):
                if not bstack1l1llll1111_opy_.bstack1l111111111_opy_:
                    self.logger.warning(bstack111ll11_opy_ (u"ࠦࡠࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢᗈ") + str(f.platform_index) + bstack111ll11_opy_ (u"ࠧࡣࠠࡢ࠳࠴ࡽࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡭ࡧࡶࡦࠢࡱࡳࡹࠦࡢࡦࡧࡱࠤࡸ࡫ࡴࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡷࡪࡹࡳࡪࡱࡱࠦᗉ"))
                    bstack1l1llll1111_opy_.bstack1l111111111_opy_ = True
                return
            bstack1l1111l111l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1111l111l_opy_:
                platform_index = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11llllll1ll_opy_, 0)
                self.logger.debug(bstack111ll11_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᗊ") + str(f.framework_name) + bstack111ll11_opy_ (u"ࠢࠣᗋ"))
                return
            command_name = f.bstack1l111l1l111_opy_(*args)
            if not command_name:
                self.logger.debug(bstack111ll11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࠥᗌ") + str(method_name) + bstack111ll11_opy_ (u"ࠤࠥᗍ"))
                return
            if f.framework_name != bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᗎ"):
                bstack11lllllllll_opy_ = f.bstack1l1lllll1l1_opy_(instance, bstack1l1llll1111_opy_.bstack1l1111ll11l_opy_, False)
                if command_name == bstack111ll11_opy_ (u"ࠦ࡬࡫ࡴࠣᗏ") and not bstack11lllllllll_opy_:
                    f.bstack11l1ll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l1111ll11l_opy_, True)
                    bstack11lllllllll_opy_ = True
                if not bstack11lllllllll_opy_ and not self.bstack1l111l11l11_opy_:
                    self.logger.debug(bstack111ll11_opy_ (u"ࠧࡴ࡯ࠡࡗࡕࡐࠥࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᗐ") + str(command_name) + bstack111ll11_opy_ (u"ࠨࠢᗑ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack111ll11_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᗒ") + str(command_name) + bstack111ll11_opy_ (u"ࠣࠤᗓ"))
                return
            self.logger.info(bstack111ll11_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡵࡦࡶ࡮ࡶࡴࡴࡡࡷࡳࡤࡸࡵ࡯ࠫࢀࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᗔ") + str(command_name) + bstack111ll11_opy_ (u"ࠥࠦᗕ"))
            scripts = [(s, bstack1l1111l111l_opy_[s]) for s in scripts_to_run if s in bstack1l1111l111l_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack111l1lllll_opy_ = datetime.now()
                    if script_name == bstack111ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᗖ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack111ll11_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨᗗ"): {
                                    bstack111ll11_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢᗘ"): bstack111ll11_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡃࡂࡐࠥᗙ"),
                                    bstack111ll11_opy_ (u"ࠣࡲࡤࡶࡦࡳࡥࡵࡧࡵࡷࠧᗚ"): [
                                        {
                                            bstack111ll11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᗛ"): command_name
                                        }
                                    ]
                                },
                                bstack111ll11_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᗜ"): {
                                    bstack111ll11_opy_ (u"ࠦࡧࡵࡤࡺࠤᗝ"): {
                                        bstack111ll11_opy_ (u"ࠧࡳࡳࡨࠤᗞ"): result.get(bstack111ll11_opy_ (u"ࠨ࡭ࡴࡩࠥᗟ"), bstack111ll11_opy_ (u"ࠢࠣᗠ")) if isinstance(result, dict) else bstack111ll11_opy_ (u"ࠣࠤᗡ"),
                                        bstack111ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᗢ"): result.get(bstack111ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᗣ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack111ll11_opy_ (u"ࠦ࠱ࠨᗤ"), bstack111ll11_opy_ (u"ࠧࡀࠢᗥ"))))
                        except Exception as bstack11111111_opy_:
                            self.logger.debug(bstack111ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡩࡧࡴࡢ࠼ࠣࠦᗦ") + str(bstack11111111_opy_) + bstack111ll11_opy_ (u"ࠢࠣᗧ"))
                    instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࠢᗨ") + script_name, datetime.now() - bstack111l1lllll_opy_)
                    if isinstance(result, dict) and not result.get(bstack111ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᗩ"), True):
                        self.logger.warning(bstack111ll11_opy_ (u"ࠥࡷࡰ࡯ࡰࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡷ࡫࡭ࡢ࡫ࡱ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࠥᗪ") + str(result) + bstack111ll11_opy_ (u"ࠦࠧᗫ"))
                        break
                except Exception as e:
                    self.logger.error(bstack111ll11_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃࠠࡦࡴࡵࡳࡷࡃࠢᗬ") + str(e) + bstack111ll11_opy_ (u"ࠨࠢᗭ"))
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴࡀࠦᗮ") + str(e) + bstack111ll11_opy_ (u"ࠣࠤᗯ"))
    def bstack1l111l1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l111llll11_opy_,
        bstack1l1ll11l11l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack111ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᗰ") not in instance.bstack1l11lll1ll1_opy_:
            tags = self._1l11111ll11_opy_(instance, args)
            capabilities = self.bstack1l1111l11l1_opy_.bstack1l11111l1l1_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l111l11ll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᗱ"))
            return
        driver = self.bstack1l1111l11l1_opy_.bstack11lllll1l11_opy_(f, instance, bstack1l1ll11l11l_opy_, *args, **kwargs)
        test_name = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
        if not test_name:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᗲ"))
            return
        test_uuid = f.bstack1l1lllll1l1_opy_(instance, TestFramework.bstack1l111l1ll1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥᗳ"))
            return
        if isinstance(self.bstack1l1111l11l1_opy_, bstack1l11lll1l11_opy_):
            framework_name = bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᗴ")
        else:
            framework_name = bstack111ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᗵ")
        if not self.save_result_done:
            self.bstack11111llll1_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack1lll11llll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack111ll11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࠤᗶ"))
            return
        bstack111l1lllll_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack111ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᗷ"), None)
        if not script_code:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᗸ") + str(framework_name) + bstack111ll11_opy_ (u"ࠦࠥࠨᗹ"))
            return
        if self.bstack1l111l11l11_opy_:
            arg = dict()
            arg[bstack111ll11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᗺ")] = method if method else bstack111ll11_opy_ (u"ࠨࠢᗻ")
            arg[bstack111ll11_opy_ (u"ࠢࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠢᗼ")] = self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣᗽ")]
            arg[bstack111ll11_opy_ (u"ࠤࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠢᗾ")] = self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᗿ")]
            arg[bstack111ll11_opy_ (u"ࠦࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣᘀ")] = self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠥᘁ")]
            arg[bstack111ll11_opy_ (u"ࠨࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠥᘂ")] = self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨᘃ")]
            arg[bstack111ll11_opy_ (u"ࠣࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠣᘄ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l111l1l11l_opy_ = self.bstack1l1111l1l1l_opy_(bstack111ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᘅ"), self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᘆ")])
            if bstack111ll11_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡖࡲ࡯ࡪࡴࠢᘇ") in bstack1l111l1l11l_opy_:
                bstack1l111l1l11l_opy_ = bstack1l111l1l11l_opy_.copy()
                bstack1l111l1l11l_opy_[bstack111ll11_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡋࡩࡦࡪࡥࡳࠤᘈ")] = bstack1l111l1l11l_opy_.pop(bstack111ll11_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᘉ"))
            arg = bstack1l11111ll1l_opy_(arg, bstack1l111l1l11l_opy_)
            bstack1l111ll111l_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l111ll111l_opy_)
            return
        instance = bstack11ll11l1l1_opy_.bstack1l1ll111l11_opy_(driver)
        if instance:
            if not bstack11ll11l1l1_opy_.bstack1l1lllll1l1_opy_(instance, bstack1l1llll1111_opy_.bstack11llllll11l_opy_, False):
                bstack11ll11l1l1_opy_.bstack11l1ll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack11llllll11l_opy_, True)
            else:
                self.logger.info(bstack111ll11_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᘊ") + str(method) + bstack111ll11_opy_ (u"ࠣࠤᘋ"))
                return
        self.logger.info(bstack111ll11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᘌ") + str(method) + bstack111ll11_opy_ (u"ࠥࠦᘍ"))
        if framework_name == bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᘎ"):
            result = self.bstack1l1111l11l1_opy_.bstack11lllllll11_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack111ll11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᘏ"): method if method else bstack111ll11_opy_ (u"ࠨࠢᘐ")})
        bstack1ll1l11l1_opy_.end(EVENTS.bstack1lll11llll_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘑ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘒ"), True, None, command=method)
        if instance:
            bstack11ll11l1l1_opy_.bstack11l1ll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack11llllll11l_opy_, False)
            instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨᘓ"), datetime.now() - bstack111l1lllll_opy_)
        return result
        def bstack11llllllll1_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1111lllll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l111l11111_opy_ = self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᘔ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᘕ"), bstack111ll11_opy_ (u"ࠬ࠶ࠧᘖ")))
            req.client_worker_id = bstack111ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᘗ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1l1l1l1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack111ll11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᘘ") + str(r) + bstack111ll11_opy_ (u"ࠣࠤᘙ"))
                else:
                    bstack1l111111ll1_opy_ = json.loads(r.bstack11lllll1ll1_opy_.decode(bstack111ll11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨᘚ")))
                    if result_type == bstack111ll11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧᘛ"):
                        return bstack1l111111ll1_opy_.get(bstack111ll11_opy_ (u"ࠦࡩࡧࡴࡢࠤᘜ"), [])
                    else:
                        return bstack1l111111ll1_opy_.get(bstack111ll11_opy_ (u"ࠧࡪࡡࡵࡣࠥᘝ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack111ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡲࡳࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࠤ࡫ࡸ࡯࡮ࠢࡦࡰ࡮ࡀࠠࠣᘞ") + str(e) + bstack111ll11_opy_ (u"ࠢࠣᘟ"))
    @measure(event_name=EVENTS.bstack1l11ll1lll_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1l1llll1111_opy_._1l1llllll1l_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l111l11l11_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11llllllll1_opy_(driver, framework_name, bstack111ll11_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᘠ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack111ll11_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᘡ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack111ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠣᘢ"), framework_name=framework_name)
            bstack111l1lllll_opy_ = datetime.now()
            if framework_name == bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᘣ"):
                result = self.bstack1l1111l11l1_opy_.bstack11lllllll11_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11ll11l1l1_opy_.bstack1l1ll111l11_opy_(driver)
            if instance:
                instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠣᘤ"), datetime.now() - bstack111l1lllll_opy_)
            return result
        finally:
            bstack1l1llll1111_opy_._1l1llllll1l_opy_.set()
    @measure(event_name=EVENTS.bstack1ll1l11l11_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1l1llll1111_opy_._1l1llllll1l_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack111ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᘥ"))
                return
            if self.bstack1l111l11l11_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11llllllll1_opy_(driver, framework_name, bstack111ll11_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᘦ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack111ll11_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᘧ"), None)
            if not script_code:
                self.logger.debug(bstack111ll11_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᘨ") + str(framework_name) + bstack111ll11_opy_ (u"ࠥࠦᘩ"))
                return
            self.perform_scan(driver, method=bstack111ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠥᘪ"), framework_name=framework_name)
            bstack111l1lllll_opy_ = datetime.now()
            if framework_name == bstack111ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᘫ"):
                result = self.bstack1l1111l11l1_opy_.bstack11lllllll11_opy_(driver, script_code)
                bstack1l1llll1111_opy_._1l1llllll1l_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11ll11l1l1_opy_.bstack1l1ll111l11_opy_(driver)
            if instance:
                instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠥᘬ"), datetime.now() - bstack111l1lllll_opy_)
            return result
        finally:
            bstack1l1llll1111_opy_._1l1llllll1l_opy_.set()
    @measure(event_name=EVENTS.bstack1l11111lll1_opy_, stage=STAGE.bstack1l1l1ll111_opy_)
    def bstack1l1111ll1l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1111lllll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack111ll11_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᘭ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1l1l1l1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack111ll11_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᘮ") + str(r) + bstack111ll11_opy_ (u"ࠤࠥᘯ"))
            else:
                self.bstack1l11111l11l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᘰ") + str(e) + bstack111ll11_opy_ (u"ࠦࠧᘱ"))
            traceback.print_exc()
            raise e
    def bstack1l11111l11l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack111ll11_opy_ (u"ࠧࡲ࡯ࡢࡦࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᘲ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l111l11l11_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᘳ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l111l111l1_opy_[bstack111ll11_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨᘴ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l111l111l1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l111ll1111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l111ll1111_opy_:
                        bstack1l111ll1111_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l111ll1111_opy_[command.method]:
                        bstack1l111ll1111_opy_[command.method][command.name] = list()
                    bstack1l111ll1111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l111ll1111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1111llll1_opy_(
        self,
        f: bstack1l11l11111l_opy_,
        exec: Tuple[bstack1l1ll1ll111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1111l11l1_opy_, bstack1l11lll1l11_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack111ll11_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᘵ"):
                    return
        if f.bstack1l1lllll1l1_opy_(instance, bstack1l1llll1111_opy_.bstack1l111l11lll_opy_, False) == True:
            return
        bstack11lllll1lll_opy_ = False
        desired_capabilities = f.bstack1l1111l11ll_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack1l111111lll_opy_(instance)
            platform_index = f.bstack1l1lllll1l1_opy_(instance, bstack1l11l11111l_opy_.bstack11llllll1ll_opy_, 0)
            bstack11lllll111l_opy_ = datetime.now()
            r = self.bstack1l1111ll1l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack11ll11lll_opy_(bstack111ll11_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᘶ"), datetime.now() - bstack11lllll111l_opy_)
            bstack11lllll1lll_opy_ = r.success
            f.bstack11l1ll11ll_opy_(instance, bstack1l1llll1111_opy_.bstack1l111l11lll_opy_, bstack11lllll1lll_opy_)
        else:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥ࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡰࡲࡸࠥࡿࡥࡵࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩ࠱ࠦࡷࡪ࡮࡯ࠤࡷ࡫ࡴࡳࡻࠣࡳࡳࠦ࡮ࡦࡺࡷࠤࡰ࡫ࡹࡸࡱࡵࡨࠧᘷ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l1111ll1l1_opy_ = self.config.get(bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᘸ"))
        if not bstack1l1111ll1l1_opy_:
            return True
        try:
            include_tags = bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘹ")] if bstack111ll11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘺ") in bstack1l1111ll1l1_opy_ and isinstance(bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘻ")], list) else []
            exclude_tags = bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘼ")] if bstack111ll11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘽ") in bstack1l1111ll1l1_opy_ and isinstance(bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘾ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack111ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᘿ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l111l11l11_opy_:
                bstack11lllllll1l_opy_ = caps.get(bstack111ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᙀ"))
                if bstack11lllllll1l_opy_ is not None and str(bstack11lllllll1l_opy_).lower() == bstack111ll11_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢᙁ"):
                    bstack1l111ll11l1_opy_ = caps.get(bstack111ll11_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᙂ")) or caps.get(bstack111ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᙃ"))
                    if bstack1l111ll11l1_opy_ is not None and int(bstack1l111ll11l1_opy_) < 11:
                        self.logger.warning(bstack111ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡄࡲࡩࡸ࡯ࡪࡦࠣ࠵࠶ࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦ࠰ࠣࡇࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠ࠾ࠢࡾࢁ࠳ࠨᙄ").format(bstack1l111ll11l1_opy_))
                        return False
                return True
            bstack1l1111ll111_opy_ = caps.get(bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᙅ"), {}).get(bstack111ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᙆ"), caps.get(bstack111ll11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᙇ"), bstack111ll11_opy_ (u"࠭ࠧᙈ")))
            if bstack1l1111ll111_opy_:
                self.logger.warning(bstack111ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᙉ"))
                return False
            browser = caps.get(bstack111ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᙊ"), bstack111ll11_opy_ (u"ࠩࠪᙋ")).lower()
            if browser != bstack111ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᙌ"):
                self.logger.warning(bstack111ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᙍ"))
                return False
            bstack1l111l1111l_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᙎ")) or self.config.get(bstack111ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᙏ")):
                bstack1l111l1111l_opy_ = bstack1l1111l1lll_opy_
            browser_version = caps.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙐ"))
            if not browser_version:
                browser_version = caps.get(bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᙑ"), {}).get(bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙒ"), bstack111ll11_opy_ (u"ࠪࠫᙓ"))
            bstack1l1111l1111_opy_ = str(browser_version).lower() if browser_version is not None else bstack111ll11_opy_ (u"ࠫࠬᙔ")
            if bstack1l1111l1111_opy_:
                if bstack1l1111l1111_opy_.startswith(bstack111ll11_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᙕ")):
                    if bstack1l1111l1111_opy_.startswith(bstack111ll11_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᙖ")):
                        bstack1l1111lll11_opy_ = bstack1l1111l1111_opy_[len(bstack111ll11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺ࠭ࠨᙗ")):]
                        if bstack1l1111lll11_opy_ and not bstack1l1111lll11_opy_.isdigit():
                            self.logger.warning(bstack111ll11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡫ࡵࡲ࡮ࡣࡷࠤࠬࢁࡽࠨ࠽ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥ࠭࡬ࡢࡶࡨࡷࡹ࠭ࠠࡰࡴࠣࠫࡱࡧࡴࡦࡵࡷ࠱ࡁࡴࡵ࡮ࡤࡨࡶࡃ࠭࠮ࠣᙘ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack1l1111l1111_opy_.split(bstack111ll11_opy_ (u"ࠩ࠱ࠫᙙ"))[0]) <= bstack1l111l1111l_opy_:
                            self.logger.warning(bstack111ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࢃ࠮ࠣᙚ").format(bstack1l111l1111l_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack111ll11_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠩࡾࢁࠬࡀࠠࡼࡿࠥᙛ").format(browser_version, e))
            bstack1l111l1l1ll_opy_ = caps.get(bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙜ"), {}).get(bstack111ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙝ"))
            if not bstack1l111l1l1ll_opy_:
                bstack1l111l1l1ll_opy_ = caps.get(bstack111ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᙞ"), {})
            if not bstack1l111l1l1ll_opy_:
                bstack1l111l1l1ll_opy_ = caps.get(bstack111ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᙟ"), {})
            if bstack1l111l1l1ll_opy_ and any(arg == bstack111ll11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᙠ") or (arg.startswith(bstack111ll11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽ࠨᙡ")) and arg != bstack111ll11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࡰࡨࡻࠬᙢ"))
                                     for arg in bstack1l111l1l1ll_opy_.get(bstack111ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪᙣ"), [])):
                self.logger.warning(bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᙤ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᙥ") + str(error))
            return False
    def bstack1l111l1ll11_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l11111llll_opy_ = {
            bstack111ll11_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᙦ"): test_uuid,
        }
        bstack1l111l1l1l1_opy_ = {}
        if result.success:
            bstack1l111l1l1l1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l11111ll1l_opy_(bstack1l11111llll_opy_, bstack1l111l1l1l1_opy_)
    def bstack1l1111l1l1l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡦࡶࡦ࡬ࠥࡩࡥ࡯ࡶࡵࡥࡱࠦࡡࡶࡶ࡫ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡸࡩࡲࡪࡲࡷࠤࡳࡧ࡭ࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡩࡡࡤࡪࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯ࡦࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡩࡩࡹࡩࡨࡦࡦ࠯ࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠠ࡭ࡱࡤࡨࡸࠦࡡ࡯ࡦࠣࡧࡦࡩࡨࡦࡵࠣ࡭ࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧ࠽ࠤࡓࡧ࡭ࡦࠢࡲࡪࠥࡺࡨࡦࠢࡶࡧࡷ࡯ࡰࡵࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡲࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠼࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠱ࠦࡥ࡮ࡲࡷࡽࠥࡪࡩࡤࡶࠣ࡭࡫ࠦࡥࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᙧ")
        try:
            if self.bstack1l1111l1l11_opy_:
                return self.bstack1l1111ll1ll_opy_
            self.bstack1l1111lllll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111ll11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᙨ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᙩ"), bstack111ll11_opy_ (u"ࠬ࠶ࠧᙪ")))
            req.client_worker_id = bstack111ll11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᙫ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1l1l1l1l_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1111ll1ll_opy_ = self.bstack1l111l1ll11_opy_(test_uuid, r)
                self.bstack1l1111l1l11_opy_ = True
            else:
                self.logger.error(bstack111ll11_opy_ (u"ࠢࡧࡧࡷࡧ࡭ࡉࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡄ࠵࠶ࡿࡃࡰࡰࡩ࡭࡬ࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡴࡸࠠࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃ࠺ࠡࠤᙬ") + str(r.error) + bstack111ll11_opy_ (u"ࠣࠤ᙭"))
                self.bstack1l1111ll1ll_opy_ = dict()
            return self.bstack1l1111ll1ll_opy_
        except Exception as e:
            self.logger.error(bstack111ll11_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦ᙮") + str(traceback.format_exc()) + bstack111ll11_opy_ (u"ࠥࠦᙯ"))
            return dict()
    def bstack11111llll1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack11111l11ll_opy_ = None
        bstack1l1llll1111_opy_._1l1llllll1l_opy_.clear()
        try:
            self.bstack1l1111lllll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111ll11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᙰ")
            req.script_name = bstack111ll11_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᙱ")
            req.platform_index = str(os.environ.get(bstack111ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᙲ"), bstack111ll11_opy_ (u"ࠧ࠱ࠩᙳ")))
            req.client_worker_id = bstack111ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᙴ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1l1l1l1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack111ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᙵ") + str(r.error) + bstack111ll11_opy_ (u"ࠥࠦᙶ"))
            else:
                bstack1l11111llll_opy_ = self.bstack1l111l1ll11_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack111ll11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᙷ") + str(bstack1l11111llll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack111ll11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᙸ") + str(framework_name) + bstack111ll11_opy_ (u"ࠨࠠࠣᙹ"))
                return
            bstack11111l11ll_opy_ = bstack1ll1l11l1_opy_.bstack11lllll1_opy_(EVENTS.bstack11lllll11ll_opy_.value)
            self.bstack1l11111l1ll_opy_(driver, script_code, bstack1l11111llll_opy_, framework_name)
            try:
                bstack1l111l11l1l_opy_ = {
                    bstack111ll11_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᙺ"): {
                        bstack111ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᙻ"): bstack111ll11_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᙼ"),
                    },
                    bstack111ll11_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᙽ"): {
                        bstack111ll11_opy_ (u"ࠦࡧࡵࡤࡺࠤᙾ"): {
                            bstack111ll11_opy_ (u"ࠧࡳࡳࡨࠤᙿ"): bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤ "),
                            bstack111ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᚁ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l111l11l1l_opy_, separators=(bstack111ll11_opy_ (u"ࠨ࠮ࠪᚂ"), bstack111ll11_opy_ (u"ࠩ࠽ࠫᚃ"))))
            except Exception as bstack11111111_opy_:
                self.logger.debug(bstack111ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᚄ") + str(bstack11111111_opy_) + bstack111ll11_opy_ (u"ࠦࠧᚅ"))
            self.logger.info(bstack111ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᚆ"))
            bstack1ll1l11l1_opy_.end(EVENTS.bstack11lllll11ll_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᚇ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᚈ"), True, None, command=bstack111ll11_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᚉ"),test_name=name)
        except Exception as bstack1l1111l1ll1_opy_:
            self.logger.error(bstack111ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᚊ") + bstack111ll11_opy_ (u"ࠥࡷࡹࡸࠨࡱࡣࡷ࡬࠮ࠨᚋ") + bstack111ll11_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᚌ") + str(bstack1l1111l1ll1_opy_))
            bstack1ll1l11l1_opy_.end(EVENTS.bstack11lllll11ll_opy_.value, bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᚍ"), bstack11111l11ll_opy_+bstack111ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᚎ"), False, bstack1l1111l1ll1_opy_, command=bstack111ll11_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᚏ"),test_name=name)
        finally:
            bstack1l1llll1111_opy_._1l1llllll1l_opy_.set()
    def bstack1ll11111l11_opy_(self):
        bstack111ll11_opy_ (u"ࠣࠤࠥࡇࡦࡲ࡬ࡦࡦࠣࡪࡷࡵ࡭ࠡࡴࡲࡦࡴࡺ࡟࡭࡫ࡶࡸࡪࡴࡥࡳࡡࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡷࡩࡧࡱࠤࡦࠦࡣ࡭ࡱࡶࡩࠥࡱࡥࡺࡹࡲࡶࡩࠦࡩࡴࠢࡤࡦࡴࡻࡴࠡࡶࡲࠤࡪࡾࡥࡤࡷࡷࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠣࠤࠥᚐ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack111ll11_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡤࡣࡳࡸࡺࡸࡥࡠࡤࡨࡪࡴࡸࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥ࠻ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦᚑ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack111ll11_opy_ (u"ࠥࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࡡࡥࡩ࡫ࡵࡲࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࡡࡱࡥࡲ࡫ࠠࡰࡴࠣࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠤᚒ"))
            return
        self.logger.debug(bstack111ll11_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡦࡥࡵࡺࡵࡳࡧࡢࡦࡪ࡬࡯ࡳࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧ࠽ࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡹࡴࡰࡲࡢࡸࡪࡹࡴࡠࡥࡤࡴࡹࡻࡲࡦࠤᚓ"))
        self.bstack11111llll1_opy_(None, self._current_test_name, bstack111ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᚔ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack1l11111l1ll_opy_(self, driver, script_code, bstack1l11111llll_opy_, framework_name):
        if framework_name == bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᚕ"):
            self.bstack1l1111l11l1_opy_.bstack11lllllll11_opy_(driver, script_code, bstack1l11111llll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l11111llll_opy_))
    def _1l11111ll11_opy_(self, instance: bstack1l111llll11_opy_, args: Tuple) -> list:
        bstack111ll11_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦᚖ")
        if bstack111ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᚗ") in instance.bstack1l11lll1ll1_opy_:
            return args[2].tags if hasattr(args[2], bstack111ll11_opy_ (u"ࠩࡷࡥ࡬ࡹࠧᚘ")) else []
        if hasattr(args[0], bstack111ll11_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨᚙ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack111ll11_opy_ (u"ࠫࡹࡧࡧࡴࠩᚚ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l111l11ll1_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)