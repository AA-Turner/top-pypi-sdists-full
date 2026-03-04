# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll1l1ll1l_opy_ import (
    bstack1ll1l1l11ll_opy_,
    bstack1ll1llll111_opy_,
    bstack1lll1111l11_opy_,
    bstack1ll1llll11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111lll1l_opy_ import bstack1ll11l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll111l1l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11111111_opy_ import bstack1ll11l1ll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111lll_opy_ import bstack1ll11ll1lll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1111_opy_ import bstack1ll1l1111l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1lll111l1ll_opy_
from bstack_utils.helper import bstack1l1l1lll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1ll1l111_opy_ import bstack1l11l11ll1_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll11ll1111_opy_(bstack1ll11l1ll11_opy_):
    bstack1l1l1l11ll1_opy_ = False
    bstack1l1l1l11l1l_opy_ = bstack1lll1l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣ፴")
    bstack1l1ll111lll_opy_ = bstack1lll1l_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢ፵")
    bstack1l1l11ll11l_opy_ = bstack1lll1l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥ፶")
    bstack1l1l1111lll_opy_ = bstack1lll1l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦ፷")
    bstack1l1l11l1l1l_opy_ = bstack1lll1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣ፸")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1111l1l1_opy_, bstack1ll11111ll1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1ll111111_opy_ = False
        self.bstack1l1l111l1l1_opy_ = dict()
        self.bstack1llll11111_opy_ = logger_utils.bstack1l1l1l111_opy_(__name__)
        self.bstack1l1l1ll1111_opy_ = False
        self.bstack1l1l11l11ll_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l111l111_opy_ = bstack1ll11111ll1_opy_
        bstack1ll1111l1l1_opy_.bstack1l1l1lll1ll_opy_((bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_, bstack1ll1llll111_opy_.PRE), self.bstack1l1l1l111ll_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l1l1lll1_opy_)
        TestFramework.bstack1l1l1lll1ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1l1l1111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l1l1lll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1l11111_opy_(instance, args)
        test_framework = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l111ll1l_opy_)
        if self.bstack1l1ll111111_opy_:
            self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣ፹")] = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
        if bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭፺") in instance.bstack1l1l1ll1l1l_opy_:
            platform_index = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1lll111_opy_)
            self.accessibility = self.bstack1l1l1l1l111_opy_(tags, self.config[bstack1lll1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭፻")][platform_index])
        else:
            capabilities = self.bstack1l1l111l111_opy_.bstack1l1l11ll1l1_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ፼") + str(kwargs) + bstack1lll1l_opy_ (u"ࠧࠨ፽"))
                return
            self.accessibility = self.bstack1l1l1l1l111_opy_(tags, capabilities)
        if self.bstack1l1l111l111_opy_.pages and self.bstack1l1l111l111_opy_.pages.values():
            bstack1l1l11llll1_opy_ = list(self.bstack1l1l111l111_opy_.pages.values())
            if bstack1l1l11llll1_opy_ and isinstance(bstack1l1l11llll1_opy_[0], (list, tuple)) and bstack1l1l11llll1_opy_[0]:
                bstack1l1ll11l11l_opy_ = bstack1l1l11llll1_opy_[0][0]
                if callable(bstack1l1ll11l11l_opy_):
                    page = bstack1l1ll11l11l_opy_()
                    def bstack1ll1lllll1_opy_():
                        self.get_accessibility_results(page, bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥ፾"))
                    def bstack1l1l11l11l1_opy_():
                        self.get_accessibility_results_summary(page, bstack1lll1l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ፿"))
                    setattr(page, bstack1lll1l_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᎀ"), bstack1ll1lllll1_opy_)
                    setattr(page, bstack1lll1l_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᎁ"), bstack1l1l11l11l1_opy_)
        self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᎂ") + str(self.accessibility) + bstack1lll1l_opy_ (u"ࠦࠧᎃ"))
    def bstack1l1l1l111ll_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1l11ll1_opy_ = datetime.now()
            self.bstack1l1ll111l1l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᎄ"), datetime.now() - bstack1l1l11ll1_opy_)
            bstack1ll1l1l1lll_opy_ = instance.data.get(bstack1lll1l_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᎅ"), None)
            if (
                not f.bstack1l1l11lllll_opy_(method_name)
                or f.bstack1l1l11lll1l_opy_(method_name, *args)
                or f.bstack1l1l1l1l1ll_opy_(method_name, *args)
                or (bstack1ll1l1l1lll_opy_ and int(bstack1ll1l1l1lll_opy_)>1)
            ):
                return
            if not f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l11ll11l_opy_, False):
                if not bstack1ll11ll1111_opy_.bstack1l1l1l11ll1_opy_:
                    self.logger.warning(bstack1lll1l_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᎆ") + str(f.platform_index) + bstack1lll1l_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᎇ"))
                    bstack1ll11ll1111_opy_.bstack1l1l1l11ll1_opy_ = True
                return
            bstack1l1l1l1ll11_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l1l1ll11_opy_:
                platform_index = f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_, 0)
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᎈ") + str(f.framework_name) + bstack1lll1l_opy_ (u"ࠥࠦᎉ"))
                return
            command_name = f.bstack1l1l1llll1l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᎊ") + str(method_name) + bstack1lll1l_opy_ (u"ࠧࠨᎋ"))
                return
            bstack1l1ll111l11_opy_ = f.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l11l1l1l_opy_, False)
            if command_name == bstack1lll1l_opy_ (u"ࠨࡧࡦࡶࠥᎌ") and not bstack1l1ll111l11_opy_:
                f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l11l1l1l_opy_, True)
                bstack1l1ll111l11_opy_ = True
            if not bstack1l1ll111l11_opy_ and not self.bstack1l1ll111111_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᎍ") + str(command_name) + bstack1lll1l_opy_ (u"ࠣࠤᎎ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᎏ") + str(command_name) + bstack1lll1l_opy_ (u"ࠥࠦ᎐"))
                return
            self.logger.info(bstack1lll1l_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨ᎑") + str(command_name) + bstack1lll1l_opy_ (u"ࠧࠨ᎒"))
            scripts = [(s, bstack1l1l1l1ll11_opy_[s]) for s in scripts_to_run if s in bstack1l1l1l1ll11_opy_]
            for script_name, bstack1l1l11ll111_opy_ in scripts:
                try:
                    bstack1l1l11ll1_opy_ = datetime.now()
                    if script_name == bstack1lll1l_opy_ (u"ࠨࡳࡤࡣࡱࠦ᎓"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack11ll1l1l_opy_ = {
                                bstack1lll1l_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣ᎔"): {
                                    bstack1lll1l_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ᎕"): bstack1lll1l_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧ᎖"),
                                    bstack1lll1l_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢ᎗"): [
                                        {
                                            bstack1lll1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ᎘"): command_name
                                        }
                                    ]
                                },
                                bstack1lll1l_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ᎙"): {
                                    bstack1lll1l_opy_ (u"ࠨࡢࡰࡦࡼࠦ᎚"): {
                                        bstack1lll1l_opy_ (u"ࠢ࡮ࡵࡪࠦ᎛"): result.get(bstack1lll1l_opy_ (u"ࠣ࡯ࡶ࡫ࠧ᎜"), bstack1lll1l_opy_ (u"ࠤࠥ᎝")) if isinstance(result, dict) else bstack1lll1l_opy_ (u"ࠥࠦ᎞"),
                                        bstack1lll1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧ᎟"): result.get(bstack1lll1l_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᎠ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack1llll11111_opy_.info(json.dumps(bstack11ll1l1l_opy_, separators=(bstack1lll1l_opy_ (u"ࠨࠬࠣᎡ"), bstack1lll1l_opy_ (u"ࠢ࠻ࠤᎢ"))))
                        except Exception as bstack11llll11l1_opy_:
                            self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨᎣ") + str(bstack11llll11l1_opy_) + bstack1lll1l_opy_ (u"ࠤࠥᎤ"))
                    instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᎥ") + script_name, datetime.now() - bstack1l1l11ll1_opy_)
                    if isinstance(result, dict) and not result.get(bstack1lll1l_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᎦ"), True):
                        self.logger.warning(bstack1lll1l_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᎧ") + str(result) + bstack1lll1l_opy_ (u"ࠨࠢᎨ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1lll1l_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᎩ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᎪ"))
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᎫ") + str(e) + bstack1lll1l_opy_ (u"ࠥࠦᎬ"))
    def bstack1l1l1l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1l1l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1lll1l_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᎭ") not in instance.bstack1l1l1ll1l1l_opy_:
            tags = self._1l1l1l11111_opy_(instance, args)
            capabilities = self.bstack1l1l111l111_opy_.bstack1l1l11ll1l1_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l1l1l1l111_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᎮ"))
            return
        driver = self.bstack1l1l111l111_opy_.bstack1l1l1l1l1l1_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        test_name = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l111llll_opy_)
        if not test_name:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᎯ"))
            return
        test_uuid = f.bstack1lll111l1l1_opy_(instance, TestFramework.bstack1l1l1l1ll1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᎰ"))
            return
        if isinstance(self.bstack1l1l111l111_opy_, bstack1ll1l1111l1_opy_):
            framework_name = bstack1lll1l_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᎱ")
        else:
            framework_name = bstack1lll1l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᎲ")
        self.bstack11111ll11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack111l1ll1l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᎳ"))
            return
        bstack1l1l11ll1_opy_ = datetime.now()
        bstack1l1l11ll111_opy_ = self.scripts.get(framework_name, {}).get(bstack1lll1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᎴ"), None)
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᎵ") + str(framework_name) + bstack1lll1l_opy_ (u"ࠨࠠࠣᎶ"))
            return
        if self.bstack1l1ll111111_opy_:
            arg = dict()
            arg[bstack1lll1l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᎷ")] = method if method else bstack1lll1l_opy_ (u"ࠣࠤᎸ")
            arg[bstack1lll1l_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᎹ")] = self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᎺ")]
            arg[bstack1lll1l_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᎻ")] = self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᎼ")]
            arg[bstack1lll1l_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᎽ")] = self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᎾ")]
            arg[bstack1lll1l_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᎿ")] = self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᏀ")]
            arg[bstack1lll1l_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᏁ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1l11l111l_opy_ = self.bstack1l1l1l11lll_opy_(bstack1lll1l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᏂ"), self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᏃ")])
            if bstack1lll1l_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᏄ") in bstack1l1l11l111l_opy_:
                bstack1l1l11l111l_opy_ = bstack1l1l11l111l_opy_.copy()
                bstack1l1l11l111l_opy_[bstack1lll1l_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᏅ")] = bstack1l1l11l111l_opy_.pop(bstack1lll1l_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᏆ"))
            arg = bstack1l1l1lll11l_opy_(arg, bstack1l1l11l111l_opy_)
            bstack1l1l1111l11_opy_ = bstack1l1l11ll111_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1l1111l11_opy_)
            return
        instance = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(driver)
        if instance:
            if not bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l1111lll_opy_, False):
                bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l1111lll_opy_, True)
            else:
                self.logger.info(bstack1lll1l_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᏇ") + str(method) + bstack1lll1l_opy_ (u"ࠥࠦᏈ"))
                return
        self.logger.info(bstack1lll1l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᏉ") + str(method) + bstack1lll1l_opy_ (u"ࠧࠨᏊ"))
        if framework_name == bstack1lll1l_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᏋ"):
            result = self.bstack1l1l111l111_opy_.bstack1l1l1llll11_opy_(driver, bstack1l1l11ll111_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l11ll111_opy_, {bstack1lll1l_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᏌ"): method if method else bstack1lll1l_opy_ (u"ࠣࠤᏍ")})
        bstack1l11l11ll1_opy_.end(EVENTS.bstack111l1ll1l1_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᏎ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᏏ"), True, None, command=method)
        if instance:
            bstack1lll1111l11_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l1111lll_opy_, False)
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᏐ"), datetime.now() - bstack1l1l11ll1_opy_)
        return result
        def bstack1l1l11lll11_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l1111ll1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l1l1llll_opy_ = self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᏑ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1lll1l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꮢ"), bstack1lll1l_opy_ (u"ࠧ࠱ࠩᏓ")))
            req.client_worker_id = bstack1lll1l_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᏔ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1lll111lll1_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᏕ") + str(r) + bstack1lll1l_opy_ (u"ࠥࠦᏖ"))
                else:
                    bstack1l1l11l1ll1_opy_ = json.loads(r.bstack1l1l1ll1lll_opy_.decode(bstack1lll1l_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᏗ")))
                    if result_type == bstack1lll1l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᏘ"):
                        return bstack1l1l11l1ll1_opy_.get(bstack1lll1l_opy_ (u"ࠨࡤࡢࡶࡤࠦᏙ"), [])
                    else:
                        return bstack1l1l11l1ll1_opy_.get(bstack1lll1l_opy_ (u"ࠢࡥࡣࡷࡥࠧᏚ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1lll1l_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᏛ") + str(e) + bstack1lll1l_opy_ (u"ࠤࠥᏜ"))
    @measure(event_name=EVENTS.bstack11l1l11ll_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᏝ"))
            return
        if self.bstack1l1ll111111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡥࡵࡶࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᏞ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l11lll11_opy_(driver, framework_name, bstack1lll1l_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᏟ"))
        bstack1l1l11ll111_opy_ = self.scripts.get(framework_name, {}).get(bstack1lll1l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᏠ"), None)
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᏡ") + str(framework_name) + bstack1lll1l_opy_ (u"ࠣࠤᏢ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1l11ll1_opy_ = datetime.now()
        if framework_name == bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭Ꮳ"):
            result = self.bstack1l1l111l111_opy_.bstack1l1l1llll11_opy_(driver, bstack1l1l11ll111_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l11ll111_opy_)
        instance = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(driver)
        if instance:
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᏤ"), datetime.now() - bstack1l1l11ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1ll11ll1_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᏥ"))
            return
        if self.bstack1l1ll111111_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l11lll11_opy_(driver, framework_name, bstack1lll1l_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᏦ"))
        bstack1l1l11ll111_opy_ = self.scripts.get(framework_name, {}).get(bstack1lll1l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᏧ"), None)
        if not bstack1l1l11ll111_opy_:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᏨ") + str(framework_name) + bstack1lll1l_opy_ (u"ࠣࠤᏩ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1l11ll1_opy_ = datetime.now()
        if framework_name == bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭Ꮺ"):
            result = self.bstack1l1l111l111_opy_.bstack1l1l1llll11_opy_(driver, bstack1l1l11ll111_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l11ll111_opy_)
        instance = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(driver)
        if instance:
            instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᏫ"), datetime.now() - bstack1l1l11ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l11l1lll_opy_, stage=STAGE.bstack1lllll1ll1_opy_)
    def bstack1l1l1lll1l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l1111ll1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1lll1l_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᏬ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1lll111lll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᏭ") + str(r) + bstack1lll1l_opy_ (u"ࠨࠢᏮ"))
            else:
                self.bstack1l1l1111l1l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᏯ") + str(e) + bstack1lll1l_opy_ (u"ࠣࠤᏰ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1111l1l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᏱ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1ll111111_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᏲ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1l111l1l1_opy_[bstack1lll1l_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᏳ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1l111l1l1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l111lll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1l1l11l1l_opy_ and command.module == self.bstack1l1ll111lll_opy_:
                        if command.method and not command.method in bstack1l1l111lll1_opy_:
                            bstack1l1l111lll1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1l111lll1_opy_[command.method]:
                            bstack1l1l111lll1_opy_[command.method][command.name] = list()
                        bstack1l1l111lll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l111lll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1ll111l1l_opy_(
        self,
        f: bstack1ll11l11l11_opy_,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l111l111_opy_, bstack1ll1l1111l1_opy_) and method_name != bstack1lll1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭Ᏼ"):
            return
        if bstack1lll1111l11_opy_.bstack1ll1l1l1l1l_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l11ll11l_opy_):
            return
        if f.bstack1l1l1ll1l11_opy_(method_name, *args):
            bstack1l1ll1111ll_opy_ = False
            desired_capabilities = f.bstack1l1l11l1111_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1l1lllll1_opy_(instance)
                platform_index = f.bstack1lll111l1l1_opy_(instance, bstack1ll11l11l11_opy_.bstack1l1l1lll111_opy_, 0)
                bstack1l1ll11111l_opy_ = datetime.now()
                r = self.bstack1l1l1lll1l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l111ll11_opy_(bstack1lll1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᏵ"), datetime.now() - bstack1l1ll11111l_opy_)
                bstack1l1ll1111ll_opy_ = r.success
            else:
                self.logger.error(bstack1lll1l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤ᏶") + str(desired_capabilities) + bstack1lll1l_opy_ (u"ࠣࠤ᏷"))
            f.bstack1lll1l11lll_opy_(instance, bstack1ll11ll1111_opy_.bstack1l1l11ll11l_opy_, bstack1l1ll1111ll_opy_)
    def bstack1lll11ll_opy_(self, test_tags):
        bstack1l1l1lll1l1_opy_ = self.config.get(bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᏸ"))
        if not bstack1l1l1lll1l1_opy_:
            return True
        try:
            include_tags = bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᏹ")] if bstack1lll1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᏺ") in bstack1l1l1lll1l1_opy_ and isinstance(bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᏻ")], list) else []
            exclude_tags = bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᏼ")] if bstack1lll1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᏽ") in bstack1l1l1lll1l1_opy_ and isinstance(bstack1l1l1lll1l1_opy_[bstack1lll1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᏾")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤ᏿") + str(error))
        return False
    def bstack1l1ll1111_opy_(self, caps):
        try:
            if self.bstack1l1ll111111_opy_:
                bstack1l1ll11l111_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ᐀"))
                if bstack1l1ll11l111_opy_ is not None and str(bstack1l1ll11l111_opy_).lower() == bstack1lll1l_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᐁ"):
                    bstack1l1l1llllll_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᐂ")) or caps.get(bstack1lll1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᐃ"))
                    if bstack1l1l1llllll_opy_ is not None and int(bstack1l1l1llllll_opy_) < 11:
                        self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡂࡰࡧࡶࡴ࡯ࡤࠡ࠳࠴ࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫࠮ࠡࡅࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠢᐄ") + str(bstack1l1l1llllll_opy_) + bstack1lll1l_opy_ (u"ࠣࠤᐅ"))
                        return False
                return True
            bstack1l1ll1111l1_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᐆ"), {}).get(bstack1lll1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᐇ"), caps.get(bstack1lll1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᐈ"), bstack1lll1l_opy_ (u"ࠬ࠭ᐉ")))
            if bstack1l1ll1111l1_opy_:
                self.logger.warning(bstack1lll1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᐊ"))
                return False
            browser = caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᐋ"), bstack1lll1l_opy_ (u"ࠨࠩᐌ")).lower()
            if browser != bstack1lll1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᐍ"):
                self.logger.warning(bstack1lll1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᐎ"))
                return False
            bstack1l1ll111ll1_opy_ = bstack1l1l111l1ll_opy_
            if not self.config.get(bstack1lll1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᐏ")) or self.config.get(bstack1lll1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᐐ")):
                bstack1l1ll111ll1_opy_ = bstack1l1l1l1l11l_opy_
            browser_version = caps.get(bstack1lll1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᐑ"))
            if not browser_version:
                browser_version = caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᐒ"), {}).get(bstack1lll1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᐓ"), bstack1lll1l_opy_ (u"ࠩࠪᐔ"))
            bstack1l1l11l1l11_opy_ = str(browser_version).lower() if browser_version is not None else bstack1lll1l_opy_ (u"ࠪࠫᐕ")
            if bstack1l1l11l1l11_opy_:
                if bstack1l1l11l1l11_opy_.startswith(bstack1lll1l_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᐖ")):
                    if bstack1l1l11l1l11_opy_.startswith(bstack1lll1l_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ᐗ")):
                        bstack1l1l1l111l1_opy_ = bstack1l1l11l1l11_opy_[len(bstack1lll1l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᐘ")):]
                        if bstack1l1l1l111l1_opy_ and not bstack1l1l1l111l1_opy_.isdigit():
                            self.logger.warning(bstack1lll1l_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࡪࡴࡸ࡭ࡢࡶࠣࠫࠧᐙ") + str(browser_version) + bstack1lll1l_opy_ (u"ࠣࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࠧ࡭ࡣࡷࡩࡸࡺࠧࠡࡱࡵࠤࠬࡲࡡࡵࡧࡶࡸ࠲ࡂ࡮ࡶ࡯ࡥࡩࡷࡄࠧ࠯ࠤᐚ"))
                            return False
                else:
                    try:
                        if int(bstack1l1l11l1l11_opy_.split(bstack1lll1l_opy_ (u"ࠩ࠱ࠫᐛ"))[0]) <= bstack1l1ll111ll1_opy_:
                            self.logger.warning(bstack1lll1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࠧᐜ") + str(bstack1l1ll111ll1_opy_) + bstack1lll1l_opy_ (u"ࠦ࠳ࠨᐝ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1lll1l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠪࡿࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࢃࠧ࠻ࠢࠥᐞ") + str(e) + bstack1lll1l_opy_ (u"ࠨࠢᐟ"))
            bstack1l1l111ll11_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᐠ"), {}).get(bstack1lll1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᐡ"))
            if not bstack1l1l111ll11_opy_:
                bstack1l1l111ll11_opy_ = caps.get(bstack1lll1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᐢ"), {})
            if bstack1l1l111ll11_opy_ and bstack1lll1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᐣ") in bstack1l1l111ll11_opy_.get(bstack1lll1l_opy_ (u"ࠫࡦࡸࡧࡴࠩᐤ"), []):
                self.logger.warning(bstack1lll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᐥ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᐦ") + str(error))
            return False
    def bstack1l1l1l11l11_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1l1ll11ll_opy_ = {
            bstack1lll1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᐧ"): test_uuid,
        }
        bstack1l1l11ll1ll_opy_ = {}
        if result.success:
            bstack1l1l11ll1ll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l1lll11l_opy_(bstack1l1l1ll11ll_opy_, bstack1l1l11ll1ll_opy_)
    def bstack1l1l1l11lll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1lll1l_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌࡥࡵࡥ࡫ࠤࡨ࡫࡮ࡵࡴࡤࡰࠥࡧࡵࡵࡪࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡷࡨࡸࡩࡱࡶࠣࡲࡦࡳࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡨࡧࡣࡩࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡨࡨࡸࡨ࡮ࡥࡥ࠮ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠦ࡬ࡰࡣࡧࡷࠥࡧ࡮ࡥࠢࡦࡥࡨ࡮ࡥࡴࠢ࡬ࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡵࡦࡶ࡮ࡶࡴࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡸࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡹࡺ࡯ࡤ࠻ࠢࡘ࡙ࡎࡊࠠࡰࡨࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠰ࠥ࡫࡭ࡱࡶࡼࠤࡩ࡯ࡣࡵࠢ࡬ࡪࠥ࡫ࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᐨ")
        try:
            if self.bstack1l1l1ll1111_opy_:
                return self.bstack1l1l11l11ll_opy_
            self.bstack1l1l1111ll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1lll1l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᐩ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᐪ"), bstack1lll1l_opy_ (u"ࠫ࠵࠭ᐫ")))
            req.client_worker_id = bstack1lll1l_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᐬ").format(threading.get_ident(), os.getpid())
            r = self.bstack1lll111lll1_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1l11l11ll_opy_ = self.bstack1l1l1l11l11_opy_(test_uuid, r)
                self.bstack1l1l1ll1111_opy_ = True
            else:
                self.logger.error(bstack1lll1l_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣᐭ") + str(r.error) + bstack1lll1l_opy_ (u"ࠢࠣᐮ"))
                self.bstack1l1l11l11ll_opy_ = dict()
            return self.bstack1l1l11l11ll_opy_
        except Exception as e:
            self.logger.error(bstack1lll1l_opy_ (u"ࠣࡨࡨࡸࡨ࡮ࡃࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡅ࠶࠷ࡹࡄࡱࡱࡪ࡮࡭࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡵࡲࠡࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᐯ") + str(traceback.format_exc()) + bstack1lll1l_opy_ (u"ࠤࠥᐰ"))
            return dict()
    def bstack11111ll11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll111111l_opy_ = None
        try:
            self.bstack1l1l1111ll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1lll1l_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᐱ")
            req.script_name = bstack1lll1l_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᐲ")
            req.platform_index = str(os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᐳ"), bstack1lll1l_opy_ (u"࠭࠰ࠨᐴ")))
            req.client_worker_id = bstack1lll1l_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᐵ").format(threading.get_ident(), os.getpid())
            r = self.bstack1lll111lll1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᐶ") + str(r.error) + bstack1lll1l_opy_ (u"ࠤࠥᐷ"))
            else:
                bstack1l1l1ll11ll_opy_ = self.bstack1l1l1l11l11_opy_(test_uuid, r)
                bstack1l1l11ll111_opy_ = r.script
            self.logger.debug(bstack1lll1l_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᐸ") + str(bstack1l1l1ll11ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1l11ll111_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᐹ") + str(framework_name) + bstack1lll1l_opy_ (u"ࠧࠦࠢᐺ"))
                return
            bstack1ll111111l_opy_ = bstack1l11l11ll1_opy_.bstack1111l1lll_opy_(EVENTS.bstack1l1l1ll11l1_opy_.value)
            self.bstack1l1l1ll111l_opy_(driver, bstack1l1l11ll111_opy_, bstack1l1l1ll11ll_opy_, framework_name)
            try:
                bstack1l1l111l11l_opy_ = {
                    bstack1lll1l_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢᐻ"): {
                        bstack1lll1l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᐼ"): bstack1lll1l_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᐽ"),
                    },
                    bstack1lll1l_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᐾ"): {
                        bstack1lll1l_opy_ (u"ࠥࡦࡴࡪࡹࠣᐿ"): {
                            bstack1lll1l_opy_ (u"ࠦࡲࡹࡧࠣᑀ"): bstack1lll1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᑁ"),
                            bstack1lll1l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᑂ"): True
                        }
                    }
                }
                self.bstack1llll11111_opy_.info(json.dumps(bstack1l1l111l11l_opy_, separators=(bstack1lll1l_opy_ (u"ࠧ࠭ࠩᑃ"), bstack1lll1l_opy_ (u"ࠨ࠼ࠪᑄ"))))
            except Exception as bstack11llll11l1_opy_:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣᑅ") + str(bstack11llll11l1_opy_) + bstack1lll1l_opy_ (u"ࠥࠦᑆ"))
            self.logger.info(bstack1lll1l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᑇ"))
            bstack1l11l11ll1_opy_.end(EVENTS.bstack1l1l1ll11l1_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᑈ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᑉ"), True, None, command=bstack1lll1l_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᑊ"),test_name=name)
        except Exception as bstack1l1l1ll1ll1_opy_:
            self.logger.error(bstack1lll1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᑋ") + bstack1lll1l_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧᑌ") + bstack1lll1l_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᑍ") + str(bstack1l1l1ll1ll1_opy_))
            bstack1l11l11ll1_opy_.end(EVENTS.bstack1l1l1ll11l1_opy_.value, bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᑎ"), bstack1ll111111l_opy_+bstack1lll1l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᑏ"), False, bstack1l1l1ll1ll1_opy_, command=bstack1lll1l_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᑐ"),test_name=name)
    def bstack1l1l1ll111l_opy_(self, driver, bstack1l1l11ll111_opy_, bstack1l1l1ll11ll_opy_, framework_name):
        if framework_name == bstack1lll1l_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᑑ"):
            self.bstack1l1l111l111_opy_.bstack1l1l1llll11_opy_(driver, bstack1l1l11ll111_opy_, bstack1l1l1ll11ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1l11ll111_opy_, bstack1l1l1ll11ll_opy_))
    def _1l1l1l11111_opy_(self, instance: bstack1ll111l1l1l_opy_, args: Tuple) -> list:
        bstack1lll1l_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧᑒ")
        if bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᑓ") in instance.bstack1l1l1ll1l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack1lll1l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᑔ")) else []
        if hasattr(args[0], bstack1lll1l_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩᑕ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1l1l1l111_opy_(self, tags, capabilities):
        return self.bstack1lll11ll_opy_(tags) and self.bstack1l1ll1111_opy_(capabilities)