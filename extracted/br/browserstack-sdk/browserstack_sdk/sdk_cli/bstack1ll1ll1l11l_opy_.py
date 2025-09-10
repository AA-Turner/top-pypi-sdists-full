# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllll1l1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll111ll_opy_,
    bstack1llllll1111_opy_,
    bstack1llll1ll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1ll111l_opy_ import bstack1ll1l1ll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_, bstack1lll11ll1l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11ll111_opy_ import bstack1ll1l1l11l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1lll1111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1l111_opy_ import bstack1lll1l1111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lll1111_opy_ import bstack1lll1lll111_opy_
from bstack_utils.helper import bstack1ll1111ll11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1ll11l1l_opy_ import bstack1ll1ll11ll1_opy_
import grpc
import traceback
import json
class bstack1ll1ll11lll_opy_(bstack1ll1l1l11l1_opy_):
    bstack1ll11l11l11_opy_ = False
    bstack1ll1l111111_opy_ = bstack1ll11ll_opy_ (u"ࠤࡶࡩࡱ࡫࡮ࡪࡷࡰ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᆂ")
    bstack1ll111l1ll1_opy_ = bstack1ll11ll_opy_ (u"ࠥࡶࡪࡳ࡯ࡵࡧ࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᆃ")
    bstack1ll1l111l1l_opy_ = bstack1ll11ll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡴࡩࡵࠤᆄ")
    bstack1ll11l1ll11_opy_ = bstack1ll11ll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯ࡳࡠࡵࡦࡥࡳࡴࡩ࡯ࡩࠥᆅ")
    bstack1ll1l11111l_opy_ = bstack1ll11ll_opy_ (u"ࠨࡤࡳ࡫ࡹࡩࡷࡥࡨࡢࡵࡢࡹࡷࡲࠢᆆ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1lll1l1l_opy_, bstack1ll1ll1l1l1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll111l1l11_opy_ = False
        self.bstack1ll111ll111_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11lll1l1_opy_ = bstack1ll1ll1l1l1_opy_
        bstack1ll1lll1l1l_opy_.bstack1ll111l11ll_opy_((bstack1lllll1l111_opy_.bstack1llllllllll_opy_, bstack1lllll111ll_opy_.PRE), self.bstack1ll1l111lll_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.PRE), self.bstack1ll11ll1l11_opy_)
        TestFramework.bstack1ll111l11ll_opy_((bstack1lll1l1ll11_opy_.TEST, bstack1ll1lllll11_opy_.POST), self.bstack1ll1l1111ll_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll1l11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11l111ll_opy_(instance, args)
        test_framework = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11ll111l_opy_)
        if self.bstack1ll111l1l11_opy_:
            self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᆇ")] = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
        if bstack1ll11ll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᆈ") in instance.bstack1ll1l111l11_opy_:
            platform_index = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll1111lll1_opy_)
            self.accessibility = self.bstack1ll11l1lll1_opy_(tags, self.config[bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᆉ")][platform_index])
        else:
            capabilities = self.bstack1ll11lll1l1_opy_.bstack1ll1l111ll1_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᆊ") + str(kwargs) + bstack1ll11ll_opy_ (u"ࠦࠧᆋ"))
                return
            self.accessibility = self.bstack1ll11l1lll1_opy_(tags, capabilities)
        if self.bstack1ll11lll1l1_opy_.pages and self.bstack1ll11lll1l1_opy_.pages.values():
            bstack1ll1l11l111_opy_ = list(self.bstack1ll11lll1l1_opy_.pages.values())
            if bstack1ll1l11l111_opy_ and isinstance(bstack1ll1l11l111_opy_[0], (list, tuple)) and bstack1ll1l11l111_opy_[0]:
                bstack1ll11l1l111_opy_ = bstack1ll1l11l111_opy_[0][0]
                if callable(bstack1ll11l1l111_opy_):
                    page = bstack1ll11l1l111_opy_()
                    def bstack1l11l111_opy_():
                        self.get_accessibility_results(page, bstack1ll11ll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᆌ"))
                    def bstack1ll111l11l1_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll11ll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᆍ"))
                    setattr(page, bstack1ll11ll_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡵࠥᆎ"), bstack1l11l111_opy_)
                    setattr(page, bstack1ll11ll_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥᆏ"), bstack1ll111l11l1_opy_)
        self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡶ࡬ࡴࡻ࡬ࡥࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮ࡸࡩࡂࠨᆐ") + str(self.accessibility) + bstack1ll11ll_opy_ (u"ࠥࠦᆑ"))
    def bstack1ll1l111lll_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        bstack1llll1ll1l1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll111ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll111l11_opy_ = datetime.now()
            self.bstack1ll11l11l1l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᆒ"), datetime.now() - bstack1ll111l11_opy_)
            if (
                not f.bstack1ll11ll1l1l_opy_(method_name)
                or f.bstack1ll11l1l1l1_opy_(method_name, *args)
                or f.bstack1ll1111l1ll_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llll1lllll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll1l111l1l_opy_, False):
                if not bstack1ll1ll11lll_opy_.bstack1ll11l11l11_opy_:
                    self.logger.warning(bstack1ll11ll_opy_ (u"ࠧࡡࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣᆓ") + str(f.platform_index) + bstack1ll11ll_opy_ (u"ࠨ࡝ࠡࡣ࠴࠵ࡾࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡮ࡡࡷࡧࠣࡲࡴࡺࠠࡣࡧࡨࡲࠥࡹࡥࡵࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᆔ"))
                    bstack1ll1ll11lll_opy_.bstack1ll11l11l11_opy_ = True
                return
            bstack1ll11l1l11l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11l1l11l_opy_:
                platform_index = f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_, 0)
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᆕ") + str(f.framework_name) + bstack1ll11ll_opy_ (u"ࠣࠤᆖ"))
                return
            command_name = f.bstack1ll111ll1l1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࠦᆗ") + str(method_name) + bstack1ll11ll_opy_ (u"ࠥࠦᆘ"))
                return
            bstack1ll11l1l1ll_opy_ = f.bstack1llll1lllll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll1l11111l_opy_, False)
            if command_name == bstack1ll11ll_opy_ (u"ࠦ࡬࡫ࡴࠣᆙ") and not bstack1ll11l1l1ll_opy_:
                f.bstack1llll1l1lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll1l11111l_opy_, True)
                bstack1ll11l1l1ll_opy_ = True
            if not bstack1ll11l1l1ll_opy_ and not self.bstack1ll111l1l11_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡴ࡯ࠡࡗࡕࡐࠥࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᆚ") + str(command_name) + bstack1ll11ll_opy_ (u"ࠨࠢᆛ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᆜ") + str(command_name) + bstack1ll11ll_opy_ (u"ࠣࠤᆝ"))
                return
            self.logger.info(bstack1ll11ll_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡵࡦࡶ࡮ࡶࡴࡴࡡࡷࡳࡤࡸࡵ࡯ࠫࢀࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᆞ") + str(command_name) + bstack1ll11ll_opy_ (u"ࠥࠦᆟ"))
            scripts = [(s, bstack1ll11l1l11l_opy_[s]) for s in scripts_to_run if s in bstack1ll11l1l11l_opy_]
            for script_name, bstack1ll11ll1ll1_opy_ in scripts:
                try:
                    bstack1ll111l11_opy_ = datetime.now()
                    if script_name == bstack1ll11ll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᆠ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                    instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦᆡ") + script_name, datetime.now() - bstack1ll111l11_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll11ll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᆢ"), True):
                        self.logger.warning(bstack1ll11ll_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢᆣ") + str(result) + bstack1ll11ll_opy_ (u"ࠣࠤᆤ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll11ll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦᆥ") + str(e) + bstack1ll11ll_opy_ (u"ࠥࠦᆦ"))
        except Exception as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣᆧ") + str(e) + bstack1ll11ll_opy_ (u"ࠧࠨᆨ"))
    def bstack1ll1l1111ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11ll1l1_opy_,
        bstack1llll1ll1l1_opy_: Tuple[bstack1lll1l1ll11_opy_, bstack1ll1lllll11_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11l111ll_opy_(instance, args)
        capabilities = self.bstack1ll11lll1l1_opy_.bstack1ll1l111ll1_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll11l1lll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᆩ"))
            return
        driver = self.bstack1ll11lll1l1_opy_.bstack1ll1111l1l1_opy_(f, instance, bstack1llll1ll1l1_opy_, *args, **kwargs)
        test_name = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11l111l1_opy_)
        if not test_name:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᆪ"))
            return
        test_uuid = f.bstack1llll1lllll_opy_(instance, TestFramework.bstack1ll11l1111l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᆫ"))
            return
        if isinstance(self.bstack1ll11lll1l1_opy_, bstack1lll1l1111l_opy_):
            framework_name = bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᆬ")
        else:
            framework_name = bstack1ll11ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᆭ")
        self.bstack1l11ll1l11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack11ll111l11_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᆮ"))
            return
        bstack1ll111l11_opy_ = datetime.now()
        bstack1ll11ll1ll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll11ll_opy_ (u"ࠧࡹࡣࡢࡰࠥᆯ"), None)
        if not bstack1ll11ll1ll1_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᆰ") + str(framework_name) + bstack1ll11ll_opy_ (u"ࠢࠡࠤᆱ"))
            return
        if self.bstack1ll111l1l11_opy_:
            arg = dict()
            arg[bstack1ll11ll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᆲ")] = method if method else bstack1ll11ll_opy_ (u"ࠤࠥᆳ")
            arg[bstack1ll11ll_opy_ (u"ࠥࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠥᆴ")] = self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᆵ")]
            arg[bstack1ll11ll_opy_ (u"ࠧࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠥᆶ")] = self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᆷ")]
            arg[bstack1ll11ll_opy_ (u"ࠢࡢࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᆸ")] = self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳࠨᆹ")]
            arg[bstack1ll11ll_opy_ (u"ࠤࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳࠨᆺ")] = self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᆻ")]
            arg[bstack1ll11ll_opy_ (u"ࠦࡸࡩࡡ࡯ࡖ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠦᆼ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11lllll1_opy_ = bstack1ll11ll1ll1_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11lllll1_opy_)
            return
        instance = bstack1llllll1111_opy_.bstack1llllllll11_opy_(driver)
        if instance:
            if not bstack1llllll1111_opy_.bstack1llll1lllll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll11l1ll11_opy_, False):
                bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll11l1ll11_opy_, True)
            else:
                self.logger.info(bstack1ll11ll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࡬ࡳࡧࡤࡨࡾࠦࡩ࡯ࠢࡳࡶࡴ࡭ࡲࡦࡵࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᆽ") + str(method) + bstack1ll11ll_opy_ (u"ࠨࠢᆾ"))
                return
        self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᆿ") + str(method) + bstack1ll11ll_opy_ (u"ࠣࠤᇀ"))
        if framework_name == bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᇁ"):
            result = self.bstack1ll11lll1l1_opy_.bstack1ll111l111l_opy_(driver, bstack1ll11ll1ll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1ll1_opy_, {bstack1ll11ll_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᇂ"): method if method else bstack1ll11ll_opy_ (u"ࠦࠧᇃ")})
        bstack1ll1ll11ll1_opy_.end(EVENTS.bstack11ll111l11_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᇄ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᇅ"), True, None, command=method)
        if instance:
            bstack1llllll1111_opy_.bstack1llll1l1lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll11l1ll11_opy_, False)
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱࠦᇆ"), datetime.now() - bstack1ll111l11_opy_)
        return result
        def bstack1ll11l1ll1l_opy_(self, driver: object, framework_name, bstack111l1l1ll_opy_: str):
            self.bstack1ll11l11lll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll11lll1ll_opy_ = self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣᇇ")]
            req.bstack111l1l1ll_opy_ = bstack111l1l1ll_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1ll1llllll1_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᇈ") + str(r) + bstack1ll11ll_opy_ (u"ࠥࠦᇉ"))
                else:
                    bstack1ll111l1l1l_opy_ = json.loads(r.bstack1ll11llll1l_opy_.decode(bstack1ll11ll_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᇊ")))
                    if bstack111l1l1ll_opy_ == bstack1ll11ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᇋ"):
                        return bstack1ll111l1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠨࡤࡢࡶࡤࠦᇌ"), [])
                    else:
                        return bstack1ll111l1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠢࡥࡣࡷࡥࠧᇍ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᇎ") + str(e) + bstack1ll11ll_opy_ (u"ࠤࠥᇏ"))
    @measure(event_name=EVENTS.bstack1l11lll11_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᇐ"))
            return
        if self.bstack1ll111l1l11_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡥࡵࡶࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᇑ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l1ll1l_opy_(driver, framework_name, bstack1ll11ll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᇒ"))
        bstack1ll11ll1ll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll11ll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᇓ"), None)
        if not bstack1ll11ll1ll1_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᇔ") + str(framework_name) + bstack1ll11ll_opy_ (u"ࠣࠤᇕ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll111l11_opy_ = datetime.now()
        if framework_name == bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᇖ"):
            result = self.bstack1ll11lll1l1_opy_.bstack1ll111l111l_opy_(driver, bstack1ll11ll1ll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1ll1_opy_)
        instance = bstack1llllll1111_opy_.bstack1llllllll11_opy_(driver)
        if instance:
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᇗ"), datetime.now() - bstack1ll111l11_opy_)
        return result
    @measure(event_name=EVENTS.bstack11111ll1_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᇘ"))
            return
        if self.bstack1ll111l1l11_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l1ll1l_opy_(driver, framework_name, bstack1ll11ll_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᇙ"))
        bstack1ll11ll1ll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll11ll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᇚ"), None)
        if not bstack1ll11ll1ll1_opy_:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᇛ") + str(framework_name) + bstack1ll11ll_opy_ (u"ࠣࠤᇜ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll111l11_opy_ = datetime.now()
        if framework_name == bstack1ll11ll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᇝ"):
            result = self.bstack1ll11lll1l1_opy_.bstack1ll111l111l_opy_(driver, bstack1ll11ll1ll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1ll1_opy_)
        instance = bstack1llllll1111_opy_.bstack1llllllll11_opy_(driver)
        if instance:
            instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᇞ"), datetime.now() - bstack1ll111l11_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll111ll11l_opy_, stage=STAGE.bstack11lll1ll1l_opy_)
    def bstack1ll111llll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11l11lll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1ll1llllll1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᇟ") + str(r) + bstack1ll11ll_opy_ (u"ࠧࠨᇠ"))
            else:
                self.bstack1ll1111l11l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠨࡲࡱࡥ࠰ࡩࡷࡸ࡯ࡳ࠼ࠣࠦᇡ") + str(e) + bstack1ll11ll_opy_ (u"ࠢࠣᇢ"))
            traceback.print_exc()
            raise e
    def bstack1ll1111l11l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣ࡮ࡲࡥࡩࡥࡣࡰࡰࡩ࡭࡬ࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡩࡳࡺࡴࡤࠣᇣ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll111l1l11_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᇤ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll111ll111_opy_[bstack1ll11ll_opy_ (u"ࠥࡸ࡭ࡥࡪࡸࡶࡢࡸࡴࡱࡥ࡯ࠤᇥ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll111ll111_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll111lll1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l111111_opy_ and command.module == self.bstack1ll111l1ll1_opy_:
                        if command.method and not command.method in bstack1ll111lll1l_opy_:
                            bstack1ll111lll1l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll111lll1l_opy_[command.method]:
                            bstack1ll111lll1l_opy_[command.method][command.name] = list()
                        bstack1ll111lll1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll111lll1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll11l11l1l_opy_(
        self,
        f: bstack1ll1l1ll111_opy_,
        exec: Tuple[bstack1llll1ll111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11lll1l1_opy_, bstack1lll1l1111l_opy_) and method_name != bstack1ll11ll_opy_ (u"ࠫࡨࡵ࡮࡯ࡧࡦࡸࠬᇦ"):
            return
        if bstack1llllll1111_opy_.bstack1llllll1lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll1l111l1l_opy_):
            return
        if f.bstack1ll111lll11_opy_(method_name, *args):
            bstack1ll111l1lll_opy_ = False
            desired_capabilities = f.bstack1ll11ll11ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11ll1111_opy_(instance)
                platform_index = f.bstack1llll1lllll_opy_(instance, bstack1ll1l1ll111_opy_.bstack1ll1111lll1_opy_, 0)
                bstack1ll11l11ll1_opy_ = datetime.now()
                r = self.bstack1ll111llll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1lll1111l1_opy_(bstack1ll11ll_opy_ (u"ࠧ࡭ࡲࡱࡥ࠽ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᇧ"), datetime.now() - bstack1ll11l11ll1_opy_)
                bstack1ll111l1lll_opy_ = r.success
            else:
                self.logger.error(bstack1ll11ll_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡥࡧࡶ࡭ࡷ࡫ࡤࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠽ࠣᇨ") + str(desired_capabilities) + bstack1ll11ll_opy_ (u"ࠢࠣᇩ"))
            f.bstack1llll1l1lll_opy_(instance, bstack1ll1ll11lll_opy_.bstack1ll1l111l1l_opy_, bstack1ll111l1lll_opy_)
    def bstack1l1l1l11ll_opy_(self, test_tags):
        bstack1ll111llll1_opy_ = self.config.get(bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᇪ"))
        if not bstack1ll111llll1_opy_:
            return True
        try:
            include_tags = bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᇫ")] if bstack1ll11ll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᇬ") in bstack1ll111llll1_opy_ and isinstance(bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᇭ")], list) else []
            exclude_tags = bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᇮ")] if bstack1ll11ll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᇯ") in bstack1ll111llll1_opy_ and isinstance(bstack1ll111llll1_opy_[bstack1ll11ll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᇰ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᇱ") + str(error))
        return False
    def bstack11ll1l1l1_opy_(self, caps):
        try:
            if self.bstack1ll111l1l11_opy_:
                bstack1ll11llllll_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᇲ"))
                if bstack1ll11llllll_opy_ is not None and str(bstack1ll11llllll_opy_).lower() == bstack1ll11ll_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᇳ"):
                    bstack1ll11ll11l1_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᇴ")) or caps.get(bstack1ll11ll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᇵ"))
                    if bstack1ll11ll11l1_opy_ is not None and int(bstack1ll11ll11l1_opy_) < 11:
                        self.logger.warning(bstack1ll11ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡁ࡯ࡦࡵࡳ࡮ࡪࠠ࠲࠳ࠣࡥࡳࡪࠠࡢࡤࡲࡺࡪ࠴ࠠࡄࡷࡵࡶࡪࡴࡴࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡂࠨᇶ") + str(bstack1ll11ll11l1_opy_) + bstack1ll11ll_opy_ (u"ࠢࠣᇷ"))
                        return False
                return True
            bstack1ll1l1111l1_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᇸ"), {}).get(bstack1ll11ll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᇹ"), caps.get(bstack1ll11ll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᇺ"), bstack1ll11ll_opy_ (u"ࠫࠬᇻ")))
            if bstack1ll1l1111l1_opy_:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᇼ"))
                return False
            browser = caps.get(bstack1ll11ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᇽ"), bstack1ll11ll_opy_ (u"ࠧࠨᇾ")).lower()
            if browser != bstack1ll11ll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᇿ"):
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧሀ"))
                return False
            bstack1ll11lll11l_opy_ = bstack1ll11l11111_opy_
            if not self.config.get(bstack1ll11ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬሁ")) or self.config.get(bstack1ll11ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨሂ")):
                bstack1ll11lll11l_opy_ = bstack1ll11l1llll_opy_
            browser_version = caps.get(bstack1ll11ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ሃ"))
            if not browser_version:
                browser_version = caps.get(bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧሄ"), {}).get(bstack1ll11ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨህ"), bstack1ll11ll_opy_ (u"ࠨࠩሆ"))
            if browser_version and browser_version != bstack1ll11ll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩሇ") and int(browser_version.split(bstack1ll11ll_opy_ (u"ࠪ࠲ࠬለ"))[0]) <= bstack1ll11lll11l_opy_:
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࠨሉ") + str(bstack1ll11lll11l_opy_) + bstack1ll11ll_opy_ (u"ࠧ࠴ࠢሊ"))
                return False
            bstack1ll11lll111_opy_ = caps.get(bstack1ll11ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧላ"), {}).get(bstack1ll11ll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧሌ"))
            if not bstack1ll11lll111_opy_:
                bstack1ll11lll111_opy_ = caps.get(bstack1ll11ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ል"), {})
            if bstack1ll11lll111_opy_ and bstack1ll11ll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ሎ") in bstack1ll11lll111_opy_.get(bstack1ll11ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨሏ"), []):
                self.logger.warning(bstack1ll11ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨሐ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢሑ") + str(error))
            return False
    def bstack1ll1111l111_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1111llll_opy_ = {
            bstack1ll11ll_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭ሒ"): test_uuid,
        }
        bstack1ll11llll11_opy_ = {}
        if result.success:
            bstack1ll11llll11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1111ll11_opy_(bstack1ll1111llll_opy_, bstack1ll11llll11_opy_)
    def bstack1l11ll1l11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll111ll1ll_opy_ = None
        try:
            self.bstack1ll11l11lll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll11ll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢሓ")
            req.script_name = bstack1ll11ll_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨሔ")
            r = self.bstack1ll1llllll1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤࡩࡸࡩࡷࡧࡵࠤࡪࡾࡥࡤࡷࡷࡩࠥࡶࡡࡳࡣࡰࡷࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧሕ") + str(r.error) + bstack1ll11ll_opy_ (u"ࠥࠦሖ"))
            else:
                bstack1ll1111llll_opy_ = self.bstack1ll1111l111_opy_(test_uuid, r)
                bstack1ll11ll1ll1_opy_ = r.script
            self.logger.debug(bstack1ll11ll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧሗ") + str(bstack1ll1111llll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11ll1ll1_opy_:
                self.logger.debug(bstack1ll11ll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧመ") + str(framework_name) + bstack1ll11ll_opy_ (u"ࠨࠠࠣሙ"))
                return
            bstack1ll111ll1ll_opy_ = bstack1ll1ll11ll1_opy_.bstack1ll111l1111_opy_(EVENTS.bstack1ll111lllll_opy_.value)
            self.bstack1ll1111ll1l_opy_(driver, bstack1ll11ll1ll1_opy_, bstack1ll1111llll_opy_, framework_name)
            self.logger.info(bstack1ll11ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥሚ"))
            bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1ll111lllll_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣማ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሜ"), True, None, command=bstack1ll11ll_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨም"),test_name=name)
        except Exception as bstack1ll11ll1lll_opy_:
            self.logger.error(bstack1ll11ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨሞ") + bstack1ll11ll_opy_ (u"ࠧࡹࡴࡳࠪࡳࡥࡹ࡮ࠩࠣሟ") + bstack1ll11ll_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣሠ") + str(bstack1ll11ll1lll_opy_))
            bstack1ll1ll11ll1_opy_.end(EVENTS.bstack1ll111lllll_opy_.value, bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢሡ"), bstack1ll111ll1ll_opy_+bstack1ll11ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨሢ"), False, bstack1ll11ll1lll_opy_, command=bstack1ll11ll_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧሣ"),test_name=name)
    def bstack1ll1111ll1l_opy_(self, driver, bstack1ll11ll1ll1_opy_, bstack1ll1111llll_opy_, framework_name):
        if framework_name == bstack1ll11ll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧሤ"):
            self.bstack1ll11lll1l1_opy_.bstack1ll111l111l_opy_(driver, bstack1ll11ll1ll1_opy_, bstack1ll1111llll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11ll1ll1_opy_, bstack1ll1111llll_opy_))
    def _1ll11l111ll_opy_(self, instance: bstack1lll11ll1l1_opy_, args: Tuple) -> list:
        bstack1ll11ll_opy_ (u"ࠦࠧࠨࡅࡹࡶࡵࡥࡨࡺࠠࡵࡣࡪࡷࠥࡨࡡࡴࡧࡧࠤࡴࡴࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯࠳ࠨࠢࠣሥ")
        if bstack1ll11ll_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩሦ") in instance.bstack1ll1l111l11_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll11ll_opy_ (u"࠭ࡴࡢࡩࡶࠫሧ")) else []
        if hasattr(args[0], bstack1ll11ll_opy_ (u"ࠧࡰࡹࡱࡣࡲࡧࡲ࡬ࡧࡵࡷࠬረ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll11l1lll1_opy_(self, tags, capabilities):
        return self.bstack1l1l1l11ll_opy_(tags) and self.bstack11ll1l1l1_opy_(capabilities)