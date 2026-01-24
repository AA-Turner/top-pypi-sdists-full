# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll11ll1l1_opy_ import (
    bstack1lll111lll1_opy_,
    bstack1lll1l1ll1l_opy_,
    bstack1lll1ll1l1l_opy_,
    bstack1lll1l1111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1l1l11_opy_ import bstack1ll1l111l1l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_, bstack1ll111l1lll_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll111l111l_opy_ import bstack1ll1ll111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11l11lll_opy_ import bstack1ll11l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll11llll1l_opy_ import bstack1ll111lll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll11ll1ll1_opy_ import bstack1ll1ll11ll1_opy_
from bstack_utils.helper import bstack1l1lll111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
from bstack_utils import bstack111llll1ll_opy_
import grpc
import traceback
import json
class bstack1ll1ll1l1l1_opy_(bstack1ll1ll111l1_opy_):
    bstack1l1ll111lll_opy_ = False
    bstack1l1lll1l111_opy_ = bstack1l1111_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤሺ")
    bstack1l1ll1l1lll_opy_ = bstack1l1111_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣሻ")
    bstack1l1llll1l11_opy_ = bstack1l1111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦሼ")
    bstack1l1llllll11_opy_ = bstack1l1111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧሽ")
    bstack1l1l1llll1l_opy_ = bstack1l1111_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤሾ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll111l1ll1_opy_, bstack1ll1l1ll1ll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1llll11_opy_ = False
        self.bstack1l1ll1l11l1_opy_ = dict()
        self.bstack11l1lll11_opy_ = bstack111llll1ll_opy_.bstack1l11ll11l_opy_(__name__)
        self.bstack1l1lll11111_opy_ = False
        self.bstack1l1lll1l1l1_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1lll11lll_opy_ = bstack1ll1l1ll1ll_opy_
        bstack1ll111l1ll1_opy_.bstack1l1lll1ll11_opy_((bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_, bstack1lll1l1ll1l_opy_.PRE), self.bstack1l1lllll11l_opy_)
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.PRE), self.bstack1l1llll1l1l_opy_)
        TestFramework.bstack1l1lll1ll11_opy_((bstack1ll1ll111ll_opy_.TEST, bstack1ll1l111111_opy_.POST), self.bstack1l1ll1ll11l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1llll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1ll111111_opy_(instance, args)
        test_framework = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll1ll1l_opy_)
        if self.bstack1l1l1llll11_opy_:
            self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤሿ")] = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
        if bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧቀ") in instance.bstack1l1ll1l1l1l_opy_:
            platform_index = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1ll1l11ll_opy_)
            self.accessibility = self.bstack1l1ll11l111_opy_(tags, self.config[bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧቁ")][platform_index])
        else:
            capabilities = self.bstack1l1lll11lll_opy_.bstack1l1llllllll_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧቂ") + str(kwargs) + bstack1l1111_opy_ (u"ࠨࠢቃ"))
                return
            self.accessibility = self.bstack1l1ll11l111_opy_(tags, capabilities)
        if self.bstack1l1lll11lll_opy_.pages and self.bstack1l1lll11lll_opy_.pages.values():
            bstack1l1llll11ll_opy_ = list(self.bstack1l1lll11lll_opy_.pages.values())
            if bstack1l1llll11ll_opy_ and isinstance(bstack1l1llll11ll_opy_[0], (list, tuple)) and bstack1l1llll11ll_opy_[0]:
                bstack1l1ll11l1l1_opy_ = bstack1l1llll11ll_opy_[0][0]
                if callable(bstack1l1ll11l1l1_opy_):
                    page = bstack1l1ll11l1l1_opy_()
                    def bstack1l11lll11l_opy_():
                        self.get_accessibility_results(page, bstack1l1111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦቄ"))
                    def bstack1l1llll1ll1_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧቅ"))
                    setattr(page, bstack1l1111_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧቆ"), bstack1l11lll11l_opy_)
                    setattr(page, bstack1l1111_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧቇ"), bstack1l1llll1ll1_opy_)
        self.logger.debug(bstack1l1111_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣቈ") + str(self.accessibility) + bstack1l1111_opy_ (u"ࠧࠨ቉"))
    def bstack1l1lllll11l_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        driver: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll1lll11l_opy_ = datetime.now()
            self.bstack1l1l1llllll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤቊ"), datetime.now() - bstack1ll1lll11l_opy_)
            if (
                not f.bstack1l1llll111l_opy_(method_name)
                or f.bstack1l1lll11l1l_opy_(method_name, *args)
                or f.bstack1l1llllll1l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lll1l11lll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1llll1l11_opy_, False):
                if not bstack1ll1ll1l1l1_opy_.bstack1l1ll111lll_opy_:
                    self.logger.warning(bstack1l1111_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥቋ") + str(f.platform_index) + bstack1l1111_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢቌ"))
                    bstack1ll1ll1l1l1_opy_.bstack1l1ll111lll_opy_ = True
                return
            bstack1l1ll11l1ll_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l1ll11l1ll_opy_:
                platform_index = f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_, 0)
                self.logger.debug(bstack1l1111_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢቍ") + str(f.framework_name) + bstack1l1111_opy_ (u"ࠥࠦ቎"))
                return
            command_name = f.bstack1l1ll111ll1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨ቏") + str(method_name) + bstack1l1111_opy_ (u"ࠧࠨቐ"))
                return
            bstack1l1ll1llll1_opy_ = f.bstack1lll1l11lll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l1llll1l_opy_, False)
            if command_name == bstack1l1111_opy_ (u"ࠨࡧࡦࡶࠥቑ") and not bstack1l1ll1llll1_opy_:
                f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1l1llll1l_opy_, True)
                bstack1l1ll1llll1_opy_ = True
            if not bstack1l1ll1llll1_opy_ and not self.bstack1l1l1llll11_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨቒ") + str(command_name) + bstack1l1111_opy_ (u"ࠣࠤቓ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1111_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢቔ") + str(command_name) + bstack1l1111_opy_ (u"ࠥࠦቕ"))
                return
            self.logger.info(bstack1l1111_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨቖ") + str(command_name) + bstack1l1111_opy_ (u"ࠧࠨ቗"))
            scripts = [(s, bstack1l1ll11l1ll_opy_[s]) for s in scripts_to_run if s in bstack1l1ll11l1ll_opy_]
            for script_name, bstack1l1ll1l1ll1_opy_ in scripts:
                try:
                    bstack1ll1lll11l_opy_ = datetime.now()
                    if script_name == bstack1l1111_opy_ (u"ࠨࡳࡤࡣࡱࠦቘ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack111l111lll_opy_ = {
                                bstack1l1111_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣ቙"): {
                                    bstack1l1111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤቚ"): bstack1l1111_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧቛ"),
                                    bstack1l1111_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢቜ"): [
                                        {
                                            bstack1l1111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦቝ"): command_name
                                        }
                                    ]
                                },
                                bstack1l1111_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢ቞"): {
                                    bstack1l1111_opy_ (u"ࠨࡢࡰࡦࡼࠦ቟"): {
                                        bstack1l1111_opy_ (u"ࠢ࡮ࡵࡪࠦበ"): result.get(bstack1l1111_opy_ (u"ࠣ࡯ࡶ࡫ࠧቡ"), bstack1l1111_opy_ (u"ࠤࠥቢ")) if isinstance(result, dict) else bstack1l1111_opy_ (u"ࠥࠦባ"),
                                        bstack1l1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧቤ"): result.get(bstack1l1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨብ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack11l1lll11_opy_.info(json.dumps(bstack111l111lll_opy_, separators=(bstack1l1111_opy_ (u"ࠨࠬࠣቦ"), bstack1l1111_opy_ (u"ࠢ࠻ࠤቧ"))))
                        except Exception as bstack1l1l111111_opy_:
                            self.logger.debug(bstack1l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨቨ") + str(bstack1l1l111111_opy_) + bstack1l1111_opy_ (u"ࠤࠥቩ"))
                    instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤቪ") + script_name, datetime.now() - bstack1ll1lll11l_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧቫ"), True):
                        self.logger.warning(bstack1l1111_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧቬ") + str(result) + bstack1l1111_opy_ (u"ࠨࠢቭ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤቮ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤቯ"))
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨተ") + str(e) + bstack1l1111_opy_ (u"ࠥࠦቱ"))
    def bstack1l1ll1ll11l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll111l1lll_opy_,
        bstack1lll111llll_opy_: Tuple[bstack1ll1ll111ll_opy_, bstack1ll1l111111_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1l1ll111111_opy_(instance, args)
        capabilities = self.bstack1l1lll11lll_opy_.bstack1l1llllllll_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1l1ll11l111_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣቲ"))
            return
        driver = self.bstack1l1lll11lll_opy_.bstack1l1lll11l11_opy_(f, instance, bstack1lll111llll_opy_, *args, **kwargs)
        test_name = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1ll11111l_opy_)
        if not test_name:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡴࡡ࡮ࡧࠥታ"))
            return
        test_uuid = f.bstack1lll1l11lll_opy_(instance, TestFramework.bstack1l1lll111ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡵࡶ࡫ࡧࠦቴ"))
            return
        if isinstance(self.bstack1l1lll11lll_opy_, bstack1ll111lll1l_opy_):
            framework_name = bstack1l1111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫት")
        else:
            framework_name = bstack1l1111_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪቶ")
        self.bstack111ll1ll1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack11l1l1llll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࠥቷ"))
            return
        bstack1ll1lll11l_opy_ = datetime.now()
        bstack1l1ll1l1ll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣቸ"), None)
        if not bstack1l1ll1l1ll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡤࡣࡱࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦቹ") + str(framework_name) + bstack1l1111_opy_ (u"ࠧࠦࠢቺ"))
            return
        if self.bstack1l1l1llll11_opy_:
            arg = dict()
            arg[bstack1l1111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨቻ")] = method if method else bstack1l1111_opy_ (u"ࠢࠣቼ")
            arg[bstack1l1111_opy_ (u"ࠣࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠣች")] = self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤቾ")]
            arg[bstack1l1111_opy_ (u"ࠥࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠣቿ")] = self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠤኀ")]
            arg[bstack1l1111_opy_ (u"ࠧࡧࡵࡵࡪࡋࡩࡦࡪࡥࡳࠤኁ")] = self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠦኂ")]
            arg[bstack1l1111_opy_ (u"ࠢࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠦኃ")] = self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠣࡶ࡫ࡣ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠢኄ")]
            arg[bstack1l1111_opy_ (u"ࠤࡶࡧࡦࡴࡔࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠤኅ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l1ll1ll1ll_opy_ = self.bstack1l1ll1lll1l_opy_(bstack1l1111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣኆ"), self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦኇ")])
            if bstack1l1111_opy_ (u"ࠧࡩࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡗࡳࡰ࡫࡮ࠣኈ") in bstack1l1ll1ll1ll_opy_:
                bstack1l1ll1ll1ll_opy_ = bstack1l1ll1ll1ll_opy_.copy()
                bstack1l1ll1ll1ll_opy_[bstack1l1111_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥ኉")] = bstack1l1ll1ll1ll_opy_.pop(bstack1l1111_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠥኊ"))
            arg = bstack1l1lll111l1_opy_(arg, bstack1l1ll1ll1ll_opy_)
            bstack1l1ll1ll1l1_opy_ = bstack1l1ll1l1ll1_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1ll1ll1l1_opy_)
            return
        instance = bstack1lll1ll1l1l_opy_.bstack1lll11l1lll_opy_(driver)
        if instance:
            if not bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1llllll11_opy_, False):
                bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1llllll11_opy_, True)
            else:
                self.logger.info(bstack1l1111_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡲࠥࡶࡲࡰࡩࡵࡩࡸࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧኋ") + str(method) + bstack1l1111_opy_ (u"ࠤࠥኌ"))
                return
        self.logger.info(bstack1l1111_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣኍ") + str(method) + bstack1l1111_opy_ (u"ࠦࠧ኎"))
        if framework_name == bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩ኏"):
            result = self.bstack1l1lll11lll_opy_.bstack1l1lll1l11l_opy_(driver, bstack1l1ll1l1ll1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1ll1l1ll1_opy_, {bstack1l1111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨነ"): method if method else bstack1l1111_opy_ (u"ࠢࠣኑ")})
        bstack11ll111lll_opy_.end(EVENTS.bstack11l1l1llll_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣኒ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢና"), True, None, command=method)
        if instance:
            bstack1lll1ll1l1l_opy_.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1llllll11_opy_, False)
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢኔ"), datetime.now() - bstack1ll1lll11l_opy_)
        return result
        def bstack1l1ll1lllll_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l1lllllll1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1ll1l1111_opy_ = self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦን")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬኖ"), bstack1l1111_opy_ (u"࠭࠰ࠨኗ")))
            req.client_worker_id = bstack1l1111_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨኘ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1111l1ll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1l1111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥኙ") + str(r) + bstack1l1111_opy_ (u"ࠤࠥኚ"))
                else:
                    bstack1l1llll1111_opy_ = json.loads(r.bstack1ll11111111_opy_.decode(bstack1l1111_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩኛ")))
                    if result_type == bstack1l1111_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨኜ"):
                        return bstack1l1llll1111_opy_.get(bstack1l1111_opy_ (u"ࠧࡪࡡࡵࡣࠥኝ"), [])
                    else:
                        return bstack1l1llll1111_opy_.get(bstack1l1111_opy_ (u"ࠨࡤࡢࡶࡤࠦኞ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1l1111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡳࡴࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࠥ࡬ࡲࡰ࡯ࠣࡧࡱ࡯࠺ࠡࠤኟ") + str(e) + bstack1l1111_opy_ (u"ࠣࠤአ"))
    @measure(event_name=EVENTS.bstack1ll111ll1_opy_, stage=STAGE.bstack1111lll11_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1111_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦኡ"))
            return
        if self.bstack1l1l1llll11_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡤࡴࡵࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ኢ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1ll1lllll_opy_(driver, framework_name, bstack1l1111_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣኣ"))
        bstack1l1ll1l1ll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1111_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤኤ"), None)
        if not bstack1l1ll1l1ll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧእ") + str(framework_name) + bstack1l1111_opy_ (u"ࠢࠣኦ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1lll11l_opy_ = datetime.now()
        if framework_name == bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬኧ"):
            result = self.bstack1l1lll11lll_opy_.bstack1l1lll1l11l_opy_(driver, bstack1l1ll1l1ll1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1ll1l1ll1_opy_)
        instance = bstack1lll1ll1l1l_opy_.bstack1lll11l1lll_opy_(driver)
        if instance:
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧከ"), datetime.now() - bstack1ll1lll11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1llll1ll1l_opy_, stage=STAGE.bstack1111lll11_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨኩ"))
            return
        if self.bstack1l1l1llll11_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1ll1lllll_opy_(driver, framework_name, bstack1l1111_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨኪ"))
        bstack1l1ll1l1ll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1111_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤካ"), None)
        if not bstack1l1ll1l1ll1_opy_:
            self.logger.debug(bstack1l1111_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧኬ") + str(framework_name) + bstack1l1111_opy_ (u"ࠢࠣክ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1lll11l_opy_ = datetime.now()
        if framework_name == bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬኮ"):
            result = self.bstack1l1lll11lll_opy_.bstack1l1lll1l11l_opy_(driver, bstack1l1ll1l1ll1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1ll1l1ll1_opy_)
        instance = bstack1lll1ll1l1l_opy_.bstack1lll11l1lll_opy_(driver)
        if instance:
            instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨኯ"), datetime.now() - bstack1ll1lll11l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1ll1l1l11_opy_, stage=STAGE.bstack1111lll11_opy_)
    def bstack1l1lllll1l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l1lllllll1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1l1111_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤኰ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1111l1ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨ኱") + str(r) + bstack1l1111_opy_ (u"ࠧࠨኲ"))
            else:
                self.bstack1l1ll11l11l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦኳ") + str(e) + bstack1l1111_opy_ (u"ࠢࠣኴ"))
            traceback.print_exc()
            raise e
    def bstack1l1ll11l11l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1111_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣኵ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1llll11_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢ኶")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1ll1l11l1_opy_[bstack1l1111_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤ኷")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1ll1l11l1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1ll1ll111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1lll1l111_opy_ and command.module == self.bstack1l1ll1l1lll_opy_:
                        if command.method and not command.method in bstack1l1ll1ll111_opy_:
                            bstack1l1ll1ll111_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1ll1ll111_opy_[command.method]:
                            bstack1l1ll1ll111_opy_[command.method][command.name] = list()
                        bstack1l1ll1ll111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1ll1ll111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l1l1llllll_opy_(
        self,
        f: bstack1ll1l111l1l_opy_,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1lll11lll_opy_, bstack1ll111lll1l_opy_) and method_name != bstack1l1111_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬኸ"):
            return
        if bstack1lll1ll1l1l_opy_.bstack1lll1l11111_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1llll1l11_opy_):
            return
        if f.bstack1l1lll1lll1_opy_(method_name, *args):
            bstack1l1ll11lll1_opy_ = False
            desired_capabilities = f.bstack1l1lll1l1ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1ll1lll11_opy_(instance)
                platform_index = f.bstack1lll1l11lll_opy_(instance, bstack1ll1l111l1l_opy_.bstack1l1ll1l11ll_opy_, 0)
                bstack1l1ll11ll1l_opy_ = datetime.now()
                r = self.bstack1l1lllll1l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11l1l11ll_opy_(bstack1l1111_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥኹ"), datetime.now() - bstack1l1ll11ll1l_opy_)
                bstack1l1ll11lll1_opy_ = r.success
            else:
                self.logger.error(bstack1l1111_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡥࡧࡶ࡭ࡷ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠽ࠣኺ") + str(desired_capabilities) + bstack1l1111_opy_ (u"ࠢࠣኻ"))
            f.bstack1lll11l1ll1_opy_(instance, bstack1ll1ll1l1l1_opy_.bstack1l1llll1l11_opy_, bstack1l1ll11lll1_opy_)
    def bstack1lllll11ll_opy_(self, test_tags):
        bstack1l1lllll1l1_opy_ = self.config.get(bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨኼ"))
        if not bstack1l1lllll1l1_opy_:
            return True
        try:
            include_tags = bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧኽ")] if bstack1l1111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨኾ") in bstack1l1lllll1l1_opy_ and isinstance(bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ኿")], list) else []
            exclude_tags = bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪዀ")] if bstack1l1111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ዁") in bstack1l1lllll1l1_opy_ and isinstance(bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬዂ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣዃ") + str(error))
        return False
    def bstack111l11111_opy_(self, caps):
        try:
            if self.bstack1l1l1llll11_opy_:
                bstack1l1ll111l11_opy_ = caps.get(bstack1l1111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣዄ"))
                if bstack1l1ll111l11_opy_ is not None and str(bstack1l1ll111l11_opy_).lower() == bstack1l1111_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦዅ"):
                    bstack1l1ll11llll_opy_ = caps.get(bstack1l1111_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ዆")) or caps.get(bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢ዇"))
                    if bstack1l1ll11llll_opy_ is not None and int(bstack1l1ll11llll_opy_) < 11:
                        self.logger.warning(bstack1l1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠ࠲࠳ࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡂࠨወ") + str(bstack1l1ll11llll_opy_) + bstack1l1111_opy_ (u"ࠢࠣዉ"))
                        return False
                return True
            bstack1l1llll1lll_opy_ = caps.get(bstack1l1111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩዊ"), {}).get(bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ዋ"), caps.get(bstack1l1111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪዌ"), bstack1l1111_opy_ (u"ࠫࠬው")))
            if bstack1l1llll1lll_opy_:
                self.logger.warning(bstack1l1111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤዎ"))
                return False
            browser = caps.get(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫዏ"), bstack1l1111_opy_ (u"ࠧࠨዐ")).lower()
            if browser != bstack1l1111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨዑ"):
                self.logger.warning(bstack1l1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧዒ"))
                return False
            bstack1l1lllll1ll_opy_ = bstack1l1llll11l1_opy_
            if not self.config.get(bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬዓ")) or self.config.get(bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨዔ")):
                bstack1l1lllll1ll_opy_ = bstack1l1ll11ll11_opy_
            browser_version = caps.get(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ዕ"))
            if not browser_version:
                browser_version = caps.get(bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧዖ"), {}).get(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ዗"), bstack1l1111_opy_ (u"ࠨࠩዘ"))
            bstack1l1ll111l1l_opy_ = str(browser_version).lower() if browser_version is not None else bstack1l1111_opy_ (u"ࠩࠪዙ")
            if bstack1l1ll111l1l_opy_:
                if bstack1l1ll111l1l_opy_.startswith(bstack1l1111_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪዚ")):
                    if bstack1l1ll111l1l_opy_.startswith(bstack1l1111_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷ࠱ࠬዛ")):
                        bstack1l1l1lllll1_opy_ = bstack1l1ll111l1l_opy_[len(bstack1l1111_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ዜ")):]
                        if bstack1l1l1lllll1_opy_ and not bstack1l1l1lllll1_opy_.isdigit():
                            self.logger.warning(bstack1l1111_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡩࡳࡷࡳࡡࡵࠢࠪࠦዝ") + str(browser_version) + bstack1l1111_opy_ (u"ࠢࠨ࠽ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥ࠭࡬ࡢࡶࡨࡷࡹ࠭ࠠࡰࡴࠣࠫࡱࡧࡴࡦࡵࡷ࠱ࡁࡴࡵ࡮ࡤࡨࡶࡃ࠭࠮ࠣዞ"))
                            return False
                else:
                    try:
                        if int(bstack1l1ll111l1l_opy_.split(bstack1l1111_opy_ (u"ࠨ࠰ࠪዟ"))[0]) <= bstack1l1lllll1ll_opy_:
                            self.logger.warning(bstack1l1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࠦዠ") + str(bstack1l1lllll1ll_opy_) + bstack1l1111_opy_ (u"ࠥ࠲ࠧዡ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1l1111_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠩࡾࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࢂ࠭࠺ࠡࠤዢ") + str(e) + bstack1l1111_opy_ (u"ࠧࠨዣ"))
            bstack1l1ll1111l1_opy_ = caps.get(bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧዤ"), {}).get(bstack1l1111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧዥ"))
            if not bstack1l1ll1111l1_opy_:
                bstack1l1ll1111l1_opy_ = caps.get(bstack1l1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ዦ"), {})
            if bstack1l1ll1111l1_opy_ and bstack1l1111_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ዧ") in bstack1l1ll1111l1_opy_.get(bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨየ"), []):
                self.logger.warning(bstack1l1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨዩ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢዪ") + str(error))
            return False
    def bstack1ll1111111l_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1lll11ll1_opy_ = {
            bstack1l1111_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭ያ"): test_uuid,
        }
        bstack1l1ll1l111l_opy_ = {}
        if result.success:
            bstack1l1ll1l111l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1lll111l1_opy_(bstack1l1lll11ll1_opy_, bstack1l1ll1l111l_opy_)
    def bstack1l1ll1lll1l_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1l1111_opy_ (u"ࠢࠣࠤࠍࠤࠥࠦࠠࠡࠢࠣࠤࡋ࡫ࡴࡤࡪࠣࡧࡪࡴࡴࡳࡣ࡯ࠤࡦࡻࡴࡩࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡩࡳࡷࠦࡴࡩࡧࠣ࡫࡮ࡼࡥ࡯ࠢࡶࡧࡷ࡯ࡰࡵࠢࡱࡥࡲ࡫࠮ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡧࡦࡩࡨࡦࡦࠣࡧࡴࡴࡦࡪࡩࠣ࡭࡫ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡧࡧࡷࡧ࡭࡫ࡤ࠭ࠢࡲࡸ࡭࡫ࡲࡸ࡫ࡶࡩࠥࡲ࡯ࡢࡦࡶࠤࡦࡴࡤࠡࡥࡤࡧ࡭࡫ࡳࠡ࡫ࡷ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡁࡳࡩࡶ࠾ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥ࠻ࠢࡑࡥࡲ࡫ࠠࡰࡨࠣࡸ࡭࡫ࠠࡴࡥࡵ࡭ࡵࡺࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡦࡳࡳ࡬ࡩࡨࠢࡩࡳࡷࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪ࠺ࠡࡗࡘࡍࡉࠦ࡯ࡧࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡽࡨࡪࡥ࡫ࠤࡹࡵࠠࡧࡧࡷࡧ࡭ࠦࡣࡰࡰࡩ࡭࡬ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡓࡧࡷࡹࡷࡴࡳ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡥ࡫ࡦࡸ࠿ࠦࡃࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡤࡪࡥࡷ࡭ࡴࡴࡡࡳࡻ࠯ࠤࡪࡳࡰࡵࡻࠣࡨ࡮ࡩࡴࠡ࡫ࡩࠤࡪࡸࡲࡰࡴࠣࡳࡨࡩࡵࡳࡵࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢዬ")
        try:
            if self.bstack1l1lll11111_opy_:
                return self.bstack1l1lll1l1l1_opy_
            self.bstack1l1lllllll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1111_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣይ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩዮ"), bstack1l1111_opy_ (u"ࠪ࠴ࠬዯ")))
            req.client_worker_id = bstack1l1111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥደ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1111l1ll_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l1lll1l1l1_opy_ = self.bstack1ll1111111l_opy_(test_uuid, r)
                self.bstack1l1lll11111_opy_ = True
            else:
                self.logger.error(bstack1l1111_opy_ (u"ࠧ࡬ࡥࡵࡥ࡫ࡇࡪࡴࡴࡳࡣ࡯ࡅࡺࡺࡨࡂ࠳࠴ࡽࡈࡵ࡮ࡧ࡫ࡪ࠾ࠥࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡲࡶࠥࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢዱ") + str(r.error) + bstack1l1111_opy_ (u"ࠨࠢዲ"))
                self.bstack1l1lll1l1l1_opy_ = dict()
            return self.bstack1l1lll1l1l1_opy_
        except Exception as e:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡧࡧࡷࡧ࡭ࡉࡥ࡯ࡶࡵࡥࡱࡇࡵࡵࡪࡄ࠵࠶ࡿࡃࡰࡰࡩ࡭࡬ࡀࠠࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡪࡪࡺࡣࡩࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡴࡸࠠࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃ࠺ࠡࠤዳ") + str(traceback.format_exc()) + bstack1l1111_opy_ (u"ࠣࠤዴ"))
            return dict()
    def bstack111ll1ll1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1111lll_opy_ = None
        try:
            self.bstack1l1lllllll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1111_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤድ")
            req.script_name = bstack1l1111_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣዶ")
            req.platform_index = str(os.environ.get(bstack1l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫዷ"), bstack1l1111_opy_ (u"ࠬ࠶ࠧዸ")))
            req.client_worker_id = bstack1l1111_opy_ (u"ࠨࡻࡾ࠯ࡾࢁࠧዹ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1111l1ll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥዺ") + str(r.error) + bstack1l1111_opy_ (u"ࠣࠤዻ"))
            else:
                bstack1l1lll11ll1_opy_ = self.bstack1ll1111111l_opy_(test_uuid, r)
                bstack1l1ll1l1ll1_opy_ = r.script
            self.logger.debug(bstack1l1111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬዼ") + str(bstack1l1lll11ll1_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1ll1l1ll1_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥዽ") + str(framework_name) + bstack1l1111_opy_ (u"ࠦࠥࠨዾ"))
                return
            bstack1ll1111lll_opy_ = bstack11ll111lll_opy_.bstack111llllll_opy_(EVENTS.bstack1l1lllll111_opy_.value)
            self.bstack1l1lll1111l_opy_(driver, bstack1l1ll1l1ll1_opy_, bstack1l1lll11ll1_opy_, framework_name)
            try:
                bstack1l1lll1llll_opy_ = {
                    bstack1l1111_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨዿ"): {
                        bstack1l1111_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢጀ"): bstack1l1111_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡁࡗࡇࡢࡖࡊ࡙ࡕࡍࡖࡖࠦጁ"),
                    },
                    bstack1l1111_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥጂ"): {
                        bstack1l1111_opy_ (u"ࠤࡥࡳࡩࡿࠢጃ"): {
                            bstack1l1111_opy_ (u"ࠥࡱࡸ࡭ࠢጄ"): bstack1l1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢጅ"),
                            bstack1l1111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨጆ"): True
                        }
                    }
                }
                self.bstack11l1lll11_opy_.info(json.dumps(bstack1l1lll1llll_opy_, separators=(bstack1l1111_opy_ (u"࠭ࠬࠨጇ"), bstack1l1111_opy_ (u"ࠧ࠻ࠩገ"))))
            except Exception as bstack1l1l111111_opy_:
                self.logger.debug(bstack1l1111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡤࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹࠠࡥࡣࡷࡥ࠿ࠦࠢጉ") + str(bstack1l1l111111_opy_) + bstack1l1111_opy_ (u"ࠤࠥጊ"))
            self.logger.info(bstack1l1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨጋ"))
            bstack11ll111lll_opy_.end(EVENTS.bstack1l1lllll111_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦጌ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥግ"), True, None, command=bstack1l1111_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫጎ"),test_name=name)
        except Exception as bstack1l1ll1111ll_opy_:
            self.logger.error(bstack1l1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤጏ") + bstack1l1111_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦጐ") + bstack1l1111_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦ጑") + str(bstack1l1ll1111ll_opy_))
            bstack11ll111lll_opy_.end(EVENTS.bstack1l1lllll111_opy_.value, bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥጒ"), bstack1ll1111lll_opy_+bstack1l1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤጓ"), False, bstack1l1ll1111ll_opy_, command=bstack1l1111_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪጔ"),test_name=name)
    def bstack1l1lll1111l_opy_(self, driver, bstack1l1ll1l1ll1_opy_, bstack1l1lll11ll1_opy_, framework_name):
        if framework_name == bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪጕ"):
            self.bstack1l1lll11lll_opy_.bstack1l1lll1l11l_opy_(driver, bstack1l1ll1l1ll1_opy_, bstack1l1lll11ll1_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1ll1l1ll1_opy_, bstack1l1lll11ll1_opy_))
    def _1l1ll111111_opy_(self, instance: bstack1ll111l1lll_opy_, args: Tuple) -> list:
        bstack1l1111_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦ጖")
        if bstack1l1111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬ጗") in instance.bstack1l1ll1l1l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack1l1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧጘ")) else []
        if hasattr(args[0], bstack1l1111_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨጙ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l1ll11l111_opy_(self, tags, capabilities):
        return self.bstack1lllll11ll_opy_(tags) and self.bstack111l11111_opy_(capabilities)