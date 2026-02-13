# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll1111l1l_opy_ import (
    bstack1ll1lllllll_opy_,
    bstack1ll1l1llll1_opy_,
    bstack1ll1ll11l11_opy_,
    bstack1ll1l1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1l1lll1llll_opy_ import bstack1l1llllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_, bstack1ll11l111ll_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111111l1_opy_ import bstack1l1ll1lll11_opy_
from browserstack_sdk.sdk_cli.bstack1ll11lllll1_opy_ import bstack1ll1l111l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1111l1_opy_ import bstack1l1ll1ll111_opy_
from browserstack_sdk.sdk_cli.bstack1l1llll11ll_opy_ import bstack1l1lllll11l_opy_
from bstack_utils.helper import bstack1l1l111ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll11ll1l_opy_ import bstack111l1lllll_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll1111ll11_opy_(bstack1l1ll1lll11_opy_):
    bstack1l1l1lll1ll_opy_ = False
    bstack1l1l1ll11ll_opy_ = bstack11l11_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢዠ")
    bstack1l1ll11l111_opy_ = bstack11l11_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧ࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨዡ")
    bstack1l1ll11l11l_opy_ = bstack11l11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠤዢ")
    bstack1l1ll1111l1_opy_ = bstack11l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯ࡳࡠࡵࡦࡥࡳࡴࡩ࡯ࡩࠥዣ")
    bstack1l1ll11l1ll_opy_ = bstack11l11_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡨࡢࡵࡢࡹࡷࡲࠢዤ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1111ll1l_opy_, bstack1ll111l1l1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l11l1l1l_opy_ = False
        self.bstack1l1l11lll1l_opy_ = dict()
        self.bstack111111l11_opy_ = logger_utils.bstack11llll1l11_opy_(__name__)
        self.bstack1l1l1llll1l_opy_ = False
        self.bstack1l1l1lll11l_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l11llll1_opy_ = bstack1ll111l1l1l_opy_
        bstack1ll1111ll1l_opy_.bstack1l1l1l111ll_opy_((bstack1ll1lllllll_opy_.bstack1ll1ll1l11l_opy_, bstack1ll1l1llll1_opy_.PRE), self.bstack1l1l11lll11_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.PRE), self.bstack1l1l11ll111_opy_)
        TestFramework.bstack1l1l1l111ll_opy_((bstack1l1lllllll1_opy_.TEST, bstack1l1lllll1ll_opy_.POST), self.bstack1l1l1llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1l1ll11_opy_(instance, args)
        test_framework = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l1l11l11_opy_)
        if self.bstack1l1l11l1l1l_opy_:
            self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢዥ")] = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
        if bstack11l11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬዦ") in instance.bstack1l1l1l11l1l_opy_:
            platform_index = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l111l11l_opy_)
            self.accessibility = self.bstack1l1l111l1l1_opy_(tags, self.config[bstack11l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬዧ")][platform_index])
        else:
            capabilities = self.bstack1l1l11llll1_opy_.bstack1l1l1ll1lll_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥየ") + str(kwargs) + bstack11l11_opy_ (u"ࠦࠧዩ"))
                return
            self.accessibility = self.bstack1l1l111l1l1_opy_(tags, capabilities)
        if self.bstack1l1l11llll1_opy_.pages and self.bstack1l1l11llll1_opy_.pages.values():
            bstack1l1l1l1111l_opy_ = list(self.bstack1l1l11llll1_opy_.pages.values())
            if bstack1l1l1l1111l_opy_ and isinstance(bstack1l1l1l1111l_opy_[0], (list, tuple)) and bstack1l1l1l1111l_opy_[0]:
                bstack1l1l1lllll1_opy_ = bstack1l1l1l1111l_opy_[0][0]
                if callable(bstack1l1l1lllll1_opy_):
                    page = bstack1l1l1lllll1_opy_()
                    def bstack1l11llll_opy_():
                        self.get_accessibility_results(page, bstack11l11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤዪ"))
                    def bstack1l1l111ll11_opy_():
                        self.get_accessibility_results_summary(page, bstack11l11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥያ"))
                    setattr(page, bstack11l11_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡵࠥዬ"), bstack1l11llll_opy_)
                    setattr(page, bstack11l11_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥይ"), bstack1l1l111ll11_opy_)
        self.logger.debug(bstack11l11_opy_ (u"ࠤࡶ࡬ࡴࡻ࡬ࡥࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮ࡸࡩࡂࠨዮ") + str(self.accessibility) + bstack11l11_opy_ (u"ࠥࠦዯ"))
    def bstack1l1l11lll11_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        bstack1ll1l1lll1l_opy_: Tuple[bstack1ll1lllllll_opy_, bstack1ll1l1llll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1lllll111_opy_ = datetime.now()
            self.bstack1l1l111lll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢደ"), datetime.now() - bstack1lllll111_opy_)
            bstack1ll1llll1l1_opy_ = instance.data.get(bstack11l11_opy_ (u"ࠬࡸࡡ࡯࡭ࠪዱ"), None)
            if (
                not f.bstack1l1l1l1ll1l_opy_(method_name)
                or f.bstack1l1l1llllll_opy_(method_name, *args)
                or f.bstack1l1l1l1lll1_opy_(method_name, *args)
                or (bstack1ll1llll1l1_opy_ and int(bstack1ll1llll1l1_opy_)>1)
            ):
                return
            if not f.bstack1lll111111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll11l11l_opy_, False):
                if not bstack1ll1111ll11_opy_.bstack1l1l1lll1ll_opy_:
                    self.logger.warning(bstack11l11_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤዲ") + str(f.platform_index) + bstack11l11_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨዳ"))
                    bstack1ll1111ll11_opy_.bstack1l1l1lll1ll_opy_ = True
                return
            bstack1l1l11ll1ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1l11ll1ll_opy_:
                platform_index = f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_, 0)
                self.logger.debug(bstack11l11_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨዴ") + str(f.framework_name) + bstack11l11_opy_ (u"ࠤࠥድ"))
                return
            command_name = f.bstack1l1l11ll11l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧዶ") + str(method_name) + bstack11l11_opy_ (u"ࠦࠧዷ"))
                return
            bstack1l1l1ll1l11_opy_ = f.bstack1lll111111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll11l1ll_opy_, False)
            if command_name == bstack11l11_opy_ (u"ࠧ࡭ࡥࡵࠤዸ") and not bstack1l1l1ll1l11_opy_:
                f.bstack1ll1lll111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll11l1ll_opy_, True)
                bstack1l1l1ll1l11_opy_ = True
            if not bstack1l1l1ll1l11_opy_ and not self.bstack1l1l11l1l1l_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠨ࡮ࡰࠢࡘࡖࡑࠦ࡬ࡰࡣࡧࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧዹ") + str(command_name) + bstack11l11_opy_ (u"ࠢࠣዺ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11l11_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨዻ") + str(command_name) + bstack11l11_opy_ (u"ࠤࠥዼ"))
                return
            self.logger.info(bstack11l11_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡶࡧࡷ࡯ࡰࡵࡵࡢࡸࡴࡥࡲࡶࡰࠬࢁࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧዽ") + str(command_name) + bstack11l11_opy_ (u"ࠦࠧዾ"))
            scripts = [(s, bstack1l1l11ll1ll_opy_[s]) for s in scripts_to_run if s in bstack1l1l11ll1ll_opy_]
            for script_name, bstack1l1l1l1l1l1_opy_ in scripts:
                try:
                    bstack1lllll111_opy_ = datetime.now()
                    if script_name == bstack11l11_opy_ (u"ࠧࡹࡣࡢࡰࠥዿ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack1llll11l1_opy_ = {
                                bstack11l11_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢጀ"): {
                                    bstack11l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣጁ"): bstack11l11_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡄࡃࡑࠦጂ"),
                                    bstack11l11_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠨጃ"): [
                                        {
                                            bstack11l11_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥጄ"): command_name
                                        }
                                    ]
                                },
                                bstack11l11_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨጅ"): {
                                    bstack11l11_opy_ (u"ࠧࡨ࡯ࡥࡻࠥጆ"): {
                                        bstack11l11_opy_ (u"ࠨ࡭ࡴࡩࠥጇ"): result.get(bstack11l11_opy_ (u"ࠢ࡮ࡵࡪࠦገ"), bstack11l11_opy_ (u"ࠣࠤጉ")) if isinstance(result, dict) else bstack11l11_opy_ (u"ࠤࠥጊ"),
                                        bstack11l11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦጋ"): result.get(bstack11l11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧጌ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack111111l11_opy_.info(json.dumps(bstack1llll11l1_opy_, separators=(bstack11l11_opy_ (u"ࠧ࠲ࠢግ"), bstack11l11_opy_ (u"ࠨ࠺ࠣጎ"))))
                        except Exception as bstack11llll1l_opy_:
                            self.logger.debug(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥࡪࡡࡵࡣ࠽ࠤࠧጏ") + str(bstack11llll1l_opy_) + bstack11l11_opy_ (u"ࠣࠤጐ"))
                    instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࠣ጑") + script_name, datetime.now() - bstack1lllll111_opy_)
                    if isinstance(result, dict) and not result.get(bstack11l11_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦጒ"), True):
                        self.logger.warning(bstack11l11_opy_ (u"ࠦࡸࡱࡩࡱࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡸࡥ࡮ࡣ࡬ࡲ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴࡴ࠼ࠣࠦጓ") + str(result) + bstack11l11_opy_ (u"ࠧࠨጔ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11l11_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴ࠾ࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽࠡࡧࡵࡶࡴࡸ࠽ࠣጕ") + str(e) + bstack11l11_opy_ (u"ࠢࠣ጖"))
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡫ࡲࡳࡱࡵࡁࠧ጗") + str(e) + bstack11l11_opy_ (u"ࠤࠥጘ"))
    def bstack1l1l1llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l111ll_opy_,
        bstack1ll1l1lll1l_opy_: Tuple[bstack1l1lllllll1_opy_, bstack1l1lllll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1l1ll11_opy_(instance, args)
        capabilities = self.bstack1l1l11llll1_opy_.bstack1l1l1ll1lll_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l1l111l1l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢጙ"))
            return
        driver = self.bstack1l1l11llll1_opy_.bstack1l1l11l111l_opy_(f, instance, bstack1ll1l1lll1l_opy_, *args, **kwargs)
        test_name = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1ll11111l_opy_)
        if not test_name:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤጚ"))
            return
        test_uuid = f.bstack1lll111111l_opy_(instance, TestFramework.bstack1l1l11l11l1_opy_)
        if not test_uuid:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥጛ"))
            return
        if isinstance(self.bstack1l1l11llll1_opy_, bstack1l1ll1ll111_opy_):
            framework_name = bstack11l11_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪጜ")
        else:
            framework_name = bstack11l11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩጝ")
        self.bstack1ll1l111l1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack11ll1l1lll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࠤጞ"))
            return
        bstack1lllll111_opy_ = datetime.now()
        bstack1l1l1l1l1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11l11_opy_ (u"ࠤࡶࡧࡦࡴࠢጟ"), None)
        if not bstack1l1l1l1l1l1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥጠ") + str(framework_name) + bstack11l11_opy_ (u"ࠦࠥࠨጡ"))
            return
        if self.bstack1l1l11l1l1l_opy_:
            arg = dict()
            arg[bstack11l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧጢ")] = method if method else bstack11l11_opy_ (u"ࠨࠢጣ")
            arg[bstack11l11_opy_ (u"ࠢࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠢጤ")] = self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣጥ")]
            arg[bstack11l11_opy_ (u"ࠤࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠢጦ")] = self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣጧ")]
            arg[bstack11l11_opy_ (u"ࠦࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣጨ")] = self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠥጩ")]
            arg[bstack11l11_opy_ (u"ࠨࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠥጪ")] = self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨጫ")]
            arg[bstack11l11_opy_ (u"ࠣࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠣጬ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1l1ll1111_opy_ = self.bstack1l1l11lllll_opy_(bstack11l11_opy_ (u"ࠤࡶࡧࡦࡴࠢጭ"), self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥጮ")])
            if bstack11l11_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡖࡲ࡯ࡪࡴࠢጯ") in bstack1l1l1ll1111_opy_:
                bstack1l1l1ll1111_opy_ = bstack1l1l1ll1111_opy_.copy()
                bstack1l1l1ll1111_opy_[bstack11l11_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡋࡩࡦࡪࡥࡳࠤጰ")] = bstack1l1l1ll1111_opy_.pop(bstack11l11_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤጱ"))
            arg = bstack1l1l111ll1l_opy_(arg, bstack1l1l1ll1111_opy_)
            bstack1l1ll111l11_opy_ = bstack1l1l1l1l1l1_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1ll111l11_opy_)
            return
        instance = bstack1ll1ll11l11_opy_.bstack1ll1ll11111_opy_(driver)
        if instance:
            if not bstack1ll1ll11l11_opy_.bstack1lll111111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1111l1_opy_, False):
                bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1111l1_opy_, True)
            else:
                self.logger.info(bstack11l11_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦጲ") + str(method) + bstack11l11_opy_ (u"ࠣࠤጳ"))
                return
        self.logger.info(bstack11l11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢጴ") + str(method) + bstack11l11_opy_ (u"ࠥࠦጵ"))
        if framework_name == bstack11l11_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨጶ"):
            result = self.bstack1l1l11llll1_opy_.bstack1l1l1ll11l1_opy_(driver, bstack1l1l1l1l1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1l1l1l1_opy_, {bstack11l11_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧጷ"): method if method else bstack11l11_opy_ (u"ࠨࠢጸ")})
        bstack111l1lllll_opy_.end(EVENTS.bstack11ll1l1lll_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢጹ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨጺ"), True, None, command=method)
        if instance:
            bstack1ll1ll11l11_opy_.bstack1ll1lll111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll1111l1_opy_, False)
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨጻ"), datetime.now() - bstack1lllll111_opy_)
        return result
        def bstack1l1l1l11111_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1l11l1111_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1ll1111ll_opy_ = self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥጼ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫጽ"), bstack11l11_opy_ (u"ࠬ࠶ࠧጾ")))
            req.client_worker_id = bstack11l11_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧጿ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1l1l1lll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11l11_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤፀ") + str(r) + bstack11l11_opy_ (u"ࠣࠤፁ"))
                else:
                    bstack1l1l1l1l111_opy_ = json.loads(r.bstack1l1l111l1ll_opy_.decode(bstack11l11_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨፂ")))
                    if result_type == bstack11l11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧፃ"):
                        return bstack1l1l1l1l111_opy_.get(bstack11l11_opy_ (u"ࠦࡩࡧࡴࡢࠤፄ"), [])
                    else:
                        return bstack1l1l1l1l111_opy_.get(bstack11l11_opy_ (u"ࠧࡪࡡࡵࡣࠥፅ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11l11_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡲࡳࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࠤ࡫ࡸ࡯࡮ࠢࡦࡰ࡮ࡀࠠࠣፆ") + str(e) + bstack11l11_opy_ (u"ࠢࠣፇ"))
    @measure(event_name=EVENTS.bstack111ll1l11_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l11_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥፈ"))
            return
        if self.bstack1l1l11l1l1l_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡣࡳࡴࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬፉ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1l11111_opy_(driver, framework_name, bstack11l11_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢፊ"))
        bstack1l1l1l1l1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11l11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣፋ"), None)
        if not bstack1l1l1l1l1l1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦፌ") + str(framework_name) + bstack11l11_opy_ (u"ࠨࠢፍ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1lllll111_opy_ = datetime.now()
        if framework_name == bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫፎ"):
            result = self.bstack1l1l11llll1_opy_.bstack1l1l1ll11l1_opy_(driver, bstack1l1l1l1l1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1l1l1l1_opy_)
        instance = bstack1ll1ll11l11_opy_.bstack1ll1ll11111_opy_(driver)
        if instance:
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦፏ"), datetime.now() - bstack1lllll111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1llll1ll11_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l11_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧፐ"))
            return
        if self.bstack1l1l11l1l1l_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1l11111_opy_(driver, framework_name, bstack11l11_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧፑ"))
        bstack1l1l1l1l1l1_opy_ = self.scripts.get(framework_name, {}).get(bstack11l11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣፒ"), None)
        if not bstack1l1l1l1l1l1_opy_:
            self.logger.debug(bstack11l11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦፓ") + str(framework_name) + bstack11l11_opy_ (u"ࠨࠢፔ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1lllll111_opy_ = datetime.now()
        if framework_name == bstack11l11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫፕ"):
            result = self.bstack1l1l11llll1_opy_.bstack1l1l1ll11l1_opy_(driver, bstack1l1l1l1l1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1l1l1l1_opy_)
        instance = bstack1ll1ll11l11_opy_.bstack1ll1ll11111_opy_(driver)
        if instance:
            instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧፖ"), datetime.now() - bstack1lllll111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1ll11l1l1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l1l1l11ll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1l11l1111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11l11_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣፗ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1l1l1lll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧፘ") + str(r) + bstack11l11_opy_ (u"ࠦࠧፙ"))
            else:
                self.bstack1l1l11ll1l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l11_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥፚ") + str(e) + bstack11l11_opy_ (u"ࠨࠢ፛"))
            traceback.print_exc()
            raise e
    def bstack1l1l11ll1l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11l11_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢ፜"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l11l1l1l_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨ፝")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1l11lll1l_opy_[bstack11l11_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣ፞")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1l11lll1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l1lll111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1l1ll11ll_opy_ and command.module == self.bstack1l1ll11l111_opy_:
                        if command.method and not command.method in bstack1l1l1lll111_opy_:
                            bstack1l1l1lll111_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1l1lll111_opy_[command.method]:
                            bstack1l1l1lll111_opy_[command.method][command.name] = list()
                        bstack1l1l1lll111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l1lll111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1l111lll1_opy_(
        self,
        f: bstack1l1llllllll_opy_,
        exec: Tuple[bstack1ll1l1ll1ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l11llll1_opy_, bstack1l1ll1ll111_opy_) and method_name != bstack11l11_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫ፟"):
            return
        if bstack1ll1ll11l11_opy_.bstack1ll1l1lll11_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll11l11l_opy_):
            return
        if f.bstack1l1l11l1lll_opy_(method_name, *args):
            bstack1l1l11l1ll1_opy_ = False
            desired_capabilities = f.bstack1l1l1l111l1_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1l1ll1l1l_opy_(instance)
                platform_index = f.bstack1lll111111l_opy_(instance, bstack1l1llllllll_opy_.bstack1l1l111l11l_opy_, 0)
                bstack1l1l11l1l11_opy_ = datetime.now()
                r = self.bstack1l1l1l11ll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1lll1ll1_opy_(bstack11l11_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤ፠"), datetime.now() - bstack1l1l11l1l11_opy_)
                bstack1l1l11l1ll1_opy_ = r.success
            else:
                self.logger.error(bstack11l11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡤࡦࡵ࡬ࡶࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡃࠢ፡") + str(desired_capabilities) + bstack11l11_opy_ (u"ࠨࠢ።"))
            f.bstack1ll1lll111l_opy_(instance, bstack1ll1111ll11_opy_.bstack1l1ll11l11l_opy_, bstack1l1l11l1ll1_opy_)
    def bstack11l11l1lll_opy_(self, test_tags):
        bstack1l1l1l11ll1_opy_ = self.config.get(bstack11l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ፣"))
        if not bstack1l1l1l11ll1_opy_:
            return True
        try:
            include_tags = bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭፤")] if bstack11l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ፥") in bstack1l1l1l11ll1_opy_ and isinstance(bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ፦")], list) else []
            exclude_tags = bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ፧")] if bstack11l11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ፨") in bstack1l1l1l11ll1_opy_ and isinstance(bstack1l1l1l11ll1_opy_[bstack11l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ፩")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11l11_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢ፪") + str(error))
        return False
    def bstack11l111l1l_opy_(self, caps):
        try:
            if self.bstack1l1l11l1l1l_opy_:
                bstack1l1l1lll1l1_opy_ = caps.get(bstack11l11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ፫"))
                if bstack1l1l1lll1l1_opy_ is not None and str(bstack1l1l1lll1l1_opy_).lower() == bstack11l11_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥ፬"):
                    bstack1l1ll11ll1l_opy_ = caps.get(bstack11l11_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ፭")) or caps.get(bstack11l11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ፮"))
                    if bstack1l1ll11ll1l_opy_ is not None and int(bstack1l1ll11ll1l_opy_) < 11:
                        self.logger.warning(bstack11l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠧ፯") + str(bstack1l1ll11ll1l_opy_) + bstack11l11_opy_ (u"ࠨࠢ፰"))
                        return False
                return True
            bstack1l1ll111l1l_opy_ = caps.get(bstack11l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ፱"), {}).get(bstack11l11_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬ፲"), caps.get(bstack11l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩ፳"), bstack11l11_opy_ (u"ࠪࠫ፴")))
            if bstack1l1ll111l1l_opy_:
                self.logger.warning(bstack11l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ፵"))
                return False
            browser = caps.get(bstack11l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪ፶"), bstack11l11_opy_ (u"࠭ࠧ፷")).lower()
            if browser != bstack11l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ፸"):
                self.logger.warning(bstack11l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ፹"))
                return False
            bstack1l1ll111111_opy_ = bstack1l1l1ll111l_opy_
            if not self.config.get(bstack11l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ፺")) or self.config.get(bstack11l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ፻")):
                bstack1l1ll111111_opy_ = bstack1l1ll111lll_opy_
            browser_version = caps.get(bstack11l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ፼"))
            if not browser_version:
                browser_version = caps.get(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭፽"), {}).get(bstack11l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ፾"), bstack11l11_opy_ (u"ࠧࠨ፿"))
            bstack1l1l11l11ll_opy_ = str(browser_version).lower() if browser_version is not None else bstack11l11_opy_ (u"ࠨࠩᎀ")
            if bstack1l1l11l11ll_opy_:
                if bstack1l1l11l11ll_opy_.startswith(bstack11l11_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᎁ")):
                    if bstack1l1l11l11ll_opy_.startswith(bstack11l11_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫᎂ")):
                        bstack1l1l111llll_opy_ = bstack1l1l11l11ll_opy_[len(bstack11l11_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬᎃ")):]
                        if bstack1l1l111llll_opy_ and not bstack1l1l111llll_opy_.isdigit():
                            self.logger.warning(bstack11l11_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡨࡲࡶࡲࡧࡴࠡࠩࠥᎄ") + str(browser_version) + bstack11l11_opy_ (u"ࠨࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࠬࡲࡡࡵࡧࡶࡸࠬࠦ࡯ࡳࠢࠪࡰࡦࡺࡥࡴࡶ࠰ࡀࡳࡻ࡭ࡣࡧࡵࡂࠬ࠴ࠢᎅ"))
                            return False
                else:
                    try:
                        if int(bstack1l1l11l11ll_opy_.split(bstack11l11_opy_ (u"ࠧ࠯ࠩᎆ"))[0]) <= bstack1l1ll111111_opy_:
                            self.logger.warning(bstack11l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥᎇ") + str(bstack1l1ll111111_opy_) + bstack11l11_opy_ (u"ࠤ࠱ࠦᎈ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11l11_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠨࡽࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࢁࠬࡀࠠࠣᎉ") + str(e) + bstack11l11_opy_ (u"ࠦࠧᎊ"))
            bstack1l1ll11ll11_opy_ = caps.get(bstack11l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᎋ"), {}).get(bstack11l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᎌ"))
            if not bstack1l1ll11ll11_opy_:
                bstack1l1ll11ll11_opy_ = caps.get(bstack11l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᎍ"), {})
            if bstack1l1ll11ll11_opy_ and bstack11l11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᎎ") in bstack1l1ll11ll11_opy_.get(bstack11l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᎏ"), []):
                self.logger.warning(bstack11l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧ᎐"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11l11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨ᎑") + str(error))
            return False
    def bstack1l1l1l1l11l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1ll11lll1_opy_ = {
            bstack11l11_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ᎒"): test_uuid,
        }
        bstack1l1ll111ll1_opy_ = {}
        if result.success:
            bstack1l1ll111ll1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l111ll1l_opy_(bstack1l1ll11lll1_opy_, bstack1l1ll111ll1_opy_)
    def bstack1l1l11lllll_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11l11_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡪࡺࡣࡩࠢࡦࡩࡳࡺࡲࡢ࡮ࠣࡥࡺࡺࡨࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡰࡤࡱࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡦࡥࡨ࡮ࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡦࡦࡶࡦ࡬ࡪࡪࠬࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠤࡱࡵࡡࡥࡵࠣࡥࡳࡪࠠࡤࡣࡦ࡬ࡪࡹࠠࡪࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫࠺ࠡࡐࡤࡱࡪࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡳࡤࡴ࡬ࡴࡹࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡶࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࡀࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠮ࠣࡩࡲࡶࡴࡺࠢࡧ࡭ࡨࡺࠠࡪࡨࠣࡩࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨ᎓")
        try:
            if self.bstack1l1l1llll1l_opy_:
                return self.bstack1l1l1lll11l_opy_
            self.bstack1l1l11l1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l11_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ᎔")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨ᎕"), bstack11l11_opy_ (u"ࠩ࠳ࠫ᎖")))
            req.client_worker_id = bstack11l11_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤ᎗").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1l1l1lll_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1l1lll11l_opy_ = self.bstack1l1l1l1l11l_opy_(test_uuid, r)
                self.bstack1l1l1llll1l_opy_ = True
            else:
                self.logger.error(bstack11l11_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨ᎘") + str(r.error) + bstack11l11_opy_ (u"ࠧࠨ᎙"))
                self.bstack1l1l1lll11l_opy_ = dict()
            return self.bstack1l1l1lll11l_opy_
        except Exception as e:
            self.logger.error(bstack11l11_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣ᎚") + str(traceback.format_exc()) + bstack11l11_opy_ (u"ࠢࠣ᎛"))
            return dict()
    def bstack1ll1l111l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l111l111l_opy_ = None
        try:
            self.bstack1l1l11l1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l11_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣ᎜")
            req.script_name = bstack11l11_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢ᎝")
            req.platform_index = str(os.environ.get(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪ᎞"), bstack11l11_opy_ (u"ࠫ࠵࠭᎟")))
            req.client_worker_id = bstack11l11_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᎠ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1l1l1lll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11l11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᎡ") + str(r.error) + bstack11l11_opy_ (u"ࠢࠣᎢ"))
            else:
                bstack1l1ll11lll1_opy_ = self.bstack1l1l1l1l11l_opy_(test_uuid, r)
                bstack1l1l1l1l1l1_opy_ = r.script
            self.logger.debug(bstack11l11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᎣ") + str(bstack1l1ll11lll1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1l1l1l1l1_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᎤ") + str(framework_name) + bstack11l11_opy_ (u"ࠥࠤࠧᎥ"))
                return
            bstack1l111l111l_opy_ = bstack111l1lllll_opy_.bstack1l11111111_opy_(EVENTS.bstack1l1l1l11lll_opy_.value)
            self.bstack1l1l1l1l1ll_opy_(driver, bstack1l1l1l1l1l1_opy_, bstack1l1ll11lll1_opy_, framework_name)
            try:
                bstack1l1l1ll1ll1_opy_ = {
                    bstack11l11_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧᎦ"): {
                        bstack11l11_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨᎧ"): bstack11l11_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥᎨ"),
                    },
                    bstack11l11_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤᎩ"): {
                        bstack11l11_opy_ (u"ࠣࡤࡲࡨࡾࠨᎪ"): {
                            bstack11l11_opy_ (u"ࠤࡰࡷ࡬ࠨᎫ"): bstack11l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᎬ"),
                            bstack11l11_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᎭ"): True
                        }
                    }
                }
                self.bstack111111l11_opy_.info(json.dumps(bstack1l1l1ll1ll1_opy_, separators=(bstack11l11_opy_ (u"ࠬ࠲ࠧᎮ"), bstack11l11_opy_ (u"࠭࠺ࠨᎯ"))))
            except Exception as bstack11llll1l_opy_:
                self.logger.debug(bstack11l11_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨᎰ") + str(bstack11llll1l_opy_) + bstack11l11_opy_ (u"ࠣࠤᎱ"))
            self.logger.info(bstack11l11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᎲ"))
            bstack111l1lllll_opy_.end(EVENTS.bstack1l1l1l11lll_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᎳ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᎴ"), True, None, command=bstack11l11_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᎵ"),test_name=name)
        except Exception as bstack1l1l1l1llll_opy_:
            self.logger.error(bstack11l11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᎶ") + bstack11l11_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥᎷ") + bstack11l11_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᎸ") + str(bstack1l1l1l1llll_opy_))
            bstack111l1lllll_opy_.end(EVENTS.bstack1l1l1l11lll_opy_.value, bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᎹ"), bstack1l111l111l_opy_+bstack11l11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᎺ"), False, bstack1l1l1l1llll_opy_, command=bstack11l11_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᎻ"),test_name=name)
    def bstack1l1l1l1l1ll_opy_(self, driver, bstack1l1l1l1l1l1_opy_, bstack1l1ll11lll1_opy_, framework_name):
        if framework_name == bstack11l11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᎼ"):
            self.bstack1l1l11llll1_opy_.bstack1l1l1ll11l1_opy_(driver, bstack1l1l1l1l1l1_opy_, bstack1l1ll11lll1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1l1l1l1l1_opy_, bstack1l1ll11lll1_opy_))
    def _1l1l1l1ll11_opy_(self, instance: bstack1ll11l111ll_opy_, args: Tuple) -> list:
        bstack11l11_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᎽ")
        if bstack11l11_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᎾ") in instance.bstack1l1l1l11l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack11l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭Ꮏ")) else []
        if hasattr(args[0], bstack11l11_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧᏀ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1l111l1l1_opy_(self, tags, capabilities):
        return self.bstack11l11l1lll_opy_(tags) and self.bstack11l111l1l_opy_(capabilities)