# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1l11111ll_opy_ import (
    bstack1ll1l1ll11_opy_,
    bstack1ll11ll1ll_opy_,
    bstack111l1ll111_opy_,
    bstack1ll111lllll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1ll11111111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l1l111l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1ll111l11ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l111_opy_ import bstack1l1l1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l111l_opy_ import bstack1l1llll11l1_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1l11l_opy_ import bstack1l111lllll_opy_
from bstack_utils.helper import bstack1l11ll11111_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll1ll1111l_opy_(bstack1ll111l11ll_opy_):
    bstack1l1l11111ll_opy_ = False
    bstack1l11ll1111l_opy_ = bstack1ll11_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᑧ")
    bstack1l11ll1llll_opy_ = bstack1ll11_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᑨ")
    bstack1l1l11l111l_opy_ = bstack1ll11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣᑩ")
    bstack1l11l1l1l11_opy_ = bstack1ll11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᑪ")
    bstack1l11lllllll_opy_ = bstack1ll11_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨᑫ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1ll1ll111ll_opy_ = threading.Event()
    _1ll1ll111ll_opy_.set()
    def __init__(self, bstack1l1l11ll1l1_opy_, bstack1l1l1l1ll11_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l11lll11l1_opy_ = False
        self.bstack1l11ll1l1l1_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l1l1111ll1_opy_ = False
        self.bstack1l11ll1lll1_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l11ll111ll_opy_ = bstack1l1l1l1ll11_opy_
        bstack1l1l11ll1l1_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll1l1l1ll1_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack1ll1l1l1l11_opy_)
        bstack1l1l11ll1l1_opy_.bstack1l11lll1lll_opy_((bstack1ll1l1ll11_opy_.bstack1ll11lllll_opy_, bstack1ll11ll1ll_opy_.PRE), self.bstack1l11l1lllll_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l11llll1ll_opy_)
        TestFramework.bstack1l11lll1lll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1l111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l11llll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l11lllll1l_opy_(instance, args)
        test_framework = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l11llll_opy_)
        if self.bstack1l11lll11l1_opy_:
            self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᑬ")] = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
        if bstack1ll11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᑭ") in instance.bstack1l1l111lll1_opy_:
            platform_index = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11llll11l_opy_)
            self.accessibility = self.bstack1l1l1111l1l_opy_(tags, self.config[bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᑮ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
            self._current_test_uuid = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
            self.save_result_done = False
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡷࡵࡢࡰࡶ࠰ࡴࡼࠦࡴࡢࡩࡶ࠱ࡴࡴ࡬ࡺࠢࡦ࡬ࡪࡩ࡫࠭ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠿ࠥᑯ") + str(self.accessibility) + bstack1ll11_opy_ (u"ࠥࠦᑰ"))
        else:
            capabilities = self.bstack1l11ll111ll_opy_.bstack1l11l1ll1l1_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᑱ") + str(kwargs) + bstack1ll11_opy_ (u"ࠧࠨᑲ"))
                return
            self.accessibility = self.bstack1l1l1111l1l_opy_(tags, capabilities)
        if self.bstack1l11ll111ll_opy_.pages and self.bstack1l11ll111ll_opy_.pages.values():
            bstack1l11l11lll1_opy_ = list(self.bstack1l11ll111ll_opy_.pages.values())
            if bstack1l11l11lll1_opy_ and isinstance(bstack1l11l11lll1_opy_[0], (list, tuple)) and bstack1l11l11lll1_opy_[0]:
                bstack1l11l1llll1_opy_ = bstack1l11l11lll1_opy_[0][0]
                if callable(bstack1l11l1llll1_opy_):
                    page = bstack1l11l1llll1_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack1ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᑳ"))
                    def bstack1l11l1l1l1l_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᑴ"))
                    setattr(page, bstack1ll11_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᑵ"), get_results)
                    setattr(page, bstack1ll11_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᑶ"), bstack1l11l1l1l1l_opy_)
        self.logger.debug(bstack1ll11_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᑷ") + str(self.accessibility) + bstack1ll11_opy_ (u"ࠦࠧᑸ"))
    def bstack1l11l1lllll_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack1ll11_opy_ (u"ࠧࠨࠢࡄࡣ࡯ࡰࡪࡪࠠࡢࡶࠣࡇࡗࡋࡁࡕࡇ࠱ࡔࡗࡋࠠࡢࡨࡷࡩࡷࠦࡄࡳ࡫ࡹࡩࡷࡏ࡮ࡪࡶࠣ࡭ࡳࠦࡒࡰࡤࡲࡸ࠲ࡖࡗࠡࡨ࡯ࡳࡼ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡪ࡮ࡴࡥࡴࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡰࡦ࡭ࠠࡸ࡫ࡷ࡬ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡥ࡫ࡩࡨࡱ࠮ࠣࠤࠥᑹ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l11ll111ll_opy_.bstack1l11l1ll1l1_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡧࡶ࡮ࡼࡥࡳࡡࡦࡶࡪࡧࡴࡦ࠼ࠣࡲࡴࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥࠣᑺ"))
            return
        bstack1l11l1l111l_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1l11l1l111l_opy_
        self.logger.debug(bstack1ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡨࡷ࡯ࡶࡦࡴࡢࡧࡷ࡫ࡡࡵࡧ࠽ࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡾ࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࠦᑻ") + str(self.accessibility) + bstack1ll11_opy_ (u"ࠣࠤᑼ"))
    def bstack1ll1l1l1l11_opy_(
        self,
        f: bstack1ll11111111_opy_,
        driver: object,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        bstack1ll11l11lll_opy_: Tuple[bstack1ll1l1ll11_opy_, bstack1ll11ll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l11ll1l1ll_opy_(method_name, *args):
                bstack11l111ll1_opy_ = datetime.now()
                self.bstack1l1l111l111_opy_(f, exec, *args, **kwargs)
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡪࡰ࡬ࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᑽ"), datetime.now() - bstack11l111ll1_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack1ll11_opy_ (u"ࠥࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᑾ"))
                return
            bstack11l111ll1_opy_ = datetime.now()
            self.bstack1l1l111l111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᑿ"), datetime.now() - bstack11l111ll1_opy_)
            bstack1ll11ll1l1l_opy_ = instance.data.get(bstack1ll11_opy_ (u"ࠬࡸࡡ࡯࡭ࠪᒀ"), None)
            if (
                not f.bstack1l11l1l1lll_opy_(method_name)
                or f.bstack1l11lll11ll_opy_(method_name, *args)
                or f.bstack1l11ll11ll1_opy_(method_name, *args)
                or (bstack1ll11ll1l1l_opy_ and int(bstack1ll11ll1l1l_opy_)>1)
            ):
                return
            if not f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l1l11l111l_opy_, False):
                if not bstack1ll1ll1111l_opy_.bstack1l1l11111ll_opy_:
                    self.logger.warning(bstack1ll11_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᒁ") + str(f.platform_index) + bstack1ll11_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᒂ"))
                    bstack1ll1ll1111l_opy_.bstack1l1l11111ll_opy_ = True
                return
            bstack1l11l1lll1l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l11l1lll1l_opy_:
                platform_index = f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_, 0)
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᒃ") + str(f.framework_name) + bstack1ll11_opy_ (u"ࠤࠥᒄ"))
                return
            command_name = f.bstack1l1l111ll11_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1ll11_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧᒅ") + str(method_name) + bstack1ll11_opy_ (u"ࠦࠧᒆ"))
                return
            if f.framework_name != bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᒇ"):
                bstack1l1l111llll_opy_ = f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11lllllll_opy_, False)
                if command_name == bstack1ll11_opy_ (u"ࠨࡧࡦࡶࠥᒈ") and not bstack1l1l111llll_opy_:
                    f.bstack1l11lllll_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11lllllll_opy_, True)
                    bstack1l1l111llll_opy_ = True
                if not bstack1l1l111llll_opy_ and not self.bstack1l11lll11l1_opy_:
                    self.logger.debug(bstack1ll11_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᒉ") + str(command_name) + bstack1ll11_opy_ (u"ࠣࠤᒊ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll11_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᒋ") + str(command_name) + bstack1ll11_opy_ (u"ࠥࠦᒌ"))
                return
            self.logger.info(bstack1ll11_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᒍ") + str(command_name) + bstack1ll11_opy_ (u"ࠧࠨᒎ"))
            scripts = [(s, bstack1l11l1lll1l_opy_[s]) for s in scripts_to_run if s in bstack1l11l1lll1l_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack11l111ll1_opy_ = datetime.now()
                    if script_name == bstack1ll11_opy_ (u"ࠨࡳࡤࡣࡱࠦᒏ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack1ll11_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᒐ"): {
                                    bstack1ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᒑ"): bstack1ll11_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧᒒ"),
                                    bstack1ll11_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢᒓ"): [
                                        {
                                            bstack1ll11_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᒔ"): command_name
                                        }
                                    ]
                                },
                                bstack1ll11_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᒕ"): {
                                    bstack1ll11_opy_ (u"ࠨࡢࡰࡦࡼࠦᒖ"): {
                                        bstack1ll11_opy_ (u"ࠢ࡮ࡵࡪࠦᒗ"): result.get(bstack1ll11_opy_ (u"ࠣ࡯ࡶ࡫ࠧᒘ"), bstack1ll11_opy_ (u"ࠤࠥᒙ")) if isinstance(result, dict) else bstack1ll11_opy_ (u"ࠥࠦᒚ"),
                                        bstack1ll11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᒛ"): result.get(bstack1ll11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᒜ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack1ll11_opy_ (u"ࠨࠬࠣᒝ"), bstack1ll11_opy_ (u"ࠢ࠻ࠤᒞ"))))
                        except Exception as bstack1ll1l1llll_opy_:
                            self.logger.debug(bstack1ll11_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨᒟ") + str(bstack1ll1l1llll_opy_) + bstack1ll11_opy_ (u"ࠤࠥᒠ"))
                    instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᒡ") + script_name, datetime.now() - bstack11l111ll1_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᒢ"), True):
                        self.logger.warning(bstack1ll11_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᒣ") + str(result) + bstack1ll11_opy_ (u"ࠨࠢᒤ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll11_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᒥ") + str(e) + bstack1ll11_opy_ (u"ࠣࠤᒦ"))
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᒧ") + str(e) + bstack1ll11_opy_ (u"ࠥࠦᒨ"))
    def bstack1l11ll1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l1l111l1_opy_,
        bstack1ll11l11lll_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᒩ") not in instance.bstack1l1l111lll1_opy_:
            tags = self._1l11lllll1l_opy_(instance, args)
            capabilities = self.bstack1l11ll111ll_opy_.bstack1l11l1ll1l1_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l1l1111l1l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᒪ"))
            return
        driver = self.bstack1l11ll111ll_opy_.bstack1l11lll1l11_opy_(f, instance, bstack1ll11l11lll_opy_, *args, **kwargs)
        test_name = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        if not test_name:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᒫ"))
            return
        test_uuid = f.bstack1ll1ll1l1l1_opy_(instance, TestFramework.bstack1l11l1lll11_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᒬ"))
            return
        if isinstance(self.bstack1l11ll111ll_opy_, bstack1l1llll11l1_opy_):
            framework_name = bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᒭ")
        else:
            framework_name = bstack1ll11_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᒮ")
        if not self.save_result_done:
            self.bstack1l1l1ll1l_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack11ll1ll1l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᒯ"))
            return
        bstack11l111ll1_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack1ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᒰ"), None)
        if not script_code:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᒱ") + str(framework_name) + bstack1ll11_opy_ (u"ࠨࠠࠣᒲ"))
            return
        if self.bstack1l11lll11l1_opy_:
            arg = dict()
            arg[bstack1ll11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᒳ")] = method if method else bstack1ll11_opy_ (u"ࠣࠤᒴ")
            arg[bstack1ll11_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᒵ")] = self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᒶ")]
            arg[bstack1ll11_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᒷ")] = self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᒸ")]
            arg[bstack1ll11_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᒹ")] = self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᒺ")]
            arg[bstack1ll11_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᒻ")] = self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᒼ")]
            arg[bstack1ll11_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᒽ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l11l1l1ll1_opy_ = self.bstack1l11lll1111_opy_(bstack1ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᒾ"), self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᒿ")])
            if bstack1ll11_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᓀ") in bstack1l11l1l1ll1_opy_:
                bstack1l11l1l1ll1_opy_ = bstack1l11l1l1ll1_opy_.copy()
                bstack1l11l1l1ll1_opy_[bstack1ll11_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᓁ")] = bstack1l11l1l1ll1_opy_.pop(bstack1ll11_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᓂ"))
            arg = bstack1l11ll11111_opy_(arg, bstack1l11l1l1ll1_opy_)
            bstack1l11l1l11ll_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l11l1l11ll_opy_)
            return
        instance = bstack111l1ll111_opy_.bstack1ll111l1lll_opy_(driver)
        if instance:
            if not bstack111l1ll111_opy_.bstack1ll1ll1l1l1_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11l1l1l11_opy_, False):
                bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11l1l1l11_opy_, True)
            else:
                self.logger.info(bstack1ll11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᓃ") + str(method) + bstack1ll11_opy_ (u"ࠥࠦᓄ"))
                return
        self.logger.info(bstack1ll11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᓅ") + str(method) + bstack1ll11_opy_ (u"ࠧࠨᓆ"))
        if framework_name == bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᓇ"):
            result = self.bstack1l11ll111ll_opy_.bstack1l11lllll11_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack1ll11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᓈ"): method if method else bstack1ll11_opy_ (u"ࠣࠤᓉ")})
        bstack11ll11l1ll_opy_.end(EVENTS.bstack11ll1ll1l1_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᓊ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᓋ"), True, None, command=method)
        if instance:
            bstack111l1ll111_opy_.bstack1l11lllll_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l11l1l1l11_opy_, False)
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᓌ"), datetime.now() - bstack11l111ll1_opy_)
        return result
        def bstack1l11llll1l1_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l1111l11_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l11l1ll111_opy_ = self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᓍ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᓎ"), bstack1ll11_opy_ (u"ࠧ࠱ࠩᓏ")))
            req.client_worker_id = bstack1ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᓐ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1ll1ll111_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᓑ") + str(r) + bstack1ll11_opy_ (u"ࠥࠦᓒ"))
                else:
                    bstack1l1l11111l1_opy_ = json.loads(r.bstack1l11llll111_opy_.decode(bstack1ll11_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᓓ")))
                    if result_type == bstack1ll11_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᓔ"):
                        return bstack1l1l11111l1_opy_.get(bstack1ll11_opy_ (u"ࠨࡤࡢࡶࡤࠦᓕ"), [])
                    else:
                        return bstack1l1l11111l1_opy_.get(bstack1ll11_opy_ (u"ࠢࡥࡣࡷࡥࠧᓖ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1ll11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᓗ") + str(e) + bstack1ll11_opy_ (u"ࠤࠥᓘ"))
    @measure(event_name=EVENTS.bstack11lllll111_opy_, stage=STAGE.bstack11111llll_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l11lll11l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l11llll1l1_opy_(driver, framework_name, bstack1ll11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᓙ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᓚ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack1ll11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᓛ"), framework_name=framework_name)
            bstack11l111ll1_opy_ = datetime.now()
            if framework_name == bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᓜ"):
                result = self.bstack1l11ll111ll_opy_.bstack1l11lllll11_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack111l1ll111_opy_.bstack1ll111l1lll_opy_(driver)
            if instance:
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᓝ"), datetime.now() - bstack11l111ll1_opy_)
            return result
        finally:
            bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.set()
    @measure(event_name=EVENTS.bstack11l1l111ll_opy_, stage=STAGE.bstack11111llll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack1ll11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᓞ"))
                return
            if self.bstack1l11lll11l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l11llll1l1_opy_(driver, framework_name, bstack1ll11_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᓟ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack1ll11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᓠ"), None)
            if not script_code:
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᓡ") + str(framework_name) + bstack1ll11_opy_ (u"ࠧࠨᓢ"))
                return
            self.perform_scan(driver, method=bstack1ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᓣ"), framework_name=framework_name)
            bstack11l111ll1_opy_ = datetime.now()
            if framework_name == bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᓤ"):
                result = self.bstack1l11ll111ll_opy_.bstack1l11lllll11_opy_(driver, script_code)
                bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack111l1ll111_opy_.bstack1ll111l1lll_opy_(driver)
            if instance:
                instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᓥ"), datetime.now() - bstack11l111ll1_opy_)
            return result
        finally:
            bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.set()
    @measure(event_name=EVENTS.bstack1l11lll1ll1_opy_, stage=STAGE.bstack11111llll_opy_)
    def bstack1l1l111l1l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l1111l11_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᓦ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1ll1ll111_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᓧ") + str(r) + bstack1ll11_opy_ (u"ࠦࠧᓨ"))
            else:
                self.bstack1l1l1111lll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᓩ") + str(e) + bstack1ll11_opy_ (u"ࠨࠢᓪ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1111lll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll11_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᓫ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l11lll11l1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨᓬ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l11ll1l1l1_opy_[bstack1ll11_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᓭ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l11ll1l1l1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l11ll11l1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l11ll11l1l_opy_:
                        bstack1l11ll11l1l_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l11ll11l1l_opy_[command.method]:
                        bstack1l11ll11l1l_opy_[command.method][command.name] = list()
                    bstack1l11ll11l1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l11ll11l1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1l111l111_opy_(
        self,
        f: bstack1ll11111111_opy_,
        exec: Tuple[bstack1ll111lllll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l11ll111ll_opy_, bstack1l1llll11l1_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack1ll11_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᓮ"):
                    return
        if f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l1l11l111l_opy_, False) == True:
            return
        bstack1l1l111ll1l_opy_ = False
        desired_capabilities = f.bstack1l1l111111l_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack1l11ll11lll_opy_(instance)
            platform_index = f.bstack1ll1ll1l1l1_opy_(instance, bstack1ll11111111_opy_.bstack1l11llll11l_opy_, 0)
            bstack1l11llllll1_opy_ = datetime.now()
            r = self.bstack1l1l111l1l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1111111ll1_opy_(bstack1ll11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᓯ"), datetime.now() - bstack1l11llllll1_opy_)
            bstack1l1l111ll1l_opy_ = r.success
            f.bstack1l11lllll_opy_(instance, bstack1ll1ll1111l_opy_.bstack1l1l11l111l_opy_, bstack1l1l111ll1l_opy_)
        else:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧ࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡲࡴࡺࠠࡺࡧࡷࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠬࠡࡹ࡬ࡰࡱࠦࡲࡦࡶࡵࡽࠥࡵ࡮ࠡࡰࡨࡼࡹࠦ࡫ࡦࡻࡺࡳࡷࡪࠢᓰ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l1l111l1l1_opy_ = self.config.get(bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᓱ"))
        if not bstack1l1l111l1l1_opy_:
            return True
        try:
            include_tags = bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᓲ")] if bstack1ll11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᓳ") in bstack1l1l111l1l1_opy_ and isinstance(bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᓴ")], list) else []
            exclude_tags = bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᓵ")] if bstack1ll11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᓶ") in bstack1l1l111l1l1_opy_ and isinstance(bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᓷ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᓸ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l11lll11l1_opy_:
                bstack1l11l1ll11l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᓹ"))
                if bstack1l11l1ll11l_opy_ is not None and str(bstack1l11l1ll11l_opy_).lower() == bstack1ll11_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᓺ"):
                    bstack1l11ll1l11l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᓻ")) or caps.get(bstack1ll11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᓼ"))
                    if bstack1l11ll1l11l_opy_ is not None and int(bstack1l11ll1l11l_opy_) < 11:
                        self.logger.warning(bstack1ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡆࡴࡤࡳࡱ࡬ࡨࠥ࠷࠱ࠡࡣࡱࡨࠥࡧࡢࡰࡸࡨ࠲ࠥࡉࡵࡳࡴࡨࡲࡹࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡀࠤࢀࢃ࠮ࠣᓽ").format(bstack1l11ll1l11l_opy_))
                        return False
                return True
            bstack1l11lll1l1l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᓾ"), {}).get(bstack1ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᓿ"), caps.get(bstack1ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᔀ"), bstack1ll11_opy_ (u"ࠨࠩᔁ")))
            if bstack1l11lll1l1l_opy_:
                self.logger.warning(bstack1ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᔂ"))
                return False
            browser = caps.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᔃ"), bstack1ll11_opy_ (u"ࠫࠬᔄ")).lower()
            if browser != bstack1ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᔅ"):
                self.logger.warning(bstack1ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᔆ"))
                return False
            bstack1l11lll111l_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack1ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᔇ")) or self.config.get(bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᔈ")):
                bstack1l11lll111l_opy_ = bstack1l1l11l1111_opy_
            browser_version = caps.get(bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᔉ"))
            if not browser_version:
                browser_version = caps.get(bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᔊ"), {}).get(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᔋ"), bstack1ll11_opy_ (u"ࠬ࠭ᔌ"))
            bstack1l11l1l1111_opy_ = str(browser_version).lower() if browser_version is not None else bstack1ll11_opy_ (u"࠭ࠧᔍ")
            if bstack1l11l1l1111_opy_:
                if bstack1l11l1l1111_opy_.startswith(bstack1ll11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᔎ")):
                    if bstack1l11l1l1111_opy_.startswith(bstack1ll11_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴ࠮ࠩᔏ")):
                        bstack1l1l111l1ll_opy_ = bstack1l11l1l1111_opy_[len(bstack1ll11_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵ࠯ࠪᔐ")):]
                        if bstack1l1l111l1ll_opy_ and not bstack1l1l111l1ll_opy_.isdigit():
                            self.logger.warning(bstack1ll11_opy_ (u"ࠥࡍࡳࡼࡡ࡭࡫ࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡦࡰࡴࡰࡥࡹࠦࠧࡼࡿࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࠨ࡮ࡤࡸࡪࡹࡴࠨࠢࡲࡶࠥ࠭࡬ࡢࡶࡨࡷࡹ࠳࠼࡯ࡷࡰࡦࡪࡸ࠾ࠨ࠰ࠥᔑ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack1l11l1l1111_opy_.split(bstack1ll11_opy_ (u"ࠫ࠳࠭ᔒ"))[0]) <= bstack1l11lll111l_opy_:
                            self.logger.warning(bstack1ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻࡾ࠰ࠥᔓ").format(bstack1l11lll111l_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࠫࢀࢃࠧ࠻ࠢࡾࢁࠧᔔ").format(browser_version, e))
            bstack1l1l111l11l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᔕ"), {}).get(bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᔖ"))
            if not bstack1l1l111l11l_opy_:
                bstack1l1l111l11l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᔗ"), {})
            if not bstack1l1l111l11l_opy_:
                bstack1l1l111l11l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᔘ"), {})
            if bstack1l1l111l11l_opy_ and any(arg == bstack1ll11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᔙ") or (arg.startswith(bstack1ll11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪᔚ")) and arg != bstack1ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧᔛ"))
                                     for arg in bstack1l1l111l11l_opy_.get(bstack1ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᔜ"), [])):
                self.logger.warning(bstack1ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᔝ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᔞ") + str(error))
            return False
    def bstack1l11l1l11l1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l11ll1ll11_opy_ = {
            bstack1ll11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᔟ"): test_uuid,
        }
        bstack1l11l11ll1l_opy_ = {}
        if result.success:
            bstack1l11l11ll1l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l11ll11111_opy_(bstack1l11ll1ll11_opy_, bstack1l11l11ll1l_opy_)
    def bstack1l11lll1111_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1ll11_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡨࡸࡨ࡮ࠠࡤࡧࡱࡸࡷࡧ࡬ࠡࡣࡸࡸ࡭ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡳࡤࡴ࡬ࡴࡹࠦ࡮ࡢ࡯ࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡤࡣࡦ࡬ࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡨࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡫࡫ࡴࡤࡪࡨࡨ࠱ࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠢ࡯ࡳࡦࡪࡳࠡࡣࡱࡨࠥࡩࡡࡤࡪࡨࡷࠥ࡯ࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡎࡢ࡯ࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡸࡩࡲࡪࡲࡷࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡴࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡵࡶ࡫ࡧ࠾࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠬࠡࡧࡰࡴࡹࡿࠠࡥ࡫ࡦࡸࠥ࡯ࡦࠡࡧࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᔠ")
        try:
            if self.bstack1l1l1111ll1_opy_:
                return self.bstack1l11ll1lll1_opy_
            self.bstack1l1l1111l11_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᔡ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᔢ"), bstack1ll11_opy_ (u"ࠧ࠱ࠩᔣ")))
            req.client_worker_id = bstack1ll11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᔤ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1ll1ll111_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l11ll1lll1_opy_ = self.bstack1l11l1l11l1_opy_(test_uuid, r)
                self.bstack1l1l1111ll1_opy_ = True
            else:
                self.logger.error(bstack1ll11_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦᔥ") + str(r.error) + bstack1ll11_opy_ (u"ࠥࠦᔦ"))
                self.bstack1l11ll1lll1_opy_ = dict()
            return self.bstack1l11ll1lll1_opy_
        except Exception as e:
            self.logger.error(bstack1ll11_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᔧ") + str(traceback.format_exc()) + bstack1ll11_opy_ (u"ࠧࠨᔨ"))
            return dict()
    def bstack1l1l1ll1l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l11ll1ll1_opy_ = None
        bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.clear()
        try:
            self.bstack1l1l1111l11_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᔩ")
            req.script_name = bstack1ll11_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᔪ")
            req.platform_index = str(os.environ.get(bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᔫ"), bstack1ll11_opy_ (u"ࠩ࠳ࠫᔬ")))
            req.client_worker_id = bstack1ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᔭ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1ll1ll111_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1ll11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᔮ") + str(r.error) + bstack1ll11_opy_ (u"ࠧࠨᔯ"))
            else:
                bstack1l11ll1ll11_opy_ = self.bstack1l11l1l11l1_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack1ll11_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᔰ") + str(bstack1l11ll1ll11_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack1ll11_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᔱ") + str(framework_name) + bstack1ll11_opy_ (u"ࠣࠢࠥᔲ"))
                return
            bstack1l11ll1ll1_opy_ = bstack11ll11l1ll_opy_.bstack11l11l111_opy_(EVENTS.bstack1l11l1ll1ll_opy_.value)
            self.bstack1l11ll11l11_opy_(driver, script_code, bstack1l11ll1ll11_opy_, framework_name)
            try:
                bstack1l1l1111111_opy_ = {
                    bstack1ll11_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᔳ"): {
                        bstack1ll11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᔴ"): bstack1ll11_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᔵ"),
                    },
                    bstack1ll11_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᔶ"): {
                        bstack1ll11_opy_ (u"ࠨࡢࡰࡦࡼࠦᔷ"): {
                            bstack1ll11_opy_ (u"ࠢ࡮ࡵࡪࠦᔸ"): bstack1ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᔹ"),
                            bstack1ll11_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᔺ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l1l1111111_opy_, separators=(bstack1ll11_opy_ (u"ࠪ࠰ࠬᔻ"), bstack1ll11_opy_ (u"ࠫ࠿࠭ᔼ"))))
            except Exception as bstack1ll1l1llll_opy_:
                self.logger.debug(bstack1ll11_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᔽ") + str(bstack1ll1l1llll_opy_) + bstack1ll11_opy_ (u"ࠨࠢᔾ"))
            self.logger.info(bstack1ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᔿ"))
            bstack11ll11l1ll_opy_.end(EVENTS.bstack1l11l1ll1ll_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᕀ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᕁ"), True, None, command=bstack1ll11_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᕂ"),test_name=name)
        except Exception as bstack1l11ll111l1_opy_:
            self.logger.error(bstack1ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᕃ") + bstack1ll11_opy_ (u"ࠧࡹࡴࡳࠪࡳࡥࡹ࡮ࠩࠣᕄ") + bstack1ll11_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᕅ") + str(bstack1l11ll111l1_opy_))
            bstack11ll11l1ll_opy_.end(EVENTS.bstack1l11l1ll1ll_opy_.value, bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᕆ"), bstack1l11ll1ll1_opy_+bstack1ll11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᕇ"), False, bstack1l11ll111l1_opy_, command=bstack1ll11_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᕈ"),test_name=name)
        finally:
            bstack1ll1ll1111l_opy_._1ll1ll111ll_opy_.set()
    def bstack1ll1ll1ll1l_opy_(self):
        bstack1ll11_opy_ (u"ࠥࠦࠧࡉࡡ࡭࡮ࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡶࡴࡨ࡯ࡵࡡ࡯࡭ࡸࡺࡥ࡯ࡧࡵࡣࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠡࡹ࡫ࡩࡳࠦࡡࠡࡥ࡯ࡳࡸ࡫ࠠ࡬ࡧࡼࡻࡴࡸࡤࠡ࡫ࡶࠤࡦࡨ࡯ࡶࡶࠣࡸࡴࠦࡥࡹࡧࡦࡹࡹ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᕉ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack1ll11_opy_ (u"ࠦࡸࡺ࡯ࡱࡡࡦࡥࡵࡺࡵࡳࡧࡢࡦࡪ࡬࡯ࡳࡧࡢࡦࡷࡵࡷࡴࡧࡵࡣࡨࡲ࡯ࡴࡧ࠽ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠨᕊ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack1ll11_opy_ (u"ࠧࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࡣࡧ࡫ࡦࡰࡴࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࡣࡳࡧ࡭ࡦࠢࡲࡶࠥࡺࡥࡴࡶࡢࡹࡺ࡯ࡤ࠭ࠢࡶ࡯࡮ࡶࡰࡪࡰࡪࠦᕋ"))
            return
        self.logger.debug(bstack1ll11_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡴࡶࡲࡴࡤࡺࡥࡴࡶࡢࡧࡦࡶࡴࡶࡴࡨࠦᕌ"))
        self.bstack1l1l1ll1l_opy_(None, self._current_test_name, bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᕍ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack1l11ll11l11_opy_(self, driver, script_code, bstack1l11ll1ll11_opy_, framework_name):
        if framework_name == bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᕎ"):
            self.bstack1l11ll111ll_opy_.bstack1l11lllll11_opy_(driver, script_code, bstack1l11ll1ll11_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l11ll1ll11_opy_))
    def _1l11lllll1l_opy_(self, instance: bstack1l1l1l111l1_opy_, args: Tuple) -> list:
        bstack1ll11_opy_ (u"ࠤࠥࠦࡊࡾࡴࡳࡣࡦࡸࠥࡺࡡࡨࡵࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᕏ")
        if bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᕐ") in instance.bstack1l1l111lll1_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll11_opy_ (u"ࠫࡹࡧࡧࡴࠩᕑ")) else []
        if hasattr(args[0], bstack1ll11_opy_ (u"ࠬࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠪᕒ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack1ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫᕓ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l1l1111l1l_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)