# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack11l11l_opy_ = 2048
bstack1ll11l1_opy_ = 7
def bstack1l11ll1_opy_ (bstack1l1llll_opy_):
    global bstack1111ll1_opy_
    bstack1llll11_opy_ = ord (bstack1l1llll_opy_ [-1])
    bstack111ll_opy_ = bstack1l1llll_opy_ [:-1]
    bstack11l_opy_ = bstack1llll11_opy_ % len (bstack111ll_opy_)
    bstack1111111_opy_ = bstack111ll_opy_ [:bstack11l_opy_] + bstack111ll_opy_ [bstack11l_opy_:]
    if bstack1lll_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack11l11l_opy_ - (bstack1lll1_opy_ + bstack1llll11_opy_) % bstack1ll11l1_opy_) for bstack1lll1_opy_, char in enumerate (bstack1111111_opy_)])
    return eval (bstack1l1l1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllllll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1llll1l11ll_opy_,
    bstack1llllllll1l_opy_,
    bstack1lllllll111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l1l1l1_opy_ import bstack1ll1l1l1lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_, bstack1lll11l1111_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll111lll1_opy_ import bstack1ll1l1llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l11_opy_ import bstack1llll11111l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1l1_opy_ import bstack1ll1lll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l11_opy_ import bstack1ll1l1lllll_opy_
from bstack_utils.helper import bstack1ll111l1l11_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lll11l1_opy_ import bstack1lll11111l1_opy_
import grpc
import traceback
import json
class bstack1lll11l111l_opy_(bstack1ll1l1llll1_opy_):
    bstack1ll11ll1111_opy_ = False
    bstack1ll11ll1l1l_opy_ = bstack1l11ll1_opy_ (u"ࠣࡵࡨࡰࡪࡴࡩࡶ࡯࠱ࡻࡪࡨࡤࡳ࡫ࡹࡩࡷࠨᆁ")
    bstack1ll111ll11l_opy_ = bstack1l11ll1_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦ࠰ࡺࡩࡧࡪࡲࡪࡸࡨࡶࠧᆂ")
    bstack1ll11ll1l11_opy_ = bstack1l11ll1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢ࡭ࡳ࡯ࡴࠣᆃ")
    bstack1ll11llll11_opy_ = bstack1l11ll1_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣ࡮ࡹ࡟ࡴࡥࡤࡲࡳ࡯࡮ࡨࠤᆄ")
    bstack1ll11l11111_opy_ = bstack1l11ll1_opy_ (u"ࠧࡪࡲࡪࡸࡨࡶࡤ࡮ࡡࡴࡡࡸࡶࡱࠨᆅ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll111ll11_opy_, bstack1llll1111l1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll1l111l11_opy_ = False
        self.bstack1ll11l111ll_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll1111l11l_opy_ = bstack1llll1111l1_opy_
        bstack1lll111ll11_opy_.bstack1ll11ll111l_opy_((bstack1lllll1l111_opy_.bstack1lllll1lll1_opy_, bstack1llll1l11ll_opy_.PRE), self.bstack1ll111ll111_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.PRE), self.bstack1ll11l11ll1_opy_)
        TestFramework.bstack1ll11ll111l_opy_((bstack1ll1ll11l1l_opy_.TEST, bstack1lll111l1l1_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l11ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11111l_opy_(instance, args)
        test_framework = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        if self.bstack1ll1l111l11_opy_:
            self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᆆ")] = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        if bstack1l11ll1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᆇ") in instance.bstack1ll111ll1l1_opy_:
            platform_index = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll1111l1l1_opy_)
            self.accessibility = self.bstack1ll11l11lll_opy_(tags, self.config[bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᆈ")][platform_index])
        else:
            capabilities = self.bstack1ll1111l11l_opy_.bstack1ll1111llll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤࡺࡥࡴࡶ࠽ࠤࡳࡵࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡦࡰࡷࡱࡨࠥ࡬࡯ࡳࠢ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࡂࢁࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰࡿࠣࡥࡷ࡭ࡳ࠾ࡽࡤࡶ࡬ࡹࡽࠡ࡭ࡺࡥࡷ࡭ࡳ࠾ࠤᆉ") + str(kwargs) + bstack1l11ll1_opy_ (u"ࠥࠦᆊ"))
                return
            self.accessibility = self.bstack1ll11l11lll_opy_(tags, capabilities)
        if self.bstack1ll1111l11l_opy_.pages and self.bstack1ll1111l11l_opy_.pages.values():
            bstack1ll1111l1ll_opy_ = list(self.bstack1ll1111l11l_opy_.pages.values())
            if bstack1ll1111l1ll_opy_ and isinstance(bstack1ll1111l1ll_opy_[0], (list, tuple)) and bstack1ll1111l1ll_opy_[0]:
                bstack1ll11lll11l_opy_ = bstack1ll1111l1ll_opy_[0][0]
                if callable(bstack1ll11lll11l_opy_):
                    page = bstack1ll11lll11l_opy_()
                    def bstack1l1l111l1l_opy_():
                        self.get_accessibility_results(page, bstack1l11ll1_opy_ (u"ࠦࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᆋ"))
                    def bstack1ll1l1111l1_opy_():
                        self.get_accessibility_results_summary(page, bstack1l11ll1_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᆌ"))
                    setattr(page, bstack1l11ll1_opy_ (u"ࠨࡧࡦࡶࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡔࡨࡷࡺࡲࡴࡴࠤᆍ"), bstack1l1l111l1l_opy_)
                    setattr(page, bstack1l11ll1_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡕࡸࡱࡲࡧࡲࡺࠤᆎ"), bstack1ll1l1111l1_opy_)
        self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡵ࡫ࡳࡺࡲࡤࠡࡴࡸࡲࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭ࡷࡨࡁࠧᆏ") + str(self.accessibility) + bstack1l11ll1_opy_ (u"ࠤࠥᆐ"))
    def bstack1ll111ll111_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        driver: object,
        exec: Tuple[bstack1lllllll111_opy_, str],
        bstack1lllll1llll_opy_: Tuple[bstack1lllll1l111_opy_, bstack1llll1l11ll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l11ll1ll_opy_ = datetime.now()
            self.bstack1ll1l111lll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻࡫ࡱ࡭ࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᆑ"), datetime.now() - bstack1l11ll1ll_opy_)
            if (
                not f.bstack1ll11l11l11_opy_(method_name)
                or f.bstack1ll111l111l_opy_(method_name, *args)
                or f.bstack1ll11ll11l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllllllll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11ll1l11_opy_, False):
                if not bstack1lll11l111l_opy_.bstack1ll11ll1111_opy_:
                    self.logger.warning(bstack1l11ll1_opy_ (u"ࠦࡠࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࠢᆒ") + str(f.platform_index) + bstack1l11ll1_opy_ (u"ࠧࡣࠠࡢ࠳࠴ࡽࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡭ࡧࡶࡦࠢࡱࡳࡹࠦࡢࡦࡧࡱࠤࡸ࡫ࡴࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡷࡪࡹࡳࡪࡱࡱࠦᆓ"))
                    bstack1lll11l111l_opy_.bstack1ll11ll1111_opy_ = True
                return
            bstack1ll11ll1ll1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11ll1ll1_opy_:
                platform_index = f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_, 0)
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࡃࡻࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᆔ") + str(f.framework_name) + bstack1l11ll1_opy_ (u"ࠢࠣᆕ"))
                return
            command_name = f.bstack1ll1l111111_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࠥᆖ") + str(method_name) + bstack1l11ll1_opy_ (u"ࠤࠥᆗ"))
                return
            bstack1ll1111ll11_opy_ = f.bstack1llllllllll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11l11111_opy_, False)
            if command_name == bstack1l11ll1_opy_ (u"ࠥ࡫ࡪࡺࠢᆘ") and not bstack1ll1111ll11_opy_:
                f.bstack1llllll1ll1_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11l11111_opy_, True)
                bstack1ll1111ll11_opy_ = True
            if not bstack1ll1111ll11_opy_ and not self.bstack1ll1l111l11_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡳࡵࠠࡖࡔࡏࠤࡱࡵࡡࡥࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᆙ") + str(command_name) + bstack1l11ll1_opy_ (u"ࠧࠨᆚ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡮ࡰࠢࡤ࠵࠶ࡿࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᆛ") + str(command_name) + bstack1l11ll1_opy_ (u"ࠢࠣᆜ"))
                return
            self.logger.info(bstack1l11ll1_opy_ (u"ࠣࡴࡸࡲࡳ࡯࡮ࡨࠢࡾࡰࡪࡴࠨࡴࡥࡵ࡭ࡵࡺࡳࡠࡶࡲࡣࡷࡻ࡮ࠪࡿࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦ࠯ࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦ࠿ࠥᆝ") + str(command_name) + bstack1l11ll1_opy_ (u"ࠤࠥᆞ"))
            scripts = [(s, bstack1ll11ll1ll1_opy_[s]) for s in scripts_to_run if s in bstack1ll11ll1ll1_opy_]
            for script_name, bstack1ll11llllll_opy_ in scripts:
                try:
                    bstack1l11ll1ll_opy_ = datetime.now()
                    if script_name == bstack1l11ll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᆟ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                    instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࠥᆠ") + script_name, datetime.now() - bstack1l11ll1ll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l11ll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᆡ"), True):
                        self.logger.warning(bstack1l11ll1_opy_ (u"ࠨࡳ࡬࡫ࡳࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡳࡧࡰࡥ࡮ࡴࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡶ࠾ࠥࠨᆢ") + str(result) + bstack1l11ll1_opy_ (u"ࠢࠣᆣ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l11ll1_opy_ (u"ࠣࡧࡵࡶࡴࡸࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡷࡨࡸࡩࡱࡶࡀࡿࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦࡿࠣࡩࡷࡸ࡯ࡳ࠿ࠥᆤ") + str(e) + bstack1l11ll1_opy_ (u"ࠤࠥᆥ"))
        except Exception as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡥࡹࡧࡦࡹࡹ࡫ࠠࡦࡴࡵࡳࡷࡃࠢᆦ") + str(e) + bstack1l11ll1_opy_ (u"ࠦࠧᆧ"))
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll11l1111_opy_,
        bstack1lllll1llll_opy_: Tuple[bstack1ll1ll11l1l_opy_, bstack1lll111l1l1_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11111l_opy_(instance, args)
        capabilities = self.bstack1ll1111l11l_opy_.bstack1ll1111llll_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll11l11lll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᆨ"))
            return
        driver = self.bstack1ll1111l11l_opy_.bstack1ll1111l111_opy_(f, instance, bstack1lllll1llll_opy_, *args, **kwargs)
        test_name = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll11llll1l_opy_)
        if not test_name:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᆩ"))
            return
        test_uuid = f.bstack1llllllllll_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᆪ"))
            return
        if isinstance(self.bstack1ll1111l11l_opy_, bstack1ll1lll1l1l_opy_):
            framework_name = bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᆫ")
        else:
            framework_name = bstack1l11ll1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᆬ")
        self.bstack1l1ll1111_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1l1l1l1ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᆭ"))
            return
        bstack1l11ll1ll_opy_ = datetime.now()
        bstack1ll11llllll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11ll1_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᆮ"), None)
        if not bstack1ll11llllll_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᆯ") + str(framework_name) + bstack1l11ll1_opy_ (u"ࠨࠠࠣᆰ"))
            return
        if self.bstack1ll1l111l11_opy_:
            arg = dict()
            arg[bstack1l11ll1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᆱ")] = method if method else bstack1l11ll1_opy_ (u"ࠣࠤᆲ")
            arg[bstack1l11ll1_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᆳ")] = self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᆴ")]
            arg[bstack1l11ll1_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᆵ")] = self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᆶ")]
            arg[bstack1l11ll1_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᆷ")] = self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᆸ")]
            arg[bstack1l11ll1_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᆹ")] = self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᆺ")]
            arg[bstack1l11ll1_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᆻ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11lll1l1_opy_ = bstack1ll11llllll_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11lll1l1_opy_)
            return
        instance = bstack1llllllll1l_opy_.bstack1lllll11l1l_opy_(driver)
        if instance:
            if not bstack1llllllll1l_opy_.bstack1llllllllll_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11llll11_opy_, False):
                bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11llll11_opy_, True)
            else:
                self.logger.info(bstack1l11ll1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦࡲࡲࡦࡣࡧࡽࠥ࡯࡮ࠡࡲࡵࡳ࡬ࡸࡥࡴࡵࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᆼ") + str(method) + bstack1l11ll1_opy_ (u"ࠧࠨᆽ"))
                return
        self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᆾ") + str(method) + bstack1l11ll1_opy_ (u"ࠢࠣᆿ"))
        if framework_name == bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᇀ"):
            result = self.bstack1ll1111l11l_opy_.bstack1ll1l11l111_opy_(driver, bstack1ll11llllll_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11llllll_opy_, {bstack1l11ll1_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᇁ"): method if method else bstack1l11ll1_opy_ (u"ࠥࠦᇂ")})
        bstack1lll11111l1_opy_.end(EVENTS.bstack1l1l1l1ll_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᇃ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᇄ"), True, None, command=method)
        if instance:
            bstack1llllllll1l_opy_.bstack1llllll1ll1_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11llll11_opy_, False)
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰࠥᇅ"), datetime.now() - bstack1l11ll1ll_opy_)
        return result
        def bstack1ll11l1l1l1_opy_(self, driver: object, framework_name, bstack1l11l1l1l_opy_: str):
            self.bstack1ll11l111l1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll11l1l11l_opy_ = self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᇆ")]
            req.bstack1l11l1l1l_opy_ = bstack1l11l1l1l_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll111111l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᇇ") + str(r) + bstack1l11ll1_opy_ (u"ࠤࠥᇈ"))
                else:
                    bstack1ll111lllll_opy_ = json.loads(r.bstack1ll111l11l1_opy_.decode(bstack1l11ll1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᇉ")))
                    if bstack1l11l1l1l_opy_ == bstack1l11ll1_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨᇊ"):
                        return bstack1ll111lllll_opy_.get(bstack1l11ll1_opy_ (u"ࠧࡪࡡࡵࡣࠥᇋ"), [])
                    else:
                        return bstack1ll111lllll_opy_.get(bstack1l11ll1_opy_ (u"ࠨࡤࡢࡶࡤࠦᇌ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡳࡴࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࠥ࡬ࡲࡰ࡯ࠣࡧࡱ࡯࠺ࠡࠤᇍ") + str(e) + bstack1l11ll1_opy_ (u"ࠣࠤᇎ"))
    @measure(event_name=EVENTS.bstack1ll11l1111_opy_, stage=STAGE.bstack11lllll111_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠤࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᇏ"))
            return
        if self.bstack1ll1l111l11_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡤࡴࡵࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᇐ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l1l1l1_opy_(driver, framework_name, bstack1l11ll1_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠣᇑ"))
        bstack1ll11llllll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11ll1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᇒ"), None)
        if not bstack1ll11llllll_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᇓ") + str(framework_name) + bstack1l11ll1_opy_ (u"ࠢࠣᇔ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l11ll1ll_opy_ = datetime.now()
        if framework_name == bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᇕ"):
            result = self.bstack1ll1111l11l_opy_.bstack1ll1l11l111_opy_(driver, bstack1ll11llllll_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11llllll_opy_)
        instance = bstack1llllllll1l_opy_.bstack1lllll11l1l_opy_(driver)
        if instance:
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧᇖ"), datetime.now() - bstack1l11ll1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack111l1lll1_opy_, stage=STAGE.bstack11lllll111_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᇗ"))
            return
        if self.bstack1ll1l111l11_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l1l1l1_opy_(driver, framework_name, bstack1l11ll1_opy_ (u"ࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨᇘ"))
        bstack1ll11llllll_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11ll1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᇙ"), None)
        if not bstack1ll11llllll_opy_:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᇚ") + str(framework_name) + bstack1l11ll1_opy_ (u"ࠢࠣᇛ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l11ll1ll_opy_ = datetime.now()
        if framework_name == bstack1l11ll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᇜ"):
            result = self.bstack1ll1111l11l_opy_.bstack1ll1l11l111_opy_(driver, bstack1ll11llllll_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11llllll_opy_)
        instance = bstack1llllllll1l_opy_.bstack1lllll11l1l_opy_(driver)
        if instance:
            instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᇝ"), datetime.now() - bstack1l11ll1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll11l1llll_opy_, stage=STAGE.bstack11lllll111_opy_)
    def bstack1ll11lll1ll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11l111l1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll111111l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᇞ") + str(r) + bstack1l11ll1_opy_ (u"ࠦࠧᇟ"))
            else:
                self.bstack1ll111lll1l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᇠ") + str(e) + bstack1l11ll1_opy_ (u"ࠨࠢᇡ"))
            traceback.print_exc()
            raise e
    def bstack1ll111lll1l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᇢ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll1l111l11_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨᇣ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll11l111ll_opy_[bstack1l11ll1_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᇤ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll11l111ll_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l111ll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11ll1l1l_opy_ and command.module == self.bstack1ll111ll11l_opy_:
                        if command.method and not command.method in bstack1ll1l111ll1_opy_:
                            bstack1ll1l111ll1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l111ll1_opy_[command.method]:
                            bstack1ll1l111ll1_opy_[command.method][command.name] = list()
                        bstack1ll1l111ll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l111ll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1l111lll_opy_(
        self,
        f: bstack1ll1l1l1lll_opy_,
        exec: Tuple[bstack1lllllll111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1111l11l_opy_, bstack1ll1lll1l1l_opy_) and method_name != bstack1l11ll1_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᇥ"):
            return
        if bstack1llllllll1l_opy_.bstack1lllll11l11_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11ll1l11_opy_):
            return
        if f.bstack1ll11l1lll1_opy_(method_name, *args):
            bstack1ll111lll11_opy_ = False
            desired_capabilities = f.bstack1ll11l1ll1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11lll111_opy_(instance)
                platform_index = f.bstack1llllllllll_opy_(instance, bstack1ll1l1l1lll_opy_.bstack1ll1111l1l1_opy_, 0)
                bstack1ll1111lll1_opy_ = datetime.now()
                r = self.bstack1ll11lll1ll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack111l1l11_opy_(bstack1l11ll1_opy_ (u"ࠦ࡬ࡸࡰࡤ࠼ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᇦ"), datetime.now() - bstack1ll1111lll1_opy_)
                bstack1ll111lll11_opy_ = r.success
            else:
                self.logger.error(bstack1l11ll1_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡤࡦࡵ࡬ࡶࡪࡪࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࡃࠢᇧ") + str(desired_capabilities) + bstack1l11ll1_opy_ (u"ࠨࠢᇨ"))
            f.bstack1llllll1ll1_opy_(instance, bstack1lll11l111l_opy_.bstack1ll11ll1l11_opy_, bstack1ll111lll11_opy_)
    def bstack11l1lllll_opy_(self, test_tags):
        bstack1ll11lll1ll_opy_ = self.config.get(bstack1l11ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᇩ"))
        if not bstack1ll11lll1ll_opy_:
            return True
        try:
            include_tags = bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᇪ")] if bstack1l11ll1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᇫ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᇬ")], list) else []
            exclude_tags = bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᇭ")] if bstack1l11ll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᇮ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11ll1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᇯ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᇰ") + str(error))
        return False
    def bstack11l1l11111_opy_(self, caps):
        try:
            if self.bstack1ll1l111l11_opy_:
                bstack1ll11l1111l_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᇱ"))
                if bstack1ll11l1111l_opy_ is not None and str(bstack1ll11l1111l_opy_).lower() == bstack1l11ll1_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᇲ"):
                    bstack1ll11l1l1ll_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᇳ")) or caps.get(bstack1l11ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᇴ"))
                    if bstack1ll11l1l1ll_opy_ is not None and int(bstack1ll11l1l1ll_opy_) < 11:
                        self.logger.warning(bstack1l11ll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡇ࡮ࡥࡴࡲ࡭ࡩࠦ࠱࠲ࠢࡤࡲࡩࠦࡡࡣࡱࡹࡩ࠳ࠦࡃࡶࡴࡵࡩࡳࡺࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡁࠧᇵ") + str(bstack1ll11l1l1ll_opy_) + bstack1l11ll1_opy_ (u"ࠨࠢᇶ"))
                        return False
                return True
            bstack1ll111l1111_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᇷ"), {}).get(bstack1l11ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᇸ"), caps.get(bstack1l11ll1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᇹ"), bstack1l11ll1_opy_ (u"ࠪࠫᇺ")))
            if bstack1ll111l1111_opy_:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᇻ"))
                return False
            browser = caps.get(bstack1l11ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᇼ"), bstack1l11ll1_opy_ (u"࠭ࠧᇽ")).lower()
            if browser != bstack1l11ll1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᇾ"):
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᇿ"))
                return False
            bstack1ll1111ll1l_opy_ = bstack1ll11ll11ll_opy_
            if not self.config.get(bstack1l11ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫሀ")) or self.config.get(bstack1l11ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧሁ")):
                bstack1ll1111ll1l_opy_ = bstack1ll111l1ll1_opy_
            browser_version = caps.get(bstack1l11ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬሂ"))
            if not browser_version:
                browser_version = caps.get(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ሃ"), {}).get(bstack1l11ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧሄ"), bstack1l11ll1_opy_ (u"ࠧࠨህ"))
            if browser_version and browser_version != bstack1l11ll1_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨሆ") and int(browser_version.split(bstack1l11ll1_opy_ (u"ࠩ࠱ࠫሇ"))[0]) <= bstack1ll1111ll1l_opy_:
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࠧለ") + str(bstack1ll1111ll1l_opy_) + bstack1l11ll1_opy_ (u"ࠦ࠳ࠨሉ"))
                return False
            bstack1ll11l1ll11_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ሊ"), {}).get(bstack1l11ll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ላ"))
            if not bstack1ll11l1ll11_opy_:
                bstack1ll11l1ll11_opy_ = caps.get(bstack1l11ll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬሌ"), {})
            if bstack1ll11l1ll11_opy_ and bstack1l11ll1_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬል") in bstack1ll11l1ll11_opy_.get(bstack1l11ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧሎ"), []):
                self.logger.warning(bstack1l11ll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧሏ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨሐ") + str(error))
            return False
    def bstack1ll11ll1lll_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l1111ll_opy_ = {
            bstack1l11ll1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬሑ"): test_uuid,
        }
        bstack1ll11l11l1l_opy_ = {}
        if result.success:
            bstack1ll11l11l1l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll111l1l11_opy_(bstack1ll1l1111ll_opy_, bstack1ll11l11l1l_opy_)
    def bstack1l1ll1111_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll111l1lll_opy_ = None
        try:
            self.bstack1ll11l111l1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l11ll1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨሒ")
            req.script_name = bstack1l11ll1_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧሓ")
            r = self.bstack1lll111111l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦሔ") + str(r.error) + bstack1l11ll1_opy_ (u"ࠤࠥሕ"))
            else:
                bstack1ll1l1111ll_opy_ = self.bstack1ll11ll1lll_opy_(test_uuid, r)
                bstack1ll11llllll_opy_ = r.script
            self.logger.debug(bstack1l11ll1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ሖ") + str(bstack1ll1l1111ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11llllll_opy_:
                self.logger.debug(bstack1l11ll1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦሗ") + str(framework_name) + bstack1l11ll1_opy_ (u"ࠧࠦࠢመ"))
                return
            bstack1ll111l1lll_opy_ = bstack1lll11111l1_opy_.bstack1ll111l11ll_opy_(EVENTS.bstack1ll111l1l1l_opy_.value)
            self.bstack1ll111llll1_opy_(driver, bstack1ll11llllll_opy_, bstack1ll1l1111ll_opy_, framework_name)
            self.logger.info(bstack1l11ll1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤሙ"))
            bstack1lll11111l1_opy_.end(EVENTS.bstack1ll111l1l1l_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢሚ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨማ"), True, None, command=bstack1l11ll1_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧሜ"),test_name=name)
        except Exception as bstack1ll11l1l111_opy_:
            self.logger.error(bstack1l11ll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧም") + bstack1l11ll1_opy_ (u"ࠦࡸࡺࡲࠩࡲࡤࡸ࡭࠯ࠢሞ") + bstack1l11ll1_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢሟ") + str(bstack1ll11l1l111_opy_))
            bstack1lll11111l1_opy_.end(EVENTS.bstack1ll111l1l1l_opy_.value, bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨሠ"), bstack1ll111l1lll_opy_+bstack1l11ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧሡ"), False, bstack1ll11l1l111_opy_, command=bstack1l11ll1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ሢ"),test_name=name)
    def bstack1ll111llll1_opy_(self, driver, bstack1ll11llllll_opy_, bstack1ll1l1111ll_opy_, framework_name):
        if framework_name == bstack1l11ll1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ሣ"):
            self.bstack1ll1111l11l_opy_.bstack1ll1l11l111_opy_(driver, bstack1ll11llllll_opy_, bstack1ll1l1111ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11llllll_opy_, bstack1ll1l1111ll_opy_))
    def _1ll1l11111l_opy_(self, instance: bstack1lll11l1111_opy_, args: Tuple) -> list:
        bstack1l11ll1_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡩࡶࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢሤ")
        if bstack1l11ll1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨሥ") in instance.bstack1ll111ll1l1_opy_:
            return args[2].tags if hasattr(args[2], bstack1l11ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪሦ")) else []
        if hasattr(args[0], bstack1l11ll1_opy_ (u"࠭࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠫሧ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll11l11lll_opy_(self, tags, capabilities):
        return self.bstack11l1lllll_opy_(tags) and self.bstack11l1l11111_opy_(capabilities)