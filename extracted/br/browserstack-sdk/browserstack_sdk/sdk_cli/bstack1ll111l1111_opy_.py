# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1ll1l1l1_opy_,
    bstack1lll111l1l1_opy_,
    bstack1ll1ll1lll1_opy_,
    bstack1ll1lll1111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1llll11l1_opy_ import bstack1ll1111ll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_, bstack1ll1l111111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll11ll11l1_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11llll_opy_ import bstack1ll11l1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1lll_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111111l_opy_ import bstack1ll11l1111l_opy_
from bstack_utils.helper import bstack1l1l11lllll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11111111l_opy_ import bstack1111l1l1l_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll11l1ll11_opy_(bstack1ll1l1l11l1_opy_):
    bstack1l1l1ll1ll1_opy_ = False
    bstack1l1l11lll11_opy_ = bstack11ll111_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨዦ")
    bstack1l1ll11ll11_opy_ = bstack11ll111_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧዧ")
    bstack1l1l11ll11l_opy_ = bstack11ll111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣየ")
    bstack1l1ll1111l1_opy_ = bstack11ll111_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤዩ")
    bstack1l1ll11l1l1_opy_ = bstack11ll111_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨዪ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll11111l1l_opy_, bstack1l1llllll11_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1ll1lll_opy_ = False
        self.bstack1l1l1ll1l11_opy_ = dict()
        self.bstack1l1ll1ll11_opy_ = logger_utils.bstack11l1l11ll_opy_(__name__)
        self.bstack1l1l1l11ll1_opy_ = False
        self.bstack1l1ll111l11_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1ll11llll_opy_ = bstack1l1llllll11_opy_
        bstack1ll11111l1l_opy_.bstack1l1l1lll11l_opy_((bstack1ll1ll1l1l1_opy_.bstack1ll1ll1l11l_opy_, bstack1lll111l1l1_opy_.PRE), self.bstack1l1ll11lll1_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.PRE), self.bstack1l1ll1111ll_opy_)
        TestFramework.bstack1l1l1lll11l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1l1llll1l1l_opy_.POST), self.bstack1l1ll111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1l1l111_opy_(instance, args)
        test_framework = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1ll1l1_opy_)
        if self.bstack1l1l1ll1lll_opy_:
            self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨያ")] = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
        if bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫዬ") in instance.bstack1l1l1ll1l1l_opy_:
            platform_index = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1ll1lll11_opy_)
            self.accessibility = self.bstack1l1l1ll111l_opy_(tags, self.config[bstack11ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫይ")][platform_index])
        else:
            capabilities = self.bstack1l1ll11llll_opy_.bstack1l1ll11111l_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤዮ") + str(kwargs) + bstack11ll111_opy_ (u"ࠥࠦዯ"))
                return
            self.accessibility = self.bstack1l1l1ll111l_opy_(tags, capabilities)
        if self.bstack1l1ll11llll_opy_.pages and self.bstack1l1ll11llll_opy_.pages.values():
            bstack1l1l1lll1ll_opy_ = list(self.bstack1l1ll11llll_opy_.pages.values())
            if bstack1l1l1lll1ll_opy_ and isinstance(bstack1l1l1lll1ll_opy_[0], (list, tuple)) and bstack1l1l1lll1ll_opy_[0]:
                bstack1l1l1l1l1l1_opy_ = bstack1l1l1lll1ll_opy_[0][0]
                if callable(bstack1l1l1l1l1l1_opy_):
                    page = bstack1l1l1l1l1l1_opy_()
                    def bstack1lll11ll11_opy_():
                        self.get_accessibility_results(page, bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣደ"))
                    def bstack1l1l1ll11ll_opy_():
                        self.get_accessibility_results_summary(page, bstack11ll111_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤዱ"))
                    setattr(page, bstack11ll111_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡴࠤዲ"), bstack1lll11ll11_opy_)
                    setattr(page, bstack11ll111_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤዳ"), bstack1l1l1ll11ll_opy_)
        self.logger.debug(bstack11ll111_opy_ (u"ࠣࡵ࡫ࡳࡺࡲࡤࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭ࡷࡨࡁࠧዴ") + str(self.accessibility) + bstack11ll111_opy_ (u"ࠤࠥድ"))
    def bstack1l1ll11lll1_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        driver: object,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll1l1l1_opy_, bstack1lll111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack11lll11111_opy_ = datetime.now()
            self.bstack1l1ll11l111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨዶ"), datetime.now() - bstack11lll11111_opy_)
            bstack1ll1llll111_opy_ = instance.data.get(bstack11ll111_opy_ (u"ࠫࡷࡧ࡮࡬ࠩዷ"), None)
            if (
                not f.bstack1l1l1l11111_opy_(method_name)
                or f.bstack1l1ll111l1l_opy_(method_name, *args)
                or f.bstack1l1l1llll11_opy_(method_name, *args)
                or (bstack1ll1llll111_opy_ and int(bstack1ll1llll111_opy_)>1)
            ):
                return
            if not f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1l11ll11l_opy_, False):
                if not bstack1ll11l1ll11_opy_.bstack1l1l1ll1ll1_opy_:
                    self.logger.warning(bstack11ll111_opy_ (u"ࠧࡡࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣዸ") + str(f.platform_index) + bstack11ll111_opy_ (u"ࠨ࡝ࠡࡣ࠴࠵ࡾࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡮ࡡࡷࡧࠣࡲࡴࡺࠠࡣࡧࡨࡲࠥࡹࡥࡵࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧዹ"))
                    bstack1ll11l1ll11_opy_.bstack1l1l1ll1ll1_opy_ = True
                return
            bstack1l1l1l111l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l1l111l1_opy_:
                platform_index = f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_, 0)
                self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧዺ") + str(f.framework_name) + bstack11ll111_opy_ (u"ࠣࠤዻ"))
                return
            command_name = f.bstack1l1l11ll111_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࠦዼ") + str(method_name) + bstack11ll111_opy_ (u"ࠥࠦዽ"))
                return
            bstack1l1l1l1l11l_opy_ = f.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1ll11l1l1_opy_, False)
            if command_name == bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࠣዾ") and not bstack1l1l1l1l11l_opy_:
                f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1ll11l1l1_opy_, True)
                bstack1l1l1l1l11l_opy_ = True
            if not bstack1l1l1l1l11l_opy_ and not self.bstack1l1l1ll1lll_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠧࡴ࡯ࠡࡗࡕࡐࠥࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦዿ") + str(command_name) + bstack11ll111_opy_ (u"ࠨࠢጀ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧጁ") + str(command_name) + bstack11ll111_opy_ (u"ࠣࠤጂ"))
                return
            self.logger.info(bstack11ll111_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡵࡦࡶ࡮ࡶࡴࡴࡡࡷࡳࡤࡸࡵ࡯ࠫࢀࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦጃ") + str(command_name) + bstack11ll111_opy_ (u"ࠥࠦጄ"))
            scripts = [(s, bstack1l1l1l111l1_opy_[s]) for s in scripts_to_run if s in bstack1l1l1l111l1_opy_]
            for script_name, bstack1l1l1lll1l1_opy_ in scripts:
                try:
                    bstack11lll11111_opy_ = datetime.now()
                    if script_name == bstack11ll111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤጅ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack1l11l111l1_opy_ = {
                                bstack11ll111_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨጆ"): {
                                    bstack11ll111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢጇ"): bstack11ll111_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡃࡂࡐࠥገ"),
                                    bstack11ll111_opy_ (u"ࠣࡲࡤࡶࡦࡳࡥࡵࡧࡵࡷࠧጉ"): [
                                        {
                                            bstack11ll111_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤጊ"): command_name
                                        }
                                    ]
                                },
                                bstack11ll111_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧጋ"): {
                                    bstack11ll111_opy_ (u"ࠦࡧࡵࡤࡺࠤጌ"): {
                                        bstack11ll111_opy_ (u"ࠧࡳࡳࡨࠤግ"): result.get(bstack11ll111_opy_ (u"ࠨ࡭ࡴࡩࠥጎ"), bstack11ll111_opy_ (u"ࠢࠣጏ")) if isinstance(result, dict) else bstack11ll111_opy_ (u"ࠣࠤጐ"),
                                        bstack11ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥ጑"): result.get(bstack11ll111_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦጒ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack1l1ll1ll11_opy_.info(json.dumps(bstack1l11l111l1_opy_, separators=(bstack11ll111_opy_ (u"ࠦ࠱ࠨጓ"), bstack11ll111_opy_ (u"ࠧࡀࠢጔ"))))
                        except Exception as bstack111lll11l1_opy_:
                            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡤࡣࡱࠤࡩࡧࡴࡢ࠼ࠣࠦጕ") + str(bstack111lll11l1_opy_) + bstack11ll111_opy_ (u"ࠢࠣ጖"))
                    instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࠢ጗") + script_name, datetime.now() - bstack11lll11111_opy_)
                    if isinstance(result, dict) and not result.get(bstack11ll111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥጘ"), True):
                        self.logger.warning(bstack11ll111_opy_ (u"ࠥࡷࡰ࡯ࡰࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡷ࡫࡭ࡢ࡫ࡱ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࠥጙ") + str(result) + bstack11ll111_opy_ (u"ࠦࠧጚ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11ll111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃࠠࡦࡴࡵࡳࡷࡃࠢጛ") + str(e) + bstack11ll111_opy_ (u"ࠨࠢጜ"))
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴࡀࠦጝ") + str(e) + bstack11ll111_opy_ (u"ࠣࠤጞ"))
    def bstack1l1ll111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l111111_opy_,
        bstack1ll1ll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1l1llll1l1l_opy_],
        *args,
        **kwargs,
    ):
        if bstack11ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ጟ") not in instance.bstack1l1l1ll1l1l_opy_:
            tags = self._1l1l1l1l111_opy_(instance, args)
            capabilities = self.bstack1l1ll11llll_opy_.bstack1l1ll11111l_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l1l1ll111l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢጠ"))
            return
        driver = self.bstack1l1ll11llll_opy_.bstack1l1l1l1l1ll_opy_(f, instance, bstack1ll1ll1llll_opy_, *args, **kwargs)
        test_name = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1l1l1111l_opy_)
        if not test_name:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤጡ"))
            return
        test_uuid = f.bstack1ll1lllll11_opy_(instance, TestFramework.bstack1l1l11ll1ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥጢ"))
            return
        if isinstance(self.bstack1l1ll11llll_opy_, bstack1ll1l1ll1ll_opy_):
            framework_name = bstack11ll111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪጣ")
        else:
            framework_name = bstack11ll111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩጤ")
        self.bstack111l1l11l1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack111ll111ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࠤጥ"))
            return
        bstack11lll11111_opy_ = datetime.now()
        bstack1l1l1lll1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll111_opy_ (u"ࠤࡶࡧࡦࡴࠢጦ"), None)
        if not bstack1l1l1lll1l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥጧ") + str(framework_name) + bstack11ll111_opy_ (u"ࠦࠥࠨጨ"))
            return
        if self.bstack1l1l1ll1lll_opy_:
            arg = dict()
            arg[bstack11ll111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧጩ")] = method if method else bstack11ll111_opy_ (u"ࠨࠢጪ")
            arg[bstack11ll111_opy_ (u"ࠢࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠢጫ")] = self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣጬ")]
            arg[bstack11ll111_opy_ (u"ࠤࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠢጭ")] = self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣጮ")]
            arg[bstack11ll111_opy_ (u"ࠦࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣጯ")] = self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠥጰ")]
            arg[bstack11ll111_opy_ (u"ࠨࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠥጱ")] = self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨጲ")]
            arg[bstack11ll111_opy_ (u"ࠣࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠣጳ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1l1llll1l_opy_ = self.bstack1l1l1lllll1_opy_(bstack11ll111_opy_ (u"ࠤࡶࡧࡦࡴࠢጴ"), self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥጵ")])
            if bstack11ll111_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡖࡲ࡯ࡪࡴࠢጶ") in bstack1l1l1llll1l_opy_:
                bstack1l1l1llll1l_opy_ = bstack1l1l1llll1l_opy_.copy()
                bstack1l1l1llll1l_opy_[bstack11ll111_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡋࡩࡦࡪࡥࡳࠤጷ")] = bstack1l1l1llll1l_opy_.pop(bstack11ll111_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤጸ"))
            arg = bstack1l1l11lllll_opy_(arg, bstack1l1l1llll1l_opy_)
            bstack1l1ll1l1l11_opy_ = bstack1l1l1lll1l1_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1ll1l1l11_opy_)
            return
        instance = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(driver)
        if instance:
            if not bstack1ll1ll1lll1_opy_.bstack1ll1lllll11_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1ll1111l1_opy_, False):
                bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1ll1111l1_opy_, True)
            else:
                self.logger.info(bstack11ll111_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦጹ") + str(method) + bstack11ll111_opy_ (u"ࠣࠤጺ"))
                return
        self.logger.info(bstack11ll111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢጻ") + str(method) + bstack11ll111_opy_ (u"ࠥࠦጼ"))
        if framework_name == bstack11ll111_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨጽ"):
            result = self.bstack1l1ll11llll_opy_.bstack1l1ll1ll111_opy_(driver, bstack1l1l1lll1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1lll1l1_opy_, {bstack11ll111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧጾ"): method if method else bstack11ll111_opy_ (u"ࠨࠢጿ")})
        bstack1111l1l1l_opy_.end(EVENTS.bstack111ll111ll_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢፀ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨፁ"), True, None, command=method)
        if instance:
            bstack1ll1ll1lll1_opy_.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1ll1111l1_opy_, False)
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨፂ"), datetime.now() - bstack11lll11111_opy_)
        return result
        def bstack1l1l1ll11l1_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l11llll1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l1l111ll_opy_ = self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥፃ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫፄ"), bstack11ll111_opy_ (u"ࠬ࠶ࠧፅ")))
            req.client_worker_id = bstack11ll111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧፆ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1l1llllll1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11ll111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤፇ") + str(r) + bstack11ll111_opy_ (u"ࠣࠤፈ"))
                else:
                    bstack1l1l1l1llll_opy_ = json.loads(r.bstack1l1ll1l1ll1_opy_.decode(bstack11ll111_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨፉ")))
                    if result_type == bstack11ll111_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧፊ"):
                        return bstack1l1l1l1llll_opy_.get(bstack11ll111_opy_ (u"ࠦࡩࡧࡴࡢࠤፋ"), [])
                    else:
                        return bstack1l1l1l1llll_opy_.get(bstack11ll111_opy_ (u"ࠧࡪࡡࡵࡣࠥፌ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11ll111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡲࡳࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࠤ࡫ࡸ࡯࡮ࠢࡦࡰ࡮ࡀࠠࠣፍ") + str(e) + bstack11ll111_opy_ (u"ࠢࠣፎ"))
    @measure(event_name=EVENTS.bstack111ll1111_opy_, stage=STAGE.bstack1111l1111_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥፏ"))
            return
        if self.bstack1l1l1ll1lll_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡣࡳࡴࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬፐ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1ll11l1_opy_(driver, framework_name, bstack11ll111_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢፑ"))
        bstack1l1l1lll1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣፒ"), None)
        if not bstack1l1l1lll1l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦፓ") + str(framework_name) + bstack11ll111_opy_ (u"ࠨࠢፔ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11lll11111_opy_ = datetime.now()
        if framework_name == bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫፕ"):
            result = self.bstack1l1ll11llll_opy_.bstack1l1ll1ll111_opy_(driver, bstack1l1l1lll1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1lll1l1_opy_)
        instance = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(driver)
        if instance:
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦፖ"), datetime.now() - bstack11lll11111_opy_)
        return result
    @measure(event_name=EVENTS.bstack11l1111111_opy_, stage=STAGE.bstack1111l1111_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧፗ"))
            return
        if self.bstack1l1l1ll1lll_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1ll11l1_opy_(driver, framework_name, bstack11ll111_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧፘ"))
        bstack1l1l1lll1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll111_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣፙ"), None)
        if not bstack1l1l1lll1l1_opy_:
            self.logger.debug(bstack11ll111_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦፚ") + str(framework_name) + bstack11ll111_opy_ (u"ࠨࠢ፛"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11lll11111_opy_ = datetime.now()
        if framework_name == bstack11ll111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫ፜"):
            result = self.bstack1l1ll11llll_opy_.bstack1l1ll1ll111_opy_(driver, bstack1l1l1lll1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1lll1l1_opy_)
        instance = bstack1ll1ll1lll1_opy_.bstack1lll1111111_opy_(driver)
        if instance:
            instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧ፝"), datetime.now() - bstack11lll11111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l1l11l11_opy_, stage=STAGE.bstack1111l1111_opy_)
    def bstack1l1l1llllll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l11llll1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11ll111_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ፞").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1l1llllll1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧ፟") + str(r) + bstack11ll111_opy_ (u"ࠦࠧ፠"))
            else:
                self.bstack1l1l1l1ll1l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥ፡") + str(e) + bstack11ll111_opy_ (u"ࠨࠢ።"))
            traceback.print_exc()
            raise e
    def bstack1l1l1l1ll1l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ፣"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1ll1lll_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨ፤")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1l1ll1l11_opy_[bstack11ll111_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣ፥")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1l1ll1l11_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1ll111lll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1l11lll11_opy_ and command.module == self.bstack1l1ll11ll11_opy_:
                        if command.method and not command.method in bstack1l1ll111lll_opy_:
                            bstack1l1ll111lll_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1ll111lll_opy_[command.method]:
                            bstack1l1ll111lll_opy_[command.method][command.name] = list()
                        bstack1l1ll111lll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1ll111lll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1ll11l111_opy_(
        self,
        f: bstack1ll1111ll11_opy_,
        exec: Tuple[bstack1ll1lll1111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1ll11llll_opy_, bstack1ll1l1ll1ll_opy_) and method_name != bstack11ll111_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫ፦"):
            return
        if bstack1ll1ll1lll1_opy_.bstack1ll1lll111l_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1l11ll11l_opy_):
            return
        if f.bstack1l1l11lll1l_opy_(method_name, *args):
            bstack1l1l1ll1111_opy_ = False
            desired_capabilities = f.bstack1l1ll1l11ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1ll1l1111_opy_(instance)
                platform_index = f.bstack1ll1lllll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1lll11_opy_, 0)
                bstack1l1ll1l111l_opy_ = datetime.now()
                r = self.bstack1l1l1llllll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll1l1l11_opy_(bstack11ll111_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤ፧"), datetime.now() - bstack1l1ll1l111l_opy_)
                bstack1l1l1ll1111_opy_ = r.success
            else:
                self.logger.error(bstack11ll111_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡤࡦࡵ࡬ࡶࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡃࠢ፨") + str(desired_capabilities) + bstack11ll111_opy_ (u"ࠨࠢ፩"))
            f.bstack1lll11l1111_opy_(instance, bstack1ll11l1ll11_opy_.bstack1l1l11ll11l_opy_, bstack1l1l1ll1111_opy_)
    def bstack1l11ll1111_opy_(self, test_tags):
        bstack1l1l1llllll_opy_ = self.config.get(bstack11ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ፪"))
        if not bstack1l1l1llllll_opy_:
            return True
        try:
            include_tags = bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭፫")] if bstack11ll111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ፬") in bstack1l1l1llllll_opy_ and isinstance(bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ፭")], list) else []
            exclude_tags = bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ፮")] if bstack11ll111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ፯") in bstack1l1l1llllll_opy_ and isinstance(bstack1l1l1llllll_opy_[bstack11ll111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ፰")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11ll111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢ፱") + str(error))
        return False
    def bstack1l1lllll1l_opy_(self, caps):
        try:
            if self.bstack1l1l1ll1lll_opy_:
                bstack1l1l11l1lll_opy_ = caps.get(bstack11ll111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ፲"))
                if bstack1l1l11l1lll_opy_ is not None and str(bstack1l1l11l1lll_opy_).lower() == bstack11ll111_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥ፳"):
                    bstack1l1l1l1ll11_opy_ = caps.get(bstack11ll111_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ፴")) or caps.get(bstack11ll111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ፵"))
                    if bstack1l1l1l1ll11_opy_ is not None and int(bstack1l1l1l1ll11_opy_) < 11:
                        self.logger.warning(bstack11ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠧ፶") + str(bstack1l1l1l1ll11_opy_) + bstack11ll111_opy_ (u"ࠨࠢ፷"))
                        return False
                return True
            bstack1l1l1l1lll1_opy_ = caps.get(bstack11ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ፸"), {}).get(bstack11ll111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ፹"), caps.get(bstack11ll111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ፺"), bstack11ll111_opy_ (u"ࠪࠫ፻")))
            if bstack1l1l1l1lll1_opy_:
                self.logger.warning(bstack11ll111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ፼"))
                return False
            browser = caps.get(bstack11ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ፽"), bstack11ll111_opy_ (u"࠭ࠧ፾")).lower()
            if browser != bstack11ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ፿"):
                self.logger.warning(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᎀ"))
                return False
            bstack1l1ll1l1l1l_opy_ = bstack1l1ll111111_opy_
            if not self.config.get(bstack11ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᎁ")) or self.config.get(bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧᎂ")):
                bstack1l1ll1l1l1l_opy_ = bstack1l1ll11l11l_opy_
            browser_version = caps.get(bstack11ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᎃ"))
            if not browser_version:
                browser_version = caps.get(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᎄ"), {}).get(bstack11ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᎅ"), bstack11ll111_opy_ (u"ࠧࠨᎆ"))
            bstack1l1ll1ll1ll_opy_ = str(browser_version).lower() if browser_version is not None else bstack11ll111_opy_ (u"ࠨࠩᎇ")
            if bstack1l1ll1ll1ll_opy_:
                if bstack1l1ll1ll1ll_opy_.startswith(bstack11ll111_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᎈ")):
                    if bstack1l1ll1ll1ll_opy_.startswith(bstack11ll111_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᎉ")):
                        bstack1l1ll1l1lll_opy_ = bstack1l1ll1ll1ll_opy_[len(bstack11ll111_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬᎊ")):]
                        if bstack1l1ll1l1lll_opy_ and not bstack1l1ll1l1lll_opy_.isdigit():
                            self.logger.warning(bstack11ll111_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡨࡲࡶࡲࡧࡴࠡࠩࠥᎋ") + str(browser_version) + bstack11ll111_opy_ (u"ࠨࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࠬࡲࡡࡵࡧࡶࡸࠬࠦ࡯ࡳࠢࠪࡰࡦࡺࡥࡴࡶ࠰ࡀࡳࡻ࡭ࡣࡧࡵࡂࠬ࠴ࠢᎌ"))
                            return False
                else:
                    try:
                        if int(bstack1l1ll1ll1ll_opy_.split(bstack11ll111_opy_ (u"ࠧ࠯ࠩᎍ"))[0]) <= bstack1l1ll1l1l1l_opy_:
                            self.logger.warning(bstack11ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥᎎ") + str(bstack1l1ll1l1l1l_opy_) + bstack11ll111_opy_ (u"ࠤ࠱ࠦᎏ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11ll111_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠨࡽࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࢁࠬࡀࠠࠣ᎐") + str(e) + bstack11ll111_opy_ (u"ࠦࠧ᎑"))
            bstack1l1ll1ll11l_opy_ = caps.get(bstack11ll111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᎒"), {}).get(bstack11ll111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᎓"))
            if not bstack1l1ll1ll11l_opy_:
                bstack1l1ll1ll11l_opy_ = caps.get(bstack11ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᎔"), {})
            if bstack1l1ll1ll11l_opy_ and bstack11ll111_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬ᎕") in bstack1l1ll1ll11l_opy_.get(bstack11ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᎖"), []):
                self.logger.warning(bstack11ll111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧ᎗"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨ᎘") + str(error))
            return False
    def bstack1l1ll11l1ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1ll11ll1l_opy_ = {
            bstack11ll111_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ᎙"): test_uuid,
        }
        bstack1l1l1l11l1l_opy_ = {}
        if result.success:
            bstack1l1l1l11l1l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l11lllll_opy_(bstack1l1ll11ll1l_opy_, bstack1l1l1l11l1l_opy_)
    def bstack1l1l1lllll1_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11ll111_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡪࡺࡣࡩࠢࡦࡩࡳࡺࡲࡢ࡮ࠣࡥࡺࡺࡨࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡰࡤࡱࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡦࡥࡨ࡮ࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡦࡦࡶࡦ࡬ࡪࡪࠬࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠤࡱࡵࡡࡥࡵࠣࡥࡳࡪࠠࡤࡣࡦ࡬ࡪࡹࠠࡪࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫࠺ࠡࡐࡤࡱࡪࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡳࡤࡴ࡬ࡴࡹࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡶࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࡀࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠮ࠣࡩࡲࡶࡴࡺࠢࡧ࡭ࡨࡺࠠࡪࡨࠣࡩࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᎚")
        try:
            if self.bstack1l1l1l11ll1_opy_:
                return self.bstack1l1ll111l11_opy_
            self.bstack1l1l11llll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ᎛")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᎜"), bstack11ll111_opy_ (u"ࠩ࠳ࠫ᎝")))
            req.client_worker_id = bstack11ll111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᎞").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1llllll1l_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1ll111l11_opy_ = self.bstack1l1ll11l1ll_opy_(test_uuid, r)
                self.bstack1l1l1l11ll1_opy_ = True
            else:
                self.logger.error(bstack11ll111_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨ᎟") + str(r.error) + bstack11ll111_opy_ (u"ࠧࠨᎠ"))
                self.bstack1l1ll111l11_opy_ = dict()
            return self.bstack1l1ll111l11_opy_
        except Exception as e:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣᎡ") + str(traceback.format_exc()) + bstack11ll111_opy_ (u"ࠢࠣᎢ"))
            return dict()
    def bstack111l1l11l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack11llllllll_opy_ = None
        try:
            self.bstack1l1l11llll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll111_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣᎣ")
            req.script_name = bstack11ll111_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢᎤ")
            req.platform_index = str(os.environ.get(bstack11ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᎥ"), bstack11ll111_opy_ (u"ࠫ࠵࠭Ꭶ")))
            req.client_worker_id = bstack11ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᎧ").format(threading.get_ident(), os.getpid())
            r = self.bstack1l1llllll1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11ll111_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᎨ") + str(r.error) + bstack11ll111_opy_ (u"ࠢࠣᎩ"))
            else:
                bstack1l1ll11ll1l_opy_ = self.bstack1l1ll11l1ll_opy_(test_uuid, r)
                bstack1l1l1lll1l1_opy_ = r.script
            self.logger.debug(bstack11ll111_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᎪ") + str(bstack1l1ll11ll1l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1l1lll1l1_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᎫ") + str(framework_name) + bstack11ll111_opy_ (u"ࠥࠤࠧᎬ"))
                return
            bstack11llllllll_opy_ = bstack1111l1l1l_opy_.bstack1ll111l11_opy_(EVENTS.bstack1l1ll1l11l1_opy_.value)
            self.bstack1l1l11ll1l1_opy_(driver, bstack1l1l1lll1l1_opy_, bstack1l1ll11ll1l_opy_, framework_name)
            try:
                bstack1l1l1lll111_opy_ = {
                    bstack11ll111_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧᎭ"): {
                        bstack11ll111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨᎮ"): bstack11ll111_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥᎯ"),
                    },
                    bstack11ll111_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤᎰ"): {
                        bstack11ll111_opy_ (u"ࠣࡤࡲࡨࡾࠨᎱ"): {
                            bstack11ll111_opy_ (u"ࠤࡰࡷ࡬ࠨᎲ"): bstack11ll111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᎳ"),
                            bstack11ll111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᎴ"): True
                        }
                    }
                }
                self.bstack1l1ll1ll11_opy_.info(json.dumps(bstack1l1l1lll111_opy_, separators=(bstack11ll111_opy_ (u"ࠬ࠲ࠧᎵ"), bstack11ll111_opy_ (u"࠭࠺ࠨᎶ"))))
            except Exception as bstack111lll11l1_opy_:
                self.logger.debug(bstack11ll111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨᎷ") + str(bstack111lll11l1_opy_) + bstack11ll111_opy_ (u"ࠣࠤᎸ"))
            self.logger.info(bstack11ll111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᎹ"))
            bstack1111l1l1l_opy_.end(EVENTS.bstack1l1ll1l11l1_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᎺ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᎻ"), True, None, command=bstack11ll111_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᎼ"),test_name=name)
        except Exception as bstack1l1l1l11lll_opy_:
            self.logger.error(bstack11ll111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᎽ") + bstack11ll111_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥᎾ") + bstack11ll111_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᎿ") + str(bstack1l1l1l11lll_opy_))
            bstack1111l1l1l_opy_.end(EVENTS.bstack1l1ll1l11l1_opy_.value, bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᏀ"), bstack11llllllll_opy_+bstack11ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᏁ"), False, bstack1l1l1l11lll_opy_, command=bstack11ll111_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᏂ"),test_name=name)
    def bstack1l1l11ll1l1_opy_(self, driver, bstack1l1l1lll1l1_opy_, bstack1l1ll11ll1l_opy_, framework_name):
        if framework_name == bstack11ll111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᏃ"):
            self.bstack1l1ll11llll_opy_.bstack1l1ll1ll111_opy_(driver, bstack1l1l1lll1l1_opy_, bstack1l1ll11ll1l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1l1lll1l1_opy_, bstack1l1ll11ll1l_opy_))
    def _1l1l1l1l111_opy_(self, instance: bstack1ll1l111111_opy_, args: Tuple) -> list:
        bstack11ll111_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᏄ")
        if bstack11ll111_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᏅ") in instance.bstack1l1l1ll1l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack11ll111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ꮖ")) else []
        if hasattr(args[0], bstack11ll111_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧᏇ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1l1ll111l_opy_(self, tags, capabilities):
        return self.bstack1l11ll1111_opy_(tags) and self.bstack1l1lllll1l_opy_(capabilities)