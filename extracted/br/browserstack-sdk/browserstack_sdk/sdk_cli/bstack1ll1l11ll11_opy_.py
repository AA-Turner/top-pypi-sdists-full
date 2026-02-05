# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll1l1lll1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1ll1l11_opy_,
    bstack1lll111llll_opy_,
    bstack1lll11lll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1l1_opy_ import bstack1ll1ll1lll1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_, bstack1ll1ll111l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1ll1l11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll111l1l11_opy_ import bstack1ll1l11l11l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l11lll1_opy_ import bstack1ll1l1lllll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll111ll1l1_opy_
from bstack_utils.helper import bstack1l1l1lllll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
from bstack_utils import bstack1l1111l1l_opy_
import grpc
import traceback
import json
class bstack1ll1llll1l1_opy_(bstack1ll1l11l1ll_opy_):
    bstack1l1lllllll1_opy_ = False
    bstack1l1l1llll1l_opy_ = bstack11l1ll1_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣቀ")
    bstack1l1lllll1l1_opy_ = bstack11l1ll1_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢቁ")
    bstack1l1lll1l111_opy_ = bstack11l1ll1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥቂ")
    bstack1l1ll11lll1_opy_ = bstack11l1ll1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦቃ")
    bstack1l1ll111l11_opy_ = bstack11l1ll1_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣቄ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1lllll1l_opy_, bstack1ll1llllll1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1ll1ll1l1_opy_ = False
        self.bstack1l1llll11ll_opy_ = dict()
        self.bstack11llll111_opy_ = bstack1l1111l1l_opy_.bstack11l1111l11_opy_(__name__)
        self.bstack1l1ll1l11ll_opy_ = False
        self.bstack1l1ll1l11l1_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l1lll1ll_opy_ = bstack1ll1llllll1_opy_
        bstack1ll1lllll1l_opy_.bstack1l1ll11llll_opy_((bstack1lll111lll1_opy_.bstack1lll1ll111l_opy_, bstack1lll1ll1l11_opy_.PRE), self.bstack1l1ll111lll_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.PRE), self.bstack1l1ll11ll11_opy_)
        TestFramework.bstack1l1ll11llll_opy_((bstack1ll11l1l1l1_opy_.TEST, bstack1ll1111llll_opy_.POST), self.bstack1l1llll1ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1ll11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1lllll1ll_opy_(instance, args)
        test_framework = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llllll11_opy_)
        if self.bstack1l1ll1ll1l1_opy_:
            self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣቅ")] = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
        if bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ቆ") in instance.bstack1l1lll1l1ll_opy_:
            platform_index = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l1lll1l1_opy_)
            self.accessibility = self.bstack1l1llll1lll_opy_(tags, self.config[bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ቇ")][platform_index])
        else:
            capabilities = self.bstack1l1l1lll1ll_opy_.bstack1l1ll1l1l1l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦቈ") + str(kwargs) + bstack11l1ll1_opy_ (u"ࠧࠨ቉"))
                return
            self.accessibility = self.bstack1l1llll1lll_opy_(tags, capabilities)
        if self.bstack1l1l1lll1ll_opy_.pages and self.bstack1l1l1lll1ll_opy_.pages.values():
            bstack1l1ll1lll1l_opy_ = list(self.bstack1l1l1lll1ll_opy_.pages.values())
            if bstack1l1ll1lll1l_opy_ and isinstance(bstack1l1ll1lll1l_opy_[0], (list, tuple)) and bstack1l1ll1lll1l_opy_[0]:
                bstack1l1ll1l1111_opy_ = bstack1l1ll1lll1l_opy_[0][0]
                if callable(bstack1l1ll1l1111_opy_):
                    page = bstack1l1ll1l1111_opy_()
                    def bstack11l1llll_opy_():
                        self.get_accessibility_results(page, bstack11l1ll1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥቊ"))
                    def bstack1l1lll1l1l1_opy_():
                        self.get_accessibility_results_summary(page, bstack11l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦቋ"))
                    setattr(page, bstack11l1ll1_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦቌ"), bstack11l1llll_opy_)
                    setattr(page, bstack11l1ll1_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦቍ"), bstack1l1lll1l1l1_opy_)
        self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢ቎") + str(self.accessibility) + bstack11l1ll1_opy_ (u"ࠦࠧ቏"))
    def bstack1l1ll111lll_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        driver: object,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        bstack1lll1l1ll11_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1ll1l11_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack111ll1ll1_opy_ = datetime.now()
            self.bstack1l1ll111ll1_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣቐ"), datetime.now() - bstack111ll1ll1_opy_)
            if (
                not f.bstack1l1ll111111_opy_(method_name)
                or f.bstack1l1ll1ll1ll_opy_(method_name, *args)
                or f.bstack1l1ll11111l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lll1ll11l1_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1lll1l111_opy_, False):
                if not bstack1ll1llll1l1_opy_.bstack1l1lllllll1_opy_:
                    self.logger.warning(bstack11l1ll1_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤቑ") + str(f.platform_index) + bstack11l1ll1_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨቒ"))
                    bstack1ll1llll1l1_opy_.bstack1l1lllllll1_opy_ = True
                return
            bstack1l1lll11lll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1lll11lll_opy_:
                platform_index = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_, 0)
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨቓ") + str(f.framework_name) + bstack11l1ll1_opy_ (u"ࠤࠥቔ"))
                return
            command_name = f.bstack1l1llll11l1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧቕ") + str(method_name) + bstack11l1ll1_opy_ (u"ࠦࠧቖ"))
                return
            bstack1l1lll11l11_opy_ = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1ll111l11_opy_, False)
            if command_name == bstack11l1ll1_opy_ (u"ࠧ࡭ࡥࡵࠤ቗") and not bstack1l1lll11l11_opy_:
                f.bstack1lll1l1111l_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1ll111l11_opy_, True)
                bstack1l1lll11l11_opy_ = True
            if not bstack1l1lll11l11_opy_ and not self.bstack1l1ll1ll1l1_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨ࡮ࡰࠢࡘࡖࡑࠦ࡬ࡰࡣࡧࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧቘ") + str(command_name) + bstack11l1ll1_opy_ (u"ࠢࠣ቙"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨቚ") + str(command_name) + bstack11l1ll1_opy_ (u"ࠤࠥቛ"))
                return
            self.logger.info(bstack11l1ll1_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡶࡧࡷ࡯ࡰࡵࡵࡢࡸࡴࡥࡲࡶࡰࠬࢁࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧቜ") + str(command_name) + bstack11l1ll1_opy_ (u"ࠦࠧቝ"))
            scripts = [(s, bstack1l1lll11lll_opy_[s]) for s in scripts_to_run if s in bstack1l1lll11lll_opy_]
            for script_name, bstack1l1lll11l1l_opy_ in scripts:
                try:
                    bstack111ll1ll1_opy_ = datetime.now()
                    if script_name == bstack11l1ll1_opy_ (u"ࠧࡹࡣࡢࡰࠥ቞"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack1ll1ll11ll_opy_ = {
                                bstack11l1ll1_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ቟"): {
                                    bstack11l1ll1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣበ"): bstack11l1ll1_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡄࡃࡑࠦቡ"),
                                    bstack11l1ll1_opy_ (u"ࠤࡳࡥࡷࡧ࡭ࡦࡶࡨࡶࡸࠨቢ"): [
                                        {
                                            bstack11l1ll1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥባ"): command_name
                                        }
                                    ]
                                },
                                bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨቤ"): {
                                    bstack11l1ll1_opy_ (u"ࠧࡨ࡯ࡥࡻࠥብ"): {
                                        bstack11l1ll1_opy_ (u"ࠨ࡭ࡴࡩࠥቦ"): result.get(bstack11l1ll1_opy_ (u"ࠢ࡮ࡵࡪࠦቧ"), bstack11l1ll1_opy_ (u"ࠣࠤቨ")) if isinstance(result, dict) else bstack11l1ll1_opy_ (u"ࠤࠥቩ"),
                                        bstack11l1ll1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦቪ"): result.get(bstack11l1ll1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧቫ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack11llll111_opy_.info(json.dumps(bstack1ll1ll11ll_opy_, separators=(bstack11l1ll1_opy_ (u"ࠧ࠲ࠢቬ"), bstack11l1ll1_opy_ (u"ࠨ࠺ࠣቭ"))))
                        except Exception as bstack11lll11l_opy_:
                            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡥࡤࡲࠥࡪࡡࡵࡣ࠽ࠤࠧቮ") + str(bstack11lll11l_opy_) + bstack11l1ll1_opy_ (u"ࠣࠤቯ"))
                    instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࠣተ") + script_name, datetime.now() - bstack111ll1ll1_opy_)
                    if isinstance(result, dict) and not result.get(bstack11l1ll1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦቱ"), True):
                        self.logger.warning(bstack11l1ll1_opy_ (u"ࠦࡸࡱࡩࡱࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡸࡥ࡮ࡣ࡬ࡲ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴࡴ࠼ࠣࠦቲ") + str(result) + bstack11l1ll1_opy_ (u"ࠧࠨታ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴ࠾ࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽࠡࡧࡵࡶࡴࡸ࠽ࠣቴ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣት"))
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡫ࡲࡳࡱࡵࡁࠧቶ") + str(e) + bstack11l1ll1_opy_ (u"ࠤࠥቷ"))
    def bstack1l1llll1ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll111l1_opy_,
        bstack1lll1l1ll11_opy_: Tuple[bstack1ll11l1l1l1_opy_, bstack1ll1111llll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1lllll1ll_opy_(instance, args)
        capabilities = self.bstack1l1l1lll1ll_opy_.bstack1l1ll1l1l1l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l1llll1lll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢቸ"))
            return
        driver = self.bstack1l1l1lll1ll_opy_.bstack1l1ll11ll1l_opy_(f, instance, bstack1lll1l1ll11_opy_, *args, **kwargs)
        test_name = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1l1lll11l_opy_)
        if not test_name:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤቹ"))
            return
        test_uuid = f.bstack1lll1ll11l1_opy_(instance, TestFramework.bstack1l1llll1l11_opy_)
        if not test_uuid:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥቺ"))
            return
        if isinstance(self.bstack1l1l1lll1ll_opy_, bstack1ll1l1lllll_opy_):
            framework_name = bstack11l1ll1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪቻ")
        else:
            framework_name = bstack11l1ll1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩቼ")
        self.bstack11ll1l111_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack1l1l11llll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࠤች"))
            return
        bstack111ll1ll1_opy_ = datetime.now()
        bstack1l1lll11l1l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1ll1_opy_ (u"ࠤࡶࡧࡦࡴࠢቾ"), None)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥቿ") + str(framework_name) + bstack11l1ll1_opy_ (u"ࠦࠥࠨኀ"))
            return
        if self.bstack1l1ll1ll1l1_opy_:
            arg = dict()
            arg[bstack11l1ll1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧኁ")] = method if method else bstack11l1ll1_opy_ (u"ࠨࠢኂ")
            arg[bstack11l1ll1_opy_ (u"ࠢࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠢኃ")] = self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣኄ")]
            arg[bstack11l1ll1_opy_ (u"ࠤࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠢኅ")] = self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣኆ")]
            arg[bstack11l1ll1_opy_ (u"ࠦࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣኇ")] = self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠥኈ")]
            arg[bstack11l1ll1_opy_ (u"ࠨࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠥ኉")] = self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨኊ")]
            arg[bstack11l1ll1_opy_ (u"ࠣࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠣኋ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1lll1l11l_opy_ = self.bstack1l1ll11l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡶࡧࡦࡴࠢኌ"), self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥኍ")])
            if bstack11l1ll1_opy_ (u"ࠦࡨ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡖࡲ࡯ࡪࡴࠢ኎") in bstack1l1lll1l11l_opy_:
                bstack1l1lll1l11l_opy_ = bstack1l1lll1l11l_opy_.copy()
                bstack1l1lll1l11l_opy_[bstack11l1ll1_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡋࡩࡦࡪࡥࡳࠤ኏")] = bstack1l1lll1l11l_opy_.pop(bstack11l1ll1_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤነ"))
            arg = bstack1l1l1lllll1_opy_(arg, bstack1l1lll1l11l_opy_)
            bstack1l1ll1111l1_opy_ = bstack1l1lll11l1l_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1ll1111l1_opy_)
            return
        instance = bstack1lll111llll_opy_.bstack1lll11ll11l_opy_(driver)
        if instance:
            if not bstack1lll111llll_opy_.bstack1lll1ll11l1_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1ll11lll1_opy_, False):
                bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1ll11lll1_opy_, True)
            else:
                self.logger.info(bstack11l1ll1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦኑ") + str(method) + bstack11l1ll1_opy_ (u"ࠣࠤኒ"))
                return
        self.logger.info(bstack11l1ll1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢና") + str(method) + bstack11l1ll1_opy_ (u"ࠥࠦኔ"))
        if framework_name == bstack11l1ll1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨን"):
            result = self.bstack1l1l1lll1ll_opy_.bstack1l1ll1111ll_opy_(driver, bstack1l1lll11l1l_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll11l1l_opy_, {bstack11l1ll1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧኖ"): method if method else bstack11l1ll1_opy_ (u"ࠨࠢኗ")})
        bstack1ll1111ll_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢኘ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨኙ"), True, None, command=method)
        if instance:
            bstack1lll111llll_opy_.bstack1lll1l1111l_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1ll11lll1_opy_, False)
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨኚ"), datetime.now() - bstack111ll1ll1_opy_)
        return result
        def bstack1l1ll11l111_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1lll1ll1l_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1lll111l1_opy_ = self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥኛ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫኜ"), bstack11l1ll1_opy_ (u"ࠬ࠶ࠧኝ")))
            req.client_worker_id = bstack11l1ll1_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧኞ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1llll1ll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤኟ") + str(r) + bstack11l1ll1_opy_ (u"ࠣࠤአ"))
                else:
                    bstack1l1ll11l1ll_opy_ = json.loads(r.bstack1l1lll1llll_opy_.decode(bstack11l1ll1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨኡ")))
                    if result_type == bstack11l1ll1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧኢ"):
                        return bstack1l1ll11l1ll_opy_.get(bstack11l1ll1_opy_ (u"ࠦࡩࡧࡴࡢࠤኣ"), [])
                    else:
                        return bstack1l1ll11l1ll_opy_.get(bstack11l1ll1_opy_ (u"ࠧࡪࡡࡵࡣࠥኤ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡲࡳࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࠤ࡫ࡸ࡯࡮ࠢࡦࡰ࡮ࡀࠠࠣእ") + str(e) + bstack11l1ll1_opy_ (u"ࠢࠣኦ"))
    @measure(event_name=EVENTS.bstack1lll11ll_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥኧ"))
            return
        if self.bstack1l1ll1ll1l1_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡣࡳࡴࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬከ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1ll11l111_opy_(driver, framework_name, bstack11l1ll1_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢኩ"))
        bstack1l1lll11l1l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1ll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣኪ"), None)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦካ") + str(framework_name) + bstack11l1ll1_opy_ (u"ࠨࠢኬ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111ll1ll1_opy_ = datetime.now()
        if framework_name == bstack11l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫክ"):
            result = self.bstack1l1l1lll1ll_opy_.bstack1l1ll1111ll_opy_(driver, bstack1l1lll11l1l_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll11l1l_opy_)
        instance = bstack1lll111llll_opy_.bstack1lll11ll11l_opy_(driver)
        if instance:
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࠦኮ"), datetime.now() - bstack111ll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1llll1l11l_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧኯ"))
            return
        if self.bstack1l1ll1ll1l1_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1ll11l111_opy_(driver, framework_name, bstack11l1ll1_opy_ (u"ࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧኰ"))
        bstack1l1lll11l1l_opy_ = self.scripts.get(framework_name, {}).get(bstack11l1ll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣ኱"), None)
        if not bstack1l1lll11l1l_opy_:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦኲ") + str(framework_name) + bstack11l1ll1_opy_ (u"ࠨࠢኳ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack111ll1ll1_opy_ = datetime.now()
        if framework_name == bstack11l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫኴ"):
            result = self.bstack1l1l1lll1ll_opy_.bstack1l1ll1111ll_opy_(driver, bstack1l1lll11l1l_opy_)
        else:
            result = driver.execute_async_script(bstack1l1lll11l1l_opy_)
        instance = bstack1lll111llll_opy_.bstack1lll11ll11l_opy_(driver)
        if instance:
            instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧኵ"), datetime.now() - bstack111ll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1ll1ll111_opy_, stage=STAGE.bstack11lll1l1l1_opy_)
    def bstack1l1ll1l111l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1lll1ll1l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack11l1ll1_opy_ (u"ࠤࡾࢁ࠲ࢁࡽࠣ኶").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1llll1ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧ኷") + str(r) + bstack11l1ll1_opy_ (u"ࠦࠧኸ"))
            else:
                self.bstack1l1ll1l1l11_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥኹ") + str(e) + bstack11l1ll1_opy_ (u"ࠨࠢኺ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll1l1l11_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢኻ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1ll1ll1l1_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨኼ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1llll11ll_opy_[bstack11l1ll1_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣኽ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1llll11ll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1ll1l1ll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1l1llll1l_opy_ and command.module == self.bstack1l1lllll1l1_opy_:
                        if command.method and not command.method in bstack1l1ll1l1ll1_opy_:
                            bstack1l1ll1l1ll1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1ll1l1ll1_opy_[command.method]:
                            bstack1l1ll1l1ll1_opy_[command.method][command.name] = list()
                        bstack1l1ll1l1ll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1ll1l1ll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1ll111ll1_opy_(
        self,
        f: bstack1ll1ll1lll1_opy_,
        exec: Tuple[bstack1lll11lll1l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l1lll1ll_opy_, bstack1ll1l1lllll_opy_) and method_name != bstack11l1ll1_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫኾ"):
            return
        if bstack1lll111llll_opy_.bstack1lll11l1111_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1lll1l111_opy_):
            return
        if f.bstack1l1ll11l1l1_opy_(method_name, *args):
            bstack1l1lll11ll1_opy_ = False
            desired_capabilities = f.bstack1l1llll111l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1l1llllll_opy_(instance)
                platform_index = f.bstack1lll1ll11l1_opy_(instance, bstack1ll1ll1lll1_opy_.bstack1l1l1lll1l1_opy_, 0)
                bstack1l1lll111ll_opy_ = datetime.now()
                r = self.bstack1l1ll1l111l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll1l11l_opy_(bstack11l1ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤ኿"), datetime.now() - bstack1l1lll111ll_opy_)
                bstack1l1lll11ll1_opy_ = r.success
            else:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡤࡦࡵ࡬ࡶࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡃࠢዀ") + str(desired_capabilities) + bstack11l1ll1_opy_ (u"ࠨࠢ዁"))
            f.bstack1lll1l1111l_opy_(instance, bstack1ll1llll1l1_opy_.bstack1l1lll1l111_opy_, bstack1l1lll11ll1_opy_)
    def bstack1lll1l1lll_opy_(self, test_tags):
        bstack1l1ll1l111l_opy_ = self.config.get(bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧዂ"))
        if not bstack1l1ll1l111l_opy_:
            return True
        try:
            include_tags = bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ዃ")] if bstack11l1ll1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧዄ") in bstack1l1ll1l111l_opy_ and isinstance(bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨዅ")], list) else []
            exclude_tags = bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ዆")] if bstack11l1ll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ዇") in bstack1l1ll1l111l_opy_ and isinstance(bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫወ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢዉ") + str(error))
        return False
    def bstack1lll1lll1_opy_(self, caps):
        try:
            if self.bstack1l1ll1ll1l1_opy_:
                bstack1l1ll1lllll_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢዊ"))
                if bstack1l1ll1lllll_opy_ is not None and str(bstack1l1ll1lllll_opy_).lower() == bstack11l1ll1_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥዋ"):
                    bstack1l1llll1111_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧዌ")) or caps.get(bstack11l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨው"))
                    if bstack1l1llll1111_opy_ is not None and int(bstack1l1llll1111_opy_) < 11:
                        self.logger.warning(bstack11l1ll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠧዎ") + str(bstack1l1llll1111_opy_) + bstack11l1ll1_opy_ (u"ࠨࠢዏ"))
                        return False
                return True
            bstack1l1llllll1l_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨዐ"), {}).get(bstack11l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬዑ"), caps.get(bstack11l1ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩዒ"), bstack11l1ll1_opy_ (u"ࠪࠫዓ")))
            if bstack1l1llllll1l_opy_:
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣዔ"))
                return False
            browser = caps.get(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪዕ"), bstack11l1ll1_opy_ (u"࠭ࠧዖ")).lower()
            if browser != bstack11l1ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ዗"):
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦዘ"))
                return False
            bstack1l1lll1111l_opy_ = bstack1l1lllll111_opy_
            if not self.config.get(bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫዙ")) or self.config.get(bstack11l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧዚ")):
                bstack1l1lll1111l_opy_ = bstack1l1ll1l1lll_opy_
            browser_version = caps.get(bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬዛ"))
            if not browser_version:
                browser_version = caps.get(bstack11l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ዜ"), {}).get(bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧዝ"), bstack11l1ll1_opy_ (u"ࠧࠨዞ"))
            bstack1l1ll1ll11l_opy_ = str(browser_version).lower() if browser_version is not None else bstack11l1ll1_opy_ (u"ࠨࠩዟ")
            if bstack1l1ll1ll11l_opy_:
                if bstack1l1ll1ll11l_opy_.startswith(bstack11l1ll1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩዠ")):
                    if bstack1l1ll1ll11l_opy_.startswith(bstack11l1ll1_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ࠰ࠫዡ")):
                        bstack1l1llll1l1l_opy_ = bstack1l1ll1ll11l_opy_[len(bstack11l1ll1_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬዢ")):]
                        if bstack1l1llll1l1l_opy_ and not bstack1l1llll1l1l_opy_.isdigit():
                            self.logger.warning(bstack11l1ll1_opy_ (u"ࠧࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡨࡲࡶࡲࡧࡴࠡࠩࠥዣ") + str(browser_version) + bstack11l1ll1_opy_ (u"ࠨࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࠬࡲࡡࡵࡧࡶࡸࠬࠦ࡯ࡳࠢࠪࡰࡦࡺࡥࡴࡶ࠰ࡀࡳࡻ࡭ࡣࡧࡵࡂࠬ࠴ࠢዤ"))
                            return False
                else:
                    try:
                        if int(bstack1l1ll1ll11l_opy_.split(bstack11l1ll1_opy_ (u"ࠧ࠯ࠩዥ"))[0]) <= bstack1l1lll1111l_opy_:
                            self.logger.warning(bstack11l1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥዦ") + str(bstack1l1lll1111l_opy_) + bstack11l1ll1_opy_ (u"ࠤ࠱ࠦዧ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack11l1ll1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠨࡽࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࢁࠬࡀࠠࠣየ") + str(e) + bstack11l1ll1_opy_ (u"ࠦࠧዩ"))
            bstack1l1ll111l1l_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ዪ"), {}).get(bstack11l1ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ያ"))
            if not bstack1l1ll111l1l_opy_:
                bstack1l1ll111l1l_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬዬ"), {})
            if bstack1l1ll111l1l_opy_ and bstack11l1ll1_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬይ") in bstack1l1ll111l1l_opy_.get(bstack11l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧዮ"), []):
                self.logger.warning(bstack11l1ll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧዯ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨደ") + str(error))
            return False
    def bstack1l1lll1lll1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1lll11111_opy_ = {
            bstack11l1ll1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬዱ"): test_uuid,
        }
        bstack1l1lll1ll11_opy_ = {}
        if result.success:
            bstack1l1lll1ll11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l1lllll1_opy_(bstack1l1lll11111_opy_, bstack1l1lll1ll11_opy_)
    def bstack1l1ll11l11l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack11l1ll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࠥࠦࠠࠡࠢࠣࡊࡪࡺࡣࡩࠢࡦࡩࡳࡺࡲࡢ࡮ࠣࡥࡺࡺࡨࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡨࡲࡶࠥࡺࡨࡦࠢࡪ࡭ࡻ࡫࡮ࠡࡵࡦࡶ࡮ࡶࡴࠡࡰࡤࡱࡪ࠴ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡦࡥࡨ࡮ࡥࡥࠢࡦࡳࡳ࡬ࡩࡨࠢ࡬ࡪࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡦࡦࡶࡦ࡬ࡪࡪࠬࠡࡱࡷ࡬ࡪࡸࡷࡪࡵࡨࠤࡱࡵࡡࡥࡵࠣࡥࡳࡪࠠࡤࡣࡦ࡬ࡪࡹࠠࡪࡶ࠱ࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇࡲࡨࡵ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫࠺ࠡࡐࡤࡱࡪࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡳࡤࡴ࡬ࡴࡹࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡥࡲࡲ࡫࡯ࡧࠡࡨࡲࡶࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡸࡪࡹࡴࡠࡷࡸ࡭ࡩࡀࠠࡖࡗࡌࡈࠥࡵࡦࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡼ࡮ࡩࡤࡪࠣࡸࡴࠦࡦࡦࡶࡦ࡬ࠥࡩ࡯࡯ࡨ࡬࡫ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡒࡦࡶࡸࡶࡳࡹ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡤࡪࡥࡷ࠾ࠥࡉ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡪࡩࡤࡶ࡬ࡳࡳࡧࡲࡺ࠮ࠣࡩࡲࡶࡴࡺࠢࡧ࡭ࡨࡺࠠࡪࡨࠣࡩࡷࡸ࡯ࡳࠢࡲࡧࡨࡻࡲࡴࠌࠣࠤࠥࠦࠠࠡࠢࠣࠦࠧࠨዲ")
        try:
            if self.bstack1l1ll1l11ll_opy_:
                return self.bstack1l1ll1l11l1_opy_
            self.bstack1l1lll1ll1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l1ll1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢዳ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨዴ"), bstack11l1ll1_opy_ (u"ࠩ࠳ࠫድ")))
            req.client_worker_id = bstack11l1ll1_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤዶ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1llll1ll_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1ll1l11l1_opy_ = self.bstack1l1lll1lll1_opy_(test_uuid, r)
                self.bstack1l1ll1l11ll_opy_ = True
            else:
                self.logger.error(bstack11l1ll1_opy_ (u"ࠦ࡫࡫ࡴࡤࡪࡆࡩࡳࡺࡲࡢ࡮ࡄࡹࡹ࡮ࡁ࠲࠳ࡼࡇࡴࡴࡦࡪࡩ࠽ࠤࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡱࡵࠤࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨዷ") + str(r.error) + bstack11l1ll1_opy_ (u"ࠧࠨዸ"))
                self.bstack1l1ll1l11l1_opy_ = dict()
            return self.bstack1l1ll1l11l1_opy_
        except Exception as e:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣዹ") + str(traceback.format_exc()) + bstack11l1ll1_opy_ (u"ࠢࠣዺ"))
            return dict()
    def bstack11ll1l111_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1lll1llll1_opy_ = None
        try:
            self.bstack1l1lll1ll1l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11l1ll1_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣዻ")
            req.script_name = bstack11l1ll1_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢዼ")
            req.platform_index = str(os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪዽ"), bstack11l1ll1_opy_ (u"ࠫ࠵࠭ዾ")))
            req.client_worker_id = bstack11l1ll1_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦዿ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1llll1ll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤጀ") + str(r.error) + bstack11l1ll1_opy_ (u"ࠢࠣጁ"))
            else:
                bstack1l1lll11111_opy_ = self.bstack1l1lll1lll1_opy_(test_uuid, r)
                bstack1l1lll11l1l_opy_ = r.script
            self.logger.debug(bstack11l1ll1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫጂ") + str(bstack1l1lll11111_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1lll11l1l_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤጃ") + str(framework_name) + bstack11l1ll1_opy_ (u"ࠥࠤࠧጄ"))
                return
            bstack1lll1llll1_opy_ = bstack1ll1111ll_opy_.bstack11l11l1l_opy_(EVENTS.bstack1l1ll1llll1_opy_.value)
            self.bstack1l1lllll11l_opy_(driver, bstack1l1lll11l1l_opy_, bstack1l1lll11111_opy_, framework_name)
            try:
                bstack1l1l1llll11_opy_ = {
                    bstack11l1ll1_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧጅ"): {
                        bstack11l1ll1_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨጆ"): bstack11l1ll1_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥጇ"),
                    },
                    bstack11l1ll1_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤገ"): {
                        bstack11l1ll1_opy_ (u"ࠣࡤࡲࡨࡾࠨጉ"): {
                            bstack11l1ll1_opy_ (u"ࠤࡰࡷ࡬ࠨጊ"): bstack11l1ll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨጋ"),
                            bstack11l1ll1_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧጌ"): True
                        }
                    }
                }
                self.bstack11llll111_opy_.info(json.dumps(bstack1l1l1llll11_opy_, separators=(bstack11l1ll1_opy_ (u"ࠬ࠲ࠧግ"), bstack11l1ll1_opy_ (u"࠭࠺ࠨጎ"))))
            except Exception as bstack11lll11l_opy_:
                self.logger.debug(bstack11l1ll1_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨጏ") + str(bstack11lll11l_opy_) + bstack11l1ll1_opy_ (u"ࠣࠤጐ"))
            self.logger.info(bstack11l1ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ጑"))
            bstack1ll1111ll_opy_.end(EVENTS.bstack1l1ll1llll1_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥጒ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤጓ"), True, None, command=bstack11l1ll1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪጔ"),test_name=name)
        except Exception as bstack1l1ll1lll11_opy_:
            self.logger.error(bstack11l1ll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣጕ") + bstack11l1ll1_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥ጖") + bstack11l1ll1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥ጗") + str(bstack1l1ll1lll11_opy_))
            bstack1ll1111ll_opy_.end(EVENTS.bstack1l1ll1llll1_opy_.value, bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤጘ"), bstack1lll1llll1_opy_+bstack11l1ll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣጙ"), False, bstack1l1ll1lll11_opy_, command=bstack11l1ll1_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩጚ"),test_name=name)
    def bstack1l1lllll11l_opy_(self, driver, bstack1l1lll11l1l_opy_, bstack1l1lll11111_opy_, framework_name):
        if framework_name == bstack11l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩጛ"):
            self.bstack1l1l1lll1ll_opy_.bstack1l1ll1111ll_opy_(driver, bstack1l1lll11l1l_opy_, bstack1l1lll11111_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1lll11l1l_opy_, bstack1l1lll11111_opy_))
    def _1l1lllll1ll_opy_(self, instance: bstack1ll1ll111l1_opy_, args: Tuple) -> list:
        bstack11l1ll1_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥጜ")
        if bstack11l1ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫጝ") in instance.bstack1l1lll1l1ll_opy_:
            return args[2].tags if hasattr(args[2], bstack11l1ll1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ጞ")) else []
        if hasattr(args[0], bstack11l1ll1_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧጟ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1llll1lll_opy_(self, tags, capabilities):
        return self.bstack1lll1l1lll_opy_(tags) and self.bstack1lll1lll1_opy_(capabilities)