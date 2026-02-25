# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import (
    bstack1ll1lll1lll_opy_,
    bstack1lll11l111l_opy_,
    bstack1lll11ll1l1_opy_,
    bstack1ll1llll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll11lll_opy_ import bstack1l1lllll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_, bstack1l1llll111l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1l11l1_opy_ import bstack1ll11llll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1ll111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll111_opy_ import bstack1ll1l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11111l11_opy_ import bstack1l1lllll1ll_opy_
from bstack_utils.helper import bstack1l1l1l11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack111lll111l_opy_ import bstack11ll1l1l1_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll11l11ll1_opy_(bstack1ll11llll11_opy_):
    bstack1l1ll1ll11l_opy_ = False
    bstack1l1ll1ll111_opy_ = bstack11l1l11_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥዪ")
    bstack1l1l11llll1_opy_ = bstack11l1l11_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤያ")
    bstack1l1l1l11l1l_opy_ = bstack11l1l11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠧዬ")
    bstack1l1l1l11111_opy_ = bstack11l1l11_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡶࡣࡸࡩࡡ࡯ࡰ࡬ࡲ࡬ࠨይ")
    bstack1l1ll1l11ll_opy_ = bstack11l1l11_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳࡡ࡫ࡥࡸࡥࡵࡳ࡮ࠥዮ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll11l1llll_opy_, bstack1l1llll1l11_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1l1l111_opy_ = False
        self.bstack1l1l1l1ll1l_opy_ = dict()
        self.bstack11ll111ll_opy_ = logger_utils.bstack1lll1lll_opy_(__name__)
        self.bstack1l1ll1lll11_opy_ = False
        self.bstack1l1ll1l1l11_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l11lllll_opy_ = bstack1l1llll1l11_opy_
        bstack1ll11l1llll_opy_.bstack1l1l11lll1l_opy_((bstack1ll1lll1lll_opy_.bstack1lll11111ll_opy_, bstack1lll11l111l_opy_.PRE), self.bstack1l1l1ll1lll_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.PRE), self.bstack1l1ll11111l_opy_)
        TestFramework.bstack1l1l11lll1l_opy_((bstack1l1llllll1l_opy_.TEST, bstack1ll11lll1ll_opy_.POST), self.bstack1l1l1ll11l1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1ll11l1ll_opy_(instance, args)
        test_framework = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1ll1l1lll_opy_)
        if self.bstack1l1l1l1l111_opy_:
            self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥዯ")] = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
        if bstack11l1l11_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨደ") in instance.bstack1l1l1ll1ll1_opy_:
            platform_index = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
            self.accessibility = self.bstack1l1ll1l1ll1_opy_(tags, self.config[bstack11l1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨዱ")][platform_index])
        else:
            capabilities = self.bstack1l1l11lllll_opy_.bstack1l1ll1l11l1_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨዲ") + str(kwargs) + bstack11l1l11_opy_ (u"ࠢࠣዳ"))
                return
            self.accessibility = self.bstack1l1ll1l1ll1_opy_(tags, capabilities)
        if self.bstack1l1l11lllll_opy_.pages and self.bstack1l1l11lllll_opy_.pages.values():
            bstack1l1l11ll11l_opy_ = list(self.bstack1l1l11lllll_opy_.pages.values())
            if bstack1l1l11ll11l_opy_ and isinstance(bstack1l1l11ll11l_opy_[0], (list, tuple)) and bstack1l1l11ll11l_opy_[0]:
                bstack1l1l1ll111l_opy_ = bstack1l1l11ll11l_opy_[0][0]
                if callable(bstack1l1l1ll111l_opy_):
                    page = bstack1l1l1ll111l_opy_()
                    def bstack1llll11111_opy_():
                        self.get_accessibility_results(page, bstack11l1l11_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧዴ"))
                    def bstack1l1l1l1l1ll_opy_():
                        self.get_accessibility_results_summary(page, bstack11l1l11_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨድ"))
                    setattr(page, bstack11l1l11_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡸࠨዶ"), bstack1llll11111_opy_)
                    setattr(page, bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨዷ"), bstack1l1l1l1l1ll_opy_)
        self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡹࡨࡰࡷ࡯ࡨࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱࡻࡥ࠾ࠤዸ") + str(self.accessibility) + bstack11l1l11_opy_ (u"ࠨࠢዹ"))
    def bstack1l1l1ll1lll_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        driver: object,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        bstack1lll11ll111_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll11l111l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack111l11l1l1_opy_ = datetime.now()
            self.bstack1l1ll111111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥዺ"), datetime.now() - bstack111l11l1l1_opy_)
            bstack1lll1111l11_opy_ = instance.data.get(bstack11l1l11_opy_ (u"ࠨࡴࡤࡲࡰ࠭ዻ"), None)
            if (
                not f.bstack1l1ll1ll1ll_opy_(method_name)
                or f.bstack1l1l1l1111l_opy_(method_name, *args)
                or f.bstack1l1l1llll1l_opy_(method_name, *args)
                or (bstack1lll1111l11_opy_ and int(bstack1lll1111l11_opy_)>1)
            ):
                return
            if not f.bstack1ll1lll111l_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1l1l11l1l_opy_, False):
                if not bstack1ll11l11ll1_opy_.bstack1l1ll1ll11l_opy_:
                    self.logger.warning(bstack11l1l11_opy_ (u"ࠤ࡞ࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧዼ") + str(f.platform_index) + bstack11l1l11_opy_ (u"ࠥࡡࠥࡧ࠱࠲ࡻࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢ࡫ࡥࡻ࡫ࠠ࡯ࡱࡷࠤࡧ࡫ࡥ࡯ࠢࡶࡩࡹࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠤዽ"))
                    bstack1ll11l11ll1_opy_.bstack1l1ll1ll11l_opy_ = True
                return
            bstack1l1l1ll11ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l1ll11ll_opy_:
                platform_index = f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_, 0)
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤዾ") + str(f.framework_name) + bstack11l1l11_opy_ (u"ࠧࠨዿ"))
                return
            command_name = f.bstack1l1l1l11lll_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࠣጀ") + str(method_name) + bstack11l1l11_opy_ (u"ࠢࠣጁ"))
                return
            bstack1l1l1l1l11l_opy_ = f.bstack1ll1lll111l_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1ll1l11ll_opy_, False)
            if command_name == bstack11l1l11_opy_ (u"ࠣࡩࡨࡸࠧጂ") and not bstack1l1l1l1l11l_opy_:
                f.bstack1lll111ll11_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1ll1l11ll_opy_, True)
                bstack1l1l1l1l11l_opy_ = True
            if not bstack1l1l1l1l11l_opy_ and not self.bstack1l1l1l1l111_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡱࡳ࡛ࠥࡒࡍࠢ࡯ࡳࡦࡪࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣጃ") + str(command_name) + bstack11l1l11_opy_ (u"ࠥࠦጄ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤጅ") + str(command_name) + bstack11l1l11_opy_ (u"ࠧࠨጆ"))
                return
            self.logger.info(bstack11l1l11_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡹࡣࡳ࡫ࡳࡸࡸࡥࡴࡰࡡࡵࡹࡳ࠯ࡽࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣጇ") + str(command_name) + bstack11l1l11_opy_ (u"ࠢࠣገ"))
            scripts = [(s, bstack1l1l1ll11ll_opy_[s]) for s in scripts_to_run if s in bstack1l1l1ll11ll_opy_]
            for script_name, bstack1l1ll11l11l_opy_ in scripts:
                try:
                    bstack111l11l1l1_opy_ = datetime.now()
                    if script_name == bstack11l1l11_opy_ (u"ࠣࡵࡦࡥࡳࠨጉ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack11ll1llll_opy_ = {
                                bstack11l1l11_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥጊ"): {
                                    bstack11l1l11_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦጋ"): bstack11l1l11_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡇࡆࡔࠢጌ"),
                                    bstack11l1l11_opy_ (u"ࠧࡶࡡࡳࡣࡰࡩࡹ࡫ࡲࡴࠤግ"): [
                                        {
                                            bstack11l1l11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨጎ"): command_name
                                        }
                                    ]
                                },
                                bstack11l1l11_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤጏ"): {
                                    bstack11l1l11_opy_ (u"ࠣࡤࡲࡨࡾࠨጐ"): {
                                        bstack11l1l11_opy_ (u"ࠤࡰࡷ࡬ࠨ጑"): result.get(bstack11l1l11_opy_ (u"ࠥࡱࡸ࡭ࠢጒ"), bstack11l1l11_opy_ (u"ࠦࠧጓ")) if isinstance(result, dict) else bstack11l1l11_opy_ (u"ࠧࠨጔ"),
                                        bstack11l1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢጕ"): result.get(bstack11l1l11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ጖"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack11ll111ll_opy_.info(json.dumps(bstack11ll1llll_opy_, separators=(bstack11l1l11_opy_ (u"ࠣ࠮ࠥ጗"), bstack11l1l11_opy_ (u"ࠤ࠽ࠦጘ"))))
                        except Exception as bstack111l1l11ll_opy_:
                            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮ࠡࡦࡤࡸࡦࡀࠠࠣጙ") + str(bstack111l1l11ll_opy_) + bstack11l1l11_opy_ (u"ࠦࠧጚ"))
                    instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦጛ") + script_name, datetime.now() - bstack111l11l1l1_opy_)
                    if isinstance(result, dict) and not result.get(bstack11l1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢጜ"), True):
                        self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢጝ") + str(result) + bstack11l1l11_opy_ (u"ࠣࠤጞ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11l1l11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦጟ") + str(e) + bstack11l1l11_opy_ (u"ࠥࠦጠ"))
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣጡ") + str(e) + bstack11l1l11_opy_ (u"ࠧࠨጢ"))
    def bstack1l1l1ll11l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1l1llll111l_opy_,
        bstack1lll11ll111_opy_: Tuple[bstack1l1llllll1l_opy_, bstack1ll11lll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1ll11l1ll_opy_(instance, args)
        capabilities = self.bstack1l1l11lllll_opy_.bstack1l1ll1l11l1_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l1ll1l1ll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥጣ"))
            return
        driver = self.bstack1l1l11lllll_opy_.bstack1l1ll111ll1_opy_(f, instance, bstack1lll11ll111_opy_, *args, **kwargs)
        test_name = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1ll11llll_opy_)
        if not test_name:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧጤ"))
            return
        test_uuid = f.bstack1ll1lll111l_opy_(instance, TestFramework.bstack1l1l11lll11_opy_)
        if not test_uuid:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨጥ"))
            return
        if isinstance(self.bstack1l1l11lllll_opy_, bstack1ll1l11l11l_opy_):
            framework_name = bstack11l1l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ጦ")
        else:
            framework_name = bstack11l1l11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬጧ")
        self.bstack1l111ll1l1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1l11llll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧጨ"))
            return
        bstack111l11l1l1_opy_ = datetime.now()
        bstack1l1ll11l11l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠧࡹࡣࡢࡰࠥጩ"), None)
        if not bstack1l1ll11l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨጪ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠢࠡࠤጫ"))
            return
        if self.bstack1l1l1l1l111_opy_:
            arg = dict()
            arg[bstack11l1l11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣጬ")] = method if method else bstack11l1l11_opy_ (u"ࠤࠥጭ")
            arg[bstack11l1l11_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥጮ")] = self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦጯ")]
            arg[bstack11l1l11_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥጰ")] = self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦጱ")]
            arg[bstack11l1l11_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦጲ")] = self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨጳ")]
            arg[bstack11l1l11_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨጴ")] = self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤጵ")]
            arg[bstack11l1l11_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦጶ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1ll11l1l1_opy_ = self.bstack1l1l1ll1l1l_opy_(bstack11l1l11_opy_ (u"ࠧࡹࡣࡢࡰࠥጷ"), self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨጸ")])
            if bstack11l1l11_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥጹ") in bstack1l1ll11l1l1_opy_:
                bstack1l1ll11l1l1_opy_ = bstack1l1ll11l1l1_opy_.copy()
                bstack1l1ll11l1l1_opy_[bstack11l1l11_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧጺ")] = bstack1l1ll11l1l1_opy_.pop(bstack11l1l11_opy_ (u"ࠤࡦࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠧጻ"))
            arg = bstack1l1l1l11l11_opy_(arg, bstack1l1ll11l1l1_opy_)
            bstack1l1l1l11ll1_opy_ = bstack1l1ll11l11l_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1l1l11ll1_opy_)
            return
        instance = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(driver)
        if instance:
            if not bstack1lll11ll1l1_opy_.bstack1ll1lll111l_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1l1l11111_opy_, False):
                bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1l1l11111_opy_, True)
            else:
                self.logger.info(bstack11l1l11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥࡱࡸࡥࡢࡦࡼࠤ࡮ࡴࠠࡱࡴࡲ࡫ࡷ࡫ࡳࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢጼ") + str(method) + bstack11l1l11_opy_ (u"ࠦࠧጽ"))
                return
        self.logger.info(bstack11l1l11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥጾ") + str(method) + bstack11l1l11_opy_ (u"ࠨࠢጿ"))
        if framework_name == bstack11l1l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫፀ"):
            result = self.bstack1l1l11lllll_opy_.bstack1l1l1ll1l11_opy_(driver, bstack1l1ll11l11l_opy_)
        else:
            result = driver.execute_async_script(bstack1l1ll11l11l_opy_, {bstack11l1l11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣፁ"): method if method else bstack11l1l11_opy_ (u"ࠤࠥፂ")})
        bstack11ll1l1l1_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥፃ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤፄ"), True, None, command=method)
        if instance:
            bstack1lll11ll1l1_opy_.bstack1lll111ll11_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1l1l11111_opy_, False)
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯ࠤፅ"), datetime.now() - bstack111l11l1l1_opy_)
        return result
        def bstack1l1l1lll11l_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l1ll1111_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l1lll1ll_opy_ = self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨፆ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧፇ"), bstack11l1l11_opy_ (u"ࠨ࠲ࠪፈ")))
            req.client_worker_id = bstack11l1l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣፉ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1ll11111_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧፊ") + str(r) + bstack11l1l11_opy_ (u"ࠦࠧፋ"))
                else:
                    bstack1l1l1l111l1_opy_ = json.loads(r.bstack1l1l1l111ll_opy_.decode(bstack11l1l11_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫፌ")))
                    if result_type == bstack11l1l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪፍ"):
                        return bstack1l1l1l111l1_opy_.get(bstack11l1l11_opy_ (u"ࠢࡥࡣࡷࡥࠧፎ"), [])
                    else:
                        return bstack1l1l1l111l1_opy_.get(bstack11l1l11_opy_ (u"ࠣࡦࡤࡸࡦࠨፏ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11l1l11_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡵࡶ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡩ࡬ࡪ࠼ࠣࠦፐ") + str(e) + bstack11l1l11_opy_ (u"ࠥࠦፑ"))
    @measure(event_name=EVENTS.bstack1l11ll11_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨፒ"))
            return
        if self.bstack1l1l1l1l111_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡦࡶࡰࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨፓ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1lll11l_opy_(driver, framework_name, bstack11l1l11_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥፔ"))
        bstack1l1ll11l11l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦፕ"), None)
        if not bstack1l1ll11l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢፖ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠤࠥፗ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111l11l1l1_opy_ = datetime.now()
        if framework_name == bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧፘ"):
            result = self.bstack1l1l11lllll_opy_.bstack1l1l1ll1l11_opy_(driver, bstack1l1ll11l11l_opy_)
        else:
            result = driver.execute_async_script(bstack1l1ll11l11l_opy_)
        instance = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(driver)
        if instance:
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹࠢፙ"), datetime.now() - bstack111l11l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack11l11l11l1_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣፚ"))
            return
        if self.bstack1l1l1l1l111_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1lll11l_opy_(driver, framework_name, bstack11l1l11_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪ፛"))
        bstack1l1ll11l11l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1l11_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦ፜"), None)
        if not bstack1l1ll11l11l_opy_:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢ፝") + str(framework_name) + bstack11l1l11_opy_ (u"ࠤࠥ፞"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111l11l1l1_opy_ = datetime.now()
        if framework_name == bstack11l1l11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧ፟"):
            result = self.bstack1l1l11lllll_opy_.bstack1l1l1ll1l11_opy_(driver, bstack1l1ll11l11l_opy_)
        else:
            result = driver.execute_async_script(bstack1l1ll11l11l_opy_)
        instance = bstack1lll11ll1l1_opy_.bstack1lll11ll11l_opy_(driver)
        if instance:
            instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣ፠"), datetime.now() - bstack111l11l1l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l1l1llll_opy_, stage=STAGE.bstack1l11l1l11l_opy_)
    def bstack1l1l1lllll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l1ll1111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦ፡").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1ll11111_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣ።") + str(r) + bstack11l1l11_opy_ (u"ࠢࠣ፣"))
            else:
                self.bstack1l1l1llll11_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨ፤") + str(e) + bstack11l1l11_opy_ (u"ࠤࠥ፥"))
            traceback.print_exc()
            raise e
    def bstack1l1l1llll11_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡰࡴࡧࡤࡠࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥ፦"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1l1l111_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠤ፧")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1l1l1ll1l_opy_[bstack11l1l11_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦ፨")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1l1l1ll1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1ll1lll1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1ll1ll111_opy_ and command.module == self.bstack1l1l11llll1_opy_:
                        if command.method and not command.method in bstack1l1ll1lll1l_opy_:
                            bstack1l1ll1lll1l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1ll1lll1l_opy_[command.method]:
                            bstack1l1ll1lll1l_opy_[command.method][command.name] = list()
                        bstack1l1ll1lll1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1ll1lll1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1ll111111_opy_(
        self,
        f: bstack1l1lllll1l1_opy_,
        exec: Tuple[bstack1ll1llll111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l11lllll_opy_, bstack1ll1l11l11l_opy_) and method_name != bstack11l1l11_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧ፩"):
            return
        if bstack1lll11ll1l1_opy_.bstack1lll111l111_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1l1l11l1l_opy_):
            return
        if f.bstack1l1ll1111l1_opy_(method_name, *args):
            bstack1l1ll111l11_opy_ = False
            desired_capabilities = f.bstack1l1l11ll1l1_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1l11ll1ll_opy_(instance)
                platform_index = f.bstack1ll1lll111l_opy_(instance, bstack1l1lllll1l1_opy_.bstack1l1l1l1ll11_opy_, 0)
                bstack1l1ll11lll1_opy_ = datetime.now()
                r = self.bstack1l1l1lllll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11l1lllll1_opy_(bstack11l1l11_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧ፪"), datetime.now() - bstack1l1ll11lll1_opy_)
                bstack1l1ll111l11_opy_ = r.success
            else:
                self.logger.error(bstack11l1l11_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥ፫") + str(desired_capabilities) + bstack11l1l11_opy_ (u"ࠤࠥ፬"))
            f.bstack1lll111ll11_opy_(instance, bstack1ll11l11ll1_opy_.bstack1l1l1l11l1l_opy_, bstack1l1ll111l11_opy_)
    def bstack11ll1lll1l_opy_(self, test_tags):
        bstack1l1l1lllll1_opy_ = self.config.get(bstack11l1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ፭"))
        if not bstack1l1l1lllll1_opy_:
            return True
        try:
            include_tags = bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ፮")] if bstack11l1l11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ፯") in bstack1l1l1lllll1_opy_ and isinstance(bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ፰")], list) else []
            exclude_tags = bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ፱")] if bstack11l1l11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭፲") in bstack1l1l1lllll1_opy_ and isinstance(bstack1l1l1lllll1_opy_[bstack11l1l11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ፳")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥ፴") + str(error))
        return False
    def bstack11l1llllll_opy_(self, caps):
        try:
            if self.bstack1l1l1l1l111_opy_:
                bstack1l1ll11ll1l_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ፵"))
                if bstack1l1ll11ll1l_opy_ is not None and str(bstack1l1ll11ll1l_opy_).lower() == bstack11l1l11_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨ፶"):
                    bstack1l1ll1ll1l1_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ፷")) or caps.get(bstack11l1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ፸"))
                    if bstack1l1ll1ll1l1_opy_ is not None and int(bstack1l1ll1ll1l1_opy_) < 11:
                        self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡃࡱࡨࡷࡵࡩࡥࠢ࠴࠵ࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥ࠯ࠢࡆࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠣ፹") + str(bstack1l1ll1ll1l1_opy_) + bstack11l1l11_opy_ (u"ࠤࠥ፺"))
                        return False
                return True
            bstack1l1ll1111ll_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ፻"), {}).get(bstack11l1l11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨ፼"), caps.get(bstack11l1l11_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬ፽"), bstack11l1l11_opy_ (u"࠭ࠧ፾")))
            if bstack1l1ll1111ll_opy_:
                self.logger.warning(bstack11l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ፿"))
                return False
            browser = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᎀ"), bstack11l1l11_opy_ (u"ࠩࠪᎁ")).lower()
            if browser != bstack11l1l11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᎂ"):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᎃ"))
                return False
            bstack1l1ll111lll_opy_ = bstack1l1ll11l111_opy_
            if not self.config.get(bstack11l1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᎄ")) or self.config.get(bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᎅ")):
                bstack1l1ll111lll_opy_ = bstack1l1ll1l1l1l_opy_
            browser_version = caps.get(bstack11l1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᎆ"))
            if not browser_version:
                browser_version = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᎇ"), {}).get(bstack11l1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᎈ"), bstack11l1l11_opy_ (u"ࠪࠫᎉ"))
            bstack1l1ll11ll11_opy_ = str(browser_version).lower() if browser_version is not None else bstack11l1l11_opy_ (u"ࠫࠬᎊ")
            if bstack1l1ll11ll11_opy_:
                if bstack1l1ll11ll11_opy_.startswith(bstack11l1l11_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᎋ")):
                    if bstack1l1ll11ll11_opy_.startswith(bstack11l1l11_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᎌ")):
                        bstack1l1ll1l1111_opy_ = bstack1l1ll11ll11_opy_[len(bstack11l1l11_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺ࠭ࠨᎍ")):]
                        if bstack1l1ll1l1111_opy_ and not bstack1l1ll1l1111_opy_.isdigit():
                            self.logger.warning(bstack11l1l11_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡫ࡵࡲ࡮ࡣࡷࠤࠬࠨᎎ") + str(browser_version) + bstack11l1l11_opy_ (u"ࠤࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠࠨ࡮ࡤࡸࡪࡹࡴࠨࠢࡲࡶࠥ࠭࡬ࡢࡶࡨࡷࡹ࠳࠼࡯ࡷࡰࡦࡪࡸ࠾ࠨ࠰ࠥᎏ"))
                            return False
                else:
                    try:
                        if int(bstack1l1ll11ll11_opy_.split(bstack11l1l11_opy_ (u"ࠪ࠲ࠬ᎐"))[0]) <= bstack1l1ll111lll_opy_:
                            self.logger.warning(bstack11l1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࠨ᎑") + str(bstack1l1ll111lll_opy_) + bstack11l1l11_opy_ (u"ࠧ࠴ࠢ᎒"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11l1l11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࠫࢀࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࡽࠨ࠼ࠣࠦ᎓") + str(e) + bstack11l1l11_opy_ (u"ࠢࠣ᎔"))
            bstack1l1l1lll111_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᎕"), {}).get(bstack11l1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᎖"))
            if not bstack1l1l1lll111_opy_:
                bstack1l1l1lll111_opy_ = caps.get(bstack11l1l11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᎗"), {})
            if bstack1l1l1lll111_opy_ and bstack11l1l11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᎘") in bstack1l1l1lll111_opy_.get(bstack11l1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪ᎙"), []):
                self.logger.warning(bstack11l1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣ᎚"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11l1l11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤ᎛") + str(error))
            return False
    def bstack1l1l11ll111_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1l1l1l1l1_opy_ = {
            bstack11l1l11_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨ᎜"): test_uuid,
        }
        bstack1l1l1lll1l1_opy_ = {}
        if result.success:
            bstack1l1l1lll1l1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l1l11l11_opy_(bstack1l1l1l1l1l1_opy_, bstack1l1l1lll1l1_opy_)
    def bstack1l1l1ll1l1l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11l1l11_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡆࡦࡶࡦ࡬ࠥࡩࡥ࡯ࡶࡵࡥࡱࠦࡡࡶࡶ࡫ࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥ࡭ࡩࡷࡧࡱࠤࡸࡩࡲࡪࡲࡷࠤࡳࡧ࡭ࡦ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡩࡡࡤࡪࡨࡨࠥࡩ࡯࡯ࡨ࡬࡫ࠥ࡯ࡦࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡩࡩࡹࡩࡨࡦࡦ࠯ࠤࡴࡺࡨࡦࡴࡺ࡭ࡸ࡫ࠠ࡭ࡱࡤࡨࡸࠦࡡ࡯ࡦࠣࡧࡦࡩࡨࡦࡵࠣ࡭ࡹ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡃࡵ࡫ࡸࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧ࠽ࠤࡓࡧ࡭ࡦࠢࡲࡪࠥࡺࡨࡦࠢࡶࡧࡷ࡯ࡰࡵࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡫ࡵࡲࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡦࡵࡷࡣࡺࡻࡩࡥ࠼࡙࡚ࠣࡏࡄࠡࡱࡩࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡸࡪ࡬ࡧ࡭ࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧ࡭ࡨࡺ࠺ࠡࡅࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡦ࡬ࡧࡹ࡯࡯࡯ࡣࡵࡽ࠱ࠦࡥ࡮ࡲࡷࡽࠥࡪࡩࡤࡶࠣ࡭࡫ࠦࡥࡳࡴࡲࡶࠥࡵࡣࡤࡷࡵࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤ᎝")
        try:
            if self.bstack1l1ll1lll11_opy_:
                return self.bstack1l1ll1l1l11_opy_
            self.bstack1l1l1ll1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l1l11_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥ᎞")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ᎟"), bstack11l1l11_opy_ (u"ࠬ࠶ࠧᎠ")))
            req.client_worker_id = bstack11l1l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧᎡ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1ll11111_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1ll1l1l11_opy_ = self.bstack1l1l11ll111_opy_(test_uuid, r)
                self.bstack1l1ll1lll11_opy_ = True
            else:
                self.logger.error(bstack11l1l11_opy_ (u"ࠢࡧࡧࡷࡧ࡭ࡉࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡄ࠵࠶ࡿࡃࡰࡰࡩ࡭࡬ࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡴࡸࠠࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃ࠺ࠡࠤᎢ") + str(r.error) + bstack11l1l11_opy_ (u"ࠣࠤᎣ"))
                self.bstack1l1ll1l1l11_opy_ = dict()
            return self.bstack1l1ll1l1l11_opy_
        except Exception as e:
            self.logger.error(bstack11l1l11_opy_ (u"ࠤࡩࡩࡹࡩࡨࡄࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡆ࠷࠱ࡺࡅࡲࡲ࡫࡯ࡧ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥ࡬ࡥࡵࡥ࡫ࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬࡯ࡳࠢࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾ࠼ࠣࠦᎤ") + str(traceback.format_exc()) + bstack11l1l11_opy_ (u"ࠥࠦᎥ"))
            return dict()
    def bstack1l111ll1l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l1l1l1111_opy_ = None
        try:
            self.bstack1l1l1ll1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l1l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᎦ")
            req.script_name = bstack11l1l11_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᎧ")
            req.platform_index = str(os.environ.get(bstack11l1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭Ꭸ"), bstack11l1l11_opy_ (u"ࠧ࠱ࠩᎩ")))
            req.client_worker_id = bstack11l1l11_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᎪ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1ll11111_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᎫ") + str(r.error) + bstack11l1l11_opy_ (u"ࠥࠦᎬ"))
            else:
                bstack1l1l1l1l1l1_opy_ = self.bstack1l1l11ll111_opy_(test_uuid, r)
                bstack1l1ll11l11l_opy_ = r.script
            self.logger.debug(bstack11l1l11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᎭ") + str(bstack1l1l1l1l1l1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1ll11l11l_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᎮ") + str(framework_name) + bstack11l1l11_opy_ (u"ࠨࠠࠣᎯ"))
                return
            bstack1l1l1l1111_opy_ = bstack11ll1l1l1_opy_.bstack1l11l111ll_opy_(EVENTS.bstack1l1l1llllll_opy_.value)
            self.bstack1l1l1l1lll1_opy_(driver, bstack1l1ll11l11l_opy_, bstack1l1l1l1l1l1_opy_, framework_name)
            try:
                bstack1l1ll1l111l_opy_ = {
                    bstack11l1l11_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᎰ"): {
                        bstack11l1l11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᎱ"): bstack11l1l11_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᎲ"),
                    },
                    bstack11l1l11_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᎳ"): {
                        bstack11l1l11_opy_ (u"ࠦࡧࡵࡤࡺࠤᎴ"): {
                            bstack11l1l11_opy_ (u"ࠧࡳࡳࡨࠤᎵ"): bstack11l1l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᎶ"),
                            bstack11l1l11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᎷ"): True
                        }
                    }
                }
                self.bstack11ll111ll_opy_.info(json.dumps(bstack1l1ll1l111l_opy_, separators=(bstack11l1l11_opy_ (u"ࠨ࠮ࠪᎸ"), bstack11l1l11_opy_ (u"ࠩ࠽ࠫᎹ"))))
            except Exception as bstack111l1l11ll_opy_:
                self.logger.debug(bstack11l1l11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᎺ") + str(bstack111l1l11ll_opy_) + bstack11l1l11_opy_ (u"ࠦࠧᎻ"))
            self.logger.info(bstack11l1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᎼ"))
            bstack11ll1l1l1_opy_.end(EVENTS.bstack1l1l1llllll_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᎽ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᎾ"), True, None, command=bstack11l1l11_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭Ꮏ"),test_name=name)
        except Exception as bstack1l1ll111l1l_opy_:
            self.logger.error(bstack11l1l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᏀ") + bstack11l1l11_opy_ (u"ࠥࡷࡹࡸࠨࡱࡣࡷ࡬࠮ࠨᏁ") + bstack11l1l11_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᏂ") + str(bstack1l1ll111l1l_opy_))
            bstack11ll1l1l1_opy_.end(EVENTS.bstack1l1l1llllll_opy_.value, bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᏃ"), bstack1l1l1l1111_opy_+bstack11l1l11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᏄ"), False, bstack1l1ll111l1l_opy_, command=bstack11l1l11_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᏅ"),test_name=name)
    def bstack1l1l1l1lll1_opy_(self, driver, bstack1l1ll11l11l_opy_, bstack1l1l1l1l1l1_opy_, framework_name):
        if framework_name == bstack11l1l11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᏆ"):
            self.bstack1l1l11lllll_opy_.bstack1l1l1ll1l11_opy_(driver, bstack1l1ll11l11l_opy_, bstack1l1l1l1l1l1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1ll11l11l_opy_, bstack1l1l1l1l1l1_opy_))
    def _1l1ll11l1ll_opy_(self, instance: bstack1l1llll111l_opy_, args: Tuple) -> list:
        bstack11l1l11_opy_ (u"ࠤࠥࠦࡊࡾࡴࡳࡣࡦࡸࠥࡺࡡࡨࡵࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᏇ")
        if bstack11l1l11_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᏈ") in instance.bstack1l1l1ll1ll1_opy_:
            return args[2].tags if hasattr(args[2], bstack11l1l11_opy_ (u"ࠫࡹࡧࡧࡴࠩᏉ")) else []
        if hasattr(args[0], bstack11l1l11_opy_ (u"ࠬࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠪᏊ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1ll1l1ll1_opy_(self, tags, capabilities):
        return self.bstack11ll1lll1l_opy_(tags) and self.bstack11l1llllll_opy_(capabilities)