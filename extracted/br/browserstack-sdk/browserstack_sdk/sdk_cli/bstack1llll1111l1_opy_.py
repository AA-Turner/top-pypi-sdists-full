# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1llllll1lll_opy_ import (
    bstack1lllll1lll1_opy_,
    bstack1llllll1111_opy_,
    bstack11111111l1_opy_,
    bstack1lllll1ll11_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1lll1lll11l_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll111l_opy_, bstack1lll111111l_opy_, bstack1ll1ll1l1l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11l11l1_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll111l11l_opy_
from browserstack_sdk.sdk_cli.bstack1lll11111l1_opy_ import bstack1llll1l1l11_opy_
from bstack_utils.helper import bstack1ll1l11lll1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l11111_opy_ import bstack1ll1llll11l_opy_
import grpc
import traceback
import json
class bstack1lll1ll1lll_opy_(bstack1llll11l111_opy_):
    bstack1ll11l11l1l_opy_ = False
    bstack1ll1l111ll1_opy_ = bstack1111lll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᅾ")
    bstack1ll11l11ll1_opy_ = bstack1111lll_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᅿ")
    bstack1ll11ll11ll_opy_ = bstack1111lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠧᆀ")
    bstack1ll111lll1l_opy_ = bstack1111lll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡶࡣࡸࡩࡡ࡯ࡰ࡬ࡲ࡬ࠨᆁ")
    bstack1ll1l11l11l_opy_ = bstack1111lll_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳࡡ࡫ࡥࡸࡥࡵࡳ࡮ࠥᆂ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll11l1lll_opy_, bstack1llll1l1l1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll111l1lll_opy_ = False
        self.bstack1ll11l11l11_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11ll111l_opy_ = bstack1llll1l1l1l_opy_
        bstack1lll11l1lll_opy_.bstack1ll11l111l1_opy_((bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll11lll111_opy_)
        TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.PRE), self.bstack1ll1l11l111_opy_)
        TestFramework.bstack1ll11l111l1_opy_((bstack1ll1lll111l_opy_.TEST, bstack1lll111111l_opy_.POST), self.bstack1ll1l11ll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l11l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l111l11_opy_(instance, args)
        test_framework = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll11l1l1l1_opy_)
        if self.bstack1ll111l1lll_opy_:
            self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᆃ")] = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll111lllll_opy_)
        if bstack1111lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᆄ") in instance.bstack1ll11l111ll_opy_:
            platform_index = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll11l1ll11_opy_)
            self.accessibility = self.bstack1ll11ll1lll_opy_(tags, self.config[bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᆅ")][platform_index])
        else:
            capabilities = self.bstack1ll11ll111l_opy_.bstack1ll11llll1l_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1111lll_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᆆ") + str(kwargs) + bstack1111lll_opy_ (u"ࠢࠣᆇ"))
                return
            self.accessibility = self.bstack1ll11ll1lll_opy_(tags, capabilities)
        if self.bstack1ll11ll111l_opy_.pages and self.bstack1ll11ll111l_opy_.pages.values():
            bstack1ll1l11ll1l_opy_ = list(self.bstack1ll11ll111l_opy_.pages.values())
            if bstack1ll1l11ll1l_opy_ and isinstance(bstack1ll1l11ll1l_opy_[0], (list, tuple)) and bstack1ll1l11ll1l_opy_[0]:
                bstack1ll11l1l1ll_opy_ = bstack1ll1l11ll1l_opy_[0][0]
                if callable(bstack1ll11l1l1ll_opy_):
                    page = bstack1ll11l1l1ll_opy_()
                    def bstack11ll11ll1_opy_():
                        self.get_accessibility_results(page, bstack1111lll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᆈ"))
                    def bstack1ll111l11ll_opy_():
                        self.get_accessibility_results_summary(page, bstack1111lll_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᆉ"))
                    setattr(page, bstack1111lll_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡸࠨᆊ"), bstack11ll11ll1_opy_)
                    setattr(page, bstack1111lll_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨᆋ"), bstack1ll111l11ll_opy_)
        self.logger.debug(bstack1111lll_opy_ (u"ࠧࡹࡨࡰࡷ࡯ࡨࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱࡻࡥ࠾ࠤᆌ") + str(self.accessibility) + bstack1111lll_opy_ (u"ࠨࠢᆍ"))
    def bstack1ll11lll111_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack11l1l1ll1l_opy_ = datetime.now()
            self.bstack1ll111l1l1l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᆎ"), datetime.now() - bstack11l1l1ll1l_opy_)
            if (
                not f.bstack1ll11llllll_opy_(method_name)
                or f.bstack1ll11lllll1_opy_(method_name, *args)
                or f.bstack1ll111l11l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllll1l11_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11ll11ll_opy_, False):
                if not bstack1lll1ll1lll_opy_.bstack1ll11l11l1l_opy_:
                    self.logger.warning(bstack1111lll_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦᆏ") + str(f.platform_index) + bstack1111lll_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆐ"))
                    bstack1lll1ll1lll_opy_.bstack1ll11l11l1l_opy_ = True
                return
            bstack1ll1l1111l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l1111l1_opy_:
                platform_index = f.bstack1llllll1l11_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll11l1ll11_opy_, 0)
                self.logger.debug(bstack1111lll_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᆑ") + str(f.framework_name) + bstack1111lll_opy_ (u"ࠦࠧᆒ"))
                return
            command_name = f.bstack1ll11lll11l_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1111lll_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢᆓ") + str(method_name) + bstack1111lll_opy_ (u"ࠨࠢᆔ"))
                return
            bstack1ll11ll1111_opy_ = f.bstack1llllll1l11_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l11l11l_opy_, False)
            if command_name == bstack1111lll_opy_ (u"ࠢࡨࡧࡷࠦᆕ") and not bstack1ll11ll1111_opy_:
                f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll1l11l11l_opy_, True)
                bstack1ll11ll1111_opy_ = True
            if not bstack1ll11ll1111_opy_ and not self.bstack1ll111l1lll_opy_:
                self.logger.debug(bstack1111lll_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᆖ") + str(command_name) + bstack1111lll_opy_ (u"ࠤࠥᆗ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1111lll_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᆘ") + str(command_name) + bstack1111lll_opy_ (u"ࠦࠧᆙ"))
                return
            self.logger.info(bstack1111lll_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᆚ") + str(command_name) + bstack1111lll_opy_ (u"ࠨࠢᆛ"))
            scripts = [(s, bstack1ll1l1111l1_opy_[s]) for s in scripts_to_run if s in bstack1ll1l1111l1_opy_]
            for script_name, bstack1ll1l111l1l_opy_ in scripts:
                try:
                    bstack11l1l1ll1l_opy_ = datetime.now()
                    if script_name == bstack1111lll_opy_ (u"ࠢࡴࡥࡤࡲࠧᆜ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                    instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࠢᆝ") + script_name, datetime.now() - bstack11l1l1ll1l_opy_)
                    if isinstance(result, dict) and not result.get(bstack1111lll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᆞ"), True):
                        self.logger.warning(bstack1111lll_opy_ (u"ࠥࡷࡰ࡯ࡰࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡷ࡫࡭ࡢ࡫ࡱ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࠥᆟ") + str(result) + bstack1111lll_opy_ (u"ࠦࠧᆠ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1111lll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃࠠࡦࡴࡵࡳࡷࡃࠢᆡ") + str(e) + bstack1111lll_opy_ (u"ࠨࠢᆢ"))
        except Exception as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴࡀࠦᆣ") + str(e) + bstack1111lll_opy_ (u"ࠣࠤᆤ"))
    def bstack1ll1l11ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll1l1l1_opy_,
        bstack1llllll11ll_opy_: Tuple[bstack1ll1lll111l_opy_, bstack1lll111111l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l111l11_opy_(instance, args)
        capabilities = self.bstack1ll11ll111l_opy_.bstack1ll11llll1l_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll11ll1lll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᆥ"))
            return
        driver = self.bstack1ll11ll111l_opy_.bstack1ll11l1ll1l_opy_(f, instance, bstack1llllll11ll_opy_, *args, **kwargs)
        test_name = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll1111llll_opy_)
        if not test_name:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᆦ"))
            return
        test_uuid = f.bstack1llllll1l11_opy_(instance, TestFramework.bstack1ll111lllll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᆧ"))
            return
        if isinstance(self.bstack1ll11ll111l_opy_, bstack1lll111l11l_opy_):
            framework_name = bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᆨ")
        else:
            framework_name = bstack1111lll_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᆩ")
        self.bstack1ll1ll1l1l_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11l1l11l_opy_ = bstack1ll1llll11l_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1l1ll1lll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1111lll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࠣᆪ"))
            return
        bstack11l1l1ll1l_opy_ = datetime.now()
        bstack1ll1l111l1l_opy_ = self.scripts.get(framework_name, {}).get(bstack1111lll_opy_ (u"ࠣࡵࡦࡥࡳࠨᆫ"), None)
        if not bstack1ll1l111l1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡩࡡ࡯ࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᆬ") + str(framework_name) + bstack1111lll_opy_ (u"ࠥࠤࠧᆭ"))
            return
        if self.bstack1ll111l1lll_opy_:
            arg = dict()
            arg[bstack1111lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᆮ")] = method if method else bstack1111lll_opy_ (u"ࠧࠨᆯ")
            arg[bstack1111lll_opy_ (u"ࠨࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩࠨᆰ")] = self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᆱ")]
            arg[bstack1111lll_opy_ (u"ࠣࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩࠨᆲ")] = self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᆳ")]
            arg[bstack1111lll_opy_ (u"ࠥࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸࠢᆴ")] = self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠤᆵ")]
            arg[bstack1111lll_opy_ (u"ࠧࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠤᆶ")] = self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠨࡴࡩࡡ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠧᆷ")]
            arg[bstack1111lll_opy_ (u"ࠢࡴࡥࡤࡲ࡙࡯࡭ࡦࡵࡷࡥࡲࡶࠢᆸ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11ll1ll1_opy_ = bstack1ll1l111l1l_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11ll1ll1_opy_)
            return
        instance = bstack11111111l1_opy_.bstack1lllll1111l_opy_(driver)
        if instance:
            if not bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll111lll1l_opy_, False):
                bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll111lll1l_opy_, True)
            else:
                self.logger.info(bstack1111lll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡲࠥࡶࡲࡰࡩࡵࡩࡸࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᆹ") + str(method) + bstack1111lll_opy_ (u"ࠤࠥᆺ"))
                return
        self.logger.info(bstack1111lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᆻ") + str(method) + bstack1111lll_opy_ (u"ࠦࠧᆼ"))
        if framework_name == bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᆽ"):
            result = self.bstack1ll11ll111l_opy_.bstack1ll1l11l1l1_opy_(driver, bstack1ll1l111l1l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l111l1l_opy_, {bstack1111lll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᆾ"): method if method else bstack1111lll_opy_ (u"ࠢࠣᆿ")})
        bstack1ll1llll11l_opy_.end(EVENTS.bstack1l1ll1lll1_opy_.value, bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᇀ"), bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᇁ"), True, None, command=method)
        if instance:
            bstack11111111l1_opy_.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll111lll1l_opy_, False)
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢᇂ"), datetime.now() - bstack11l1l1ll1l_opy_)
        return result
        def bstack1ll11l1l111_opy_(self, driver: object, framework_name, bstack1ll1l11ll1_opy_: str):
            self.bstack1ll1l111lll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll1111lll1_opy_ = self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᇃ")]
            req.bstack1ll1l11ll1_opy_ = bstack1ll1l11ll1_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll1llll11_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1111lll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᇄ") + str(r) + bstack1111lll_opy_ (u"ࠨࠢᇅ"))
                else:
                    bstack1ll111ll1l1_opy_ = json.loads(r.bstack1ll111l1l11_opy_.decode(bstack1111lll_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᇆ")))
                    if bstack1ll1l11ll1_opy_ == bstack1111lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᇇ"):
                        return bstack1ll111ll1l1_opy_.get(bstack1111lll_opy_ (u"ࠤࡧࡥࡹࡧࠢᇈ"), [])
                    else:
                        return bstack1ll111ll1l1_opy_.get(bstack1111lll_opy_ (u"ࠥࡨࡦࡺࡡࠣᇉ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1111lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡰࡱࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡤ࡮࡬࠾ࠥࠨᇊ") + str(e) + bstack1111lll_opy_ (u"ࠧࠨᇋ"))
    @measure(event_name=EVENTS.bstack1ll1l1ll11_opy_, stage=STAGE.bstack11111lll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111lll_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᇌ"))
            return
        if self.bstack1ll111l1lll_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡡࡱࡲࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᇍ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l1l111_opy_(driver, framework_name, bstack1111lll_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᇎ"))
        bstack1ll1l111l1l_opy_ = self.scripts.get(framework_name, {}).get(bstack1111lll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᇏ"), None)
        if not bstack1ll1l111l1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᇐ") + str(framework_name) + bstack1111lll_opy_ (u"ࠦࠧᇑ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11l1l1ll1l_opy_ = datetime.now()
        if framework_name == bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᇒ"):
            result = self.bstack1ll11ll111l_opy_.bstack1ll1l11l1l1_opy_(driver, bstack1ll1l111l1l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l111l1l_opy_)
        instance = bstack11111111l1_opy_.bstack1lllll1111l_opy_(driver)
        if instance:
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࠤᇓ"), datetime.now() - bstack11l1l1ll1l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1lll1l_opy_, stage=STAGE.bstack11111lll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111lll_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᇔ"))
            return
        if self.bstack1ll111l1lll_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l1l111_opy_(driver, framework_name, bstack1111lll_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᇕ"))
        bstack1ll1l111l1l_opy_ = self.scripts.get(framework_name, {}).get(bstack1111lll_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᇖ"), None)
        if not bstack1ll1l111l1l_opy_:
            self.logger.debug(bstack1111lll_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᇗ") + str(framework_name) + bstack1111lll_opy_ (u"ࠦࠧᇘ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11l1l1ll1l_opy_ = datetime.now()
        if framework_name == bstack1111lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᇙ"):
            result = self.bstack1ll11ll111l_opy_.bstack1ll1l11l1l1_opy_(driver, bstack1ll1l111l1l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l111l1l_opy_)
        instance = bstack11111111l1_opy_.bstack1lllll1111l_opy_(driver)
        if instance:
            instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠥᇚ"), datetime.now() - bstack11l1l1ll1l_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll111lll11_opy_, stage=STAGE.bstack11111lll_opy_)
    def bstack1ll11ll11l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l111lll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1llll11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1111lll_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇛ") + str(r) + bstack1111lll_opy_ (u"ࠣࠤᇜ"))
            else:
                self.bstack1ll1l1111ll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111lll_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᇝ") + str(e) + bstack1111lll_opy_ (u"ࠥࠦᇞ"))
            traceback.print_exc()
            raise e
    def bstack1ll1l1111ll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡱࡵࡡࡥࡡࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᇟ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll111l1lll_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᇠ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll11l11l11_opy_[bstack1111lll_opy_ (u"ࠨࡴࡩࡡ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠧᇡ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll11l11l11_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll111l111l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l111ll1_opy_ and command.module == self.bstack1ll11l11ll1_opy_:
                        if command.method and not command.method in bstack1ll111l111l_opy_:
                            bstack1ll111l111l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll111l111l_opy_[command.method]:
                            bstack1ll111l111l_opy_[command.method][command.name] = list()
                        bstack1ll111l111l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll111l111l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll111l1l1l_opy_(
        self,
        f: bstack1lll1lll11l_opy_,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11ll111l_opy_, bstack1lll111l11l_opy_) and method_name != bstack1111lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᇢ"):
            return
        if bstack11111111l1_opy_.bstack1lllll11ll1_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11ll11ll_opy_):
            return
        if f.bstack1ll11ll1l11_opy_(method_name, *args):
            bstack1ll11l1lll1_opy_ = False
            desired_capabilities = f.bstack1ll11ll1l1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11l11111_opy_(instance)
                platform_index = f.bstack1llllll1l11_opy_(instance, bstack1lll1lll11l_opy_.bstack1ll11l1ll11_opy_, 0)
                bstack1ll1l11111l_opy_ = datetime.now()
                r = self.bstack1ll11ll11l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l11ll111_opy_(bstack1111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᇣ"), datetime.now() - bstack1ll1l11111l_opy_)
                bstack1ll11l1lll1_opy_ = r.success
            else:
                self.logger.error(bstack1111lll_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡨࡪࡹࡩࡳࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࡀࠦᇤ") + str(desired_capabilities) + bstack1111lll_opy_ (u"ࠥࠦᇥ"))
            f.bstack1llllll1l1l_opy_(instance, bstack1lll1ll1lll_opy_.bstack1ll11ll11ll_opy_, bstack1ll11l1lll1_opy_)
    def bstack11llll111l_opy_(self, test_tags):
        bstack1ll11ll11l1_opy_ = self.config.get(bstack1111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᇦ"))
        if not bstack1ll11ll11l1_opy_:
            return True
        try:
            include_tags = bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᇧ")] if bstack1111lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᇨ") in bstack1ll11ll11l1_opy_ and isinstance(bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᇩ")], list) else []
            exclude_tags = bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᇪ")] if bstack1111lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᇫ") in bstack1ll11ll11l1_opy_ and isinstance(bstack1ll11ll11l1_opy_[bstack1111lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᇬ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1111lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᇭ") + str(error))
        return False
    def bstack1111111l_opy_(self, caps):
        try:
            if self.bstack1ll111l1lll_opy_:
                bstack1ll111l1111_opy_ = caps.get(bstack1111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᇮ"))
                if bstack1ll111l1111_opy_ is not None and str(bstack1ll111l1111_opy_).lower() == bstack1111lll_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢᇯ"):
                    bstack1ll11lll1ll_opy_ = caps.get(bstack1111lll_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᇰ")) or caps.get(bstack1111lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᇱ"))
                    if bstack1ll11lll1ll_opy_ is not None and int(bstack1ll11lll1ll_opy_) < 11:
                        self.logger.warning(bstack1111lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡄࡲࡩࡸ࡯ࡪࡦࠣ࠵࠶ࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦ࠰ࠣࡇࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠ࠾ࠤᇲ") + str(bstack1ll11lll1ll_opy_) + bstack1111lll_opy_ (u"ࠥࠦᇳ"))
                        return False
                return True
            bstack1ll11l1llll_opy_ = caps.get(bstack1111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᇴ"), {}).get(bstack1111lll_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᇵ"), caps.get(bstack1111lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᇶ"), bstack1111lll_opy_ (u"ࠧࠨᇷ")))
            if bstack1ll11l1llll_opy_:
                self.logger.warning(bstack1111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᇸ"))
                return False
            browser = caps.get(bstack1111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᇹ"), bstack1111lll_opy_ (u"ࠪࠫᇺ")).lower()
            if browser != bstack1111lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᇻ"):
                self.logger.warning(bstack1111lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᇼ"))
                return False
            bstack1ll1l111111_opy_ = bstack1ll111ll11l_opy_
            if not self.config.get(bstack1111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᇽ")) or self.config.get(bstack1111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᇾ")):
                bstack1ll1l111111_opy_ = bstack1ll111l1ll1_opy_
            browser_version = caps.get(bstack1111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᇿ"))
            if not browser_version:
                browser_version = caps.get(bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪሀ"), {}).get(bstack1111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫሁ"), bstack1111lll_opy_ (u"ࠫࠬሂ"))
            if browser_version and browser_version != bstack1111lll_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬሃ") and int(browser_version.split(bstack1111lll_opy_ (u"࠭࠮ࠨሄ"))[0]) <= bstack1ll1l111111_opy_:
                self.logger.warning(bstack1111lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࠤህ") + str(bstack1ll1l111111_opy_) + bstack1111lll_opy_ (u"ࠣ࠰ࠥሆ"))
                return False
            bstack1ll11lll1l1_opy_ = caps.get(bstack1111lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪሇ"), {}).get(bstack1111lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪለ"))
            if not bstack1ll11lll1l1_opy_:
                bstack1ll11lll1l1_opy_ = caps.get(bstack1111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩሉ"), {})
            if bstack1ll11lll1l1_opy_ and bstack1111lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩሊ") in bstack1ll11lll1l1_opy_.get(bstack1111lll_opy_ (u"࠭ࡡࡳࡩࡶࠫላ"), []):
                self.logger.warning(bstack1111lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤሌ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥል") + str(error))
            return False
    def bstack1ll111ll111_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll111ll1ll_opy_ = {
            bstack1111lll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩሎ"): test_uuid,
        }
        bstack1ll11l1111l_opy_ = {}
        if result.success:
            bstack1ll11l1111l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1l11lll1_opy_(bstack1ll111ll1ll_opy_, bstack1ll11l1111l_opy_)
    def bstack1ll1ll1l1l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11l1l11l_opy_ = None
        try:
            self.bstack1ll1l111lll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1111lll_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥሏ")
            req.script_name = bstack1111lll_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤሐ")
            r = self.bstack1lll1llll11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1111lll_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣሑ") + str(r.error) + bstack1111lll_opy_ (u"ࠨࠢሒ"))
            else:
                bstack1ll111ll1ll_opy_ = self.bstack1ll111ll111_opy_(test_uuid, r)
                bstack1ll1l111l1l_opy_ = r.script
            self.logger.debug(bstack1111lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪሓ") + str(bstack1ll111ll1ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l111l1l_opy_:
                self.logger.debug(bstack1111lll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣሔ") + str(framework_name) + bstack1111lll_opy_ (u"ࠤࠣࠦሕ"))
                return
            bstack1ll11l1l11l_opy_ = bstack1ll1llll11l_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1ll11llll11_opy_.value)
            self.bstack1ll1l11l1ll_opy_(driver, bstack1ll1l111l1l_opy_, bstack1ll111ll1ll_opy_, framework_name)
            self.logger.info(bstack1111lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨሖ"))
            bstack1ll1llll11l_opy_.end(EVENTS.bstack1ll11llll11_opy_.value, bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦሗ"), bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥመ"), True, None, command=bstack1111lll_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫሙ"),test_name=name)
        except Exception as bstack1ll11l11lll_opy_:
            self.logger.error(bstack1111lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤሚ") + bstack1111lll_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦማ") + bstack1111lll_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦሜ") + str(bstack1ll11l11lll_opy_))
            bstack1ll1llll11l_opy_.end(EVENTS.bstack1ll11llll11_opy_.value, bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥም"), bstack1ll11l1l11l_opy_+bstack1111lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤሞ"), False, bstack1ll11l11lll_opy_, command=bstack1111lll_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪሟ"),test_name=name)
    def bstack1ll1l11l1ll_opy_(self, driver, bstack1ll1l111l1l_opy_, bstack1ll111ll1ll_opy_, framework_name):
        if framework_name == bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪሠ"):
            self.bstack1ll11ll111l_opy_.bstack1ll1l11l1l1_opy_(driver, bstack1ll1l111l1l_opy_, bstack1ll111ll1ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l111l1l_opy_, bstack1ll111ll1ll_opy_))
    def _1ll1l111l11_opy_(self, instance: bstack1ll1ll1l1l1_opy_, args: Tuple) -> list:
        bstack1111lll_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦሡ")
        if bstack1111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬሢ") in instance.bstack1ll11l111ll_opy_:
            return args[2].tags if hasattr(args[2], bstack1111lll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧሣ")) else []
        if hasattr(args[0], bstack1111lll_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨሤ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll11ll1lll_opy_(self, tags, capabilities):
        return self.bstack11llll111l_opy_(tags) and self.bstack1111111l_opy_(capabilities)