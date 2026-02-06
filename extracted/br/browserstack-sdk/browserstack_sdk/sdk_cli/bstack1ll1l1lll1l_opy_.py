# coding: UTF-8
import sys
bstack11ll1l1_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack1ll1lll_opy_ = 7
def bstack11lllll_opy_ (bstack11ll1_opy_):
    global bstack1llllll_opy_
    bstack111l_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1111l11_opy_ = bstack11ll1_opy_ [:-1]
    bstack1lllll1l_opy_ = bstack111l_opy_ % len (bstack1111l11_opy_)
    bstack1ll1ll_opy_ = bstack1111l11_opy_ [:bstack1lllll1l_opy_] + bstack1111l11_opy_ [bstack1lllll1l_opy_:]
    if bstack11ll1l1_opy_:
        bstack1l1llll_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    else:
        bstack1l1llll_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1ll1l_opy_ + bstack111l_opy_) % bstack1ll1lll_opy_) for bstack1ll1l_opy_, char in enumerate (bstack1ll1ll_opy_)])
    return eval (bstack1l1llll_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll1l1ll11_opy_ import (
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll11ll_opy_,
    bstack1lll1ll1ll1_opy_,
    bstack1lll1l1l11l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l11ll1_opy_ import bstack1lll11lllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_, bstack1ll11111ll1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1lll1l1_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11l11l_opy_ import bstack1ll11l1llll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1111l1ll_opy_ import bstack1ll11lll11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1lll1lll11l_opy_
from bstack_utils.helper import bstack1l1lll11l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11lll1l11l_opy_ import bstack1lll11l1ll_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1l1llllll11_opy_(bstack1lll1l1l1l1_opy_):
    bstack1l1l1lll1l1_opy_ = False
    bstack1l1ll11l111_opy_ = bstack11lllll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤቝ")
    bstack1l1lll11ll1_opy_ = bstack11lllll_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣ቞")
    bstack1l1ll11111l_opy_ = bstack11lllll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦ቟")
    bstack1l1ll11lll1_opy_ = bstack11lllll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧበ")
    bstack1l1ll1lllll_opy_ = bstack11lllll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤቡ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll11lll111_opy_, bstack1ll1lll11l1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1ll1ll1_opy_ = False
        self.bstack1l1ll111lll_opy_ = dict()
        self.bstack1l111l111l_opy_ = logger_utils.bstack1l1l11111l_opy_(__name__)
        self.bstack1l1lll111ll_opy_ = False
        self.bstack1l1ll1ll111_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l1l1ll11_opy_ = bstack1ll1lll11l1_opy_
        bstack1ll11lll111_opy_.bstack1lll1l1l1ll_opy_((bstack1lll1l1ll1l_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll11ll_opy_.PRE), self.bstack1l1l1llllll_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.PRE), self.bstack1l1lll1111l_opy_)
        TestFramework.bstack1lll1l1l1ll_opy_((bstack1ll11111l1l_opy_.TEST, bstack1ll11l1l11l_opy_.POST), self.bstack1l1l1l1l1ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1lll1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1lll1ll_opy_(instance, args)
        test_framework = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1ll111ll1_opy_)
        if self.bstack1l1l1ll1ll1_opy_:
            self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤቢ")] = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
        if bstack11lllll_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧባ") in instance.bstack1l1ll1l111l_opy_:
            platform_index = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1l1lllll1_opy_)
            self.accessibility = self.bstack1l1ll11l1l1_opy_(tags, self.config[bstack11lllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቤ")][platform_index])
        else:
            capabilities = self.bstack1l1l1l1ll11_opy_.bstack1l1l1ll11l1_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧብ") + str(kwargs) + bstack11lllll_opy_ (u"ࠨࠢቦ"))
                return
            self.accessibility = self.bstack1l1ll11l1l1_opy_(tags, capabilities)
        if self.bstack1l1l1l1ll11_opy_.pages and self.bstack1l1l1l1ll11_opy_.pages.values():
            bstack1l1l1ll1l11_opy_ = list(self.bstack1l1l1l1ll11_opy_.pages.values())
            if bstack1l1l1ll1l11_opy_ and isinstance(bstack1l1l1ll1l11_opy_[0], (list, tuple)) and bstack1l1l1ll1l11_opy_[0]:
                bstack1l1ll111111_opy_ = bstack1l1l1ll1l11_opy_[0][0]
                if callable(bstack1l1ll111111_opy_):
                    page = bstack1l1ll111111_opy_()
                    def bstack11l1l1l1ll_opy_():
                        self.get_accessibility_results(page, bstack11lllll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦቧ"))
                    def bstack1l1l1llll11_opy_():
                        self.get_accessibility_results_summary(page, bstack11lllll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧቨ"))
                    setattr(page, bstack11lllll_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧቩ"), bstack11l1l1l1ll_opy_)
                    setattr(page, bstack11lllll_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧቪ"), bstack1l1l1llll11_opy_)
        self.logger.debug(bstack11lllll_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣቫ") + str(self.accessibility) + bstack11lllll_opy_ (u"ࠧࠨቬ"))
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        bstack1lll1l11lll_opy_: Tuple[bstack1lll1l1ll1l_opy_, bstack1lll1ll11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1111l111_opy_ = datetime.now()
            self.bstack1l1l1l1lll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤቭ"), datetime.now() - bstack1l1111l111_opy_)
            bstack1lll1l111ll_opy_ = instance.data.get(bstack11lllll_opy_ (u"ࠧࡳࡣࡱ࡯ࠬቮ"), None)
            if (
                not f.bstack1l1ll11ll1l_opy_(method_name)
                or f.bstack1l1l1l1ll1l_opy_(method_name, *args)
                or f.bstack1l1l1ll1l1l_opy_(method_name, *args)
                or (bstack1lll1l111ll_opy_ and int(bstack1lll1l111ll_opy_)>1)
            ):
                return
            if not f.bstack1lll1l1l111_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll11111l_opy_, False):
                if not bstack1l1llllll11_opy_.bstack1l1l1lll1l1_opy_:
                    self.logger.warning(bstack11lllll_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦቯ") + str(f.platform_index) + bstack11lllll_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣተ"))
                    bstack1l1llllll11_opy_.bstack1l1l1lll1l1_opy_ = True
                return
            bstack1l1lll1l1ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1lll1l1ll_opy_:
                platform_index = f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_, 0)
                self.logger.debug(bstack11lllll_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣቱ") + str(f.framework_name) + bstack11lllll_opy_ (u"ࠦࠧቲ"))
                return
            command_name = f.bstack1l1l1lll11l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11lllll_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢታ") + str(method_name) + bstack11lllll_opy_ (u"ࠨࠢቴ"))
                return
            bstack1l1ll111l1l_opy_ = f.bstack1lll1l1l111_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll1lllll_opy_, False)
            if command_name == bstack11lllll_opy_ (u"ࠢࡨࡧࡷࠦት") and not bstack1l1ll111l1l_opy_:
                f.bstack1lll1ll1lll_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll1lllll_opy_, True)
                bstack1l1ll111l1l_opy_ = True
            if not bstack1l1ll111l1l_opy_ and not self.bstack1l1l1ll1ll1_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢቶ") + str(command_name) + bstack11lllll_opy_ (u"ࠤࠥቷ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11lllll_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣቸ") + str(command_name) + bstack11lllll_opy_ (u"ࠦࠧቹ"))
                return
            self.logger.info(bstack11lllll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢቺ") + str(command_name) + bstack11lllll_opy_ (u"ࠨࠢቻ"))
            scripts = [(s, bstack1l1lll1l1ll_opy_[s]) for s in scripts_to_run if s in bstack1l1lll1l1ll_opy_]
            for script_name, bstack1l1lll1ll11_opy_ in scripts:
                try:
                    bstack1l1111l111_opy_ = datetime.now()
                    if script_name == bstack11lllll_opy_ (u"ࠢࡴࡥࡤࡲࠧቼ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack1llll11ll1_opy_ = {
                                bstack11lllll_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤች"): {
                                    bstack11lllll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥቾ"): bstack11lllll_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡆࡅࡓࠨቿ"),
                                    bstack11lllll_opy_ (u"ࠦࡵࡧࡲࡢ࡯ࡨࡸࡪࡸࡳࠣኀ"): [
                                        {
                                            bstack11lllll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧኁ"): command_name
                                        }
                                    ]
                                },
                                bstack11lllll_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣኂ"): {
                                    bstack11lllll_opy_ (u"ࠢࡣࡱࡧࡽࠧኃ"): {
                                        bstack11lllll_opy_ (u"ࠣ࡯ࡶ࡫ࠧኄ"): result.get(bstack11lllll_opy_ (u"ࠤࡰࡷ࡬ࠨኅ"), bstack11lllll_opy_ (u"ࠥࠦኆ")) if isinstance(result, dict) else bstack11lllll_opy_ (u"ࠦࠧኇ"),
                                        bstack11lllll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨኈ"): result.get(bstack11lllll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ኉"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack1l111l111l_opy_.info(json.dumps(bstack1llll11ll1_opy_, separators=(bstack11lllll_opy_ (u"ࠢ࠭ࠤኊ"), bstack11lllll_opy_ (u"ࠣ࠼ࠥኋ"))))
                        except Exception as bstack111l1l1l_opy_:
                            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡧࡦࡴࠠࡥࡣࡷࡥ࠿ࠦࠢኌ") + str(bstack111l1l1l_opy_) + bstack11lllll_opy_ (u"ࠥࠦኍ"))
                    instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥ኎") + script_name, datetime.now() - bstack1l1111l111_opy_)
                    if isinstance(result, dict) and not result.get(bstack11lllll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨ኏"), True):
                        self.logger.warning(bstack11lllll_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨነ") + str(result) + bstack11lllll_opy_ (u"ࠢࠣኑ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11lllll_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥኒ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥና"))
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢኔ") + str(e) + bstack11lllll_opy_ (u"ࠦࠧን"))
    def bstack1l1l1l1l1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11111ll1_opy_,
        bstack1lll1l11lll_opy_: Tuple[bstack1ll11111l1l_opy_, bstack1ll11l1l11l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1lll1ll_opy_(instance, args)
        capabilities = self.bstack1l1l1l1ll11_opy_.bstack1l1l1ll11l1_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l1ll11l1l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤኖ"))
            return
        driver = self.bstack1l1l1l1ll11_opy_.bstack1l1ll11l1ll_opy_(f, instance, bstack1lll1l11lll_opy_, *args, **kwargs)
        test_name = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1lll11111_opy_)
        if not test_name:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦኗ"))
            return
        test_uuid = f.bstack1lll1l1l111_opy_(instance, TestFramework.bstack1l1lll1l111_opy_)
        if not test_uuid:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧኘ"))
            return
        if isinstance(self.bstack1l1l1l1ll11_opy_, bstack1ll11lll11l_opy_):
            framework_name = bstack11lllll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬኙ")
        else:
            framework_name = bstack11lllll_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫኚ")
        self.bstack1111ll1ll_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1ll1l111l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦኛ"))
            return
        bstack1l1111l111_opy_ = datetime.now()
        bstack1l1lll1ll11_opy_ = self.scripts.get(framework_name, {}).get(bstack11lllll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤኜ"), None)
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧኝ") + str(framework_name) + bstack11lllll_opy_ (u"ࠨࠠࠣኞ"))
            return
        if self.bstack1l1l1ll1ll1_opy_:
            arg = dict()
            arg[bstack11lllll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢኟ")] = method if method else bstack11lllll_opy_ (u"ࠣࠤአ")
            arg[bstack11lllll_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤኡ")] = self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥኢ")]
            arg[bstack11lllll_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤኣ")] = self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥኤ")]
            arg[bstack11lllll_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥእ")] = self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧኦ")]
            arg[bstack11lllll_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧኧ")] = self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣከ")]
            arg[bstack11lllll_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥኩ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1ll1l1lll_opy_ = self.bstack1l1ll1lll11_opy_(bstack11lllll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤኪ"), self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧካ")])
            if bstack11lllll_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤኬ") in bstack1l1ll1l1lll_opy_:
                bstack1l1ll1l1lll_opy_ = bstack1l1ll1l1lll_opy_.copy()
                bstack1l1ll1l1lll_opy_[bstack11lllll_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦክ")] = bstack1l1ll1l1lll_opy_.pop(bstack11lllll_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦኮ"))
            arg = bstack1l1lll11l11_opy_(arg, bstack1l1ll1l1lll_opy_)
            bstack1l1lll1l1l1_opy_ = bstack1l1lll1ll11_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1lll1l1l1_opy_)
            return
        instance = bstack1lll1ll1ll1_opy_.bstack1lll111ll1l_opy_(driver)
        if instance:
            if not bstack1lll1ll1ll1_opy_.bstack1lll1l1l111_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll11lll1_opy_, False):
                bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll11lll1_opy_, True)
            else:
                self.logger.info(bstack11lllll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨኯ") + str(method) + bstack11lllll_opy_ (u"ࠥࠦኰ"))
                return
        self.logger.info(bstack11lllll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤ኱") + str(method) + bstack11lllll_opy_ (u"ࠧࠨኲ"))
        if framework_name == bstack11lllll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪኳ"):
            result = self.bstack1l1l1l1ll11_opy_.bstack1l1ll1l1l11_opy_(driver, bstack1l1lll1ll11_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll1ll11_opy_, {bstack11lllll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢኴ"): method if method else bstack11lllll_opy_ (u"ࠣࠤኵ")})
        bstack1lll11l1ll_opy_.end(EVENTS.bstack1ll1l111l1_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ኶"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ኷"), True, None, command=method)
        if instance:
            bstack1lll1ll1ll1_opy_.bstack1lll1ll1lll_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll11lll1_opy_, False)
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣኸ"), datetime.now() - bstack1l1111l111_opy_)
        return result
        def bstack1l1l1llll1l_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1ll1l11ll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l1ll111l_opy_ = self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧኹ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11lllll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ኺ"), bstack11lllll_opy_ (u"ࠧ࠱ࠩኻ")))
            req.client_worker_id = bstack11lllll_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢኼ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1l1l1ll1_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11lllll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦኽ") + str(r) + bstack11lllll_opy_ (u"ࠥࠦኾ"))
                else:
                    bstack1l1ll1lll1l_opy_ = json.loads(r.bstack1l1ll1l1111_opy_.decode(bstack11lllll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪ኿")))
                    if result_type == bstack11lllll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩዀ"):
                        return bstack1l1ll1lll1l_opy_.get(bstack11lllll_opy_ (u"ࠨࡤࡢࡶࡤࠦ዁"), [])
                    else:
                        return bstack1l1ll1lll1l_opy_.get(bstack11lllll_opy_ (u"ࠢࡥࡣࡷࡥࠧዂ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11lllll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥዃ") + str(e) + bstack11lllll_opy_ (u"ࠤࠥዄ"))
    @measure(event_name=EVENTS.bstack1ll111ll11_opy_, stage=STAGE.bstack1llll11111_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11lllll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧዅ"))
            return
        if self.bstack1l1l1ll1ll1_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡥࡵࡶࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ዆"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1llll1l_opy_(driver, framework_name, bstack11lllll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤ዇"))
        bstack1l1lll1ll11_opy_ = self.scripts.get(framework_name, {}).get(bstack11lllll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥወ"), None)
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨዉ") + str(framework_name) + bstack11lllll_opy_ (u"ࠣࠤዊ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1111l111_opy_ = datetime.now()
        if framework_name == bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ዋ"):
            result = self.bstack1l1l1l1ll11_opy_.bstack1l1ll1l1l11_opy_(driver, bstack1l1lll1ll11_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll1ll11_opy_)
        instance = bstack1lll1ll1ll1_opy_.bstack1lll111ll1l_opy_(driver)
        if instance:
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨዌ"), datetime.now() - bstack1l1111l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l11lll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11lllll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢው"))
            return
        if self.bstack1l1l1ll1ll1_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1llll1l_opy_(driver, framework_name, bstack11lllll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩዎ"))
        bstack1l1lll1ll11_opy_ = self.scripts.get(framework_name, {}).get(bstack11lllll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥዏ"), None)
        if not bstack1l1lll1ll11_opy_:
            self.logger.debug(bstack11lllll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨዐ") + str(framework_name) + bstack11lllll_opy_ (u"ࠣࠤዑ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1111l111_opy_ = datetime.now()
        if framework_name == bstack11lllll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ዒ"):
            result = self.bstack1l1l1l1ll11_opy_.bstack1l1ll1l1l11_opy_(driver, bstack1l1lll1ll11_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll1ll11_opy_)
        instance = bstack1lll1ll1ll1_opy_.bstack1lll111ll1l_opy_(driver)
        if instance:
            instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢዓ"), datetime.now() - bstack1l1111l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1lll11lll_opy_, stage=STAGE.bstack1llll11111_opy_)
    def bstack1l1ll111l11_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1ll1l11ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11lllll_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥዔ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1l1l1ll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢዕ") + str(r) + bstack11lllll_opy_ (u"ࠨࠢዖ"))
            else:
                self.bstack1l1ll1ll1l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧ዗") + str(e) + bstack11lllll_opy_ (u"ࠣࠤዘ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1ll1l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤዙ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1ll1ll1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣዚ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1ll111lll_opy_[bstack11lllll_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥዛ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1ll111lll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l1l1llll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1ll11l111_opy_ and command.module == self.bstack1l1lll11ll1_opy_:
                        if command.method and not command.method in bstack1l1l1l1llll_opy_:
                            bstack1l1l1l1llll_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1l1l1llll_opy_[command.method]:
                            bstack1l1l1l1llll_opy_[command.method][command.name] = list()
                        bstack1l1l1l1llll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l1l1llll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1l1l1lll1_opy_(
        self,
        f: bstack1lll11lllll_opy_,
        exec: Tuple[bstack1lll1l1l11l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l1l1ll11_opy_, bstack1ll11lll11l_opy_) and method_name != bstack11lllll_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ዜ"):
            return
        if bstack1lll1ll1ll1_opy_.bstack1lll111ll11_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll11111l_opy_):
            return
        if f.bstack1l1lll1l11l_opy_(method_name, *args):
            bstack1l1ll1l1l1l_opy_ = False
            desired_capabilities = f.bstack1l1lll1ll1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1ll11llll_opy_(instance)
                platform_index = f.bstack1lll1l1l111_opy_(instance, bstack1lll11lllll_opy_.bstack1l1l1lllll1_opy_, 0)
                bstack1l1lll11l1l_opy_ = datetime.now()
                r = self.bstack1l1ll111l11_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll1l1111l_opy_(bstack11lllll_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦዝ"), datetime.now() - bstack1l1lll11l1l_opy_)
                bstack1l1ll1l1l1l_opy_ = r.success
            else:
                self.logger.error(bstack11lllll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤዞ") + str(desired_capabilities) + bstack11lllll_opy_ (u"ࠣࠤዟ"))
            f.bstack1lll1ll1lll_opy_(instance, bstack1l1llllll11_opy_.bstack1l1ll11111l_opy_, bstack1l1ll1l1l1l_opy_)
    def bstack1l11lll111_opy_(self, test_tags):
        bstack1l1ll111l11_opy_ = self.config.get(bstack11lllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩዠ"))
        if not bstack1l1ll111l11_opy_:
            return True
        try:
            include_tags = bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨዡ")] if bstack11lllll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩዢ") in bstack1l1ll111l11_opy_ and isinstance(bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪዣ")], list) else []
            exclude_tags = bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫዤ")] if bstack11lllll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬዥ") in bstack1l1ll111l11_opy_ and isinstance(bstack1l1ll111l11_opy_[bstack11lllll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ዦ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11lllll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤዧ") + str(error))
        return False
    def bstack1l1l1l1l1l_opy_(self, caps):
        try:
            if self.bstack1l1l1ll1ll1_opy_:
                bstack1l1l1lll111_opy_ = caps.get(bstack11lllll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤየ"))
                if bstack1l1l1lll111_opy_ is not None and str(bstack1l1l1lll111_opy_).lower() == bstack11lllll_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧዩ"):
                    bstack1l1ll1111l1_opy_ = caps.get(bstack11lllll_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢዪ")) or caps.get(bstack11lllll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣያ"))
                    if bstack1l1ll1111l1_opy_ is not None and int(bstack1l1ll1111l1_opy_) < 11:
                        self.logger.warning(bstack11lllll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡂࡰࡧࡶࡴ࡯ࡤࠡ࠳࠴ࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫࠮ࠡࡅࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠢዬ") + str(bstack1l1ll1111l1_opy_) + bstack11lllll_opy_ (u"ࠣࠤይ"))
                        return False
                return True
            bstack1l1l1l1l1l1_opy_ = caps.get(bstack11lllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪዮ"), {}).get(bstack11lllll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧዯ"), caps.get(bstack11lllll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫደ"), bstack11lllll_opy_ (u"ࠬ࠭ዱ")))
            if bstack1l1l1l1l1l1_opy_:
                self.logger.warning(bstack11lllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥዲ"))
                return False
            browser = caps.get(bstack11lllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬዳ"), bstack11lllll_opy_ (u"ࠨࠩዴ")).lower()
            if browser != bstack11lllll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩድ"):
                self.logger.warning(bstack11lllll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨዶ"))
                return False
            bstack1l1ll1llll1_opy_ = bstack1l1l1ll1111_opy_
            if not self.config.get(bstack11lllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ዷ")) or self.config.get(bstack11lllll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩዸ")):
                bstack1l1ll1llll1_opy_ = bstack1l1ll11l11l_opy_
            browser_version = caps.get(bstack11lllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧዹ"))
            if not browser_version:
                browser_version = caps.get(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨዺ"), {}).get(bstack11lllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩዻ"), bstack11lllll_opy_ (u"ࠩࠪዼ"))
            bstack1l1lll111l1_opy_ = str(browser_version).lower() if browser_version is not None else bstack11lllll_opy_ (u"ࠪࠫዽ")
            if bstack1l1lll111l1_opy_:
                if bstack1l1lll111l1_opy_.startswith(bstack11lllll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫዾ")):
                    if bstack1l1lll111l1_opy_.startswith(bstack11lllll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ዿ")):
                        bstack1l1ll11ll11_opy_ = bstack1l1lll111l1_opy_[len(bstack11lllll_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧጀ")):]
                        if bstack1l1ll11ll11_opy_ and not bstack1l1ll11ll11_opy_.isdigit():
                            self.logger.warning(bstack11lllll_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࡪࡴࡸ࡭ࡢࡶࠣࠫࠧጁ") + str(browser_version) + bstack11lllll_opy_ (u"ࠣࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࠧ࡭ࡣࡷࡩࡸࡺࠧࠡࡱࡵࠤࠬࡲࡡࡵࡧࡶࡸ࠲ࡂ࡮ࡶ࡯ࡥࡩࡷࡄࠧ࠯ࠤጂ"))
                            return False
                else:
                    try:
                        if int(bstack1l1lll111l1_opy_.split(bstack11lllll_opy_ (u"ࠩ࠱ࠫጃ"))[0]) <= bstack1l1ll1llll1_opy_:
                            self.logger.warning(bstack11lllll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࠧጄ") + str(bstack1l1ll1llll1_opy_) + bstack11lllll_opy_ (u"ࠦ࠳ࠨጅ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11lllll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠪࡿࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࢃࠧ࠻ࠢࠥጆ") + str(e) + bstack11lllll_opy_ (u"ࠨࠢጇ"))
            bstack1l1l1ll1lll_opy_ = caps.get(bstack11lllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨገ"), {}).get(bstack11lllll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨጉ"))
            if not bstack1l1l1ll1lll_opy_:
                bstack1l1l1ll1lll_opy_ = caps.get(bstack11lllll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧጊ"), {})
            if bstack1l1l1ll1lll_opy_ and bstack11lllll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧጋ") in bstack1l1l1ll1lll_opy_.get(bstack11lllll_opy_ (u"ࠫࡦࡸࡧࡴࠩጌ"), []):
                self.logger.warning(bstack11lllll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢግ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11lllll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣጎ") + str(error))
            return False
    def bstack1l1ll1111ll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1ll1l11l1_opy_ = {
            bstack11lllll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧጏ"): test_uuid,
        }
        bstack1l1ll1ll1ll_opy_ = {}
        if result.success:
            bstack1l1ll1ll1ll_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1lll11l11_opy_(bstack1l1ll1l11l1_opy_, bstack1l1ll1ll1ll_opy_)
    def bstack1l1ll1lll11_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11lllll_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌࡥࡵࡥ࡫ࠤࡨ࡫࡮ࡵࡴࡤࡰࠥࡧࡵࡵࡪࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡷࡨࡸࡩࡱࡶࠣࡲࡦࡳࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡨࡧࡣࡩࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡨࡨࡸࡨ࡮ࡥࡥ࠮ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠦ࡬ࡰࡣࡧࡷࠥࡧ࡮ࡥࠢࡦࡥࡨ࡮ࡥࡴࠢ࡬ࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡵࡦࡶ࡮ࡶࡴࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡸࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡹࡺ࡯ࡤ࠻ࠢࡘ࡙ࡎࡊࠠࡰࡨࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠰ࠥ࡫࡭ࡱࡶࡼࠤࡩ࡯ࡣࡵࠢ࡬ࡪࠥ࡫ࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣጐ")
        try:
            if self.bstack1l1lll111ll_opy_:
                return self.bstack1l1ll1ll111_opy_
            self.bstack1l1ll1l11ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11lllll_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ጑")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11lllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪጒ"), bstack11lllll_opy_ (u"ࠫ࠵࠭ጓ")))
            req.client_worker_id = bstack11lllll_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦጔ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1l1l1ll1_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1ll1ll111_opy_ = self.bstack1l1ll1111ll_opy_(test_uuid, r)
                self.bstack1l1lll111ll_opy_ = True
            else:
                self.logger.error(bstack11lllll_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣጕ") + str(r.error) + bstack11lllll_opy_ (u"ࠢࠣ጖"))
                self.bstack1l1ll1ll111_opy_ = dict()
            return self.bstack1l1ll1ll111_opy_
        except Exception as e:
            self.logger.error(bstack11lllll_opy_ (u"ࠣࡨࡨࡸࡨ࡮ࡃࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡅ࠶࠷ࡹࡄࡱࡱࡪ࡮࡭࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡵࡲࠡࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥ጗") + str(traceback.format_exc()) + bstack11lllll_opy_ (u"ࠤࠥጘ"))
            return dict()
    def bstack1111ll1ll_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11111l_opy_ = None
        try:
            self.bstack1l1ll1l11ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11lllll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥጙ")
            req.script_name = bstack11lllll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤጚ")
            req.platform_index = str(os.environ.get(bstack11lllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬጛ"), bstack11lllll_opy_ (u"࠭࠰ࠨጜ")))
            req.client_worker_id = bstack11lllll_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨጝ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1l1l1ll1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11lllll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦጞ") + str(r.error) + bstack11lllll_opy_ (u"ࠤࠥጟ"))
            else:
                bstack1l1ll1l11l1_opy_ = self.bstack1l1ll1111ll_opy_(test_uuid, r)
                bstack1l1lll1ll11_opy_ = r.script
            self.logger.debug(bstack11lllll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ጠ") + str(bstack1l1ll1l11l1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1lll1ll11_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦጡ") + str(framework_name) + bstack11lllll_opy_ (u"ࠧࠦࠢጢ"))
                return
            bstack1ll11111l_opy_ = bstack1lll11l1ll_opy_.bstack1llll1l1ll_opy_(EVENTS.bstack1l1l1l1l11l_opy_.value)
            self.bstack1l1l1ll11ll_opy_(driver, bstack1l1lll1ll11_opy_, bstack1l1ll1l11l1_opy_, framework_name)
            try:
                bstack1l1ll1ll11l_opy_ = {
                    bstack11lllll_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢጣ"): {
                        bstack11lllll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣጤ"): bstack11lllll_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧጥ"),
                    },
                    bstack11lllll_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦጦ"): {
                        bstack11lllll_opy_ (u"ࠥࡦࡴࡪࡹࠣጧ"): {
                            bstack11lllll_opy_ (u"ࠦࡲࡹࡧࠣጨ"): bstack11lllll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣጩ"),
                            bstack11lllll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢጪ"): True
                        }
                    }
                }
                self.bstack1l111l111l_opy_.info(json.dumps(bstack1l1ll1ll11l_opy_, separators=(bstack11lllll_opy_ (u"ࠧ࠭ࠩጫ"), bstack11lllll_opy_ (u"ࠨ࠼ࠪጬ"))))
            except Exception as bstack111l1l1l_opy_:
                self.logger.debug(bstack11lllll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣጭ") + str(bstack111l1l1l_opy_) + bstack11lllll_opy_ (u"ࠥࠦጮ"))
            self.logger.info(bstack11lllll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢጯ"))
            bstack1lll11l1ll_opy_.end(EVENTS.bstack1l1l1l1l11l_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧጰ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦጱ"), True, None, command=bstack11lllll_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬጲ"),test_name=name)
        except Exception as bstack1l1ll1l1ll1_opy_:
            self.logger.error(bstack11lllll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥጳ") + bstack11lllll_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧጴ") + bstack11lllll_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧጵ") + str(bstack1l1ll1l1ll1_opy_))
            bstack1lll11l1ll_opy_.end(EVENTS.bstack1l1l1l1l11l_opy_.value, bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦጶ"), bstack1ll11111l_opy_+bstack11lllll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥጷ"), False, bstack1l1ll1l1ll1_opy_, command=bstack11lllll_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫጸ"),test_name=name)
    def bstack1l1l1ll11ll_opy_(self, driver, bstack1l1lll1ll11_opy_, bstack1l1ll1l11l1_opy_, framework_name):
        if framework_name == bstack11lllll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫጹ"):
            self.bstack1l1l1l1ll11_opy_.bstack1l1ll1l1l11_opy_(driver, bstack1l1lll1ll11_opy_, bstack1l1ll1l11l1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1lll1ll11_opy_, bstack1l1ll1l11l1_opy_))
    def _1l1l1lll1ll_opy_(self, instance: bstack1ll11111ll1_opy_, args: Tuple) -> list:
        bstack11lllll_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧጺ")
        if bstack11lllll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ጻ") in instance.bstack1l1ll1l111l_opy_:
            return args[2].tags if hasattr(args[2], bstack11lllll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨጼ")) else []
        if hasattr(args[0], bstack11lllll_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩጽ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1ll11l1l1_opy_(self, tags, capabilities):
        return self.bstack1l11lll111_opy_(tags) and self.bstack1l1l1l1l1l_opy_(capabilities)