# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import (
    bstack1ll1lll1ll1_opy_,
    bstack1ll1l1lll1l_opy_,
    bstack1lll11l1ll1_opy_,
    bstack1ll1ll1l111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1ll1l_opy_ import bstack1ll11l11111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll11ll111l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11l11l1l_opy_ import bstack1ll111l1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111ll11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111llll_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l1l1_opy_ import bstack1lll11l11ll_opy_
from bstack_utils.helper import bstack1l1l111l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll1l11ll1_opy_ import bstack1l11l1ll_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1l1ll1l11l1_opy_(bstack1ll111l1l1l_opy_):
    bstack1l1l1lll1ll_opy_ = False
    bstack1l1l1l1l1l1_opy_ = bstack1111_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤ፵")
    bstack1l1l1l11l11_opy_ = bstack1111_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣ፶")
    bstack1l1l1l111ll_opy_ = bstack1111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦ፷")
    bstack1l1l1l11ll1_opy_ = bstack1111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧ፸")
    bstack1l1l1111l1l_opy_ = bstack1111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤ፹")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1l1111ll_opy_, bstack1ll11l1lll1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1l1lll1_opy_ = False
        self.bstack1l1l1llll1l_opy_ = dict()
        self.bstack11llllll1l_opy_ = logger_utils.bstack1ll11llll1_opy_(__name__)
        self.bstack1l1l1ll1lll_opy_ = False
        self.bstack1l1l11ll111_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l1lll111_opy_ = bstack1ll11l1lll1_opy_
        bstack1ll1l1111ll_opy_.bstack1l1ll1111ll_opy_((bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_, bstack1ll1l1lll1l_opy_.PRE), self.bstack1l1l111ll11_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11l11ll_opy_)
        TestFramework.bstack1l1ll1111ll_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1ll111l_opy_(instance, args)
        test_framework = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l1111l11_opy_)
        if self.bstack1l1l1l1lll1_opy_:
            self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤ፺")] = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_)
        if bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ፻") in instance.bstack1l1ll111l11_opy_:
            platform_index = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1ll1_opy_)
            self.accessibility = self.bstack1l1l1l111l1_opy_(tags, self.config[bstack1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ፼")][platform_index])
        else:
            capabilities = self.bstack1l1l1lll111_opy_.bstack1l1l1l11111_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧ፽") + str(kwargs) + bstack1111_opy_ (u"ࠨࠢ፾"))
                return
            self.accessibility = self.bstack1l1l1l111l1_opy_(tags, capabilities)
        if self.bstack1l1l1lll111_opy_.pages and self.bstack1l1l1lll111_opy_.pages.values():
            bstack1l1l111lll1_opy_ = list(self.bstack1l1l1lll111_opy_.pages.values())
            if bstack1l1l111lll1_opy_ and isinstance(bstack1l1l111lll1_opy_[0], (list, tuple)) and bstack1l1l111lll1_opy_[0]:
                bstack1l1l111l1l1_opy_ = bstack1l1l111lll1_opy_[0][0]
                if callable(bstack1l1l111l1l1_opy_):
                    page = bstack1l1l111l1l1_opy_()
                    def bstack1l1llll11_opy_():
                        self.get_accessibility_results(page, bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ፿"))
                    def bstack1l1l11lll1l_opy_():
                        self.get_accessibility_results_summary(page, bstack1111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᎀ"))
                    setattr(page, bstack1111_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᎁ"), bstack1l1llll11_opy_)
                    setattr(page, bstack1111_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᎂ"), bstack1l1l11lll1l_opy_)
        self.logger.debug(bstack1111_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᎃ") + str(self.accessibility) + bstack1111_opy_ (u"ࠧࠨᎄ"))
    def bstack1l1l111ll11_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1llll111_opy_ = datetime.now()
            self.bstack1l1l1llllll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᎅ"), datetime.now() - bstack1l1llll111_opy_)
            bstack1ll1l1l11ll_opy_ = instance.data.get(bstack1111_opy_ (u"ࠧࡳࡣࡱ࡯ࠬᎆ"), None)
            if (
                not f.bstack1l1l111l1ll_opy_(method_name)
                or f.bstack1l1l11l1111_opy_(method_name, *args)
                or f.bstack1l1l1lll11l_opy_(method_name, *args)
                or (bstack1ll1l1l11ll_opy_ and int(bstack1ll1l1l11ll_opy_)>1)
            ):
                return
            if not f.bstack1lll1l11111_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1l111ll_opy_, False):
                if not bstack1l1ll1l11l1_opy_.bstack1l1l1lll1ll_opy_:
                    self.logger.warning(bstack1111_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦᎇ") + str(f.platform_index) + bstack1111_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᎈ"))
                    bstack1l1ll1l11l1_opy_.bstack1l1l1lll1ll_opy_ = True
                return
            bstack1l1l1lll1l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l1lll1l1_opy_:
                platform_index = f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_, 0)
                self.logger.debug(bstack1111_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᎉ") + str(f.framework_name) + bstack1111_opy_ (u"ࠦࠧᎊ"))
                return
            command_name = f.bstack1l1l1l11lll_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1111_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢᎋ") + str(method_name) + bstack1111_opy_ (u"ࠨࠢᎌ"))
                return
            bstack1l1l1l1l111_opy_ = f.bstack1lll1l11111_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1111l1l_opy_, False)
            if command_name == bstack1111_opy_ (u"ࠢࡨࡧࡷࠦᎍ") and not bstack1l1l1l1l111_opy_:
                f.bstack1lll1l11l1l_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1111l1l_opy_, True)
                bstack1l1l1l1l111_opy_ = True
            if not bstack1l1l1l1l111_opy_ and not self.bstack1l1l1l1lll1_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᎎ") + str(command_name) + bstack1111_opy_ (u"ࠤࠥᎏ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1111_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣ᎐") + str(command_name) + bstack1111_opy_ (u"ࠦࠧ᎑"))
                return
            self.logger.info(bstack1111_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢ᎒") + str(command_name) + bstack1111_opy_ (u"ࠨࠢ᎓"))
            scripts = [(s, bstack1l1l1lll1l1_opy_[s]) for s in scripts_to_run if s in bstack1l1l1lll1l1_opy_]
            for script_name, bstack1l1l11ll1ll_opy_ in scripts:
                try:
                    bstack1l1llll111_opy_ = datetime.now()
                    if script_name == bstack1111_opy_ (u"ࠢࡴࡥࡤࡲࠧ᎔"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack1llll11l_opy_ = {
                                bstack1111_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤ᎕"): {
                                    bstack1111_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥ᎖"): bstack1111_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡆࡅࡓࠨ᎗"),
                                    bstack1111_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠣ᎘"): [
                                        {
                                            bstack1111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧ᎙"): command_name
                                        }
                                    ]
                                },
                                bstack1111_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣ᎚"): {
                                    bstack1111_opy_ (u"ࠢࡣࡱࡧࡽࠧ᎛"): {
                                        bstack1111_opy_ (u"ࠣ࡯ࡶ࡫ࠧ᎜"): result.get(bstack1111_opy_ (u"ࠤࡰࡷ࡬ࠨ᎝"), bstack1111_opy_ (u"ࠥࠦ᎞")) if isinstance(result, dict) else bstack1111_opy_ (u"ࠦࠧ᎟"),
                                        bstack1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᎠ"): result.get(bstack1111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᎡ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack11llllll1l_opy_.info(json.dumps(bstack1llll11l_opy_, separators=(bstack1111_opy_ (u"ࠢ࠭ࠤᎢ"), bstack1111_opy_ (u"ࠣ࠼ࠥᎣ"))))
                        except Exception as bstack1l111l1l11_opy_:
                            self.logger.debug(bstack1111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࠢᎤ") + str(bstack1l111l1l11_opy_) + bstack1111_opy_ (u"ࠥࠦᎥ"))
                    instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᎦ") + script_name, datetime.now() - bstack1l1llll111_opy_)
                    if isinstance(result, dict) and not result.get(bstack1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᎧ"), True):
                        self.logger.warning(bstack1111_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᎨ") + str(result) + bstack1111_opy_ (u"ࠢࠣᎩ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1111_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᎪ") + str(e) + bstack1111_opy_ (u"ࠤࠥᎫ"))
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᎬ") + str(e) + bstack1111_opy_ (u"ࠦࠧᎭ"))
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11ll111l_opy_,
        bstack1ll1ll1ll1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1111_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᎮ") not in instance.bstack1l1ll111l11_opy_:
            tags = self._1l1l1ll111l_opy_(instance, args)
            capabilities = self.bstack1l1l1lll111_opy_.bstack1l1l1l11111_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l1l1l111l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᎯ"))
            return
        driver = self.bstack1l1l1lll111_opy_.bstack1l1l1l1l11l_opy_(f, instance, bstack1ll1ll1ll1l_opy_, *args, **kwargs)
        test_name = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
        if not test_name:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᎰ"))
            return
        test_uuid = f.bstack1lll1l11111_opy_(instance, TestFramework.bstack1l1l11l1l1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1111_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᎱ"))
            return
        if isinstance(self.bstack1l1l1lll111_opy_, bstack1ll111l1lll_opy_):
            framework_name = bstack1111_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭Ꮂ")
        else:
            framework_name = bstack1111_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᎳ")
        self.bstack1ll1ll1l11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack11l11lll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1111_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᎴ"))
            return
        bstack1l1llll111_opy_ = datetime.now()
        bstack1l1l11ll1ll_opy_ = self.scripts.get(framework_name, {}).get(bstack1111_opy_ (u"ࠧࡹࡣࡢࡰࠥᎵ"), None)
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᎶ") + str(framework_name) + bstack1111_opy_ (u"ࠢࠡࠤᎷ"))
            return
        if self.bstack1l1l1l1lll1_opy_:
            arg = dict()
            arg[bstack1111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᎸ")] = method if method else bstack1111_opy_ (u"ࠤࠥᎹ")
            arg[bstack1111_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥᎺ")] = self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᎻ")]
            arg[bstack1111_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥᎼ")] = self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᎽ")]
            arg[bstack1111_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᎾ")] = self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨᎿ")]
            arg[bstack1111_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨᏀ")] = self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᏁ")]
            arg[bstack1111_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦᏂ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1l1l1l1ll_opy_ = self.bstack1l1ll111lll_opy_(bstack1111_opy_ (u"ࠧࡹࡣࡢࡰࠥᏃ"), self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᏄ")])
            if bstack1111_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥᏅ") in bstack1l1l1l1l1ll_opy_:
                bstack1l1l1l1l1ll_opy_ = bstack1l1l1l1l1ll_opy_.copy()
                bstack1l1l1l1l1ll_opy_[bstack1111_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧᏆ")] = bstack1l1l1l1l1ll_opy_.pop(bstack1111_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧᏇ"))
            arg = bstack1l1l111l111_opy_(arg, bstack1l1l1l1l1ll_opy_)
            bstack1l1l11111l1_opy_ = bstack1l1l11ll1ll_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1l11111l1_opy_)
            return
        instance = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(driver)
        if instance:
            if not bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1l11ll1_opy_, False):
                bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1l11ll1_opy_, True)
            else:
                self.logger.info(bstack1111_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᏈ") + str(method) + bstack1111_opy_ (u"ࠦࠧᏉ"))
                return
        self.logger.info(bstack1111_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᏊ") + str(method) + bstack1111_opy_ (u"ࠨࠢᏋ"))
        if framework_name == bstack1111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᏌ"):
            result = self.bstack1l1l1lll111_opy_.bstack1l1l1l1111l_opy_(driver, bstack1l1l11ll1ll_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l11ll1ll_opy_, {bstack1111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᏍ"): method if method else bstack1111_opy_ (u"ࠤࠥᏎ")})
        bstack1l11l1ll_opy_.end(EVENTS.bstack11l11lll_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᏏ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᏐ"), True, None, command=method)
        if instance:
            bstack1lll11l1ll1_opy_.bstack1lll1l11l1l_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1l11ll1_opy_, False)
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤᏑ"), datetime.now() - bstack1l1llll111_opy_)
        return result
        def bstack1l1ll111l1l_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l111ll1l_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l111l11l_opy_ = self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᏒ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᏓ"), bstack1111_opy_ (u"ࠨ࠲ࠪᏔ")))
            req.client_worker_id = bstack1111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣᏕ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1lll111l111_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᏖ") + str(r) + bstack1111_opy_ (u"ࠦࠧᏗ"))
                else:
                    bstack1l1l11111ll_opy_ = json.loads(r.bstack1l1ll11111l_opy_.decode(bstack1111_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᏘ")))
                    if result_type == bstack1111_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᏙ"):
                        return bstack1l1l11111ll_opy_.get(bstack1111_opy_ (u"ࠢࡥࡣࡷࡥࠧᏚ"), [])
                    else:
                        return bstack1l1l11111ll_opy_.get(bstack1111_opy_ (u"ࠣࡦࡤࡸࡦࠨᏛ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡵࡶ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡩ࡬ࡪ࠼ࠣࠦᏜ") + str(e) + bstack1111_opy_ (u"ࠥࠦᏝ"))
    @measure(event_name=EVENTS.bstack11l11l1lll_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᏞ"))
            return
        if self.bstack1l1l1l1lll1_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡦࡶࡰࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᏟ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1ll111l1l_opy_(driver, framework_name, bstack1111_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᏠ"))
        bstack1l1l11ll1ll_opy_ = self.scripts.get(framework_name, {}).get(bstack1111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᏡ"), None)
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᏢ") + str(framework_name) + bstack1111_opy_ (u"ࠤࠥᏣ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1llll111_opy_ = datetime.now()
        if framework_name == bstack1111_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᏤ"):
            result = self.bstack1l1l1lll111_opy_.bstack1l1l1l1111l_opy_(driver, bstack1l1l11ll1ll_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l11ll1ll_opy_)
        instance = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(driver)
        if instance:
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹࠢᏥ"), datetime.now() - bstack1l1llll111_opy_)
        return result
    @measure(event_name=EVENTS.bstack11l1lll1l1_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᏦ"))
            return
        if self.bstack1l1l1l1lll1_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1ll111l1l_opy_(driver, framework_name, bstack1111_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᏧ"))
        bstack1l1l11ll1ll_opy_ = self.scripts.get(framework_name, {}).get(bstack1111_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᏨ"), None)
        if not bstack1l1l11ll1ll_opy_:
            self.logger.debug(bstack1111_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᏩ") + str(framework_name) + bstack1111_opy_ (u"ࠤࠥᏪ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1llll111_opy_ = datetime.now()
        if framework_name == bstack1111_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᏫ"):
            result = self.bstack1l1l1lll111_opy_.bstack1l1l1l1111l_opy_(driver, bstack1l1l11ll1ll_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l11ll1ll_opy_)
        instance = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(driver)
        if instance:
            instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣᏬ"), datetime.now() - bstack1l1llll111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l11lllll_opy_, stage=STAGE.bstack111l1lllll_opy_)
    def bstack1l1l1111lll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l111ll1l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᏭ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1lll111l111_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᏮ") + str(r) + bstack1111_opy_ (u"ࠢࠣᏯ"))
            else:
                self.bstack1l1l11ll1l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᏰ") + str(e) + bstack1111_opy_ (u"ࠤࠥᏱ"))
            traceback.print_exc()
            raise e
    def bstack1l1l11ll1l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡰࡴࡧࡤࡠࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥᏲ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1l1lll1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠤᏳ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1l1llll1l_opy_[bstack1111_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦᏴ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1l1llll1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l111llll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1l1l1l1l1_opy_ and command.module == self.bstack1l1l1l11l11_opy_:
                        if command.method and not command.method in bstack1l1l111llll_opy_:
                            bstack1l1l111llll_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1l111llll_opy_[command.method]:
                            bstack1l1l111llll_opy_[command.method][command.name] = list()
                        bstack1l1l111llll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l111llll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1ll11l11111_opy_,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l1lll111_opy_, bstack1ll111l1lll_opy_) and method_name != bstack1111_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᏵ"):
            return
        if bstack1lll11l1ll1_opy_.bstack1ll1l1l1ll1_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1l111ll_opy_):
            return
        if f.bstack1l1l1lllll1_opy_(method_name, *args):
            bstack1l1l1ll1l11_opy_ = False
            desired_capabilities = f.bstack1l1l1ll1ll1_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1ll111111_opy_(instance)
                platform_index = f.bstack1lll1l11111_opy_(instance, bstack1ll11l11111_opy_.bstack1l1l11l1ll1_opy_, 0)
                bstack1l1l11l1lll_opy_ = datetime.now()
                r = self.bstack1l1l1111lll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11ll1llll_opy_(bstack1111_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧ᏶"), datetime.now() - bstack1l1l11l1lll_opy_)
                bstack1l1l1ll1l11_opy_ = r.success
            else:
                self.logger.error(bstack1111_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥ᏷") + str(desired_capabilities) + bstack1111_opy_ (u"ࠤࠥᏸ"))
            f.bstack1lll1l11l1l_opy_(instance, bstack1l1ll1l11l1_opy_.bstack1l1l1l111ll_opy_, bstack1l1l1ll1l11_opy_)
    def bstack111l1lll1_opy_(self, test_tags):
        bstack1l1l1111lll_opy_ = self.config.get(bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᏹ"))
        if not bstack1l1l1111lll_opy_:
            return True
        try:
            include_tags = bstack1l1l1111lll_opy_[bstack1111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᏺ")] if bstack1111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᏻ") in bstack1l1l1111lll_opy_ and isinstance(bstack1l1l1111lll_opy_[bstack1111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᏼ")], list) else []
            exclude_tags = bstack1l1l1111lll_opy_[bstack1111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᏽ")] if bstack1111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᏾") in bstack1l1l1111lll_opy_ and isinstance(bstack1l1l1111lll_opy_[bstack1111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᏿")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥ᐀") + str(error))
        return False
    def bstack1ll1111l1l_opy_(self, caps):
        try:
            if self.bstack1l1l1l1lll1_opy_:
                bstack1l1l1l1llll_opy_ = caps.get(bstack1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᐁ"))
                if bstack1l1l1l1llll_opy_ is not None and str(bstack1l1l1l1llll_opy_).lower() == bstack1111_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᐂ"):
                    bstack1l1l1l1ll1l_opy_ = caps.get(bstack1111_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᐃ")) or caps.get(bstack1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᐄ"))
                    if bstack1l1l1l1ll1l_opy_ is not None and int(bstack1l1l1l1ll1l_opy_) < 11:
                        self.logger.warning(bstack1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡃࡱࡨࡷࡵࡩࡥࠢ࠴࠵ࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥ࠯ࠢࡆࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠣᐅ") + str(bstack1l1l1l1ll1l_opy_) + bstack1111_opy_ (u"ࠤࠥᐆ"))
                        return False
                return True
            bstack1l1ll1111l1_opy_ = caps.get(bstack1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᐇ"), {}).get(bstack1111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᐈ"), caps.get(bstack1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᐉ"), bstack1111_opy_ (u"࠭ࠧᐊ")))
            if bstack1l1ll1111l1_opy_:
                self.logger.warning(bstack1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᐋ"))
                return False
            browser = caps.get(bstack1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᐌ"), bstack1111_opy_ (u"ࠩࠪᐍ")).lower()
            if browser != bstack1111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᐎ"):
                self.logger.warning(bstack1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᐏ"))
                return False
            bstack1l1l11ll11l_opy_ = bstack1l1l1ll1111_opy_
            if not self.config.get(bstack1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᐐ")) or self.config.get(bstack1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᐑ")):
                bstack1l1l11ll11l_opy_ = bstack1l1l1111ll1_opy_
            browser_version = caps.get(bstack1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᐒ"))
            if not browser_version:
                browser_version = caps.get(bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐓ"), {}).get(bstack1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᐔ"), bstack1111_opy_ (u"ࠪࠫᐕ"))
            bstack1l1l1llll11_opy_ = str(browser_version).lower() if browser_version is not None else bstack1111_opy_ (u"ࠫࠬᐖ")
            if bstack1l1l1llll11_opy_:
                if bstack1l1l1llll11_opy_.startswith(bstack1111_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᐗ")):
                    if bstack1l1l1llll11_opy_.startswith(bstack1111_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᐘ")):
                        bstack1l1l11l1l11_opy_ = bstack1l1l1llll11_opy_[len(bstack1111_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺ࠭ࠨᐙ")):]
                        if bstack1l1l11l1l11_opy_ and not bstack1l1l11l1l11_opy_.isdigit():
                            self.logger.warning(bstack1111_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡫ࡵࡲ࡮ࡣࡷࠤࠬࠨᐚ") + str(browser_version) + bstack1111_opy_ (u"ࠤࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࠨ࡮ࡤࡸࡪࡹࡴࠨࠢࡲࡶࠥ࠭࡬ࡢࡶࡨࡷࡹ࠳࠼࡯ࡷࡰࡦࡪࡸ࠾ࠨ࠰ࠥᐛ"))
                            return False
                else:
                    try:
                        if int(bstack1l1l1llll11_opy_.split(bstack1111_opy_ (u"ࠪ࠲ࠬᐜ"))[0]) <= bstack1l1l11ll11l_opy_:
                            self.logger.warning(bstack1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࠨᐝ") + str(bstack1l1l11ll11l_opy_) + bstack1111_opy_ (u"ࠧ࠴ࠢᐞ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1111_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࠫࢀࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࡽࠨ࠼ࠣࠦᐟ") + str(e) + bstack1111_opy_ (u"ࠢࠣᐠ"))
            bstack1l1l1l1ll11_opy_ = caps.get(bstack1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᐡ"), {}).get(bstack1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᐢ"))
            if not bstack1l1l1l1ll11_opy_:
                bstack1l1l1l1ll11_opy_ = caps.get(bstack1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᐣ"), {})
            if bstack1l1l1l1ll11_opy_ and bstack1111_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᐤ") in bstack1l1l1l1ll11_opy_.get(bstack1111_opy_ (u"ࠬࡧࡲࡨࡵࠪᐥ"), []):
                self.logger.warning(bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᐦ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᐧ") + str(error))
            return False
    def bstack1l1l11l111l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1l11l11l1_opy_ = {
            bstack1111_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᐨ"): test_uuid,
        }
        bstack1l1l1l11l1l_opy_ = {}
        if result.success:
            bstack1l1l1l11l1l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l111l111_opy_(bstack1l1l11l11l1_opy_, bstack1l1l1l11l1l_opy_)
    def bstack1l1ll111lll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1111_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡦࡶࡦ࡬ࠥࡩࡥ࡯ࡶࡵࡥࡱࠦࡡࡶࡶ࡫ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡸࡩࡲࡪࡲࡷࠤࡳࡧ࡭ࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡩࡡࡤࡪࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯ࡦࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡩࡩࡹࡩࡨࡦࡦ࠯ࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠠ࡭ࡱࡤࡨࡸࠦࡡ࡯ࡦࠣࡧࡦࡩࡨࡦࡵࠣ࡭ࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧ࠽ࠤࡓࡧ࡭ࡦࠢࡲࡪࠥࡺࡨࡦࠢࡶࡧࡷ࡯ࡰࡵࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡲࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠼࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠱ࠦࡥ࡮ࡲࡷࡽࠥࡪࡩࡤࡶࠣ࡭࡫ࠦࡥࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᐩ")
        try:
            if self.bstack1l1l1ll1lll_opy_:
                return self.bstack1l1l11ll111_opy_
            self.bstack1l1l111ll1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᐪ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫᐫ"), bstack1111_opy_ (u"ࠬ࠶ࠧᐬ")))
            req.client_worker_id = bstack1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᐭ").format(threading.get_ident(), os.getpid())
            r = self.bstack1lll111l111_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1l11ll111_opy_ = self.bstack1l1l11l111l_opy_(test_uuid, r)
                self.bstack1l1l1ll1lll_opy_ = True
            else:
                self.logger.error(bstack1111_opy_ (u"ࠢࡧࡧࡷࡧ࡭ࡉࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡄ࠵࠶ࡿࡃࡰࡰࡩ࡭࡬ࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡴࡸࠠࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃ࠺ࠡࠤᐮ") + str(r.error) + bstack1111_opy_ (u"ࠣࠤᐯ"))
                self.bstack1l1l11ll111_opy_ = dict()
            return self.bstack1l1l11ll111_opy_
        except Exception as e:
            self.logger.error(bstack1111_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦᐰ") + str(traceback.format_exc()) + bstack1111_opy_ (u"ࠥࠦᐱ"))
            return dict()
    def bstack1ll1ll1l11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l1l1llll1_opy_ = None
        try:
            self.bstack1l1l111ll1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1111_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᐲ")
            req.script_name = bstack1111_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᐳ")
            req.platform_index = str(os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᐴ"), bstack1111_opy_ (u"ࠧ࠱ࠩᐵ")))
            req.client_worker_id = bstack1111_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᐶ").format(threading.get_ident(), os.getpid())
            r = self.bstack1lll111l111_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᐷ") + str(r.error) + bstack1111_opy_ (u"ࠥࠦᐸ"))
            else:
                bstack1l1l11l11l1_opy_ = self.bstack1l1l11l111l_opy_(test_uuid, r)
                bstack1l1l11ll1ll_opy_ = r.script
            self.logger.debug(bstack1111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᐹ") + str(bstack1l1l11l11l1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1l11ll1ll_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᐺ") + str(framework_name) + bstack1111_opy_ (u"ࠨࠠࠣᐻ"))
                return
            bstack1l1l1llll1_opy_ = bstack1l11l1ll_opy_.bstack11l111111_opy_(EVENTS.bstack1l1l11llll1_opy_.value)
            self.bstack1l1l1ll11ll_opy_(driver, bstack1l1l11ll1ll_opy_, bstack1l1l11l11l1_opy_, framework_name)
            try:
                bstack1l1l1ll11l1_opy_ = {
                    bstack1111_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᐼ"): {
                        bstack1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᐽ"): bstack1111_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᐾ"),
                    },
                    bstack1111_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᐿ"): {
                        bstack1111_opy_ (u"ࠦࡧࡵࡤࡺࠤᑀ"): {
                            bstack1111_opy_ (u"ࠧࡳࡳࡨࠤᑁ"): bstack1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᑂ"),
                            bstack1111_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᑃ"): True
                        }
                    }
                }
                self.bstack11llllll1l_opy_.info(json.dumps(bstack1l1l1ll11l1_opy_, separators=(bstack1111_opy_ (u"ࠨ࠮ࠪᑄ"), bstack1111_opy_ (u"ࠩ࠽ࠫᑅ"))))
            except Exception as bstack1l111l1l11_opy_:
                self.logger.debug(bstack1111_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᑆ") + str(bstack1l111l1l11_opy_) + bstack1111_opy_ (u"ࠦࠧᑇ"))
            self.logger.info(bstack1111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᑈ"))
            bstack1l11l1ll_opy_.end(EVENTS.bstack1l1l11llll1_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᑉ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᑊ"), True, None, command=bstack1111_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᑋ"),test_name=name)
        except Exception as bstack1l1l1ll1l1l_opy_:
            self.logger.error(bstack1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᑌ") + bstack1111_opy_ (u"ࠥࡷࡹࡸࠨࡱࡣࡷ࡬࠮ࠨᑍ") + bstack1111_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᑎ") + str(bstack1l1l1ll1l1l_opy_))
            bstack1l11l1ll_opy_.end(EVENTS.bstack1l1l11llll1_opy_.value, bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᑏ"), bstack1l1l1llll1_opy_+bstack1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᑐ"), False, bstack1l1l1ll1l1l_opy_, command=bstack1111_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᑑ"),test_name=name)
    def bstack1l1l1ll11ll_opy_(self, driver, bstack1l1l11ll1ll_opy_, bstack1l1l11l11l1_opy_, framework_name):
        if framework_name == bstack1111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᑒ"):
            self.bstack1l1l1lll111_opy_.bstack1l1l1l1111l_opy_(driver, bstack1l1l11ll1ll_opy_, bstack1l1l11l11l1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1l11ll1ll_opy_, bstack1l1l11l11l1_opy_))
    def _1l1l1ll111l_opy_(self, instance: bstack1ll11ll111l_opy_, args: Tuple) -> list:
        bstack1111_opy_ (u"ࠤࠥࠦࡊࡾࡴࡳࡣࡦࡸࠥࡺࡡࡨࡵࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᑓ")
        if bstack1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᑔ") in instance.bstack1l1ll111l11_opy_:
            return args[2].tags if hasattr(args[2], bstack1111_opy_ (u"ࠫࡹࡧࡧࡴࠩᑕ")) else []
        if hasattr(args[0], bstack1111_opy_ (u"ࠬࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠪᑖ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1l1l111l1_opy_(self, tags, capabilities):
        return self.bstack111l1lll1_opy_(tags) and self.bstack1ll1111l1l_opy_(capabilities)