# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1ll1111111_opy_ import (
    bstack11l1ll1l1_opy_,
    bstack1lll1l11l1_opy_,
    bstack1l1l1ll11l_opy_,
    bstack1l1l111l1l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1111lllll_opy_ import bstack1l11l11l11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l11ll11l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l11l1l1l11_opy_ import bstack1l111111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l11111111l_opy_ import bstack1l1111l111l_opy_
from browserstack_sdk.sdk_cli.bstack1l11ll1lll1_opy_ import bstack1l1111ll1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll_opy_ import bstack11ll1lllll_opy_
from bstack_utils.helper import bstack11ll1ll1ll1_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1l1llll1lll_opy_(bstack1l111111l1l_opy_):
    bstack11llll1llll_opy_ = False
    bstack11llll1ll11_opy_ = bstack111l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᘧ")
    bstack11ll1ll1l11_opy_ = bstack111l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᘨ")
    bstack11llll1lll1_opy_ = bstack111l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣᘩ")
    bstack11ll1ll1l1l_opy_ = bstack111l_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᘪ")
    bstack11lll1l11ll_opy_ = bstack111l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨᘫ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1l1lll1l1ll_opy_ = threading.Event()
    _1l1lll1l1ll_opy_.set()
    def __init__(self, bstack1l111l1l1ll_opy_, bstack1l11ll1ll1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack11ll1lll1l1_opy_ = False
        self.bstack11llll111ll_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack11llll1ll1l_opy_ = False
        self.bstack11lll11lll1_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack11ll1llll11_opy_ = bstack1l11ll1ll1l_opy_
        bstack1l111l1l1ll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack1ll1111l1l1_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack1l1lllllll1_opy_)
        bstack1l111l1l1ll_opy_.bstack11llll1l1l1_opy_((bstack11l1ll1l1_opy_.bstack11llll111l_opy_, bstack1lll1l11l1_opy_.PRE), self.bstack11lll1l1l11_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack11lll1ll1ll_opy_)
        TestFramework.bstack11llll1l1l1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack11lll1ll111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack11lll1ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._11lll11l111_opy_(instance, args)
        test_framework = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1l1l11_opy_)
        if self.bstack11ll1lll1l1_opy_:
            self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᘬ")] = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
        if bstack111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᘭ") in instance.bstack1l1ll1ll11l_opy_:
            platform_index = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_)
            self.accessibility = self.bstack11lll11llll_opy_(tags, self.config[bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘮ")][platform_index])
        elif test_framework == bstack111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪᘯ"):
            platform_index = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1l11ll1_opy_)
            self.accessibility = self.bstack11lll11llll_opy_(tags, self.config[bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘰ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1lll1l_opy_)
            self._current_test_uuid = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
            self.save_result_done = False
            self.logger.debug(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦࡲࡰࡤࡲࡸ࠲ࡶࡷࠡࡶࡤ࡫ࡸ࠳࡯࡯࡮ࡼࠤࡨ࡮ࡥࡤ࡭࠯ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡁࠧᘱ") + str(self.accessibility) + bstack111l_opy_ (u"ࠧࠨᘲ"))
        else:
            capabilities = self.bstack11ll1llll11_opy_.bstack11llll1l111_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack111l_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᘳ") + str(kwargs) + bstack111l_opy_ (u"ࠢࠣᘴ"))
                return
            self.accessibility = self.bstack11lll11llll_opy_(tags, capabilities)
        if self.bstack11ll1llll11_opy_.pages and self.bstack11ll1llll11_opy_.pages.values():
            bstack11lllll111l_opy_ = list(self.bstack11ll1llll11_opy_.pages.values())
            if bstack11lllll111l_opy_ and isinstance(bstack11lllll111l_opy_[0], (list, tuple)) and bstack11lllll111l_opy_[0]:
                bstack11lll1l1ll1_opy_ = bstack11lllll111l_opy_[0][0]
                if callable(bstack11lll1l1ll1_opy_):
                    page = bstack11lll1l1ll1_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack111l_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᘵ"))
                    def bstack11lll11ll1l_opy_():
                        self.get_accessibility_results_summary(page, bstack111l_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᘶ"))
                    setattr(page, bstack111l_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡸࠨᘷ"), get_results)
                    setattr(page, bstack111l_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨᘸ"), bstack11lll11ll1l_opy_)
        self.logger.debug(bstack111l_opy_ (u"ࠧࡹࡨࡰࡷ࡯ࡨࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱࡻࡥ࠾ࠤᘹ") + str(self.accessibility) + bstack111l_opy_ (u"ࠨࠢᘺ"))
    def bstack11lll1l1l11_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack111l_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡤࡸࠥࡉࡒࡆࡃࡗࡉ࠳ࡖࡒࡆࠢࡤࡪࡹ࡫ࡲࠡࡆࡵ࡭ࡻ࡫ࡲࡊࡰ࡬ࡸࠥ࡯࡮ࠡࡔࡲࡦࡴࡺ࠭ࡑ࡙ࠣࡪࡱࡵࡷ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪ࡬ࡩ࡯ࡧࡶࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤ࡫ࡲࡡࡨࠢࡺ࡭ࡹ࡮ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡧ࡭࡫ࡣ࡬࠰ࠥࠦࠧᘻ")
        if not self.accessibility:
            return
        capabilities = self.bstack11ll1llll11_opy_.bstack11llll1l111_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡩࡸࡩࡷࡧࡵࡣࡨࡸࡥࡢࡶࡨ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡢࡸࡤ࡭ࡱࡧࡢ࡭ࡧࠥᘼ"))
            return
        bstack1lll111l111_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1lll111l111_opy_
        self.logger.debug(bstack111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡪࡲࡪࡸࡨࡶࡤࡩࡲࡦࡣࡷࡩ࠿ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡵࡸࡴࡵࡵࡲࡵࡧࡧࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࢀ࠰ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡂࠨᘽ") + str(self.accessibility) + bstack111l_opy_ (u"ࠥࠦᘾ"))
    def bstack1l1lllllll1_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        driver: object,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        bstack1l1l1lllll1_opy_: Tuple[bstack11l1ll1l1_opy_, bstack1lll1l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack11lll1l11l1_opy_(method_name, *args):
                bstack1lllllll1ll_opy_ = datetime.now()
                self.bstack11lll1l1lll_opy_(f, exec, *args, **kwargs)
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᘿ"), datetime.now() - bstack1lllllll1ll_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack111l_opy_ (u"ࠧࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡷࡪࡹࡳࡪࡱࡱ࠰ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᙀ"))
                return
            bstack1lllllll1ll_opy_ = datetime.now()
            self.bstack11lll1l1lll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᙁ"), datetime.now() - bstack1lllllll1ll_opy_)
            bstack1l11llll111_opy_ = instance.data.get(bstack111l_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᙂ"), None)
            if (
                not f.bstack11llll111l1_opy_(method_name)
                or f.bstack11lll111l11_opy_(method_name, *args)
                or f.bstack11lll1l1l1l_opy_(method_name, *args)
                or (bstack1l11llll111_opy_ and int(bstack1l11llll111_opy_)>1)
            ):
                return
            if not f.bstack1ll111111ll_opy_(instance, bstack1l1llll1lll_opy_.bstack11llll1lll1_opy_, False):
                if not bstack1l1llll1lll_opy_.bstack11llll1llll_opy_:
                    self.logger.warning(bstack111l_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦᙃ") + str(f.platform_index) + bstack111l_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᙄ"))
                    bstack1l1llll1lll_opy_.bstack11llll1llll_opy_ = True
                return
            bstack11ll1ll11ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack11ll1ll11ll_opy_:
                platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_, 0)
                self.logger.debug(bstack111l_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᙅ") + str(f.framework_name) + bstack111l_opy_ (u"ࠦࠧᙆ"))
                return
            command_name = f.bstack11lll1ll11l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack111l_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢᙇ") + str(method_name) + bstack111l_opy_ (u"ࠨࠢᙈ"))
                return
            if f.framework_name != bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᙉ"):
                bstack11llll1111l_opy_ = f.bstack1ll111111ll_opy_(instance, bstack1l1llll1lll_opy_.bstack11lll1l11ll_opy_, False)
                if command_name == bstack111l_opy_ (u"ࠣࡩࡨࡸࠧᙊ") and not bstack11llll1111l_opy_:
                    f.bstack1l11l1ll11_opy_(instance, bstack1l1llll1lll_opy_.bstack11lll1l11ll_opy_, True)
                    bstack11llll1111l_opy_ = True
                if not bstack11llll1111l_opy_ and not self.bstack11ll1lll1l1_opy_:
                    self.logger.debug(bstack111l_opy_ (u"ࠤࡱࡳ࡛ࠥࡒࡍࠢ࡯ࡳࡦࡪࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᙋ") + str(command_name) + bstack111l_opy_ (u"ࠥࠦᙌ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack111l_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᙍ") + str(command_name) + bstack111l_opy_ (u"ࠧࠨᙎ"))
                return
            self.logger.info(bstack111l_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡹࡣࡳ࡫ࡳࡸࡸࡥࡴࡰࡡࡵࡹࡳ࠯ࡽࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᙏ") + str(command_name) + bstack111l_opy_ (u"ࠢࠣᙐ"))
            scripts = [(s, bstack11ll1ll11ll_opy_[s]) for s in scripts_to_run if s in bstack11ll1ll11ll_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack1lllllll1ll_opy_ = datetime.now()
                    if script_name == bstack111l_opy_ (u"ࠣࡵࡦࡥࡳࠨᙑ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack111l_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᙒ"): {
                                    bstack111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᙓ"): bstack111l_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡇࡆࡔࠢᙔ"),
                                    bstack111l_opy_ (u"ࠧࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠤᙕ"): [
                                        {
                                            bstack111l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᙖ"): command_name
                                        }
                                    ]
                                },
                                bstack111l_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤᙗ"): {
                                    bstack111l_opy_ (u"ࠣࡤࡲࡨࡾࠨᙘ"): {
                                        bstack111l_opy_ (u"ࠤࡰࡷ࡬ࠨᙙ"): result.get(bstack111l_opy_ (u"ࠥࡱࡸ࡭ࠢᙚ"), bstack111l_opy_ (u"ࠦࠧᙛ")) if isinstance(result, dict) else bstack111l_opy_ (u"ࠧࠨᙜ"),
                                        bstack111l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᙝ"): result.get(bstack111l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᙞ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack111l_opy_ (u"ࠣ࠮ࠥᙟ"), bstack111l_opy_ (u"ࠤ࠽ࠦᙠ"))))
                        except Exception as bstack1111ll111l_opy_:
                            self.logger.debug(bstack111l_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡦࡤࡸࡦࡀࠠࠣᙡ") + str(bstack1111ll111l_opy_) + bstack111l_opy_ (u"ࠦࠧᙢ"))
                    instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦᙣ") + script_name, datetime.now() - bstack1lllllll1ll_opy_)
                    if isinstance(result, dict) and not result.get(bstack111l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᙤ"), True):
                        self.logger.warning(bstack111l_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢᙥ") + str(result) + bstack111l_opy_ (u"ࠣࠤᙦ"))
                        break
                except Exception as e:
                    self.logger.error(bstack111l_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦᙧ") + str(e) + bstack111l_opy_ (u"ࠥࠦᙨ"))
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣᙩ") + str(e) + bstack111l_opy_ (u"ࠧࠨᙪ"))
    def bstack11lll1ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l11ll11l_opy_,
        bstack1l1l1lllll1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack111l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᙫ") not in instance.bstack1l1ll1ll11l_opy_:
            tags = self._11lll11l111_opy_(instance, args)
            capabilities = self.bstack11ll1llll11_opy_.bstack11llll1l111_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
            self.accessibility = self.bstack11lll11llll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᙬ"))
            return
        driver = self.bstack11ll1llll11_opy_.bstack11llll11l1l_opy_(f, instance, bstack1l1l1lllll1_opy_, *args, **kwargs)
        test_name = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1ll1lll1l_opy_)
        if not test_name:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨ᙭"))
            return
        test_uuid = f.bstack1ll111111ll_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
        if not test_uuid:
            self.logger.debug(bstack111l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢ᙮"))
            return
        if isinstance(self.bstack11ll1llll11_opy_, bstack1l1111ll1l1_opy_):
            framework_name = bstack111l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᙯ")
        else:
            framework_name = bstack111l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᙰ")
        if not self.save_result_done:
            self.bstack111lll111l_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack11l1111111_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack111l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࠨᙱ"))
            return
        bstack1lllllll1ll_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack111l_opy_ (u"ࠨࡳࡤࡣࡱࠦᙲ"), None)
        if not script_code:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡧࡦࡴࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᙳ") + str(framework_name) + bstack111l_opy_ (u"ࠣࠢࠥᙴ"))
            return
        if self.bstack11ll1lll1l1_opy_:
            arg = dict()
            arg[bstack111l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᙵ")] = method if method else bstack111l_opy_ (u"ࠥࠦᙶ")
            arg[bstack111l_opy_ (u"ࠦࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠦᙷ")] = self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᙸ")]
            arg[bstack111l_opy_ (u"ࠨࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠦᙹ")] = self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠧᙺ")]
            arg[bstack111l_opy_ (u"ࠣࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧᙻ")] = self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠢᙼ")]
            arg[bstack111l_opy_ (u"ࠥࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠢᙽ")] = self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᙾ")]
            arg[bstack111l_opy_ (u"ࠧࡹࡣࡢࡰࡗ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠧᙿ")] = str(int(datetime.now().timestamp() * 1000))
            bstack11llll11ll1_opy_ = self.bstack11ll1lll1ll_opy_(bstack111l_opy_ (u"ࠨࡳࡤࡣࡱࠦ "), self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᚁ")])
            if bstack111l_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᚂ") in bstack11llll11ll1_opy_:
                bstack11llll11ll1_opy_ = bstack11llll11ll1_opy_.copy()
                bstack11llll11ll1_opy_[bstack111l_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡈࡦࡣࡧࡩࡷࠨᚃ")] = bstack11llll11ll1_opy_.pop(bstack111l_opy_ (u"ࠥࡧࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡕࡱ࡮ࡩࡳࠨᚄ"))
            arg = bstack11ll1ll1ll1_opy_(arg, bstack11llll11ll1_opy_)
            bstack11lll11ll11_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack11lll11ll11_opy_)
            return
        instance = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(driver)
        if instance:
            if not bstack1l1l1ll11l_opy_.bstack1ll111111ll_opy_(instance, bstack1l1llll1lll_opy_.bstack11ll1ll1l1l_opy_, False):
                bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, bstack1l1llll1lll_opy_.bstack11ll1ll1l1l_opy_, True)
            else:
                self.logger.info(bstack111l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᚅ") + str(method) + bstack111l_opy_ (u"ࠧࠨᚆ"))
                return
        self.logger.info(bstack111l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᚇ") + str(method) + bstack111l_opy_ (u"ࠢࠣᚈ"))
        if framework_name == bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᚉ"):
            result = self.bstack11ll1llll11_opy_.bstack11lll111ll1_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack111l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᚊ"): method if method else bstack111l_opy_ (u"ࠥࠦᚋ")})
        bstack11lll11111_opy_.end(EVENTS.bstack11l1111111_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᚌ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᚍ"), True, None, command=method)
        if instance:
            bstack1l1l1ll11l_opy_.bstack1l11l1ll11_opy_(instance, bstack1l1llll1lll_opy_.bstack11ll1ll1l1l_opy_, False)
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰࠥᚎ"), datetime.now() - bstack1lllllll1ll_opy_)
        return result
        def bstack11lll11l1ll_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack11lllll1111_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack11ll1llllll_opy_ = self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᚏ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᚐ"), bstack111l_opy_ (u"ࠩ࠳ࠫᚑ")))
            req.client_worker_id = bstack111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᚒ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack11l11lll11_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᚓ") + str(r) + bstack111l_opy_ (u"ࠧࠨᚔ"))
                else:
                    bstack11lll1111l1_opy_ = json.loads(r.bstack11llll1l11l_opy_.decode(bstack111l_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᚕ")))
                    if result_type == bstack111l_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫᚖ"):
                        return bstack11lll1111l1_opy_.get(bstack111l_opy_ (u"ࠣࡦࡤࡸࡦࠨᚗ"), [])
                    else:
                        return bstack11lll1111l1_opy_.get(bstack111l_opy_ (u"ࠤࡧࡥࡹࡧࠢᚘ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack111l_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡶࡰࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࠡࡨࡵࡳࡲࠦࡣ࡭࡫࠽ࠤࠧᚙ") + str(e) + bstack111l_opy_ (u"ࠦࠧᚚ"))
    @measure(event_name=EVENTS.bstack111lll11_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack11ll1lll1l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11lll11l1ll_opy_(driver, framework_name, bstack111l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤ᚛"))
            script_code = self.scripts.get(framework_name, {}).get(bstack111l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥ᚜"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack111l_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧ᚝"), framework_name=framework_name)
            bstack1lllllll1ll_opy_ = datetime.now()
            if framework_name == bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬ᚞"):
                result = self.bstack11ll1llll11_opy_.bstack11lll111ll1_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(driver)
            if instance:
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧ᚟"), datetime.now() - bstack1lllllll1ll_opy_)
            return result
        finally:
            bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.set()
    @measure(event_name=EVENTS.bstack1l1lll11ll_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᚠ"))
                return
            if self.bstack11ll1lll1l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack11lll11l1ll_opy_(driver, framework_name, bstack111l_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨᚡ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack111l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᚢ"), None)
            if not script_code:
                self.logger.debug(bstack111l_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᚣ") + str(framework_name) + bstack111l_opy_ (u"ࠢࠣᚤ"))
                return
            self.perform_scan(driver, method=bstack111l_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᚥ"), framework_name=framework_name)
            bstack1lllllll1ll_opy_ = datetime.now()
            if framework_name == bstack111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᚦ"):
                result = self.bstack11ll1llll11_opy_.bstack11lll111ll1_opy_(driver, script_code)
                bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1l1l1ll11l_opy_.bstack1l1l1l1l11l_opy_(driver)
            if instance:
                instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᚧ"), datetime.now() - bstack1lllllll1ll_opy_)
            return result
        finally:
            bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.set()
    @measure(event_name=EVENTS.bstack11lll1l1111_opy_, stage=STAGE.bstack1l1l11ll11_opy_)
    def bstack11ll1lllll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack11lllll1111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᚨ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack11l11lll11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᚩ") + str(r) + bstack111l_opy_ (u"ࠨࠢᚪ"))
            else:
                self.bstack11lll1ll1l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᚫ") + str(e) + bstack111l_opy_ (u"ࠣࠤᚬ"))
            traceback.print_exc()
            raise e
    def bstack11lll1ll1l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack111l_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᚭ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack11ll1lll1l1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᚮ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack11llll111ll_opy_[bstack111l_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᚯ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack11llll111ll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack11lll11l11l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack11lll11l11l_opy_:
                        bstack11lll11l11l_opy_[command.method] = dict()
                    if command.name and not command.name in bstack11lll11l11l_opy_[command.method]:
                        bstack11lll11l11l_opy_[command.method][command.name] = list()
                    bstack11lll11l11l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack11lll11l11l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack11lll1l1lll_opy_(
        self,
        f: bstack1l11l11l11l_opy_,
        exec: Tuple[bstack1l1l111l1l1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack11ll1llll11_opy_, bstack1l1111ll1l1_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack111l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᚰ"):
                    return
        if f.bstack1ll111111ll_opy_(instance, bstack1l1llll1lll_opy_.bstack11llll1lll1_opy_, False) == True:
            return
        bstack11lll1111ll_opy_ = False
        desired_capabilities = f.bstack11lll11111l_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack11ll1ll1lll_opy_(instance)
            platform_index = f.bstack1ll111111ll_opy_(instance, bstack1l11l11l11l_opy_.bstack1l1l1l11ll1_opy_, 0)
            bstack11lll1lllll_opy_ = datetime.now()
            r = self.bstack11ll1lllll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1lllll1111_opy_(bstack111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᚱ"), datetime.now() - bstack11lll1lllll_opy_)
            bstack11lll1111ll_opy_ = r.success
            f.bstack1l11l1ll11_opy_(instance, bstack1l1llll1lll_opy_.bstack11llll1lll1_opy_, bstack11lll1111ll_opy_)
        else:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡴ࡯ࡵࠢࡼࡩࡹࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦ࠮ࠣࡻ࡮ࡲ࡬ࠡࡴࡨࡸࡷࡿࠠࡰࡰࠣࡲࡪࡾࡴࠡ࡭ࡨࡽࡼࡵࡲࡥࠤᚲ"))
    def is_enabled_testcase(self, test_tags):
        bstack11ll1lllll1_opy_ = self.config.get(bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᚳ"))
        if not bstack11ll1lllll1_opy_:
            return True
        try:
            include_tags = bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᚴ")] if bstack111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᚵ") in bstack11ll1lllll1_opy_ and isinstance(bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᚶ")], list) else []
            exclude_tags = bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᚷ")] if bstack111l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᚸ") in bstack11ll1lllll1_opy_ and isinstance(bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᚹ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᚺ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack11ll1lll1l1_opy_:
                bstack11ll1llll1l_opy_ = caps.get(bstack111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᚻ"))
                if bstack11ll1llll1l_opy_ is not None and str(bstack11ll1llll1l_opy_).lower() == bstack111l_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᚼ"):
                    bstack11lll111111_opy_ = caps.get(bstack111l_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᚽ")) or caps.get(bstack111l_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᚾ"))
                    if bstack11lll111111_opy_ is not None and int(bstack11lll111111_opy_) < 11:
                        self.logger.warning(bstack111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠ࠲࠳ࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡂࠦࡻࡾ࠰ࠥᚿ").format(bstack11lll111111_opy_))
                        return False
                return True
            bstack11lll111l1l_opy_ = caps.get(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᛀ"), {}).get(bstack111l_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᛁ"), caps.get(bstack111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᛂ"), bstack111l_opy_ (u"ࠪࠫᛃ")))
            if bstack11lll111l1l_opy_:
                self.logger.warning(bstack111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᛄ"))
                return False
            browser = caps.get(bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᛅ"), bstack111l_opy_ (u"࠭ࠧᛆ")).lower()
            if browser != bstack111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᛇ"):
                self.logger.warning(bstack111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᛈ"))
                return False
            bstack11lll1llll1_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᛉ")) or self.config.get(bstack111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᛊ")):
                bstack11lll1llll1_opy_ = bstack11llll1l1ll_opy_
            browser_version = caps.get(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᛋ"))
            if not browser_version:
                browser_version = caps.get(bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᛌ"), {}).get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᛍ"), bstack111l_opy_ (u"ࠧࠨᛎ"))
            bstack11llll11lll_opy_ = str(browser_version).lower() if browser_version is not None else bstack111l_opy_ (u"ࠨࠩᛏ")
            if bstack11llll11lll_opy_:
                if bstack11llll11lll_opy_.startswith(bstack111l_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᛐ")):
                    if bstack11llll11lll_opy_.startswith(bstack111l_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᛑ")):
                        bstack11lll1lll11_opy_ = bstack11llll11lll_opy_[len(bstack111l_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬᛒ")):]
                        if bstack11lll1lll11_opy_ and not bstack11lll1lll11_opy_.isdigit():
                            self.logger.warning(bstack111l_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡨࡲࡶࡲࡧࡴࠡࠩࡾࢁࠬࡁࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࠪࡰࡦࡺࡥࡴࡶࠪࠤࡴࡸࠠࠨ࡮ࡤࡸࡪࡹࡴ࠮࠾ࡱࡹࡲࡨࡥࡳࡀࠪ࠲ࠧᛓ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack11llll11lll_opy_.split(bstack111l_opy_ (u"࠭࠮ࠨᛔ"))[0]) <= bstack11lll1llll1_opy_:
                            self.logger.warning(bstack111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡽࢀ࠲ࠧᛕ").format(bstack11lll1llll1_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࠭ࡻࡾࠩ࠽ࠤࢀࢃࠢᛖ").format(browser_version, e))
            bstack11lll1l111l_opy_ = caps.get(bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᛗ"), {}).get(bstack111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛘ"))
            if not bstack11lll1l111l_opy_:
                bstack11lll1l111l_opy_ = caps.get(bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛙ"), {})
            if not bstack11lll1l111l_opy_:
                bstack11lll1l111l_opy_ = caps.get(bstack111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛚ"), {})
            if bstack11lll1l111l_opy_ and any(arg == bstack111l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᛛ") or (arg.startswith(bstack111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࠬᛜ")) and arg != bstack111l_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࡂࡴࡥࡸࠩᛝ"))
                                     for arg in bstack11lll1l111l_opy_.get(bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᛞ"), [])):
                self.logger.warning(bstack111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᛟ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨᛠ") + str(error))
            return False
    def bstack11lll1lll1l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack11llll11111_opy_ = {
            bstack111l_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᛡ"): test_uuid,
        }
        bstack11lll111lll_opy_ = {}
        if result.success:
            bstack11lll111lll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack11ll1ll1ll1_opy_(bstack11llll11111_opy_, bstack11lll111lll_opy_)
    def bstack11ll1lll1ll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack111l_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡪࡺࡣࡩࠢࡦࡩࡳࡺࡲࡢ࡮ࠣࡥࡺࡺࡨࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡰࡤࡱࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡦࡥࡨ࡮ࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡦࡦࡶࡦ࡬ࡪࡪࠬࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠤࡱࡵࡡࡥࡵࠣࡥࡳࡪࠠࡤࡣࡦ࡬ࡪࡹࠠࡪࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫࠺ࠡࡐࡤࡱࡪࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡳࡤࡴ࡬ࡴࡹࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡶࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࡀࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠮ࠣࡩࡲࡶࡴࡺࠢࡧ࡭ࡨࡺࠠࡪࡨࠣࡩࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᛢ")
        try:
            if self.bstack11llll1ll1l_opy_:
                return self.bstack11lll11lll1_opy_
            self.bstack11lllll1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᛣ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᛤ"), bstack111l_opy_ (u"ࠩ࠳ࠫᛥ")))
            req.client_worker_id = bstack111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᛦ").format(threading.get_ident(), os.getpid())
            r = self.bstack11l11lll11_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack11lll11lll1_opy_ = self.bstack11lll1lll1l_opy_(test_uuid, r)
                self.bstack11llll1ll1l_opy_ = True
            else:
                self.logger.error(bstack111l_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᛧ") + str(r.error) + bstack111l_opy_ (u"ࠧࠨᛨ"))
                self.bstack11lll11lll1_opy_ = dict()
            return self.bstack11lll11lll1_opy_
        except Exception as e:
            self.logger.error(bstack111l_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣᛩ") + str(traceback.format_exc()) + bstack111l_opy_ (u"ࠢࠣᛪ"))
            return dict()
    def bstack111lll111l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l1l111lll_opy_ = None
        bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.clear()
        try:
            self.bstack11lllll1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣ᛫")
            req.script_name = bstack111l_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢ᛬")
            req.platform_index = str(os.environ.get(bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᛭"), bstack111l_opy_ (u"ࠫ࠵࠭ᛮ")))
            req.client_worker_id = bstack111l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᛯ").format(threading.get_ident(), os.getpid())
            r = self.bstack11l11lll11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack111l_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᛰ") + str(r.error) + bstack111l_opy_ (u"ࠢࠣᛱ"))
            else:
                bstack11llll11111_opy_ = self.bstack11lll1lll1l_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack111l_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᛲ") + str(bstack11llll11111_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᛳ") + str(framework_name) + bstack111l_opy_ (u"ࠥࠤࠧᛴ"))
                return
            bstack1l1l111lll_opy_ = bstack11lll11111_opy_.bstack111111l11l_opy_(EVENTS.bstack11ll1lll11l_opy_.value)
            self.bstack11ll1lll111_opy_(driver, script_code, bstack11llll11111_opy_, framework_name)
            try:
                bstack11lll11l1l1_opy_ = {
                    bstack111l_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧᛵ"): {
                        bstack111l_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨᛶ"): bstack111l_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥᛷ"),
                    },
                    bstack111l_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤᛸ"): {
                        bstack111l_opy_ (u"ࠣࡤࡲࡨࡾࠨ᛹"): {
                            bstack111l_opy_ (u"ࠤࡰࡷ࡬ࠨ᛺"): bstack111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ᛻"),
                            bstack111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧ᛼"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack11lll11l1l1_opy_, separators=(bstack111l_opy_ (u"ࠬ࠲ࠧ᛽"), bstack111l_opy_ (u"࠭࠺ࠨ᛾"))))
            except Exception as bstack1111ll111l_opy_:
                self.logger.debug(bstack111l_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨ᛿") + str(bstack1111ll111l_opy_) + bstack111l_opy_ (u"ࠣࠤᜀ"))
            self.logger.info(bstack111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᜁ"))
            bstack11lll11111_opy_.end(EVENTS.bstack11ll1lll11l_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᜂ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᜃ"), True, None, command=bstack111l_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᜄ"),test_name=name)
        except Exception as bstack11llll11l11_opy_:
            self.logger.error(bstack111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᜅ") + bstack111l_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥᜆ") + bstack111l_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᜇ") + str(bstack11llll11l11_opy_))
            bstack11lll11111_opy_.end(EVENTS.bstack11ll1lll11l_opy_.value, bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᜈ"), bstack1l1l111lll_opy_+bstack111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᜉ"), False, bstack11llll11l11_opy_, command=bstack111l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᜊ"),test_name=name)
        finally:
            bstack1l1llll1lll_opy_._1l1lll1l1ll_opy_.set()
    def bstack1ll111111l1_opy_(self):
        bstack111l_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡧࡴࡲࡱࠥࡸ࡯ࡣࡱࡷࡣࡱ࡯ࡳࡵࡧࡱࡩࡷࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡻ࡭࡫࡮ࠡࡣࠣࡧࡱࡵࡳࡦࠢ࡮ࡩࡾࡽ࡯ࡳࡦࠣ࡭ࡸࠦࡡࡣࡱࡸࡸࠥࡺ࡯ࠡࡧࡻࡩࡨࡻࡴࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᜋ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack111l_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠣᜌ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack111l_opy_ (u"ࠢࡴࡶࡲࡴࡤࡩࡡࡱࡶࡸࡶࡪࡥࡢࡦࡨࡲࡶࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࡥ࡮ࡢ࡯ࡨࠤࡴࡸࠠࡵࡧࡶࡸࡤࡻࡵࡪࡦ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨᜍ"))
            return
        self.logger.debug(bstack111l_opy_ (u"ࠣࡵࡷࡳࡵࡥࡣࡢࡲࡷࡹࡷ࡫࡟ࡣࡧࡩࡳࡷ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫࠺ࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡶࡸࡴࡶ࡟ࡵࡧࡶࡸࡤࡩࡡࡱࡶࡸࡶࡪࠨᜎ"))
        self.bstack111lll111l_opy_(None, self._current_test_name, bstack111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᜏ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack11ll1lll111_opy_(self, driver, script_code, bstack11llll11111_opy_, framework_name):
        if framework_name == bstack111l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᜐ"):
            self.bstack11ll1llll11_opy_.bstack11lll111ll1_opy_(driver, script_code, bstack11llll11111_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack11llll11111_opy_))
    def _11lll11l111_opy_(self, instance: bstack1l1l11ll11l_opy_, args: Tuple) -> list:
        bstack111l_opy_ (u"ࠦࠧࠨࡅࡹࡶࡵࡥࡨࡺࠠࡵࡣࡪࡷࠥࡨࡡࡴࡧࡧࠤࡴࡴࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣᜑ")
        if bstack111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᜒ") in instance.bstack1l1ll1ll11l_opy_:
            return args[2].tags if hasattr(args[2], bstack111l_opy_ (u"࠭ࡴࡢࡩࡶࠫᜓ")) else []
        if hasattr(args[0], bstack111l_opy_ (u"ࠧࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷ᜔ࠬ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack111l_opy_ (u"ࠨࡶࡤ࡫ࡸ᜕࠭")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack11lll11llll_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)