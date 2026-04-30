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
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1l11ll1ll1_opy_ import (
    bstack1lll11l1l1_opy_,
    bstack1111llll1l_opy_,
    bstack11l1l1ll11_opy_,
    bstack1l1ll11l1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1l111lll1_opy_ import bstack1l1l111l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l11l1ll111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11l1ll1ll_opy_ import bstack1l1l1111111_opy_
from browserstack_sdk.sdk_cli.bstack1l11l11ll11_opy_ import bstack1l11l11111l_opy_
from browserstack_sdk.sdk_cli.bstack1l1l11ll11l_opy_ import bstack1l1l11ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llllll11ll_opy_ import bstack111l1l11l_opy_
from bstack_utils.helper import bstack1l111l1l11l_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1l1llll1ll1_opy_(bstack1l1l1111111_opy_):
    bstack1l11111ll1l_opy_ = False
    bstack1l1111lll11_opy_ = bstack1l1111l_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦᖮ")
    bstack11lllllll1l_opy_ = bstack1l1111l_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᖯ")
    bstack11lllll1lll_opy_ = bstack1l1111l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨᖰ")
    bstack1l11111111l_opy_ = bstack1l1111l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᖱ")
    bstack1l1111ll1ll_opy_ = bstack1l1111l_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦᖲ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1l1lllll11l_opy_ = threading.Event()
    _1l1lllll11l_opy_.set()
    def __init__(self, bstack1l11lll1l1l_opy_, bstack1l1l11ll111_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l11111l111_opy_ = False
        self.bstack11llll1llll_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l111l111l1_opy_ = False
        self.bstack1l1111l1111_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l1111ll1l1_opy_ = bstack1l1l11ll111_opy_
        bstack1l11lll1l1l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1ll1111ll1l_opy_, bstack1111llll1l_opy_.PRE), self.bstack1l1lll1l1l1_opy_)
        bstack1l11lll1l1l_opy_.bstack1l1111lllll_opy_((bstack1lll11l1l1_opy_.bstack1lll1l111_opy_, bstack1111llll1l_opy_.PRE), self.bstack11lllllll11_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111111ll_opy_)
        TestFramework.bstack1l1111lllll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._11lllll1ll1_opy_(instance, args)
        test_framework = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l11111l11l_opy_)
        if self.bstack1l11111l111_opy_:
            self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᖳ")] = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_)
        if bstack1l1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᖴ") in instance.bstack1l1l1lll111_opy_:
            platform_index = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l1l111_opy_)
            self.accessibility = self.bstack1l111l1111l_opy_(tags, self.config[bstack1l1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᖵ")][platform_index])
        elif test_framework == bstack1l1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡨࡧࡱࡩࡷ࡯ࡣࠨᖶ"):
            platform_index = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l1l111_opy_)
            self.accessibility = self.bstack1l111l1111l_opy_(tags, self.config[bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᖷ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l11l1l_opy_)
            self._current_test_uuid = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_)
            self.save_result_done = False
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡷࡵࡢࡰࡶ࠰ࡴࡼࠦࡴࡢࡩࡶ࠱ࡴࡴ࡬ࡺࠢࡦ࡬ࡪࡩ࡫࠭ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠿ࠥᖸ") + str(self.accessibility) + bstack1l1111l_opy_ (u"ࠥࠦᖹ"))
        else:
            capabilities = self.bstack1l1111ll1l1_opy_.bstack11lllllllll_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᖺ") + str(kwargs) + bstack1l1111l_opy_ (u"ࠧࠨᖻ"))
                return
            self.accessibility = self.bstack1l111l1111l_opy_(tags, capabilities)
        if self.bstack1l1111ll1l1_opy_.pages and self.bstack1l1111ll1l1_opy_.pages.values():
            bstack1l111111lll_opy_ = list(self.bstack1l1111ll1l1_opy_.pages.values())
            if bstack1l111111lll_opy_ and isinstance(bstack1l111111lll_opy_[0], (list, tuple)) and bstack1l111111lll_opy_[0]:
                bstack11lllll11ll_opy_ = bstack1l111111lll_opy_[0][0]
                if callable(bstack11lllll11ll_opy_):
                    page = bstack11lllll11ll_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack1l1111l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᖼ"))
                    def bstack1l111111111_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1111l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᖽ"))
                    setattr(page, bstack1l1111l_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᖾ"), get_results)
                    setattr(page, bstack1l1111l_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᖿ"), bstack1l111111111_opy_)
        self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᗀ") + str(self.accessibility) + bstack1l1111l_opy_ (u"ࠦࠧᗁ"))
    def bstack11lllllll11_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack1l1111l_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡢࡶࠣࡇࡗࡋࡁࡕࡇ࠱ࡔࡗࡋࠠࡢࡨࡷࡩࡷࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣ࡭ࡳࠦࡒࡰࡤࡲࡸ࠲ࡖࡗࠡࡨ࡯ࡳࡼ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡪ࡮ࡴࡥࡴࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡰࡦ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡥ࡫ࡩࡨࡱ࠮ࠣࠤࠥᗂ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l1111ll1l1_opy_.bstack11lllllllll_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡧࡶ࡮ࡼࡥࡳࡡࡦࡶࡪࡧࡴࡦ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠣᗃ"))
            return
        bstack1ll1ll11l11_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1ll1ll11l11_opy_
        self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡨࡷ࡯ࡶࡦࡴࡢࡧࡷ࡫ࡡࡵࡧ࠽ࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡾ࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࠦᗄ") + str(self.accessibility) + bstack1l1111l_opy_ (u"ࠣࠤᗅ"))
    def bstack1l1lll1l1l1_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        driver: object,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        bstack1l1ll1ll111_opy_: Tuple[bstack1lll11l1l1_opy_, bstack1111llll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l111l1llll_opy_(method_name, *args):
                bstack11l11l1l_opy_ = datetime.now()
                self.bstack1l111l111ll_opy_(f, exec, *args, **kwargs)
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᗆ"), datetime.now() - bstack11l11l1l_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᗇ"))
                return
            bstack11l11l1l_opy_ = datetime.now()
            self.bstack1l111l111ll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᗈ"), datetime.now() - bstack11l11l1l_opy_)
            bstack1l1ll11l111_opy_ = instance.data.get(bstack1l1111l_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᗉ"), None)
            if (
                not f.bstack1l1111l111l_opy_(method_name)
                or f.bstack11lllll1111_opy_(method_name, *args)
                or f.bstack1l1111111l1_opy_(method_name, *args)
                or (bstack1l1ll11l111_opy_ and int(bstack1l1ll11l111_opy_)>1)
            ):
                return
            if not f.bstack1ll1111l1l1_opy_(instance, bstack1l1llll1ll1_opy_.bstack11lllll1lll_opy_, False):
                if not bstack1l1llll1ll1_opy_.bstack1l11111ll1l_opy_:
                    self.logger.warning(bstack1l1111l_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᗊ") + str(f.platform_index) + bstack1l1111l_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᗋ"))
                    bstack1l1llll1ll1_opy_.bstack1l11111ll1l_opy_ = True
                return
            bstack1l111l1l1l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l111l1l1l1_opy_:
                platform_index = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_, 0)
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᗌ") + str(f.framework_name) + bstack1l1111l_opy_ (u"ࠤࠥᗍ"))
                return
            command_name = f.bstack1l1111l11l1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧᗎ") + str(method_name) + bstack1l1111l_opy_ (u"ࠦࠧᗏ"))
                return
            if f.framework_name != bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᗐ"):
                bstack1l1111lll1l_opy_ = f.bstack1ll1111l1l1_opy_(instance, bstack1l1llll1ll1_opy_.bstack1l1111ll1ll_opy_, False)
                if command_name == bstack1l1111l_opy_ (u"ࠨࡧࡦࡶࠥᗑ") and not bstack1l1111lll1l_opy_:
                    f.bstack111l1llll1_opy_(instance, bstack1l1llll1ll1_opy_.bstack1l1111ll1ll_opy_, True)
                    bstack1l1111lll1l_opy_ = True
                if not bstack1l1111lll1l_opy_ and not self.bstack1l11111l111_opy_:
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᗒ") + str(command_name) + bstack1l1111l_opy_ (u"ࠣࠤᗓ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᗔ") + str(command_name) + bstack1l1111l_opy_ (u"ࠥࠦᗕ"))
                return
            self.logger.info(bstack1l1111l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᗖ") + str(command_name) + bstack1l1111l_opy_ (u"ࠧࠨᗗ"))
            scripts = [(s, bstack1l111l1l1l1_opy_[s]) for s in scripts_to_run if s in bstack1l111l1l1l1_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack11l11l1l_opy_ = datetime.now()
                    if script_name == bstack1l1111l_opy_ (u"ࠨࡳࡤࡣࡱࠦᗘ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack1l1111l_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᗙ"): {
                                    bstack1l1111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᗚ"): bstack1l1111l_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧᗛ"),
                                    bstack1l1111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢᗜ"): [
                                        {
                                            bstack1l1111l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᗝ"): command_name
                                        }
                                    ]
                                },
                                bstack1l1111l_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᗞ"): {
                                    bstack1l1111l_opy_ (u"ࠨࡢࡰࡦࡼࠦᗟ"): {
                                        bstack1l1111l_opy_ (u"ࠢ࡮ࡵࡪࠦᗠ"): result.get(bstack1l1111l_opy_ (u"ࠣ࡯ࡶ࡫ࠧᗡ"), bstack1l1111l_opy_ (u"ࠤࠥᗢ")) if isinstance(result, dict) else bstack1l1111l_opy_ (u"ࠥࠦᗣ"),
                                        bstack1l1111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᗤ"): result.get(bstack1l1111l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᗥ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack1l1111l_opy_ (u"ࠨࠬࠣᗦ"), bstack1l1111l_opy_ (u"ࠢ࠻ࠤᗧ"))))
                        except Exception as bstack11l111ll11_opy_:
                            self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨᗨ") + str(bstack11l111ll11_opy_) + bstack1l1111l_opy_ (u"ࠤࠥᗩ"))
                    instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᗪ") + script_name, datetime.now() - bstack11l11l1l_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l1111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᗫ"), True):
                        self.logger.warning(bstack1l1111l_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᗬ") + str(result) + bstack1l1111l_opy_ (u"ࠨࠢᗭ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᗮ") + str(e) + bstack1l1111l_opy_ (u"ࠣࠤᗯ"))
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᗰ") + str(e) + bstack1l1111l_opy_ (u"ࠥࠦᗱ"))
    def bstack1l1111ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l11l1ll111_opy_,
        bstack1l1ll1ll111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1l1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᗲ") not in instance.bstack1l1l1lll111_opy_:
            tags = self._11lllll1ll1_opy_(instance, args)
            capabilities = self.bstack1l1111ll1l1_opy_.bstack11lllllllll_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l111l1111l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᗳ"))
            return
        driver = self.bstack1l1111ll1l1_opy_.bstack1l11111l1l1_opy_(f, instance, bstack1l1ll1ll111_opy_, *args, **kwargs)
        test_name = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack1l111l11l1l_opy_)
        if not test_name:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᗴ"))
            return
        test_uuid = f.bstack1ll1111l1l1_opy_(instance, TestFramework.bstack11llllll111_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᗵ"))
            return
        if isinstance(self.bstack1l1111ll1l1_opy_, bstack1l1l11ll1l1_opy_):
            framework_name = bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᗶ")
        else:
            framework_name = bstack1l1111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᗷ")
        if not self.save_result_done:
            self.bstack1l11llll11_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack11lllll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᗸ"))
            return
        bstack11l11l1l_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack1l1111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᗹ"), None)
        if not script_code:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᗺ") + str(framework_name) + bstack1l1111l_opy_ (u"ࠨࠠࠣᗻ"))
            return
        if self.bstack1l11111l111_opy_:
            arg = dict()
            arg[bstack1l1111l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᗼ")] = method if method else bstack1l1111l_opy_ (u"ࠣࠤᗽ")
            arg[bstack1l1111l_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᗾ")] = self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᗿ")]
            arg[bstack1l1111l_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᘀ")] = self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᘁ")]
            arg[bstack1l1111l_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᘂ")] = self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᘃ")]
            arg[bstack1l1111l_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᘄ")] = self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᘅ")]
            arg[bstack1l1111l_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᘆ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l111ll111l_opy_ = self.bstack1l11111llll_opy_(bstack1l1111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘇ"), self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᘈ")])
            if bstack1l1111l_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᘉ") in bstack1l111ll111l_opy_:
                bstack1l111ll111l_opy_ = bstack1l111ll111l_opy_.copy()
                bstack1l111ll111l_opy_[bstack1l1111l_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᘊ")] = bstack1l111ll111l_opy_.pop(bstack1l1111l_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᘋ"))
            arg = bstack1l111l1l11l_opy_(arg, bstack1l111ll111l_opy_)
            bstack1l11111ll11_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l11111ll11_opy_)
            return
        instance = bstack11l1l1ll11_opy_.bstack1l1ll1ll1ll_opy_(driver)
        if instance:
            if not bstack11l1l1ll11_opy_.bstack1ll1111l1l1_opy_(instance, bstack1l1llll1ll1_opy_.bstack1l11111111l_opy_, False):
                bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, bstack1l1llll1ll1_opy_.bstack1l11111111l_opy_, True)
            else:
                self.logger.info(bstack1l1111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᘌ") + str(method) + bstack1l1111l_opy_ (u"ࠥࠦᘍ"))
                return
        self.logger.info(bstack1l1111l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᘎ") + str(method) + bstack1l1111l_opy_ (u"ࠧࠨᘏ"))
        if framework_name == bstack1l1111l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᘐ"):
            result = self.bstack1l1111ll1l1_opy_.bstack1l111111l1l_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack1l1111l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᘑ"): method if method else bstack1l1111l_opy_ (u"ࠣࠤᘒ")})
        bstack11lll1111_opy_.end(EVENTS.bstack11lllll1_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘓ"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘔ"), True, None, command=method)
        if instance:
            bstack11l1l1ll11_opy_.bstack111l1llll1_opy_(instance, bstack1l1llll1ll1_opy_.bstack1l11111111l_opy_, False)
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᘕ"), datetime.now() - bstack11l11l1l_opy_)
        return result
        def bstack11lllll111l_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1111l1ll1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack11llllll11l_opy_ = self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᘖ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᘗ"), bstack1l1111l_opy_ (u"ࠧ࠱ࠩᘘ")))
            req.client_worker_id = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᘙ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack11l1ll1lll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᘚ") + str(r) + bstack1l1111l_opy_ (u"ࠥࠦᘛ"))
                else:
                    bstack1l111111l11_opy_ = json.loads(r.bstack1l1111ll111_opy_.decode(bstack1l1111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᘜ")))
                    if result_type == bstack1l1111l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᘝ"):
                        return bstack1l111111l11_opy_.get(bstack1l1111l_opy_ (u"ࠨࡤࡢࡶࡤࠦᘞ"), [])
                    else:
                        return bstack1l111111l11_opy_.get(bstack1l1111l_opy_ (u"ࠢࡥࡣࡷࡥࠧᘟ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1l1111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᘠ") + str(e) + bstack1l1111l_opy_ (u"ࠤࠥᘡ"))
    @measure(event_name=EVENTS.bstack1lll11lll1_opy_, stage=STAGE.bstack111ll11111_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l11111l111_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11lllll111l_opy_(driver, framework_name, bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᘢ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1l1111l_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᘣ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack1l1111l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᘤ"), framework_name=framework_name)
            bstack11l11l1l_opy_ = datetime.now()
            if framework_name == bstack1l1111l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᘥ"):
                result = self.bstack1l1111ll1l1_opy_.bstack1l111111l1l_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11l1l1ll11_opy_.bstack1l1ll1ll1ll_opy_(driver)
            if instance:
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᘦ"), datetime.now() - bstack11l11l1l_opy_)
            return result
        finally:
            bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.set()
    @measure(event_name=EVENTS.bstack1ll11lll1l_opy_, stage=STAGE.bstack111ll11111_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᘧ"))
                return
            if self.bstack1l11111l111_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11lllll111l_opy_(driver, framework_name, bstack1l1111l_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᘨ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1l1111l_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᘩ"), None)
            if not script_code:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᘪ") + str(framework_name) + bstack1l1111l_opy_ (u"ࠧࠨᘫ"))
                return
            self.perform_scan(driver, method=bstack1l1111l_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᘬ"), framework_name=framework_name)
            bstack11l11l1l_opy_ = datetime.now()
            if framework_name == bstack1l1111l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᘭ"):
                result = self.bstack1l1111ll1l1_opy_.bstack1l111111l1l_opy_(driver, script_code)
                bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11l1l1ll11_opy_.bstack1l1ll1ll1ll_opy_(driver)
            if instance:
                instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᘮ"), datetime.now() - bstack11l11l1l_opy_)
            return result
        finally:
            bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.set()
    @measure(event_name=EVENTS.bstack1l111l1ll11_opy_, stage=STAGE.bstack111ll11111_opy_)
    def bstack1l111l1lll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1111l1ll1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111l_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᘯ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack11l1ll1lll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᘰ") + str(r) + bstack1l1111l_opy_ (u"ࠦࠧᘱ"))
            else:
                self.bstack1l11111l1ll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᘲ") + str(e) + bstack1l1111l_opy_ (u"ࠨࠢᘳ"))
            traceback.print_exc()
            raise e
    def bstack1l11111l1ll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᘴ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l11111l111_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨᘵ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack11llll1llll_opy_[bstack1l1111l_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᘶ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack11llll1llll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1111l1l1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l1111l1l1l_opy_:
                        bstack1l1111l1l1l_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l1111l1l1l_opy_[command.method]:
                        bstack1l1111l1l1l_opy_[command.method][command.name] = list()
                    bstack1l1111l1l1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1111l1l1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l111l111ll_opy_(
        self,
        f: bstack1l1l111l111_opy_,
        exec: Tuple[bstack1l1ll11l1ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1111ll1l1_opy_, bstack1l1l11ll1l1_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack1l1111l_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᘷ"):
                    return
        if f.bstack1ll1111l1l1_opy_(instance, bstack1l1llll1ll1_opy_.bstack11lllll1lll_opy_, False) == True:
            return
        bstack1l111l11lll_opy_ = False
        desired_capabilities = f.bstack1l111l11l11_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack11lllll1l1l_opy_(instance)
            platform_index = f.bstack1ll1111l1l1_opy_(instance, bstack1l1l111l111_opy_.bstack1l111l1l111_opy_, 0)
            bstack1l111111ll1_opy_ = datetime.now()
            r = self.bstack1l111l1lll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1ll11l11l_opy_(bstack1l1111l_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᘸ"), datetime.now() - bstack1l111111ll1_opy_)
            bstack1l111l11lll_opy_ = r.success
            f.bstack111l1llll1_opy_(instance, bstack1l1llll1ll1_opy_.bstack11lllll1lll_opy_, bstack1l111l11lll_opy_)
        else:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧ࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡹ࡬ࡰࡱࠦࡲࡦࡶࡵࡽࠥࡵ࡮ࠡࡰࡨࡼࡹࠦ࡫ࡦࡻࡺࡳࡷࡪࠢᘹ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l111l1lll1_opy_ = self.config.get(bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᘺ"))
        if not bstack1l111l1lll1_opy_:
            return True
        try:
            include_tags = bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘻ")] if bstack1l1111l_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘼ") in bstack1l111l1lll1_opy_ and isinstance(bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘽ")], list) else []
            exclude_tags = bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘾ")] if bstack1l1111l_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘿ") in bstack1l111l1lll1_opy_ and isinstance(bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᙀ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᙁ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l11111l111_opy_:
                bstack1l1111l11ll_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᙂ"))
                if bstack1l1111l11ll_opy_ is not None and str(bstack1l1111l11ll_opy_).lower() == bstack1l1111l_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᙃ"):
                    bstack1l1111l1l11_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᙄ")) or caps.get(bstack1l1111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᙅ"))
                    if bstack1l1111l1l11_opy_ is not None and int(bstack1l1111l1l11_opy_) < 11:
                        self.logger.warning(bstack1l1111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡆࡴࡤࡳࡱ࡬ࡨࠥ࠷࠱ࠡࡣࡱࡨࠥࡧࡢࡰࡸࡨ࠲ࠥࡉࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡀࠤࢀࢃ࠮ࠣᙆ").format(bstack1l1111l1l11_opy_))
                        return False
                return True
            bstack1l111ll1111_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙇ"), {}).get(bstack1l1111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᙈ"), caps.get(bstack1l1111l_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᙉ"), bstack1l1111l_opy_ (u"ࠨࠩᙊ")))
            if bstack1l111ll1111_opy_:
                self.logger.warning(bstack1l1111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᙋ"))
                return False
            browser = caps.get(bstack1l1111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᙌ"), bstack1l1111l_opy_ (u"ࠫࠬᙍ")).lower()
            if browser != bstack1l1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᙎ"):
                self.logger.warning(bstack1l1111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᙏ"))
                return False
            bstack1l11111lll1_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᙐ")) or self.config.get(bstack1l1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᙑ")):
                bstack1l11111lll1_opy_ = bstack1l1111l1lll_opy_
            browser_version = caps.get(bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙒ"))
            if not browser_version:
                browser_version = caps.get(bstack1l1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᙓ"), {}).get(bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙔ"), bstack1l1111l_opy_ (u"ࠬ࠭ᙕ"))
            bstack11lllll1l11_opy_ = str(browser_version).lower() if browser_version is not None else bstack1l1111l_opy_ (u"࠭ࠧᙖ")
            if bstack11lllll1l11_opy_:
                if bstack11lllll1l11_opy_.startswith(bstack1l1111l_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᙗ")):
                    if bstack11lllll1l11_opy_.startswith(bstack1l1111l_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴ࠮ࠩᙘ")):
                        bstack1l111l1ll1l_opy_ = bstack11lllll1l11_opy_[len(bstack1l1111l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵ࠯ࠪᙙ")):]
                        if bstack1l111l1ll1l_opy_ and not bstack1l111l1ll1l_opy_.isdigit():
                            self.logger.warning(bstack1l1111l_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡦࡰࡴࡰࡥࡹࠦࠧࡼࡿࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࠨ࡮ࡤࡸࡪࡹࡴࠨࠢࡲࡶࠥ࠭࡬ࡢࡶࡨࡷࡹ࠳࠼࡯ࡷࡰࡦࡪࡸ࠾ࠨ࠰ࠥᙚ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack11lllll1l11_opy_.split(bstack1l1111l_opy_ (u"ࠫ࠳࠭ᙛ"))[0]) <= bstack1l11111lll1_opy_:
                            self.logger.warning(bstack1l1111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻࡾ࠰ࠥᙜ").format(bstack1l11111lll1_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧᙝ").format(browser_version, e))
            bstack11llllll1l1_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᙞ"), {}).get(bstack1l1111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᙟ"))
            if not bstack11llllll1l1_opy_:
                bstack11llllll1l1_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᙠ"), {})
            if not bstack11llllll1l1_opy_:
                bstack11llllll1l1_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᙡ"), {})
            if bstack11llllll1l1_opy_ and any(arg == bstack1l1111l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᙢ") or (arg.startswith(bstack1l1111l_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪᙣ")) and arg != bstack1l1111l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧᙤ"))
                                     for arg in bstack11llllll1l1_opy_.get(bstack1l1111l_opy_ (u"ࠧࡢࡴࡪࡷࠬᙥ"), [])):
                self.logger.warning(bstack1l1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᙦ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᙧ") + str(error))
            return False
    def bstack11llllllll1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l111l1l1ll_opy_ = {
            bstack1l1111l_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᙨ"): test_uuid,
        }
        bstack11llllll1ll_opy_ = {}
        if result.success:
            bstack11llllll1ll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l111l1l11l_opy_(bstack1l111l1l1ll_opy_, bstack11llllll1ll_opy_)
    def bstack1l11111llll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡨࡸࡨ࡮ࠠࡤࡧࡱࡸࡷࡧ࡬ࠡࡣࡸࡸ࡭ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡳࡤࡴ࡬ࡴࡹࠦ࡮ࡢ࡯ࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡤࡣࡦ࡬ࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡨࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡫࡫ࡴࡤࡪࡨࡨ࠱ࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠢ࡯ࡳࡦࡪࡳࠡࡣࡱࡨࠥࡩࡡࡤࡪࡨࡷࠥ࡯ࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡎࡢ࡯ࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡸࡩࡲࡪࡲࡷࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡴࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡵࡶ࡫ࡧ࠾࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠬࠡࡧࡰࡴࡹࡿࠠࡥ࡫ࡦࡸࠥ࡯ࡦࠡࡧࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᙩ")
        try:
            if self.bstack1l111l111l1_opy_:
                return self.bstack1l1111l1111_opy_
            self.bstack1l1111l1ll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1111l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᙪ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᙫ"), bstack1l1111l_opy_ (u"ࠧ࠱ࠩᙬ")))
            req.client_worker_id = bstack1l1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢ᙭").format(threading.get_ident(), os.getpid())
            r = self.bstack11l1ll1lll_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1111l1111_opy_ = self.bstack11llllllll1_opy_(test_uuid, r)
                self.bstack1l111l111l1_opy_ = True
            else:
                self.logger.error(bstack1l1111l_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦ᙮") + str(r.error) + bstack1l1111l_opy_ (u"ࠥࠦᙯ"))
                self.bstack1l1111l1111_opy_ = dict()
            return self.bstack1l1111l1111_opy_
        except Exception as e:
            self.logger.error(bstack1l1111l_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᙰ") + str(traceback.format_exc()) + bstack1l1111l_opy_ (u"ࠧࠨᙱ"))
            return dict()
    def bstack1l11llll11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l11l1l11_opy_ = None
        bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.clear()
        try:
            self.bstack1l1111l1ll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1111l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᙲ")
            req.script_name = bstack1l1111l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᙳ")
            req.platform_index = str(os.environ.get(bstack1l1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᙴ"), bstack1l1111l_opy_ (u"ࠩ࠳ࠫᙵ")))
            req.client_worker_id = bstack1l1111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᙶ").format(threading.get_ident(), os.getpid())
            r = self.bstack11l1ll1lll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᙷ") + str(r.error) + bstack1l1111l_opy_ (u"ࠧࠨᙸ"))
            else:
                bstack1l111l1l1ll_opy_ = self.bstack11llllllll1_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack1l1111l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᙹ") + str(bstack1l111l1l1ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᙺ") + str(framework_name) + bstack1l1111l_opy_ (u"ࠣࠢࠥᙻ"))
                return
            bstack1l11l1l11_opy_ = bstack11lll1111_opy_.bstack1l11l1ll_opy_(EVENTS.bstack1l1111llll1_opy_.value)
            self.bstack11lllll11l1_opy_(driver, script_code, bstack1l111l1l1ll_opy_, framework_name)
            try:
                bstack1l111l11ll1_opy_ = {
                    bstack1l1111l_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᙼ"): {
                        bstack1l1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᙽ"): bstack1l1111l_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᙾ"),
                    },
                    bstack1l1111l_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᙿ"): {
                        bstack1l1111l_opy_ (u"ࠨࡢࡰࡦࡼࠦ "): {
                            bstack1l1111l_opy_ (u"ࠢ࡮ࡵࡪࠦᚁ"): bstack1l1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᚂ"),
                            bstack1l1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᚃ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l111l11ll1_opy_, separators=(bstack1l1111l_opy_ (u"ࠪ࠰ࠬᚄ"), bstack1l1111l_opy_ (u"ࠫ࠿࠭ᚅ"))))
            except Exception as bstack11l111ll11_opy_:
                self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᚆ") + str(bstack11l111ll11_opy_) + bstack1l1111l_opy_ (u"ࠨࠢᚇ"))
            self.logger.info(bstack1l1111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᚈ"))
            bstack11lll1111_opy_.end(EVENTS.bstack1l1111llll1_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᚉ"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᚊ"), True, None, command=bstack1l1111l_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᚋ"),test_name=name)
        except Exception as bstack1l111l11111_opy_:
            self.logger.error(bstack1l1111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᚌ") + bstack1l1111l_opy_ (u"ࠧࡹࡴࡳࠪࡳࡥࡹ࡮ࠩࠣᚍ") + bstack1l1111l_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᚎ") + str(bstack1l111l11111_opy_))
            bstack11lll1111_opy_.end(EVENTS.bstack1l1111llll1_opy_.value, bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᚏ"), bstack1l11l1l11_opy_+bstack1l1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᚐ"), False, bstack1l111l11111_opy_, command=bstack1l1111l_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᚑ"),test_name=name)
        finally:
            bstack1l1llll1ll1_opy_._1l1lllll11l_opy_.set()
    def bstack1ll111l111l_opy_(self):
        bstack1l1111l_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡹ࡫ࡩࡳࠦࡡࠡࡥ࡯ࡳࡸ࡫ࠠ࡬ࡧࡼࡻࡴࡸࡤࠡ࡫ࡶࠤࡦࡨ࡯ࡶࡶࠣࡸࡴࠦࡥࡹࡧࡦࡹࡹ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᚒ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡦࡥࡵࡺࡵࡳࡧࡢࡦࡪ࡬࡯ࡳࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧ࠽ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨᚓ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack1l1111l_opy_ (u"ࠧࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࡣࡧ࡫ࡦࡰࡴࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠢࡲࡶࠥࡺࡥࡴࡶࡢࡹࡺ࡯ࡤ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦᚔ"))
            return
        self.logger.debug(bstack1l1111l_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡴࡶࡲࡴࡤࡺࡥࡴࡶࡢࡧࡦࡶࡴࡶࡴࡨࠦᚕ"))
        self.bstack1l11llll11_opy_(None, self._current_test_name, bstack1l1111l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᚖ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack11lllll11l1_opy_(self, driver, script_code, bstack1l111l1l1ll_opy_, framework_name):
        if framework_name == bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᚗ"):
            self.bstack1l1111ll1l1_opy_.bstack1l111111l1l_opy_(driver, script_code, bstack1l111l1l1ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l111l1l1ll_opy_))
    def _11lllll1ll1_opy_(self, instance: bstack1l11l1ll111_opy_, args: Tuple) -> list:
        bstack1l1111l_opy_ (u"ࠤࠥࠦࡊࡾࡴࡳࡣࡦࡸࠥࡺࡡࡨࡵࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᚘ")
        if bstack1l1111l_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᚙ") in instance.bstack1l1l1lll111_opy_:
            return args[2].tags if hasattr(args[2], bstack1l1111l_opy_ (u"ࠫࡹࡧࡧࡴࠩᚚ")) else []
        if hasattr(args[0], bstack1l1111l_opy_ (u"ࠬࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠪ᚛")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack1l1111l_opy_ (u"࠭ࡴࡢࡩࡶࠫ᚜")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l111l1111l_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)