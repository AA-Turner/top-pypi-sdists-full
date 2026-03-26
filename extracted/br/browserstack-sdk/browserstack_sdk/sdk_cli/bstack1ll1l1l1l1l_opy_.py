# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack111l11ll11_opy_ import (
    bstack11lll111_opy_,
    bstack1l11l11l1_opy_,
    bstack11ll11l1_opy_,
    bstack1ll11ll1l11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1l1ll_opy_ import bstack1ll111l1111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1lllll1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1ll11l111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1111_opy_ import bstack1l1llll11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1l1l1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1111l_opy_ import bstack111l111ll_opy_
from bstack_utils.helper import bstack1l11l1llll1_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll1ll1l1l1_opy_(bstack1ll111l11ll_opy_):
    bstack1l11llll111_opy_ = False
    bstack1l1l111111l_opy_ = bstack1ll1lll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᑖ")
    bstack1l1l111ll1l_opy_ = bstack1ll1lll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᑗ")
    bstack1l1l111ll11_opy_ = bstack1ll1lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠧᑘ")
    bstack1l11llll1l1_opy_ = bstack1ll1lll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡶࡣࡸࡩࡡ࡯ࡰ࡬ࡲ࡬ࠨᑙ")
    bstack1l1l111lll1_opy_ = bstack1ll1lll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳࡡ࡫ࡥࡸࡥࡵࡳ࡮ࠥᑚ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1ll1ll111l1_opy_ = threading.Event()
    _1ll1ll111l1_opy_.set()
    def __init__(self, bstack1l1ll1ll1ll_opy_, bstack1l1lll111ll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l11l11l1_opy_ = False
        self.bstack1l11llllll1_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l1l111l11l_opy_ = False
        self.bstack1l11ll1ll11_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l11lllll1l_opy_ = bstack1l1lll111ll_opy_
        bstack1l1ll1ll1ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1ll1l1lllll_opy_, bstack1l11l11l1_opy_.PRE), self.bstack1ll1l1l11l1_opy_)
        bstack1l1ll1ll1ll_opy_.bstack1l11ll11111_opy_((bstack11lll111_opy_.bstack1l111ll1l1_opy_, bstack1l11l11l1_opy_.PRE), self.bstack1l11l1l1ll1_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11lllll11_opy_)
        TestFramework.bstack1l11ll11111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1111lll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11lllll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l11l1l1l11_opy_(instance, args)
        test_framework = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll1l111_opy_)
        if self.bstack1l1l11l11l1_opy_:
            self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᑛ")] = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
        if bstack1ll1lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᑜ") in instance.bstack1l11l1l11ll_opy_:
            platform_index = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11l1ll11l_opy_)
            self.accessibility = self.bstack1l11l1lll11_opy_(tags, self.config[bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᑝ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11lll1l1l_opy_)
            self._current_test_uuid = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
            self.save_result_done = False
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡴࡲࡦࡴࡺ࠭ࡱࡹࠣࡸࡦ࡭ࡳ࠮ࡱࡱࡰࡾࠦࡣࡩࡧࡦ࡯࠱ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡃࠢᑞ") + str(self.accessibility) + bstack1ll1lll_opy_ (u"ࠢࠣᑟ"))
        else:
            capabilities = self.bstack1l11lllll1l_opy_.bstack1l11ll1111l_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡹ࡫ࡳࡵ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡬࡯ࡶࡰࡧࠤ࡫ࡵࡲࠡࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࡁࢀ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯ࡾࠢࡤࡶ࡬ࡹ࠽ࡼࡣࡵ࡫ࡸࢃࠠ࡬ࡹࡤࡶ࡬ࡹ࠽ࠣᑠ") + str(kwargs) + bstack1ll1lll_opy_ (u"ࠤࠥᑡ"))
                return
            self.accessibility = self.bstack1l11l1lll11_opy_(tags, capabilities)
        if self.bstack1l11lllll1l_opy_.pages and self.bstack1l11lllll1l_opy_.pages.values():
            bstack1l11ll1l1l1_opy_ = list(self.bstack1l11lllll1l_opy_.pages.values())
            if bstack1l11ll1l1l1_opy_ and isinstance(bstack1l11ll1l1l1_opy_[0], (list, tuple)) and bstack1l11ll1l1l1_opy_[0]:
                bstack1l1l111l1ll_opy_ = bstack1l11ll1l1l1_opy_[0][0]
                if callable(bstack1l1l111l1ll_opy_):
                    page = bstack1l1l111l1ll_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack1ll1lll_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᑢ"))
                    def bstack1l1l1111ll1_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᑣ"))
                    setattr(page, bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡳࠣᑤ"), get_results)
                    setattr(page, bstack1ll1lll_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡔࡷࡰࡱࡦࡸࡹࠣᑥ"), bstack1l1l1111ll1_opy_)
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡴࡪࡲࡹࡱࡪࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡻࡧ࡬ࡶࡧࡀࠦᑦ") + str(self.accessibility) + bstack1ll1lll_opy_ (u"ࠣࠤᑧ"))
    def bstack1l11l1l1ll1_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack1ll1lll_opy_ (u"ࠤࠥࠦࡈࡧ࡬࡭ࡧࡧࠤࡦࡺࠠࡄࡔࡈࡅ࡙ࡋ࠮ࡑࡔࡈࠤࡦ࡬ࡴࡦࡴࠣࡈࡷ࡯ࡶࡦࡴࡌࡲ࡮ࡺࠠࡪࡰࠣࡖࡴࡨ࡯ࡵ࠯ࡓ࡛ࠥ࡬࡬ࡰࡹ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡧ࡫ࡱࡩࡸࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡦ࡭ࡣࡪࠤࡼ࡯ࡴࡩࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥࡩࡨࡦࡥ࡮࠲ࠧࠨࠢᑨ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l11lllll1l_opy_.bstack1l11ll1111l_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡤࡳ࡫ࡹࡩࡷࡥࡣࡳࡧࡤࡸࡪࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡤࡺࡦ࡯࡬ࡢࡤ࡯ࡩࠧᑩ"))
            return
        bstack1l11ll11ll1_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1l11ll11ll1_opy_
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡥࡴ࡬ࡺࡪࡸ࡟ࡤࡴࡨࡥࡹ࡫࠺ࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡷࡺࡶࡰࡰࡴࡷࡩࡩࡃࡻࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࢂ࠲ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࠽ࠣᑪ") + str(self.accessibility) + bstack1ll1lll_opy_ (u"ࠧࠨᑫ"))
    def bstack1ll1l1l11l1_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        driver: object,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        bstack1ll11l1l111_opy_: Tuple[bstack11lll111_opy_, bstack1l11l11l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l11l1l11l1_opy_(method_name, *args):
                bstack11lllll111_opy_ = datetime.now()
                self.bstack1l11l1lllll_opy_(f, exec, *args, **kwargs)
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᑬ"), datetime.now() - bstack11lllll111_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡴ࡭࡬ࡴࡵ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴ࡮ࡪࡰࡪࠦᑭ"))
                return
            bstack11lllll111_opy_ = datetime.now()
            self.bstack1l11l1lllll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᑮ"), datetime.now() - bstack11lllll111_opy_)
            bstack1ll11ll11ll_opy_ = instance.data.get(bstack1ll1lll_opy_ (u"ࠩࡵࡥࡳࡱࠧᑯ"), None)
            if (
                not f.bstack1l1l11111ll_opy_(method_name)
                or f.bstack1l11l11llll_opy_(method_name, *args)
                or f.bstack1l1l11111l1_opy_(method_name, *args)
                or (bstack1ll11ll11ll_opy_ and int(bstack1ll11ll11ll_opy_)>1)
            ):
                return
            if not f.bstack1ll1l11llll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l111ll11_opy_, False):
                if not bstack1ll1ll1l1l1_opy_.bstack1l11llll111_opy_:
                    self.logger.warning(bstack1ll1lll_opy_ (u"ࠥ࡟ࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࠨᑰ") + str(f.platform_index) + bstack1ll1lll_opy_ (u"ࠦࡢࠦࡡ࠲࠳ࡼࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣ࡬ࡦࡼࡥࠡࡰࡲࡸࠥࡨࡥࡦࡰࠣࡷࡪࡺࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰࠥᑱ"))
                    bstack1ll1ll1l1l1_opy_.bstack1l11llll111_opy_ = True
                return
            bstack1l1l111llll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l111llll_opy_:
                platform_index = f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_, 0)
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡴ࡯ࠡࡣ࠴࠵ࡾࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡱࡵࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࡂࢁࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᑲ") + str(f.framework_name) + bstack1ll1lll_opy_ (u"ࠨࠢᑳ"))
                return
            command_name = f.bstack1l11llll11l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫ࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࠤᑴ") + str(method_name) + bstack1ll1lll_opy_ (u"ࠣࠤᑵ"))
                return
            if f.framework_name != bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᑶ"):
                bstack1l11lll1l11_opy_ = f.bstack1ll1l11llll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l111lll1_opy_, False)
                if command_name == bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺࠢᑷ") and not bstack1l11lll1l11_opy_:
                    f.bstack1lll1111ll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l111lll1_opy_, True)
                    bstack1l11lll1l11_opy_ = True
                if not bstack1l11lll1l11_opy_ and not self.bstack1l1l11l11l1_opy_:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡳࡵࠠࡖࡔࡏࠤࡱࡵࡡࡥࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᑸ") + str(command_name) + bstack1ll1lll_opy_ (u"ࠧࠨᑹ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᑺ") + str(command_name) + bstack1ll1lll_opy_ (u"ࠢࠣᑻ"))
                return
            self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡴࡥࡵ࡭ࡵࡺࡳࡠࡶࡲࡣࡷࡻ࡮ࠪࡿࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᑼ") + str(command_name) + bstack1ll1lll_opy_ (u"ࠤࠥᑽ"))
            scripts = [(s, bstack1l1l111llll_opy_[s]) for s in scripts_to_run if s in bstack1l1l111llll_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack11lllll111_opy_ = datetime.now()
                    if script_name == bstack1ll1lll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᑾ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧᑿ"): {
                                    bstack1ll1lll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨᒀ"): bstack1ll1lll_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡉࡁࡏࠤᒁ"),
                                    bstack1ll1lll_opy_ (u"ࠢࡱࡣࡵࡥࡲ࡫ࡴࡦࡴࡶࠦᒂ"): [
                                        {
                                            bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᒃ"): command_name
                                        }
                                    ]
                                },
                                bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᒄ"): {
                                    bstack1ll1lll_opy_ (u"ࠥࡦࡴࡪࡹࠣᒅ"): {
                                        bstack1ll1lll_opy_ (u"ࠦࡲࡹࡧࠣᒆ"): result.get(bstack1ll1lll_opy_ (u"ࠧࡳࡳࡨࠤᒇ"), bstack1ll1lll_opy_ (u"ࠨࠢᒈ")) if isinstance(result, dict) else bstack1ll1lll_opy_ (u"ࠢࠣᒉ"),
                                        bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᒊ"): result.get(bstack1ll1lll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᒋ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack1ll1lll_opy_ (u"ࠥ࠰ࠧᒌ"), bstack1ll1lll_opy_ (u"ࠦ࠿ࠨᒍ"))))
                        except Exception as bstack1lll1l11ll_opy_:
                            self.logger.debug(bstack1ll1lll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࠣࡨࡦࡺࡡ࠻ࠢࠥᒎ") + str(bstack1lll1l11ll_opy_) + bstack1ll1lll_opy_ (u"ࠨࠢᒏ"))
                    instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࠨᒐ") + script_name, datetime.now() - bstack11lllll111_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᒑ"), True):
                        self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡶ࡯࡮ࡶࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡶࡪࡳࡡࡪࡰ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡹ࠺ࠡࠤᒒ") + str(result) + bstack1ll1lll_opy_ (u"ࠥࠦᒓ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll1lll_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡃࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࠦࡥࡳࡴࡲࡶࡂࠨᒔ") + str(e) + bstack1ll1lll_opy_ (u"ࠧࠨᒕ"))
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧࠣࡩࡷࡸ࡯ࡳ࠿ࠥᒖ") + str(e) + bstack1ll1lll_opy_ (u"ࠢࠣᒗ"))
    def bstack1l1l1111lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1lllll1_opy_,
        bstack1ll11l1l111_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᒘ") not in instance.bstack1l11l1l11ll_opy_:
            tags = self._1l11l1l1l11_opy_(instance, args)
            capabilities = self.bstack1l11lllll1l_opy_.bstack1l11ll1111l_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l11l1lll11_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᒙ"))
            return
        driver = self.bstack1l11lllll1l_opy_.bstack1l1l111l1l1_opy_(f, instance, bstack1ll11l1l111_opy_, *args, **kwargs)
        test_name = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11lll1l1l_opy_)
        if not test_name:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᒚ"))
            return
        test_uuid = f.bstack1ll1l11llll_opy_(instance, TestFramework.bstack1l11ll11l1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᒛ"))
            return
        if isinstance(self.bstack1l11lllll1l_opy_, bstack1l1l1ll1l1l_opy_):
            framework_name = bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᒜ")
        else:
            framework_name = bstack1ll1lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᒝ")
        if not self.save_result_done:
            self.bstack1111l1ll_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l1l1l1111_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࠣᒞ"))
            return
        bstack11lllll111_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack1ll1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᒟ"), None)
        if not script_code:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡩࡡ࡯ࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᒠ") + str(framework_name) + bstack1ll1lll_opy_ (u"ࠥࠤࠧᒡ"))
            return
        if self.bstack1l1l11l11l1_opy_:
            arg = dict()
            arg[bstack1ll1lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᒢ")] = method if method else bstack1ll1lll_opy_ (u"ࠧࠨᒣ")
            arg[bstack1ll1lll_opy_ (u"ࠨࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩࠨᒤ")] = self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᒥ")]
            arg[bstack1ll1lll_opy_ (u"ࠣࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩࠨᒦ")] = self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᒧ")]
            arg[bstack1ll1lll_opy_ (u"ࠥࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸࠢᒨ")] = self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠤᒩ")]
            arg[bstack1ll1lll_opy_ (u"ࠧࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠤᒪ")] = self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡩࡡ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠧᒫ")]
            arg[bstack1ll1lll_opy_ (u"ࠢࡴࡥࡤࡲ࡙࡯࡭ࡦࡵࡷࡥࡲࡶࠢᒬ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l11l1ll1l1_opy_ = self.bstack1l11ll1l11l_opy_(bstack1ll1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᒭ"), self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᒮ")])
            if bstack1ll1lll_opy_ (u"ࠥࡧࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡕࡱ࡮ࡩࡳࠨᒯ") in bstack1l11l1ll1l1_opy_:
                bstack1l11l1ll1l1_opy_ = bstack1l11l1ll1l1_opy_.copy()
                bstack1l11l1ll1l1_opy_[bstack1ll1lll_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣᒰ")] = bstack1l11l1ll1l1_opy_.pop(bstack1ll1lll_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡗࡳࡰ࡫࡮ࠣᒱ"))
            arg = bstack1l11l1llll1_opy_(arg, bstack1l11l1ll1l1_opy_)
            bstack1l11l1ll111_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l11l1ll111_opy_)
            return
        instance = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(driver)
        if instance:
            if not bstack11ll11l1_opy_.bstack1ll1l11llll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l11llll1l1_opy_, False):
                bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l11llll1l1_opy_, True)
            else:
                self.logger.info(bstack1ll1lll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪࡰࠣࡴࡷࡵࡧࡳࡧࡶࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᒲ") + str(method) + bstack1ll1lll_opy_ (u"ࠢࠣᒳ"))
                return
        self.logger.info(bstack1ll1lll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᒴ") + str(method) + bstack1ll1lll_opy_ (u"ࠤࠥᒵ"))
        if framework_name == bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᒶ"):
            result = self.bstack1l11lllll1l_opy_.bstack1l11ll1ll1l_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack1ll1lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᒷ"): method if method else bstack1ll1lll_opy_ (u"ࠧࠨᒸ")})
        bstack1l1l11ll1_opy_.end(EVENTS.bstack1l1l1l1111_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᒹ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᒺ"), True, None, command=method)
        if instance:
            bstack11ll11l1_opy_.bstack1lll1111ll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l11llll1l1_opy_, False)
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠧᒻ"), datetime.now() - bstack11lllll111_opy_)
        return result
        def bstack1l11lllllll_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l11l1l111l_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l11l111l_opy_ = self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᒼ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒽ"), bstack1ll1lll_opy_ (u"ࠫ࠵࠭ᒾ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᒿ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1llll1lll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᓀ") + str(r) + bstack1ll1lll_opy_ (u"ࠢࠣᓁ"))
                else:
                    bstack1l11lll1111_opy_ = json.loads(r.bstack1l11ll111l1_opy_.decode(bstack1ll1lll_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᓂ")))
                    if result_type == bstack1ll1lll_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ᓃ"):
                        return bstack1l11lll1111_opy_.get(bstack1ll1lll_opy_ (u"ࠥࡨࡦࡺࡡࠣᓄ"), [])
                    else:
                        return bstack1l11lll1111_opy_.get(bstack1ll1lll_opy_ (u"ࠦࡩࡧࡴࡢࠤᓅ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡱࡲࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࠣࡪࡷࡵ࡭ࠡࡥ࡯࡭࠿ࠦࠢᓆ") + str(e) + bstack1ll1lll_opy_ (u"ࠨࠢᓇ"))
    @measure(event_name=EVENTS.bstack11lll111ll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l1l11l11l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l11lllllll_opy_(driver, framework_name, bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᓈ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1ll1lll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᓉ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack1ll1lll_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹࠢᓊ"), framework_name=framework_name)
            bstack11lllll111_opy_ = datetime.now()
            if framework_name == bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᓋ"):
                result = self.bstack1l11lllll1l_opy_.bstack1l11ll1ll1l_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(driver)
            if instance:
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹࠢᓌ"), datetime.now() - bstack11lllll111_opy_)
            return result
        finally:
            bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.set()
    @measure(event_name=EVENTS.bstack11111111ll_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᓍ"))
                return
            if self.bstack1l1l11l11l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l11lllllll_opy_(driver, framework_name, bstack1ll1lll_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᓎ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1ll1lll_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᓏ"), None)
            if not script_code:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᓐ") + str(framework_name) + bstack1ll1lll_opy_ (u"ࠤࠥᓑ"))
                return
            self.perform_scan(driver, method=bstack1ll1lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠤᓒ"), framework_name=framework_name)
            bstack11lllll111_opy_ = datetime.now()
            if framework_name == bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᓓ"):
                result = self.bstack1l11lllll1l_opy_.bstack1l11ll1ll1l_opy_(driver, script_code)
                bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack11ll11l1_opy_.bstack1ll11ll11l1_opy_(driver)
            if instance:
                instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠤᓔ"), datetime.now() - bstack11lllll111_opy_)
            return result
        finally:
            bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.set()
    @measure(event_name=EVENTS.bstack1l11lll11l1_opy_, stage=STAGE.bstack1111l1ll1_opy_)
    def bstack1l1l11l11ll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l11l1l111l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll1lll_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᓕ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1llll1lll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᓖ") + str(r) + bstack1ll1lll_opy_ (u"ࠣࠤᓗ"))
            else:
                self.bstack1l11ll1lll1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᓘ") + str(e) + bstack1ll1lll_opy_ (u"ࠥࠦᓙ"))
            traceback.print_exc()
            raise e
    def bstack1l11ll1lll1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡱࡵࡡࡥࡡࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᓚ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l11l11l1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᓛ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l11llllll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡴࡩࡡ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠧᓜ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l11llllll1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l11l1ll1ll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l11l1ll1ll_opy_:
                        bstack1l11l1ll1ll_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l11l1ll1ll_opy_[command.method]:
                        bstack1l11l1ll1ll_opy_[command.method][command.name] = list()
                    bstack1l11l1ll1ll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l11l1ll1ll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l11l1lllll_opy_(
        self,
        f: bstack1ll111l1111_opy_,
        exec: Tuple[bstack1ll11ll1l11_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l11lllll1l_opy_, bstack1l1l1ll1l1l_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack1ll1lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᓝ"):
                    return
        if f.bstack1ll1l11llll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l111ll11_opy_, False) == True:
            return
        bstack1l11ll11lll_opy_ = False
        desired_capabilities = f.bstack1l11lll1lll_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack1l1l11l1111_opy_(instance)
            platform_index = f.bstack1ll1l11llll_opy_(instance, bstack1ll111l1111_opy_.bstack1l11l1ll11l_opy_, 0)
            bstack1l11l1l1111_opy_ = datetime.now()
            r = self.bstack1l1l11l11ll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1ll1111l11_opy_(bstack1ll1lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᓞ"), datetime.now() - bstack1l11l1l1111_opy_)
            bstack1l11ll11lll_opy_ = r.success
            f.bstack1lll1111ll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l111ll11_opy_, bstack1l11ll11lll_opy_)
        else:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤ࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠ࡯ࡱࡷࠤࡾ࡫ࡴࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࠰ࠥࡽࡩ࡭࡮ࠣࡶࡪࡺࡲࡺࠢࡲࡲࠥࡴࡥࡹࡶࠣ࡯ࡪࡿࡷࡰࡴࡧࠦᓟ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l1l11l11ll_opy_ = self.config.get(bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᓠ"))
        if not bstack1l1l11l11ll_opy_:
            return True
        try:
            include_tags = bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᓡ")] if bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᓢ") in bstack1l1l11l11ll_opy_ and isinstance(bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᓣ")], list) else []
            exclude_tags = bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᓤ")] if bstack1ll1lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᓥ") in bstack1l1l11l11ll_opy_ and isinstance(bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᓦ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᓧ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l1l11l11l1_opy_:
                bstack1l11lll11ll_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᓨ"))
                if bstack1l11lll11ll_opy_ is not None and str(bstack1l11lll11ll_opy_).lower() == bstack1ll1lll_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᓩ"):
                    bstack1l1l1111l11_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᓪ")) or caps.get(bstack1ll1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᓫ"))
                    if bstack1l1l1111l11_opy_ is not None and int(bstack1l1l1111l11_opy_) < 11:
                        self.logger.warning(bstack1ll1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡃࡱࡨࡷࡵࡩࡥࠢ࠴࠵ࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥ࠯ࠢࡆࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠡࡽࢀ࠲ࠧᓬ").format(bstack1l1l1111l11_opy_))
                        return False
                return True
            bstack1l11lll1ll1_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᓭ"), {}).get(bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᓮ"), caps.get(bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᓯ"), bstack1ll1lll_opy_ (u"ࠬ࠭ᓰ")))
            if bstack1l11lll1ll1_opy_:
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᓱ"))
                return False
            browser = caps.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᓲ"), bstack1ll1lll_opy_ (u"ࠨࠩᓳ")).lower()
            if browser != bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᓴ"):
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᓵ"))
                return False
            bstack1l11lll111l_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᓶ")) or self.config.get(bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᓷ")):
                bstack1l11lll111l_opy_ = bstack1l11ll1llll_opy_
            browser_version = caps.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᓸ"))
            if not browser_version:
                browser_version = caps.get(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓹ"), {}).get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᓺ"), bstack1ll1lll_opy_ (u"ࠩࠪᓻ"))
            bstack1l1l1111l1l_opy_ = str(browser_version).lower() if browser_version is not None else bstack1ll1lll_opy_ (u"ࠪࠫᓼ")
            if bstack1l1l1111l1l_opy_:
                if bstack1l1l1111l1l_opy_.startswith(bstack1ll1lll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᓽ")):
                    if bstack1l1l1111l1l_opy_.startswith(bstack1ll1lll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ᓾ")):
                        bstack1l11l1lll1l_opy_ = bstack1l1l1111l1l_opy_[len(bstack1ll1lll_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᓿ")):]
                        if bstack1l11l1lll1l_opy_ and not bstack1l11l1lll1l_opy_.isdigit():
                            self.logger.warning(bstack1ll1lll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࡪࡴࡸ࡭ࡢࡶࠣࠫࢀࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࠬࡲࡡࡵࡧࡶࡸࠬࠦ࡯ࡳࠢࠪࡰࡦࡺࡥࡴࡶ࠰ࡀࡳࡻ࡭ࡣࡧࡵࡂࠬ࠴ࠢᔀ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack1l1l1111l1l_opy_.split(bstack1ll1lll_opy_ (u"ࠨ࠰ࠪᔁ"))[0]) <= bstack1l11lll111l_opy_:
                            self.logger.warning(bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂ࠴ࠢᔂ").format(bstack1l11lll111l_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1ll1lll_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠨࡽࢀࠫ࠿ࠦࡻࡾࠤᔃ").format(browser_version, e))
            bstack1l11l1l1l1l_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᔄ"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᔅ"))
            if not bstack1l11l1l1l1l_opy_:
                bstack1l11l1l1l1l_opy_ = caps.get(bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᔆ"), {})
            if not bstack1l11l1l1l1l_opy_:
                bstack1l11l1l1l1l_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᔇ"), {})
            if bstack1l11l1l1l1l_opy_ and any(arg == bstack1ll1lll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᔈ") or (arg.startswith(bstack1ll1lll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧᔉ")) and arg != bstack1ll1lll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫᔊ"))
                                     for arg in bstack1l11l1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᔋ"), [])):
                self.logger.warning(bstack1ll1lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᔌ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᔍ") + str(error))
            return False
    def bstack1l11llll1ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l11ll111ll_opy_ = {
            bstack1ll1lll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᔎ"): test_uuid,
        }
        bstack1l11l1l1lll_opy_ = {}
        if result.success:
            bstack1l11l1l1lll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l11l1llll1_opy_(bstack1l11ll111ll_opy_, bstack1l11l1l1lll_opy_)
    def bstack1l11ll1l11l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1ll1lll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌࡥࡵࡥ࡫ࠤࡨ࡫࡮ࡵࡴࡤࡰࠥࡧࡵࡵࡪࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡷࡨࡸࡩࡱࡶࠣࡲࡦࡳࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡨࡧࡣࡩࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡨࡨࡸࡨ࡮ࡥࡥ࠮ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠦ࡬ࡰࡣࡧࡷࠥࡧ࡮ࡥࠢࡦࡥࡨ࡮ࡥࡴࠢ࡬ࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡵࡦࡶ࡮ࡶࡴࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡸࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡹࡺ࡯ࡤ࠻ࠢࡘ࡙ࡎࡊࠠࡰࡨࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠰ࠥ࡫࡭ࡱࡶࡼࠤࡩ࡯ࡣࡵࠢ࡬ࡪࠥ࡫ࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᔏ")
        try:
            if self.bstack1l1l111l11l_opy_:
                return self.bstack1l11ll1ll11_opy_
            self.bstack1l11l1l111l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll1lll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᔐ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᔑ"), bstack1ll1lll_opy_ (u"ࠫ࠵࠭ᔒ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᔓ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1llll1lll_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l11ll1ll11_opy_ = self.bstack1l11llll1ll_opy_(test_uuid, r)
                self.bstack1l1l111l11l_opy_ = True
            else:
                self.logger.error(bstack1ll1lll_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣᔔ") + str(r.error) + bstack1ll1lll_opy_ (u"ࠢࠣᔕ"))
                self.bstack1l11ll1ll11_opy_ = dict()
            return self.bstack1l11ll1ll11_opy_
        except Exception as e:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡨࡨࡸࡨ࡮ࡃࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡅ࠶࠷ࡹࡄࡱࡱࡪ࡮࡭࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡵࡲࠡࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᔖ") + str(traceback.format_exc()) + bstack1ll1lll_opy_ (u"ࠤࠥᔗ"))
            return dict()
    def bstack1111l1ll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack111l1l1l1_opy_ = None
        bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.clear()
        try:
            self.bstack1l11l1l111l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll1lll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᔘ")
            req.script_name = bstack1ll1lll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᔙ")
            req.platform_index = str(os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᔚ"), bstack1ll1lll_opy_ (u"࠭࠰ࠨᔛ")))
            req.client_worker_id = bstack1ll1lll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᔜ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1llll1lll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᔝ") + str(r.error) + bstack1ll1lll_opy_ (u"ࠤࠥᔞ"))
            else:
                bstack1l11ll111ll_opy_ = self.bstack1l11llll1ll_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᔟ") + str(bstack1l11ll111ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᔠ") + str(framework_name) + bstack1ll1lll_opy_ (u"ࠧࠦࠢᔡ"))
                return
            bstack111l1l1l1_opy_ = bstack1l1l11ll1_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l1l1111111_opy_.value)
            self.bstack1l11ll1l1ll_opy_(driver, script_code, bstack1l11ll111ll_opy_, framework_name)
            try:
                bstack1l1l111l111_opy_ = {
                    bstack1ll1lll_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢᔢ"): {
                        bstack1ll1lll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᔣ"): bstack1ll1lll_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᔤ"),
                    },
                    bstack1ll1lll_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᔥ"): {
                        bstack1ll1lll_opy_ (u"ࠥࡦࡴࡪࡹࠣᔦ"): {
                            bstack1ll1lll_opy_ (u"ࠦࡲࡹࡧࠣᔧ"): bstack1ll1lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᔨ"),
                            bstack1ll1lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᔩ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l1l111l111_opy_, separators=(bstack1ll1lll_opy_ (u"ࠧ࠭ࠩᔪ"), bstack1ll1lll_opy_ (u"ࠨ࠼ࠪᔫ"))))
            except Exception as bstack1lll1l11ll_opy_:
                self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣᔬ") + str(bstack1lll1l11ll_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦᔭ"))
            self.logger.info(bstack1ll1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᔮ"))
            bstack1l1l11ll1_opy_.end(EVENTS.bstack1l1l1111111_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᔯ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᔰ"), True, None, command=bstack1ll1lll_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᔱ"),test_name=name)
        except Exception as bstack1l11ll11l11_opy_:
            self.logger.error(bstack1ll1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᔲ") + bstack1ll1lll_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧᔳ") + bstack1ll1lll_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᔴ") + str(bstack1l11ll11l11_opy_))
            bstack1l1l11ll1_opy_.end(EVENTS.bstack1l1l1111111_opy_.value, bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᔵ"), bstack111l1l1l1_opy_+bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᔶ"), False, bstack1l11ll11l11_opy_, command=bstack1ll1lll_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᔷ"),test_name=name)
        finally:
            bstack1ll1ll1l1l1_opy_._1ll1ll111l1_opy_.set()
    def bstack1ll1ll11ll1_opy_(self):
        bstack1ll1lll_opy_ (u"ࠢࠣࠤࡆࡥࡱࡲࡥࡥࠢࡩࡶࡴࡳࠠࡳࡱࡥࡳࡹࡥ࡬ࡪࡵࡷࡩࡳ࡫ࡲࡠࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡽࡨࡦࡰࠣࡥࠥࡩ࡬ࡰࡵࡨࠤࡰ࡫ࡹࡸࡱࡵࡨࠥ࡯ࡳࠡࡣࡥࡳࡺࡺࠠࡵࡱࠣࡩࡽ࡫ࡣࡶࡶࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᔸ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠣࡵࡷࡳࡵࡥࡣࡢࡲࡷࡹࡷ࡫࡟ࡣࡧࡩࡳࡷ࡫࡟ࡣࡴࡲࡻࡸ࡫ࡲࡠࡥ࡯ࡳࡸ࡫࠺ࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠥᔹ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack1ll1lll_opy_ (u"ࠤࡶࡸࡴࡶ࡟ࡤࡣࡳࡸࡺࡸࡥࡠࡤࡨࡪࡴࡸࡥࡠࡤࡵࡳࡼࡹࡥࡳࡡࡦࡰࡴࡹࡥ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࡠࡰࡤࡱࡪࠦ࡯ࡳࠢࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨ࠱ࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠣᔺ"))
            return
        self.logger.debug(bstack1ll1lll_opy_ (u"ࠥࡷࡹࡵࡰࡠࡥࡤࡴࡹࡻࡲࡦࡡࡥࡩ࡫ࡵࡲࡦࡡࡥࡶࡴࡽࡳࡦࡴࡢࡧࡱࡵࡳࡦ࠼ࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡸࡺ࡯ࡱࡡࡷࡩࡸࡺ࡟ࡤࡣࡳࡸࡺࡸࡥࠣᔻ"))
        self.bstack1111l1ll_opy_(None, self._current_test_name, bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᔼ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack1l11ll1l1ll_opy_(self, driver, script_code, bstack1l11ll111ll_opy_, framework_name):
        if framework_name == bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᔽ"):
            self.bstack1l11lllll1l_opy_.bstack1l11ll1ll1l_opy_(driver, script_code, bstack1l11ll111ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l11ll111ll_opy_))
    def _1l11l1l1l11_opy_(self, instance: bstack1l1l1lllll1_opy_, args: Tuple) -> list:
        bstack1ll1lll_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᔾ")
        if bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᔿ") in instance.bstack1l11l1l11ll_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll1lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᕀ")) else []
        if hasattr(args[0], bstack1ll1lll_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧᕁ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack1ll1lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᕂ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l11l1lll11_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)