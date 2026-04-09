# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack11l1l1l11_opy_ import (
    bstack11111l1ll_opy_,
    bstack111llll1ll_opy_,
    bstack1lll1111ll_opy_,
    bstack1l1lll111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l11l111111_opy_ import bstack1l1l1ll11ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1l1l111ll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l111llllll_opy_ import bstack1l11ll11111_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1l11111_opy_ import bstack1l1l111ll11_opy_
from browserstack_sdk.sdk_cli.bstack1l1l1ll1lll_opy_ import bstack1l11l11llll_opy_
from browserstack_sdk.sdk_cli.bstack1l11111ll1_opy_ import bstack1111l11l1l_opy_
from bstack_utils.helper import bstack1l111ll11l1_opy_, is_robot_playwright_installed
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1l1llllll1l_opy_(bstack1l11ll11111_opy_):
    bstack11llllllll1_opy_ = False
    bstack1l111ll1l1l_opy_ = bstack11ll11_opy_ (u"ࠢࡴࡧ࡯ࡩࡳ࡯ࡵ࡮࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᖓ")
    bstack1l111111111_opy_ = bstack11ll11_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥ࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦᖔ")
    bstack1l11111lll1_opy_ = bstack11ll11_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡲ࡮ࡺࠢᖕ")
    bstack1l111111l1l_opy_ = bstack11ll11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡸࡥࡳࡤࡣࡱࡲ࡮ࡴࡧࠣᖖ")
    bstack1l111l1l111_opy_ = bstack11ll11_opy_ (u"ࠦࡩࡸࡩࡷࡧࡵࡣ࡭ࡧࡳࡠࡷࡵࡰࠧᖗ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    _1l1lllll111_opy_ = threading.Event()
    _1l1lllll111_opy_.set()
    def __init__(self, bstack1l11ll1l111_opy_, bstack1l11lll1l11_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1111111l1_opy_ = False
        self.bstack1l111l111l1_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l1111ll1l1_opy_ = False
        self.bstack11llllll111_opy_ = dict()
        self.save_result_done = False
        self._current_test_name = None
        self._current_test_uuid = None
        if not self.is_enabled():
            return
        self.bstack1l11111llll_opy_ = bstack1l11lll1l11_opy_
        bstack1l11ll1l111_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll1111lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack1ll1111l11l_opy_)
        bstack1l11ll1l111_opy_.bstack1l111l11l11_opy_((bstack11111l1ll_opy_.bstack1ll11lll1_opy_, bstack111llll1ll_opy_.PRE), self.bstack11llllll1ll_opy_)
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1111lll11_opy_)
        TestFramework.bstack1l111l11l11_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1111l11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._11lllll11ll_opy_(instance, args)
        test_framework = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111ll1111_opy_)
        if self.bstack1l1111111l1_opy_:
            self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᖘ")] = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l11l1l_opy_)
        if bstack11ll11_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪᖙ") in instance.bstack1l1l11l1l11_opy_:
            platform_index = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
            self.accessibility = self.bstack1l1111l1l11_opy_(tags, self.config[bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᖚ")][platform_index])
        elif test_framework == bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮࠮ࡩࡨࡲࡪࡸࡩࡤࠩᖛ"):
            platform_index = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l1lll1_opy_)
            self.accessibility = self.bstack1l1111l1l11_opy_(tags, self.config[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᖜ")][platform_index])
        elif is_robot_playwright_installed():
            self.accessibility = self.is_enabled_testcase(tags)
            self._current_test_name = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l11111l111_opy_)
            self._current_test_uuid = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l11l1l_opy_)
            self.save_result_done = False
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡸ࡯ࡣࡱࡷ࠱ࡵࡽࠠࡵࡣࡪࡷ࠲ࡵ࡮࡭ࡻࠣࡧ࡭࡫ࡣ࡬࠮ࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡀࠦᖝ") + str(self.accessibility) + bstack11ll11_opy_ (u"ࠦࠧᖞ"))
        else:
            capabilities = self.bstack1l11111llll_opy_.bstack1l11111l1ll_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᖟ") + str(kwargs) + bstack11ll11_opy_ (u"ࠨࠢᖠ"))
                return
            self.accessibility = self.bstack1l1111l1l11_opy_(tags, capabilities)
        if self.bstack1l11111llll_opy_.pages and self.bstack1l11111llll_opy_.pages.values():
            bstack1l1111ll1ll_opy_ = list(self.bstack1l11111llll_opy_.pages.values())
            if bstack1l1111ll1ll_opy_ and isinstance(bstack1l1111ll1ll_opy_[0], (list, tuple)) and bstack1l1111ll1ll_opy_[0]:
                bstack1l111l11111_opy_ = bstack1l1111ll1ll_opy_[0][0]
                if callable(bstack1l111l11111_opy_):
                    page = bstack1l111l11111_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᖡ"))
                    def bstack1l11111ll11_opy_():
                        self.get_accessibility_results_summary(page, bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᖢ"))
                    setattr(page, bstack11ll11_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᖣ"), get_results)
                    setattr(page, bstack11ll11_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᖤ"), bstack1l11111ll11_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᖥ") + str(self.accessibility) + bstack11ll11_opy_ (u"ࠧࠨᖦ"))
    def bstack11llllll1ll_opy_(
        self,
        f,
        target,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result,
        *args,
        **kwargs,
    ):
        bstack11ll11_opy_ (u"ࠨࠢࠣࡅࡤࡰࡱ࡫ࡤࠡࡣࡷࠤࡈࡘࡅࡂࡖࡈ࠲ࡕࡘࡅࠡࡣࡩࡸࡪࡸࠠࡅࡴ࡬ࡺࡪࡸࡉ࡯࡫ࡷࠤ࡮ࡴࠠࡓࡱࡥࡳࡹ࠳ࡐࡘࠢࡩࡰࡴࡽ࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩ࡫࡯࡮ࡦࡵࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡪࡱࡧࡧࠡࡹ࡬ࡸ࡭ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡦ࡬ࡪࡩ࡫࠯ࠤࠥࠦᖧ")
        if not self.accessibility:
            return
        capabilities = self.bstack1l11111llll_opy_.bstack1l11111l1ll_opy_(None, None, None)
        if not capabilities:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡨࡷ࡯ࡶࡦࡴࡢࡧࡷ࡫ࡡࡵࡧ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠤᖨ"))
            return
        bstack1ll1l1l1ll1_opy_ = self.is_platform_supported(capabilities)
        self.accessibility = self.accessibility and bstack1ll1l1l1ll1_opy_
        self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡩࡸࡩࡷࡧࡵࡣࡨࡸࡥࡢࡶࡨ࠾ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡿ࠯ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡁࠧᖩ") + str(self.accessibility) + bstack11ll11_opy_ (u"ࠤࠥᖪ"))
    def bstack1ll1111l11l_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        driver: object,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        bstack1l1ll1l11l1_opy_: Tuple[bstack11111l1ll_opy_, bstack111llll1ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l111111ll1_opy_(method_name, *args):
                bstack1l111ll1ll_opy_ = datetime.now()
                self.bstack1l111l1llll_opy_(f, exec, *args, **kwargs)
                instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᖫ"), datetime.now() - bstack1l111ll1ll_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࡲ࡮ࡴࡧࠣᖬ"))
                return
            bstack1l111ll1ll_opy_ = datetime.now()
            self.bstack1l111l1llll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᖭ"), datetime.now() - bstack1l111ll1ll_opy_)
            bstack1l1ll11llll_opy_ = instance.data.get(bstack11ll11_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᖮ"), None)
            if (
                not f.bstack1l111l1l1l1_opy_(method_name)
                or f.bstack1l11111111l_opy_(method_name, *args)
                or f.bstack1l111111lll_opy_(method_name, *args)
                or (bstack1l1ll11llll_opy_ and int(bstack1l1ll11llll_opy_)>1)
            ):
                return
            if not f.bstack1ll111l1111_opy_(instance, bstack1l1llllll1l_opy_.bstack1l11111lll1_opy_, False):
                if not bstack1l1llllll1l_opy_.bstack11llllllll1_opy_:
                    self.logger.warning(bstack11ll11_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᖯ") + str(f.platform_index) + bstack11ll11_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᖰ"))
                    bstack1l1llllll1l_opy_.bstack11llllllll1_opy_ = True
                return
            bstack1l1111lllll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1111lllll_opy_:
                platform_index = f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_, 0)
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᖱ") + str(f.framework_name) + bstack11ll11_opy_ (u"ࠥࠦᖲ"))
                return
            command_name = f.bstack1l111ll11ll_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᖳ") + str(method_name) + bstack11ll11_opy_ (u"ࠧࠨᖴ"))
                return
            if f.framework_name != bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᖵ"):
                bstack1l111l1l11l_opy_ = f.bstack1ll111l1111_opy_(instance, bstack1l1llllll1l_opy_.bstack1l111l1l111_opy_, False)
                if command_name == bstack11ll11_opy_ (u"ࠢࡨࡧࡷࠦᖶ") and not bstack1l111l1l11l_opy_:
                    f.bstack1l1l1111l1_opy_(instance, bstack1l1llllll1l_opy_.bstack1l111l1l111_opy_, True)
                    bstack1l111l1l11l_opy_ = True
                if not bstack1l111l1l11l_opy_ and not self.bstack1l1111111l1_opy_:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᖷ") + str(command_name) + bstack11ll11_opy_ (u"ࠤࠥᖸ"))
                    return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᖹ") + str(command_name) + bstack11ll11_opy_ (u"ࠦࠧᖺ"))
                return
            self.logger.info(bstack11ll11_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᖻ") + str(command_name) + bstack11ll11_opy_ (u"ࠨࠢᖼ"))
            scripts = [(s, bstack1l1111lllll_opy_[s]) for s in scripts_to_run if s in bstack1l1111lllll_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack1l111ll1ll_opy_ = datetime.now()
                    if script_name == bstack11ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᖽ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack11ll11_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤᖾ"): {
                                    bstack11ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥᖿ"): bstack11ll11_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡆࡅࡓࠨᗀ"),
                                    bstack11ll11_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠣᗁ"): [
                                        {
                                            bstack11ll11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᗂ"): command_name
                                        }
                                    ]
                                },
                                bstack11ll11_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᗃ"): {
                                    bstack11ll11_opy_ (u"ࠢࡣࡱࡧࡽࠧᗄ"): {
                                        bstack11ll11_opy_ (u"ࠣ࡯ࡶ࡫ࠧᗅ"): result.get(bstack11ll11_opy_ (u"ࠤࡰࡷ࡬ࠨᗆ"), bstack11ll11_opy_ (u"ࠥࠦᗇ")) if isinstance(result, dict) else bstack11ll11_opy_ (u"ࠦࠧᗈ"),
                                        bstack11ll11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᗉ"): result.get(bstack11ll11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᗊ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack11ll11_opy_ (u"ࠢ࠭ࠤᗋ"), bstack11ll11_opy_ (u"ࠣ࠼ࠥᗌ"))))
                        except Exception as bstack1ll1l1l1ll_opy_:
                            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࠢᗍ") + str(bstack1ll1l1l1ll_opy_) + bstack11ll11_opy_ (u"ࠥࠦᗎ"))
                    instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᗏ") + script_name, datetime.now() - bstack1l111ll1ll_opy_)
                    if isinstance(result, dict) and not result.get(bstack11ll11_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᗐ"), True):
                        self.logger.warning(bstack11ll11_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᗑ") + str(result) + bstack11ll11_opy_ (u"ࠢࠣᗒ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᗓ") + str(e) + bstack11ll11_opy_ (u"ࠤࠥᗔ"))
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᗕ") + str(e) + bstack11ll11_opy_ (u"ࠦࠧᗖ"))
    def bstack1l1111l11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1l111ll1l_opy_,
        bstack1l1ll1l11l1_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᗗ") not in instance.bstack1l1l11l1l11_opy_:
            tags = self._11lllll11ll_opy_(instance, args)
            capabilities = self.bstack1l11111llll_opy_.bstack1l11111l1ll_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l1111l1l11_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᗘ"))
            return
        driver = self.bstack1l11111llll_opy_.bstack1l1111ll111_opy_(f, instance, bstack1l1ll1l11l1_opy_, *args, **kwargs)
        test_name = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l11111l111_opy_)
        if not test_name:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᗙ"))
            return
        test_uuid = f.bstack1ll111l1111_opy_(instance, TestFramework.bstack1l111l11l1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᗚ"))
            return
        if isinstance(self.bstack1l11111llll_opy_, bstack1l11l11llll_opy_):
            framework_name = bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᗛ")
        else:
            framework_name = bstack11ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᗜ")
        if not self.save_result_done:
            self.bstack1111l1l111_opy_(driver, test_name, framework_name, test_uuid)
            self.save_result_done = True
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack1lll1l1ll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᗝ"))
            return
        bstack1l111ll1ll_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack11ll11_opy_ (u"ࠧࡹࡣࡢࡰࠥᗞ"), None)
        if not script_code:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᗟ") + str(framework_name) + bstack11ll11_opy_ (u"ࠢࠡࠤᗠ"))
            return
        if self.bstack1l1111111l1_opy_:
            arg = dict()
            arg[bstack11ll11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᗡ")] = method if method else bstack11ll11_opy_ (u"ࠤࠥᗢ")
            arg[bstack11ll11_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥᗣ")] = self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᗤ")]
            arg[bstack11ll11_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥᗥ")] = self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᗦ")]
            arg[bstack11ll11_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᗧ")] = self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨᗨ")]
            arg[bstack11ll11_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨᗩ")] = self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᗪ")]
            arg[bstack11ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦᗫ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l111l1l1ll_opy_ = self.bstack1l1111l111l_opy_(bstack11ll11_opy_ (u"ࠧࡹࡣࡢࡰࠥᗬ"), self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᗭ")])
            if bstack11ll11_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥᗮ") in bstack1l111l1l1ll_opy_:
                bstack1l111l1l1ll_opy_ = bstack1l111l1l1ll_opy_.copy()
                bstack1l111l1l1ll_opy_[bstack11ll11_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧᗯ")] = bstack1l111l1l1ll_opy_.pop(bstack11ll11_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧᗰ"))
            arg = bstack1l111ll11l1_opy_(arg, bstack1l111l1l1ll_opy_)
            bstack1l1111l1l1l_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l1111l1l1l_opy_)
            return
        instance = bstack1lll1111ll_opy_.bstack1l1ll1ll111_opy_(driver)
        if instance:
            if not bstack1lll1111ll_opy_.bstack1ll111l1111_opy_(instance, bstack1l1llllll1l_opy_.bstack1l111111l1l_opy_, False):
                bstack1lll1111ll_opy_.bstack1l1l1111l1_opy_(instance, bstack1l1llllll1l_opy_.bstack1l111111l1l_opy_, True)
            else:
                self.logger.info(bstack11ll11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᗱ") + str(method) + bstack11ll11_opy_ (u"ࠦࠧᗲ"))
                return
        self.logger.info(bstack11ll11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᗳ") + str(method) + bstack11ll11_opy_ (u"ࠨࠢᗴ"))
        if framework_name == bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᗵ"):
            result = self.bstack1l11111llll_opy_.bstack1l111l111ll_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack11ll11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᗶ"): method if method else bstack11ll11_opy_ (u"ࠤࠥᗷ")})
        bstack1ll111lll_opy_.end(EVENTS.bstack1lll1l1ll1_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᗸ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᗹ"), True, None, command=method)
        if instance:
            bstack1lll1111ll_opy_.bstack1l1l1111l1_opy_(instance, bstack1l1llllll1l_opy_.bstack1l111111l1l_opy_, False)
            instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤᗺ"), datetime.now() - bstack1l111ll1ll_opy_)
        return result
        def bstack1l1111l1111_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l11111l1l1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l111l11ll1_opy_ = self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᗻ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᗼ"), bstack11ll11_opy_ (u"ࠨ࠲ࠪᗽ")))
            req.client_worker_id = bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᗾ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1l111l1_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11ll11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᗿ") + str(r) + bstack11ll11_opy_ (u"ࠦࠧᘀ"))
                else:
                    bstack1l111l1ll1l_opy_ = json.loads(r.bstack1l1111l1lll_opy_.decode(bstack11ll11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᘁ")))
                    if result_type == bstack11ll11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᘂ"):
                        return bstack1l111l1ll1l_opy_.get(bstack11ll11_opy_ (u"ࠢࡥࡣࡷࡥࠧᘃ"), [])
                    else:
                        return bstack1l111l1ll1l_opy_.get(bstack11ll11_opy_ (u"ࠣࡦࡤࡸࡦࠨᘄ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11ll11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡵࡶ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡩ࡬ࡪ࠼ࠣࠦᘅ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦᘆ"))
    @measure(event_name=EVENTS.bstack1l1111l1l1_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def get_accessibility_results(self, driver, framework_name):
        bstack1l1llllll1l_opy_._1l1lllll111_opy_.clear()
        try:
            if not self.accessibility:
                return
            if self.bstack1l1111111l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l1111l1111_opy_(driver, framework_name, bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᘇ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᘈ"), None)
            if not script_code:
                return
            self.perform_scan(driver, method=bstack11ll11_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᘉ"), framework_name=framework_name)
            bstack1l111ll1ll_opy_ = datetime.now()
            if framework_name == bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᘊ"):
                result = self.bstack1l11111llll_opy_.bstack1l111l111ll_opy_(driver, script_code)
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1lll1111ll_opy_.bstack1l1ll1ll111_opy_(driver)
            if instance:
                instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦᘋ"), datetime.now() - bstack1l111ll1ll_opy_)
            return result
        finally:
            bstack1l1llllll1l_opy_._1l1lllll111_opy_.set()
    @measure(event_name=EVENTS.bstack11ll1l1ll1_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        bstack1l1llllll1l_opy_._1l1lllll111_opy_.clear()
        try:
            if not self.accessibility:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᘌ"))
                return
            if self.bstack1l1111111l1_opy_:
                self.perform_scan(driver, method=None, framework_name=framework_name)
                return self.bstack1l1111l1111_opy_(driver, framework_name, bstack11ll11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧᘍ"))
            script_code = self.scripts.get(framework_name, {}).get(bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᘎ"), None)
            if not script_code:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᘏ") + str(framework_name) + bstack11ll11_opy_ (u"ࠨࠢᘐ"))
                return
            self.perform_scan(driver, method=bstack11ll11_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᘑ"), framework_name=framework_name)
            bstack1l111ll1ll_opy_ = datetime.now()
            if framework_name == bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᘒ"):
                result = self.bstack1l11111llll_opy_.bstack1l111l111ll_opy_(driver, script_code)
                bstack1l1llllll1l_opy_._1l1lllll111_opy_.set()
            else:
                result = driver.execute_async_script(script_code)
            instance = bstack1lll1111ll_opy_.bstack1l1ll1ll111_opy_(driver)
            if instance:
                instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᘓ"), datetime.now() - bstack1l111ll1ll_opy_)
            return result
        finally:
            bstack1l1llllll1l_opy_._1l1lllll111_opy_.set()
    @measure(event_name=EVENTS.bstack1l11111ll1l_opy_, stage=STAGE.bstack1111l1111l_opy_)
    def bstack1l1111lll1l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l11111l1l1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᘔ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1l111l1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᘕ") + str(r) + bstack11ll11_opy_ (u"ࠧࠨᘖ"))
            else:
                self.bstack1l1111l1ll1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᘗ") + str(e) + bstack11ll11_opy_ (u"ࠢࠣᘘ"))
            traceback.print_exc()
            raise e
    def bstack1l1111l1ll1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᘙ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1111111l1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᘚ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l111l111l1_opy_[bstack11ll11_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᘛ")] = result.testhub.jwt
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
                bstack1l1111llll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.method and not command.method in bstack1l1111llll1_opy_:
                        bstack1l1111llll1_opy_[command.method] = dict()
                    if command.name and not command.name in bstack1l1111llll1_opy_[command.method]:
                        bstack1l1111llll1_opy_[command.method][command.name] = list()
                    bstack1l1111llll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1111llll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l111l1llll_opy_(
        self,
        f: bstack1l1l1ll11ll_opy_,
        exec: Tuple[bstack1l1lll111ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l11111llll_opy_, bstack1l11l11llll_opy_):
            if not is_robot_playwright_installed():
                if method_name != bstack11ll11_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᘜ"):
                    return
        if f.bstack1ll111l1111_opy_(instance, bstack1l1llllll1l_opy_.bstack1l11111lll1_opy_, False) == True:
            return
        bstack1l111ll111l_opy_ = False
        desired_capabilities = f.bstack11lllllll1l_opy_(instance)
        if isinstance(desired_capabilities, dict):
            hub_url = f.bstack11llllll1l1_opy_(instance)
            platform_index = f.bstack1ll111l1111_opy_(instance, bstack1l1l1ll11ll_opy_.bstack1l111l1lll1_opy_, 0)
            bstack11lllll1l11_opy_ = datetime.now()
            r = self.bstack1l1111lll1l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
            instance.bstack1l1l1111ll_opy_(bstack11ll11_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᘝ"), datetime.now() - bstack11lllll1l11_opy_)
            bstack1l111ll111l_opy_ = r.success
            f.bstack1l1l1111l1_opy_(instance, bstack1l1llllll1l_opy_.bstack1l11111lll1_opy_, bstack1l111ll111l_opy_)
        else:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤࡳࡵࡴࠡࡻࡨࡸࠥࡧࡶࡢ࡫࡯ࡥࡧࡲࡥ࠭ࠢࡺ࡭ࡱࡲࠠࡳࡧࡷࡶࡾࠦ࡯࡯ࠢࡱࡩࡽࡺࠠ࡬ࡧࡼࡻࡴࡸࡤࠣᘞ"))
    def is_enabled_testcase(self, test_tags):
        bstack1l1111lll1l_opy_ = self.config.get(bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᘟ"))
        if not bstack1l1111lll1l_opy_:
            return True
        try:
            include_tags = bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘠ")] if bstack11ll11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘡ") in bstack1l1111lll1l_opy_ and isinstance(bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘢ")], list) else []
            exclude_tags = bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘣ")] if bstack11ll11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘤ") in bstack1l1111lll1l_opy_ and isinstance(bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘥ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᘦ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l1111111l1_opy_:
                bstack1l1111l11ll_opy_ = caps.get(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᘧ"))
                if bstack1l1111l11ll_opy_ is not None and str(bstack1l1111l11ll_opy_).lower() == bstack11ll11_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᘨ"):
                    bstack1l11111l11l_opy_ = caps.get(bstack11ll11_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘩ")) or caps.get(bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᘪ"))
                    if bstack1l11111l11l_opy_ is not None and int(bstack1l11111l11l_opy_) < 11:
                        self.logger.warning(bstack11ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠥࢁࡽ࠯ࠤᘫ").format(bstack1l11111l11l_opy_))
                        return False
                return True
            bstack11lllll1l1l_opy_ = caps.get(bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘬ"), {}).get(bstack11ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᘭ"), caps.get(bstack11ll11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᘮ"), bstack11ll11_opy_ (u"ࠩࠪᘯ")))
            if bstack11lllll1l1l_opy_:
                self.logger.warning(bstack11ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᘰ"))
                return False
            browser = caps.get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᘱ"), bstack11ll11_opy_ (u"ࠬ࠭ᘲ")).lower()
            if browser != bstack11ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᘳ"):
                self.logger.warning(bstack11ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᘴ"))
                return False
            bstack1l111111l11_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᘵ")) or self.config.get(bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᘶ")):
                bstack1l111111l11_opy_ = bstack1l111l11lll_opy_
            browser_version = caps.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᘷ"))
            if not browser_version:
                browser_version = caps.get(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘸ"), {}).get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘹ"), bstack11ll11_opy_ (u"࠭ࠧᘺ"))
            bstack1l111ll1l11_opy_ = str(browser_version).lower() if browser_version is not None else bstack11ll11_opy_ (u"ࠧࠨᘻ")
            if bstack1l111ll1l11_opy_:
                if bstack1l111ll1l11_opy_.startswith(bstack11ll11_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᘼ")):
                    if bstack1l111ll1l11_opy_.startswith(bstack11ll11_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵ࠯ࠪᘽ")):
                        bstack1l1111ll11l_opy_ = bstack1l111ll1l11_opy_[len(bstack11ll11_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᘾ")):]
                        if bstack1l1111ll11l_opy_ and not bstack1l1111ll11l_opy_.isdigit():
                            self.logger.warning(bstack11ll11_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡧࡱࡵࡱࡦࡺࠠࠨࡽࢀࠫࡀࠦࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࠩ࡯ࡥࡹ࡫ࡳࡵࠩࠣࡳࡷࠦࠧ࡭ࡣࡷࡩࡸࡺ࠭࠽ࡰࡸࡱࡧ࡫ࡲ࠿ࠩ࠱ࠦᘿ").format(browser_version))
                            return False
                else:
                    try:
                        if int(bstack1l111ll1l11_opy_.split(bstack11ll11_opy_ (u"ࠬ࠴ࠧᙀ"))[0]) <= bstack1l111111l11_opy_:
                            self.logger.warning(bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼࡿ࠱ࠦᙁ").format(bstack1l111111l11_opy_))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤࠬࢁࡽࠨ࠼ࠣࡿࢂࠨᙂ").format(browser_version, e))
            bstack11lllll1ll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᙃ"), {}).get(bstack11ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙄ"))
            if not bstack11lllll1ll1_opy_:
                bstack11lllll1ll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᙅ"), {})
            if not bstack11lllll1ll1_opy_:
                bstack11lllll1ll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᙆ"), {})
            if bstack11lllll1ll1_opy_ and any(arg == bstack11ll11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᙇ") or (arg.startswith(bstack11ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᙈ")) and arg != bstack11ll11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᙉ"))
                                     for arg in bstack11lllll1ll1_opy_.get(bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᙊ"), [])):
                self.logger.warning(bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᙋ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᙌ") + str(error))
            return False
    def bstack11lllllll11_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack11lllllllll_opy_ = {
            bstack11ll11_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᙍ"): test_uuid,
        }
        bstack1l1111111ll_opy_ = {}
        if result.success:
            bstack1l1111111ll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l111ll11l1_opy_(bstack11lllllllll_opy_, bstack1l1111111ll_opy_)
    def bstack1l1111l111l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11ll11_opy_ (u"ࠧࠨࠢࠋࠢࠣࠤࠥࠦࠠࠡࠢࡉࡩࡹࡩࡨࠡࡥࡨࡲࡹࡸࡡ࡭ࠢࡤࡹࡹ࡮ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡩ࡬ࡺࡪࡴࠠࡴࡥࡵ࡭ࡵࡺࠠ࡯ࡣࡰࡩ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡥࡤࡧ࡭࡫ࡤࠡࡥࡲࡲ࡫࡯ࡧࠡ࡫ࡩࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡬ࡥࡵࡥ࡫ࡩࡩ࠲ࠠࡰࡶ࡫ࡩࡷࡽࡩࡴࡧࠣࡰࡴࡧࡤࡴࠢࡤࡲࡩࠦࡣࡢࡥ࡫ࡩࡸࠦࡩࡵ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡆࡸࡧࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࡀࠠࡏࡣࡰࡩࠥࡵࡦࠡࡶ࡫ࡩࠥࡹࡣࡳ࡫ࡳࡸࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠠࡧࡱࡵࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨ࠿ࠦࡕࡖࡋࡇࠤࡴ࡬ࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡻ࡭࡯ࡣࡩࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠎࠥࠦࠠࠡࠢࠣࠤࠥࡘࡥࡵࡷࡵࡲࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡪࡩࡤࡶ࠽ࠤࡈࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡩ࡯ࡣࡵ࡫ࡲࡲࡦࡸࡹ࠭ࠢࡨࡱࡵࡺࡹࠡࡦ࡬ࡧࡹࠦࡩࡧࠢࡨࡶࡷࡵࡲࠡࡱࡦࡧࡺࡸࡳࠋࠢࠣࠤࠥࠦࠠࠡࠢࠥࠦࠧᙎ")
        try:
            if self.bstack1l1111ll1l1_opy_:
                return self.bstack11llllll111_opy_
            self.bstack1l11111l1l1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᙏ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᙐ"), bstack11ll11_opy_ (u"ࠨ࠲ࠪᙑ")))
            req.client_worker_id = bstack11ll11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᙒ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1l111l1_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack11llllll111_opy_ = self.bstack11lllllll11_opy_(test_uuid, r)
                self.bstack1l1111ll1l1_opy_ = True
            else:
                self.logger.error(bstack11ll11_opy_ (u"ࠥࡪࡪࡺࡣࡩࡅࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡇ࠱࠲ࡻࡆࡳࡳ࡬ࡩࡨ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡪࡲࡪࡸࡨࡶࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡰࡢࡴࡤࡱࡸࠦࡦࡰࡴࠣࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿ࠽ࠤࠧᙓ") + str(r.error) + bstack11ll11_opy_ (u"ࠦࠧᙔ"))
                self.bstack11llllll111_opy_ = dict()
            return self.bstack11llllll111_opy_
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠧ࡬ࡥࡵࡥ࡫ࡇࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡂ࠳࠴ࡽࡈࡵ࡮ࡧ࡫ࡪ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡲࡶࠥࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢᙕ") + str(traceback.format_exc()) + bstack11ll11_opy_ (u"ࠨࠢᙖ"))
            return dict()
    def bstack1111l1l111_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1111l1ll1l_opy_ = None
        bstack1l1llllll1l_opy_._1l1lllll111_opy_.clear()
        try:
            self.bstack1l11111l1l1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢᙗ")
            req.script_name = bstack11ll11_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨᙘ")
            req.platform_index = str(os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩᙙ"), bstack11ll11_opy_ (u"ࠪ࠴ࠬᙚ")))
            req.client_worker_id = bstack11ll11_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᙛ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1l111l1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᙜ") + str(r.error) + bstack11ll11_opy_ (u"ࠨࠢᙝ"))
            else:
                bstack11lllllllll_opy_ = self.bstack11lllllll11_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᙞ") + str(bstack11lllllllll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack11ll11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᙟ") + str(framework_name) + bstack11ll11_opy_ (u"ࠤࠣࠦᙠ"))
                return
            bstack1111l1ll1l_opy_ = bstack1ll111lll_opy_.bstack1ll11l11_opy_(EVENTS.bstack1l111l1ll11_opy_.value)
            self.bstack11lllll1lll_opy_(driver, script_code, bstack11lllllllll_opy_, framework_name)
            try:
                bstack1l111l1111l_opy_ = {
                    bstack11ll11_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦᙡ"): {
                        bstack11ll11_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧᙢ"): bstack11ll11_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡆ࡜ࡅࡠࡔࡈࡗ࡚ࡒࡔࡔࠤᙣ"),
                    },
                    bstack11ll11_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣᙤ"): {
                        bstack11ll11_opy_ (u"ࠢࡣࡱࡧࡽࠧᙥ"): {
                            bstack11ll11_opy_ (u"ࠣ࡯ࡶ࡫ࠧᙦ"): bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᙧ"),
                            bstack11ll11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᙨ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l111l1111l_opy_, separators=(bstack11ll11_opy_ (u"ࠫ࠱࠭ᙩ"), bstack11ll11_opy_ (u"ࠬࡀࠧᙪ"))))
            except Exception as bstack1ll1l1l1ll_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡢࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡪࡡࡵࡣ࠽ࠤࠧᙫ") + str(bstack1ll1l1l1ll_opy_) + bstack11ll11_opy_ (u"ࠢࠣᙬ"))
            self.logger.info(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ᙭"))
            bstack1ll111lll_opy_.end(EVENTS.bstack1l111l1ll11_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᙮"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᙯ"), True, None, command=bstack11ll11_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᙰ"),test_name=name)
        except Exception as bstack11llllll11l_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᙱ") + bstack11ll11_opy_ (u"ࠨࡳࡵࡴࠫࡴࡦࡺࡨࠪࠤᙲ") + bstack11ll11_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᙳ") + str(bstack11llllll11l_opy_))
            bstack1ll111lll_opy_.end(EVENTS.bstack1l111l1ll11_opy_.value, bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᙴ"), bstack1111l1ll1l_opy_+bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᙵ"), False, bstack11llllll11l_opy_, command=bstack11ll11_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᙶ"),test_name=name)
        finally:
            bstack1l1llllll1l_opy_._1l1lllll111_opy_.set()
    def bstack1ll1111ll1l_opy_(self):
        bstack11ll11_opy_ (u"ࠦࠧࠨࡃࡢ࡮࡯ࡩࡩࠦࡦࡳࡱࡰࠤࡷࡵࡢࡰࡶࡢࡰ࡮ࡹࡴࡦࡰࡨࡶࡤࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠢࡺ࡬ࡪࡴࠠࡢࠢࡦࡰࡴࡹࡥࠡ࡭ࡨࡽࡼࡵࡲࡥࠢ࡬ࡷࠥࡧࡢࡰࡷࡷࠤࡹࡵࠠࡦࡺࡨࡧࡺࡺࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨᙷ")
        if not self.accessibility or self.save_result_done:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡹࡴࡰࡲࡢࡧࡦࡶࡴࡶࡴࡨࡣࡧ࡫ࡦࡰࡴࡨࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡩ࡬ࡰࡵࡨ࠾ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠢᙸ"))
            return
        if not self._current_test_name or not self._current_test_uuid:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡳࡵࡱࡳࡣࡨࡧࡰࡵࡷࡵࡩࡤࡨࡥࡧࡱࡵࡩࡤࡨࡲࡰࡹࡶࡩࡷࡥࡣ࡭ࡱࡶࡩ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࡤࡴࡡ࡮ࡧࠣࡳࡷࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠧᙹ"))
            return
        self.logger.debug(bstack11ll11_opy_ (u"ࠢࡴࡶࡲࡴࡤࡩࡡࡱࡶࡸࡶࡪࡥࡢࡦࡨࡲࡶࡪࡥࡢࡳࡱࡺࡷࡪࡸ࡟ࡤ࡮ࡲࡷࡪࡀࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡵࡷࡳࡵࡥࡴࡦࡵࡷࡣࡨࡧࡰࡵࡷࡵࡩࠧᙺ"))
        self.bstack1111l1l111_opy_(None, self._current_test_name, bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᙻ"), self._current_test_uuid)
        self.save_result_done = True
    def bstack11lllll1lll_opy_(self, driver, script_code, bstack11lllllllll_opy_, framework_name):
        if framework_name == bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᙼ"):
            self.bstack1l11111llll_opy_.bstack1l111l111ll_opy_(driver, script_code, bstack11lllllllll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack11lllllllll_opy_))
    def _11lllll11ll_opy_(self, instance: bstack1l1l111ll1l_opy_, args: Tuple) -> list:
        bstack11ll11_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡩࡶࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢᙽ")
        if bstack11ll11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᙾ") in instance.bstack1l1l11l1l11_opy_:
            return args[2].tags if hasattr(args[2], bstack11ll11_opy_ (u"ࠬࡺࡡࡨࡵࠪᙿ")) else []
        if hasattr(args[0], bstack11ll11_opy_ (u"࠭࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠫ ")):
            return [marker.name for marker in args[0].own_markers]
        if hasattr(args[0], bstack11ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬᚁ")):
            tags = args[0].tags
            return list(tags) if tags else []
        return []
    def bstack1l1111l1l11_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)