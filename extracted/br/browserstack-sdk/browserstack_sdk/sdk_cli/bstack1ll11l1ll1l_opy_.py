# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1ll1ll1l11l_opy_ import (
    bstack1ll1l1l1lll_opy_,
    bstack1ll1ll1111l_opy_,
    bstack1ll1llll111_opy_,
    bstack1ll1l1lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1ll11l1l1_opy_ import bstack1ll111ll1ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111lllll_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1l1llll11_opy_ import bstack1ll1111l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1l1_opy_ import bstack1l1ll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll11l1lll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1ll1llllll1_opy_
from bstack_utils.helper import bstack1l1l1111l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll11l1l11l_opy_(bstack1ll1111l1ll_opy_):
    bstack1l1l11l11l1_opy_ = False
    bstack1l11lllll1l_opy_ = bstack1111l_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᐓ")
    bstack1l1l11lll1l_opy_ = bstack1111l_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᐔ")
    bstack1l1l1l1111l_opy_ = bstack1111l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣᐕ")
    bstack1l11ll1lll1_opy_ = bstack1111l_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᐖ")
    bstack1l1l1l11lll_opy_ = bstack1111l_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨᐗ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll111ll111_opy_, bstack1l1lll1l11l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1l1lll1_opy_ = False
        self.bstack1l11lll1lll_opy_ = dict()
        self.automation_logger = logger_utils.get_automation_logger(__name__)
        self.bstack1l1l1l1llll_opy_ = False
        self.bstack1l1l1l1l1l1_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l111lll1_opy_ = bstack1l1lll1l11l_opy_
        bstack1ll111ll111_opy_.bstack1l1l11llll1_opy_((bstack1ll1l1l1lll_opy_.bstack1ll11ll1lll_opy_, bstack1ll1ll1111l_opy_.PRE), self.bstack1l1l11111l1_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l1lll_opy_)
        TestFramework.bstack1l1l11llll1_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11ll1llll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l1lll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l11lll1l11_opy_(instance, args)
        test_framework = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
        if self.bstack1l1l1l1lll1_opy_:
            self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᐘ")] = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        if bstack1111l_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᐙ") in instance.bstack1l11lll111l_opy_:
            platform_index = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l1l111ll_opy_)
            self.accessibility = self.bstack1l11lll1ll1_opy_(tags, self.config[bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᐚ")][platform_index])
        else:
            capabilities = self.bstack1l1l111lll1_opy_.bstack1l1l111l1l1_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᐛ") + str(kwargs) + bstack1111l_opy_ (u"ࠥࠦᐜ"))
                return
            self.accessibility = self.bstack1l11lll1ll1_opy_(tags, capabilities)
        if self.bstack1l1l111lll1_opy_.pages and self.bstack1l1l111lll1_opy_.pages.values():
            bstack1l1l11lllll_opy_ = list(self.bstack1l1l111lll1_opy_.pages.values())
            if bstack1l1l11lllll_opy_ and isinstance(bstack1l1l11lllll_opy_[0], (list, tuple)) and bstack1l1l11lllll_opy_[0]:
                bstack1l11llllll1_opy_ = bstack1l1l11lllll_opy_[0][0]
                if callable(bstack1l11llllll1_opy_):
                    page = bstack1l11llllll1_opy_()
                    def get_results():
                        self.get_accessibility_results(page, bstack1111l_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᐝ"))
                    def bstack1l1l1l1l111_opy_():
                        self.get_accessibility_results_summary(page, bstack1111l_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᐞ"))
                    setattr(page, bstack1111l_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡴࠤᐟ"), get_results)
                    setattr(page, bstack1111l_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤᐠ"), bstack1l1l1l1l111_opy_)
        self.logger.debug(bstack1111l_opy_ (u"ࠣࡵ࡫ࡳࡺࡲࡤࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭ࡷࡨࡁࠧᐡ") + str(self.accessibility) + bstack1111l_opy_ (u"ࠤࠥᐢ"))
    def bstack1l1l11111l1_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        bstack1ll1l111l11_opy_: Tuple[bstack1ll1l1l1lll_opy_, bstack1ll1ll1111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if f.bstack1l1l11l11ll_opy_(method_name, *args):
                bstack1lll1l11l_opy_ = datetime.now()
                self.bstack1l1l11ll1l1_opy_(f, exec, *args, **kwargs)
                instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᐣ"), datetime.now() - bstack1lll1l11l_opy_)
                return
            if not self.accessibility:
                self.logger.debug(bstack1ll1l11l1ll_opy_ (u"ࠦࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡶࡩࡸࡹࡩࡰࡰ࠯ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࡲ࡮ࡴࡧࠣᐤ"))
                return
            bstack1lll1l11l_opy_ = datetime.now()
            self.bstack1l1l11ll1l1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᐥ"), datetime.now() - bstack1lll1l11l_opy_)
            bstack1ll11lll11l_opy_ = instance.data.get(bstack1111l_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᐦ"), None)
            if (
                not f.bstack1l1l1111111_opy_(method_name)
                or f.bstack1l11lll1l1l_opy_(method_name, *args)
                or f.bstack1l1l1l11l1l_opy_(method_name, *args)
                or (bstack1ll11lll11l_opy_ and int(bstack1ll11lll11l_opy_)>1)
            ):
                return
            if not f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l1l1l1111l_opy_, False):
                if not bstack1ll11l1l11l_opy_.bstack1l1l11l11l1_opy_:
                    self.logger.warning(bstack1111l_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᐧ") + str(f.platform_index) + bstack1111l_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᐨ"))
                    bstack1ll11l1l11l_opy_.bstack1l1l11l11l1_opy_ = True
                return
            bstack1l1l111111l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l111111l_opy_:
                platform_index = f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_, 0)
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᐩ") + str(f.framework_name) + bstack1111l_opy_ (u"ࠥࠦᐪ"))
                return
            command_name = f.bstack1l11llll1ll_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1111l_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᐫ") + str(method_name) + bstack1111l_opy_ (u"ࠧࠨᐬ"))
                return
            bstack1l11lllll11_opy_ = f.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l1l1l11lll_opy_, False)
            if command_name == bstack1111l_opy_ (u"ࠨࡧࡦࡶࠥᐭ") and not bstack1l11lllll11_opy_:
                f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l1l1l11lll_opy_, True)
                bstack1l11lllll11_opy_ = True
            if not bstack1l11lllll11_opy_ and not self.bstack1l1l1l1lll1_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᐮ") + str(command_name) + bstack1111l_opy_ (u"ࠣࠤᐯ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1111l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᐰ") + str(command_name) + bstack1111l_opy_ (u"ࠥࠦᐱ"))
                return
            self.logger.info(bstack1111l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᐲ") + str(command_name) + bstack1111l_opy_ (u"ࠧࠨᐳ"))
            scripts = [(s, bstack1l1l111111l_opy_[s]) for s in scripts_to_run if s in bstack1l1l111111l_opy_]
            for script_name, script_code in scripts:
                try:
                    bstack1lll1l11l_opy_ = datetime.now()
                    if script_name == bstack1111l_opy_ (u"ࠨࡳࡤࡣࡱࠦᐴ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            log_data = {
                                bstack1111l_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᐵ"): {
                                    bstack1111l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᐶ"): bstack1111l_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧᐷ"),
                                    bstack1111l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢᐸ"): [
                                        {
                                            bstack1111l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᐹ"): command_name
                                        }
                                    ]
                                },
                                bstack1111l_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᐺ"): {
                                    bstack1111l_opy_ (u"ࠨࡢࡰࡦࡼࠦᐻ"): {
                                        bstack1111l_opy_ (u"ࠢ࡮ࡵࡪࠦᐼ"): result.get(bstack1111l_opy_ (u"ࠣ࡯ࡶ࡫ࠧᐽ"), bstack1111l_opy_ (u"ࠤࠥᐾ")) if isinstance(result, dict) else bstack1111l_opy_ (u"ࠥࠦᐿ"),
                                        bstack1111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᑀ"): result.get(bstack1111l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᑁ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.automation_logger.info(json.dumps(log_data, separators=(bstack1111l_opy_ (u"ࠨࠬࠣᑂ"), bstack1111l_opy_ (u"ࠢ࠻ࠤᑃ"))))
                        except Exception as bstack1l11111l1_opy_:
                            self.logger.debug(bstack1111l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨᑄ") + str(bstack1l11111l1_opy_) + bstack1111l_opy_ (u"ࠤࠥᑅ"))
                    instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᑆ") + script_name, datetime.now() - bstack1lll1l11l_opy_)
                    if isinstance(result, dict) and not result.get(bstack1111l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᑇ"), True):
                        self.logger.warning(bstack1111l_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᑈ") + str(result) + bstack1111l_opy_ (u"ࠨࠢᑉ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1111l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᑊ") + str(e) + bstack1111l_opy_ (u"ࠣࠤᑋ"))
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᑌ") + str(e) + bstack1111l_opy_ (u"ࠥࠦᑍ"))
    def bstack1l11ll1llll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111lllll_opy_,
        bstack1ll1l111l11_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1111l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᑎ") not in instance.bstack1l11lll111l_opy_:
            tags = self._1l11lll1l11_opy_(instance, args)
            capabilities = self.bstack1l1l111lll1_opy_.bstack1l1l111l1l1_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l11lll1ll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᑏ"))
            return
        driver = self.bstack1l1l111lll1_opy_.bstack1l1l1l11l11_opy_(f, instance, bstack1ll1l111l11_opy_, *args, **kwargs)
        test_name = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l1l111llll_opy_)
        if not test_name:
            self.logger.debug(bstack1111l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᑐ"))
            return
        test_uuid = f.bstack1ll1lll1l11_opy_(instance, TestFramework.bstack1l11ll1ll1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1111l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᑑ"))
            return
        if isinstance(self.bstack1l1l111lll1_opy_, bstack1ll11l1lll1_opy_):
            framework_name = bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᑒ")
        else:
            framework_name = bstack1111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᑓ")
        self.bstack1l1l1ll11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l11llll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1111l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᑔ"))
            return
        bstack1lll1l11l_opy_ = datetime.now()
        script_code = self.scripts.get(framework_name, {}).get(bstack1111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᑕ"), None)
        if not script_code:
            self.logger.debug(bstack1111l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᑖ") + str(framework_name) + bstack1111l_opy_ (u"ࠨࠠࠣᑗ"))
            return
        if self.bstack1l1l1l1lll1_opy_:
            arg = dict()
            arg[bstack1111l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᑘ")] = method if method else bstack1111l_opy_ (u"ࠣࠤᑙ")
            arg[bstack1111l_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᑚ")] = self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᑛ")]
            arg[bstack1111l_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᑜ")] = self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᑝ")]
            arg[bstack1111l_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᑞ")] = self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᑟ")]
            arg[bstack1111l_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᑠ")] = self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᑡ")]
            arg[bstack1111l_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᑢ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l11lll1111_opy_ = self.bstack1l11llll11l_opy_(bstack1111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᑣ"), self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᑤ")])
            if bstack1111l_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᑥ") in bstack1l11lll1111_opy_:
                bstack1l11lll1111_opy_ = bstack1l11lll1111_opy_.copy()
                bstack1l11lll1111_opy_[bstack1111l_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᑦ")] = bstack1l11lll1111_opy_.pop(bstack1111l_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᑧ"))
            arg = bstack1l1l1111l11_opy_(arg, bstack1l11lll1111_opy_)
            bstack1l11llll1l1_opy_ = script_code % json.dumps(arg)
            driver.execute_script(bstack1l11llll1l1_opy_)
            return
        instance = bstack1ll1llll111_opy_.bstack1ll1l11l111_opy_(driver)
        if instance:
            if not bstack1ll1llll111_opy_.bstack1ll1lll1l11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l11ll1lll1_opy_, False):
                bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l11ll1lll1_opy_, True)
            else:
                self.logger.info(bstack1111l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᑨ") + str(method) + bstack1111l_opy_ (u"ࠥࠦᑩ"))
                return
        self.logger.info(bstack1111l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᑪ") + str(method) + bstack1111l_opy_ (u"ࠧࠨᑫ"))
        if framework_name == bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᑬ"):
            result = self.bstack1l1l111lll1_opy_.bstack1l1l1111l1l_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code, {bstack1111l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᑭ"): method if method else bstack1111l_opy_ (u"ࠣࠤᑮ")})
        bstack1l11ll1l1_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᑯ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᑰ"), True, None, command=method)
        if instance:
            bstack1ll1llll111_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l11ll1lll1_opy_, False)
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᑱ"), datetime.now() - bstack1lll1l11l_opy_)
        return result
        def bstack1l1l1l11ll1_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l111l1ll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l11l1l1l_opy_ = self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᑲ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᑳ"), bstack1111l_opy_ (u"ࠧ࠱ࠩᑴ")))
            req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᑵ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1ll1lll1_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1111l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᑶ") + str(r) + bstack1111l_opy_ (u"ࠥࠦᑷ"))
                else:
                    bstack1l1l1l1ll11_opy_ = json.loads(r.bstack1l1l1l1l11l_opy_.decode(bstack1111l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᑸ")))
                    if result_type == bstack1111l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᑹ"):
                        return bstack1l1l1l1ll11_opy_.get(bstack1111l_opy_ (u"ࠨࡤࡢࡶࡤࠦᑺ"), [])
                    else:
                        return bstack1l1l1l1ll11_opy_.get(bstack1111l_opy_ (u"ࠢࡥࡣࡷࡥࠧᑻ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1111l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᑼ") + str(e) + bstack1111l_opy_ (u"ࠤࠥᑽ"))
    @measure(event_name=EVENTS.bstack11ll1lll1l_opy_, stage=STAGE.bstack11lll111l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᑾ"))
            return
        if self.bstack1l1l1l1lll1_opy_:
            self.logger.debug(bstack1111l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡥࡵࡶࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᑿ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1l11ll1_opy_(driver, framework_name, bstack1111l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᒀ"))
        script_code = self.scripts.get(framework_name, {}).get(bstack1111l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᒁ"), None)
        if not script_code:
            self.logger.debug(bstack1111l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᒂ") + str(framework_name) + bstack1111l_opy_ (u"ࠣࠤᒃ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1lll1l11l_opy_ = datetime.now()
        if framework_name == bstack1111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᒄ"):
            result = self.bstack1l1l111lll1_opy_.bstack1l1l1111l1l_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code)
        instance = bstack1ll1llll111_opy_.bstack1ll1l11l111_opy_(driver)
        if instance:
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᒅ"), datetime.now() - bstack1lll1l11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1lllll11l1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᒆ"))
            return
        if self.bstack1l1l1l1lll1_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1l11ll1_opy_(driver, framework_name, bstack1111l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᒇ"))
        script_code = self.scripts.get(framework_name, {}).get(bstack1111l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᒈ"), None)
        if not script_code:
            self.logger.debug(bstack1111l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᒉ") + str(framework_name) + bstack1111l_opy_ (u"ࠣࠤᒊ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1lll1l11l_opy_ = datetime.now()
        if framework_name == bstack1111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᒋ"):
            result = self.bstack1l1l111lll1_opy_.bstack1l1l1111l1l_opy_(driver, script_code)
        else:
            result = driver.execute_async_script(script_code)
        instance = bstack1ll1llll111_opy_.bstack1ll1l11l111_opy_(driver)
        if instance:
            instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᒌ"), datetime.now() - bstack1lll1l11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l1l111l1_opy_, stage=STAGE.bstack11lll111l_opy_)
    def bstack1l1l11l111l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l111l1ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1111l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᒍ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1ll1lll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᒎ") + str(r) + bstack1111l_opy_ (u"ࠨࠢᒏ"))
            else:
                self.bstack1l1l111l111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᒐ") + str(e) + bstack1111l_opy_ (u"ࠣࠤᒑ"))
            traceback.print_exc()
            raise e
    def bstack1l1l111l111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1111l_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᒒ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1l1lll1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᒓ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l11lll1lll_opy_[bstack1111l_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᒔ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l11lll1lll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l11ll111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l11lllll1l_opy_ and command.module == self.bstack1l1l11lll1l_opy_:
                        if command.method and not command.method in bstack1l1l11ll111_opy_:
                            bstack1l1l11ll111_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1l11ll111_opy_[command.method]:
                            bstack1l1l11ll111_opy_[command.method][command.name] = list()
                        bstack1l1l11ll111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l11ll111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1l11ll1l1_opy_(
        self,
        f: bstack1ll111ll1ll_opy_,
        exec: Tuple[bstack1ll1l1lll1l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l111lll1_opy_, bstack1ll11l1lll1_opy_) and method_name != bstack1111l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᒕ"):
            return
        if bstack1ll1llll111_opy_.bstack1ll1l1l11ll_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l1l1l1111l_opy_):
            return
        if f.bstack1l1l11l11ll_opy_(method_name, *args):
            bstack1l11llll111_opy_ = False
            desired_capabilities = f.bstack1l1l1ll1111_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1l11lll11_opy_(instance)
                platform_index = f.bstack1ll1lll1l11_opy_(instance, bstack1ll111ll1ll_opy_.bstack1l1l1l111ll_opy_, 0)
                bstack1l11lll11ll_opy_ = datetime.now()
                r = self.bstack1l1l11l111l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l11ll11_opy_(bstack1111l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᒖ"), datetime.now() - bstack1l11lll11ll_opy_)
                bstack1l11llll111_opy_ = r.success
            else:
                self.logger.error(bstack1111l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤᒗ") + str(desired_capabilities) + bstack1111l_opy_ (u"ࠣࠤᒘ"))
            f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1l11l_opy_.bstack1l1l1l1111l_opy_, bstack1l11llll111_opy_)
    def is_enabled_testcase(self, test_tags):
        bstack1l1l11l111l_opy_ = self.config.get(bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᒙ"))
        if not bstack1l1l11l111l_opy_:
            return True
        try:
            include_tags = bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᒚ")] if bstack1111l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᒛ") in bstack1l1l11l111l_opy_ and isinstance(bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᒜ")], list) else []
            exclude_tags = bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᒝ")] if bstack1111l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᒞ") in bstack1l1l11l111l_opy_ and isinstance(bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᒟ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᒠ") + str(error))
        return False
    def is_platform_supported(self, caps):
        try:
            if self.bstack1l1l1l1lll1_opy_:
                bstack1l1l111ll11_opy_ = caps.get(bstack1111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᒡ"))
                if bstack1l1l111ll11_opy_ is not None and str(bstack1l1l111ll11_opy_).lower() == bstack1111l_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᒢ"):
                    bstack1l1l11l1111_opy_ = caps.get(bstack1111l_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᒣ")) or caps.get(bstack1111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᒤ"))
                    if bstack1l1l11l1111_opy_ is not None and int(bstack1l1l11l1111_opy_) < 11:
                        self.logger.warning(bstack1111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡂࡰࡧࡶࡴ࡯ࡤࠡ࠳࠴ࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫࠮ࠡࡅࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠢᒥ") + str(bstack1l1l11l1111_opy_) + bstack1111l_opy_ (u"ࠣࠤᒦ"))
                        return False
                return True
            bstack1l1l11ll11l_opy_ = caps.get(bstack1111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᒧ"), {}).get(bstack1111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᒨ"), caps.get(bstack1111l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᒩ"), bstack1111l_opy_ (u"ࠬ࠭ᒪ")))
            if bstack1l1l11ll11l_opy_:
                self.logger.warning(bstack1111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᒫ"))
                return False
            browser = caps.get(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᒬ"), bstack1111l_opy_ (u"ࠨࠩᒭ")).lower()
            if browser != bstack1111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᒮ"):
                self.logger.warning(bstack1111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᒯ"))
                return False
            bstack1l11lll11l1_opy_ = MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
            if not self.config.get(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᒰ")) or self.config.get(bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᒱ")):
                bstack1l11lll11l1_opy_ = bstack1l1l11l1l11_opy_
            browser_version = caps.get(bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᒲ"))
            if not browser_version:
                browser_version = caps.get(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒳ"), {}).get(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᒴ"), bstack1111l_opy_ (u"ࠩࠪᒵ"))
            bstack1l1l11111ll_opy_ = str(browser_version).lower() if browser_version is not None else bstack1111l_opy_ (u"ࠪࠫᒶ")
            if bstack1l1l11111ll_opy_:
                if bstack1l1l11111ll_opy_.startswith(bstack1111l_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᒷ")):
                    if bstack1l1l11111ll_opy_.startswith(bstack1111l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ᒸ")):
                        bstack1l1l111l11l_opy_ = bstack1l1l11111ll_opy_[len(bstack1111l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᒹ")):]
                        if bstack1l1l111l11l_opy_ and not bstack1l1l111l11l_opy_.isdigit():
                            self.logger.warning(bstack1111l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࡪࡴࡸ࡭ࡢࡶࠣࠫࠧᒺ") + str(browser_version) + bstack1111l_opy_ (u"ࠣࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࠧ࡭ࡣࡷࡩࡸࡺࠧࠡࡱࡵࠤࠬࡲࡡࡵࡧࡶࡸ࠲ࡂ࡮ࡶ࡯ࡥࡩࡷࡄࠧ࠯ࠤᒻ"))
                            return False
                else:
                    try:
                        if int(bstack1l1l11111ll_opy_.split(bstack1111l_opy_ (u"ࠩ࠱ࠫᒼ"))[0]) <= bstack1l11lll11l1_opy_:
                            self.logger.warning(bstack1111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࠧᒽ") + str(bstack1l11lll11l1_opy_) + bstack1111l_opy_ (u"ࠦ࠳ࠨᒾ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠪࡿࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࢃࠧ࠻ࠢࠥᒿ") + str(e) + bstack1111l_opy_ (u"ࠨࠢᓀ"))
            bstack1l1l1111lll_opy_ = caps.get(bstack1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᓁ"), {}).get(bstack1111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᓂ"))
            if not bstack1l1l1111lll_opy_:
                bstack1l1l1111lll_opy_ = caps.get(bstack1111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᓃ"), {})
            if not bstack1l1l1111lll_opy_:
                bstack1l1l1111lll_opy_ = caps.get(bstack1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᓄ"), {})
            if bstack1l1l1111lll_opy_ and any(arg == bstack1111l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᓅ") or (arg.startswith(bstack1111l_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪᓆ")) and arg != bstack1111l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧᓇ"))
                                     for arg in bstack1l1l1111lll_opy_.get(bstack1111l_opy_ (u"ࠧࡢࡴࡪࡷࠬᓈ"), [])):
                self.logger.warning(bstack1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᓉ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᓊ") + str(error))
            return False
    def bstack1l1l11ll1ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1l1l1l1ll_opy_ = {
            bstack1111l_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᓋ"): test_uuid,
        }
        bstack1l11lllllll_opy_ = {}
        if result.success:
            bstack1l11lllllll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l1111l11_opy_(bstack1l1l1l1l1ll_opy_, bstack1l11lllllll_opy_)
    def bstack1l11llll11l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࠣࠤࠥࠦࠠࠡࡈࡨࡸࡨ࡮ࠠࡤࡧࡱࡸࡷࡧ࡬ࠡࡣࡸࡸ࡭ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡨ࡫ࡹࡩࡳࠦࡳࡤࡴ࡬ࡴࡹࠦ࡮ࡢ࡯ࡨ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡤࡣࡦ࡬ࡪࡪࠠࡤࡱࡱࡪ࡮࡭ࠠࡪࡨࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡫࡫ࡴࡤࡪࡨࡨ࠱ࠦ࡯ࡵࡪࡨࡶࡼ࡯ࡳࡦࠢ࡯ࡳࡦࡪࡳࠡࡣࡱࡨࠥࡩࡡࡤࡪࡨࡷࠥ࡯ࡴ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡅࡷ࡭ࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩ࠿ࠦࡎࡢ࡯ࡨࠤࡴ࡬ࠠࡵࡪࡨࠤࡸࡩࡲࡪࡲࡷࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡣࡰࡰࡩ࡭࡬ࠦࡦࡰࡴࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡨࡷࡹࡥࡵࡶ࡫ࡧ࠾࡛ࠥࡕࡊࡆࠣࡳ࡫ࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡺ࡬࡮ࡩࡨࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡩ࡯ࡣࡵ࠼ࠣࡇࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡨ࡮ࡩࡴࡪࡱࡱࡥࡷࡿࠬࠡࡧࡰࡴࡹࡿࠠࡥ࡫ࡦࡸࠥ࡯ࡦࠡࡧࡵࡶࡴࡸࠠࡰࡥࡦࡹࡷࡹࠊࠡࠢࠣࠤࠥࠦࠠࠡࠤࠥࠦᓌ")
        try:
            if self.bstack1l1l1l1llll_opy_:
                return self.bstack1l1l1l1l1l1_opy_
            self.bstack1l1l111l1ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1111l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᓍ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᓎ"), bstack1111l_opy_ (u"ࠧ࠱ࠩᓏ")))
            req.client_worker_id = bstack1111l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᓐ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1ll1lll1_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1l1l1l1l1_opy_ = self.bstack1l1l11ll1ll_opy_(test_uuid, r)
                self.bstack1l1l1l1llll_opy_ = True
            else:
                self.logger.error(bstack1111l_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦᓑ") + str(r.error) + bstack1111l_opy_ (u"ࠥࠦᓒ"))
                self.bstack1l1l1l1l1l1_opy_ = dict()
            return self.bstack1l1l1l1l1l1_opy_
        except Exception as e:
            self.logger.error(bstack1111l_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᓓ") + str(traceback.format_exc()) + bstack1111l_opy_ (u"ࠧࠨᓔ"))
            return dict()
    def bstack1l1l1ll11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l1llll1_opy_ = None
        try:
            self.bstack1l1l111l1ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1111l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᓕ")
            req.script_name = bstack1111l_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᓖ")
            req.platform_index = str(os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᓗ"), bstack1111l_opy_ (u"ࠩ࠳ࠫᓘ")))
            req.client_worker_id = bstack1111l_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᓙ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1ll1lll1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1111l_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᓚ") + str(r.error) + bstack1111l_opy_ (u"ࠧࠨᓛ"))
            else:
                bstack1l1l1l1l1ll_opy_ = self.bstack1l1l11ll1ll_opy_(test_uuid, r)
                script_code = r.script
            self.logger.debug(bstack1111l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᓜ") + str(bstack1l1l1l1l1ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not script_code:
                self.logger.debug(bstack1111l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᓝ") + str(framework_name) + bstack1111l_opy_ (u"ࠣࠢࠥᓞ"))
                return
            bstack1l1llll1_opy_ = bstack1l11ll1l1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l1l111ll1l_opy_.value)
            self.bstack1l1l1l11111_opy_(driver, script_code, bstack1l1l1l1l1ll_opy_, framework_name)
            try:
                bstack1l1l1111ll1_opy_ = {
                    bstack1111l_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᓟ"): {
                        bstack1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᓠ"): bstack1111l_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᓡ"),
                    },
                    bstack1111l_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᓢ"): {
                        bstack1111l_opy_ (u"ࠨࡢࡰࡦࡼࠦᓣ"): {
                            bstack1111l_opy_ (u"ࠢ࡮ࡵࡪࠦᓤ"): bstack1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᓥ"),
                            bstack1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᓦ"): True
                        }
                    }
                }
                self.automation_logger.info(json.dumps(bstack1l1l1111ll1_opy_, separators=(bstack1111l_opy_ (u"ࠪ࠰ࠬᓧ"), bstack1111l_opy_ (u"ࠫ࠿࠭ᓨ"))))
            except Exception as bstack1l11111l1_opy_:
                self.logger.debug(bstack1111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᓩ") + str(bstack1l11111l1_opy_) + bstack1111l_opy_ (u"ࠨࠢᓪ"))
            self.logger.info(bstack1111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᓫ"))
            bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1l111ll1l_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᓬ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᓭ"), True, None, command=bstack1111l_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨᓮ"),test_name=name)
        except Exception as bstack1l1l11l1ll1_opy_:
            self.logger.error(bstack1111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᓯ") + bstack1111l_opy_ (u"ࠧࡹࡴࡳࠪࡳࡥࡹ࡮ࠩࠣᓰ") + bstack1111l_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᓱ") + str(bstack1l1l11l1ll1_opy_))
            bstack1l11ll1l1_opy_.end(EVENTS.bstack1l1l111ll1l_opy_.value, bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᓲ"), bstack1l1llll1_opy_+bstack1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᓳ"), False, bstack1l1l11l1ll1_opy_, command=bstack1111l_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᓴ"),test_name=name)
    def bstack1l1l1l11111_opy_(self, driver, script_code, bstack1l1l1l1l1ll_opy_, framework_name):
        if framework_name == bstack1111l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᓵ"):
            self.bstack1l1l111lll1_opy_.bstack1l1l1111l1l_opy_(driver, script_code, bstack1l1l1l1l1ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(script_code, bstack1l1l1l1l1ll_opy_))
    def _1l11lll1l11_opy_(self, instance: bstack1ll111lllll_opy_, args: Tuple) -> list:
        bstack1111l_opy_ (u"ࠦࠧࠨࡅࡹࡶࡵࡥࡨࡺࠠࡵࡣࡪࡷࠥࡨࡡࡴࡧࡧࠤࡴࡴࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣᓶ")
        if bstack1111l_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᓷ") in instance.bstack1l11lll111l_opy_:
            return args[2].tags if hasattr(args[2], bstack1111l_opy_ (u"࠭ࡴࡢࡩࡶࠫᓸ")) else []
        if hasattr(args[0], bstack1111l_opy_ (u"ࠧࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠬᓹ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l11lll1ll1_opy_(self, tags, capabilities):
        return self.is_enabled_testcase(tags) and self.is_platform_supported(capabilities)