# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllll1lll1_opy_ import (
    bstack1111111l11_opy_,
    bstack1llllll1111_opy_,
    bstack1111111ll1_opy_,
    bstack1llll1ll1ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll1l1ll_opy_ import bstack1llll11l111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_, bstack1llll111l11_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll11lll1_opy_ import bstack1ll1ll1llll_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l11ll_opy_ import bstack1lll1l1l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1lll11lllll_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack1lll11l1l11_opy_ import bstack1lll1lll1l1_opy_
from bstack_utils.helper import bstack1ll1l11l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
import grpc
import traceback
import json
class bstack1llll1ll111_opy_(bstack1ll1ll1llll_opy_):
    bstack1ll111lll1l_opy_ = False
    bstack1ll11l1l1ll_opy_ = bstack11ll11_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᄽ")
    bstack1ll1l111111_opy_ = bstack11ll11_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᄾ")
    bstack1ll11l111ll_opy_ = bstack11ll11_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥᄿ")
    bstack1ll11l11ll1_opy_ = bstack11ll11_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦᅀ")
    bstack1ll11l1llll_opy_ = bstack11ll11_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣᅁ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1lllll11_opy_, bstack1lll1l111ll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll111ll11l_opy_ = bstack1lll1l111ll_opy_
        bstack1ll1lllll11_opy_.bstack1ll1l11l1l1_opy_((bstack1111111l11_opy_.bstack1lllll11lll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll11l1l1l1_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.PRE), self.bstack1ll11ll1l1l_opy_)
        TestFramework.bstack1ll1l11l1l1_opy_((bstack1llll11111l_opy_.TEST, bstack1ll1l1lll11_opy_.POST), self.bstack1ll1l111ll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11ll1l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll111llll1_opy_(instance, args)
        test_framework = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
        if bstack11ll11_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᅂ") in instance.bstack1ll11l11l1l_opy_:
            platform_index = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11111l_opy_)
            self.accessibility = self.bstack1ll111ll1l1_opy_(tags, self.config[bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᅃ")][platform_index])
        else:
            capabilities = self.bstack1ll111ll11l_opy_.bstack1ll1l1111ll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11ll11_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᅄ") + str(kwargs) + bstack11ll11_opy_ (u"ࠦࠧᅅ"))
                return
            self.accessibility = self.bstack1ll111ll1l1_opy_(tags, capabilities)
        if self.bstack1ll111ll11l_opy_.pages and self.bstack1ll111ll11l_opy_.pages.values():
            bstack1ll1l111l11_opy_ = list(self.bstack1ll111ll11l_opy_.pages.values())
            if bstack1ll1l111l11_opy_ and isinstance(bstack1ll1l111l11_opy_[0], (list, tuple)) and bstack1ll1l111l11_opy_[0]:
                bstack1ll11ll1111_opy_ = bstack1ll1l111l11_opy_[0][0]
                if callable(bstack1ll11ll1111_opy_):
                    page = bstack1ll11ll1111_opy_()
                    def bstack1ll1l1llll_opy_():
                        self.get_accessibility_results(page, bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᅆ"))
                    def bstack1ll11lll11l_opy_():
                        self.get_accessibility_results_summary(page, bstack11ll11_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᅇ"))
                    setattr(page, bstack11ll11_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡵࠥᅈ"), bstack1ll1l1llll_opy_)
                    setattr(page, bstack11ll11_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥᅉ"), bstack1ll11lll11l_opy_)
        self.logger.debug(bstack11ll11_opy_ (u"ࠤࡶ࡬ࡴࡻ࡬ࡥࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮ࡸࡩࡂࠨᅊ") + str(self.accessibility) + bstack11ll11_opy_ (u"ࠥࠦᅋ"))
    def bstack1ll11l1l1l1_opy_(
        self,
        f: bstack1llll11l111_opy_,
        driver: object,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        bstack111111111l_opy_: Tuple[bstack1111111l11_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll1lll1ll_opy_ = datetime.now()
            self.bstack1ll11llll1l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᅌ"), datetime.now() - bstack1ll1lll1ll_opy_)
            if (
                not f.bstack1ll1l11ll1l_opy_(method_name)
                or f.bstack1ll111lll11_opy_(method_name, *args)
                or f.bstack1ll11lll1l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lllll1l1ll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l111ll_opy_, False):
                if not bstack1llll1ll111_opy_.bstack1ll111lll1l_opy_:
                    self.logger.warning(bstack11ll11_opy_ (u"ࠧࡡࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣᅍ") + str(f.platform_index) + bstack11ll11_opy_ (u"ࠨ࡝ࠡࡣ࠴࠵ࡾࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡮ࡡࡷࡧࠣࡲࡴࡺࠠࡣࡧࡨࡲࠥࡹࡥࡵࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᅎ"))
                    bstack1llll1ll111_opy_.bstack1ll111lll1l_opy_ = True
                return
            bstack1ll11lll111_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11lll111_opy_:
                platform_index = f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_, 0)
                self.logger.debug(bstack11ll11_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅏ") + str(f.framework_name) + bstack11ll11_opy_ (u"ࠣࠤᅐ"))
                return
            bstack1ll11ll1lll_opy_ = f.bstack1ll11l1ll1l_opy_(*args)
            if not bstack1ll11ll1lll_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࠦᅑ") + str(method_name) + bstack11ll11_opy_ (u"ࠥࠦᅒ"))
                return
            bstack1ll11l1l111_opy_ = f.bstack1lllll1l1ll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l1llll_opy_, False)
            if bstack1ll11ll1lll_opy_ == bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࠣᅓ") and not bstack1ll11l1l111_opy_:
                f.bstack1llllllllll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l1llll_opy_, True)
                bstack1ll11l1l111_opy_ = True
            if not bstack1ll11l1l111_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠧࡴ࡯ࠡࡗࡕࡐࠥࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᅔ") + str(bstack1ll11ll1lll_opy_) + bstack11ll11_opy_ (u"ࠨࠢᅕ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll11ll1lll_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack11ll11_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᅖ") + str(bstack1ll11ll1lll_opy_) + bstack11ll11_opy_ (u"ࠣࠤᅗ"))
                return
            self.logger.info(bstack11ll11_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡵࡦࡶ࡮ࡶࡴࡴࡡࡷࡳࡤࡸࡵ࡯ࠫࢀࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᅘ") + str(bstack1ll11ll1lll_opy_) + bstack11ll11_opy_ (u"ࠥࠦᅙ"))
            scripts = [(s, bstack1ll11lll111_opy_[s]) for s in scripts_to_run if s in bstack1ll11lll111_opy_]
            for script_name, bstack1ll1l11l11l_opy_ in scripts:
                try:
                    bstack1ll1lll1ll_opy_ = datetime.now()
                    if script_name == bstack11ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᅚ"):
                        result = self.perform_scan(driver, method=bstack1ll11ll1lll_opy_, framework_name=f.framework_name)
                    instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦᅛ") + script_name, datetime.now() - bstack1ll1lll1ll_opy_)
                    if isinstance(result, dict) and not result.get(bstack11ll11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᅜ"), True):
                        self.logger.warning(bstack11ll11_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢᅝ") + str(result) + bstack11ll11_opy_ (u"ࠣࠤᅞ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11ll11_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦᅟ") + str(e) + bstack11ll11_opy_ (u"ࠥࠦᅠ"))
        except Exception as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣᅡ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨᅢ"))
    def bstack1ll1l111ll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1llll111l11_opy_,
        bstack111111111l_opy_: Tuple[bstack1llll11111l_opy_, bstack1ll1l1lll11_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll111llll1_opy_(instance, args)
        capabilities = self.bstack1ll111ll11l_opy_.bstack1ll1l1111ll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll111ll1l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᅣ"))
            return
        driver = self.bstack1ll111ll11l_opy_.bstack1ll11ll11ll_opy_(f, instance, bstack111111111l_opy_, *args, **kwargs)
        test_name = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        if not test_name:
            self.logger.debug(bstack11ll11_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᅤ"))
            return
        test_uuid = f.bstack1lllll1l1ll_opy_(instance, TestFramework.bstack1ll1l11ll11_opy_)
        if not test_uuid:
            self.logger.debug(bstack11ll11_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᅥ"))
            return
        if isinstance(self.bstack1ll111ll11l_opy_, bstack1llll111111_opy_):
            framework_name = bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᅦ")
        else:
            framework_name = bstack11ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᅧ")
        self.bstack1ll1l1l111_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1lllll1l11_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᅨ"))
            return
        bstack1ll1lll1ll_opy_ = datetime.now()
        bstack1ll1l11l11l_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll11_opy_ (u"ࠧࡹࡣࡢࡰࠥᅩ"), None)
        if not bstack1ll1l11l11l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᅪ") + str(framework_name) + bstack11ll11_opy_ (u"ࠢࠡࠤᅫ"))
            return
        instance = bstack1111111ll1_opy_.bstack11111111l1_opy_(driver)
        if instance:
            if not bstack1111111ll1_opy_.bstack1lllll1l1ll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l11ll1_opy_, False):
                bstack1111111ll1_opy_.bstack1llllllllll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l11ll1_opy_, True)
            else:
                self.logger.info(bstack11ll11_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡲࠥࡶࡲࡰࡩࡵࡩࡸࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᅬ") + str(method) + bstack11ll11_opy_ (u"ࠤࠥᅭ"))
                return
        self.logger.info(bstack11ll11_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᅮ") + str(method) + bstack11ll11_opy_ (u"ࠦࠧᅯ"))
        if framework_name == bstack11ll11_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᅰ"):
            result = self.bstack1ll111ll11l_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll1l11l11l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l11l11l_opy_, {bstack11ll11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᅱ"): method if method else bstack11ll11_opy_ (u"ࠢࠣᅲ")})
        bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1lllll1l11_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᅳ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᅴ"), True, None, command=method)
        if instance:
            bstack1111111ll1_opy_.bstack1llllllllll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l11ll1_opy_, False)
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢᅵ"), datetime.now() - bstack1ll1lll1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1llll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᅶ"))
            return
        bstack1ll1l11l11l_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll11_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᅷ"), None)
        if not bstack1ll1l11l11l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅸ") + str(framework_name) + bstack11ll11_opy_ (u"ࠢࠣᅹ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1lll1ll_opy_ = datetime.now()
        if framework_name == bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᅺ"):
            result = self.bstack1ll111ll11l_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll1l11l11l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l11l11l_opy_)
        instance = bstack1111111ll1_opy_.bstack11111111l1_opy_(driver)
        if instance:
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧᅻ"), datetime.now() - bstack1ll1lll1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll11l1l_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll11_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᅼ"))
            return
        bstack1ll1l11l11l_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll11_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᅽ"), None)
        if not bstack1ll1l11l11l_opy_:
            self.logger.debug(bstack11ll11_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᅾ") + str(framework_name) + bstack11ll11_opy_ (u"ࠨࠢᅿ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1lll1ll_opy_ = datetime.now()
        if framework_name == bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᆀ"):
            result = self.bstack1ll111ll11l_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll1l11l11l_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l11l11l_opy_)
        instance = bstack1111111ll1_opy_.bstack11111111l1_opy_(driver)
        if instance:
            instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᆁ"), datetime.now() - bstack1ll1lll1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l11l1ll_opy_, stage=STAGE.bstack1lll11llll_opy_)
    def bstack1ll11ll1ll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l1l1111_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1llll1l1l11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᆂ") + str(r) + bstack11ll11_opy_ (u"ࠥࠦᆃ"))
            else:
                self.bstack1ll11llll11_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll11_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᆄ") + str(e) + bstack11ll11_opy_ (u"ࠧࠨᆅ"))
            traceback.print_exc()
            raise e
    def bstack1ll11llll11_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11ll11_opy_ (u"ࠨ࡬ࡰࡣࡧࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᆆ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11l1111l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11l1l1ll_opy_ and command.module == self.bstack1ll1l111111_opy_:
                        if command.method and not command.method in bstack1ll11l1111l_opy_:
                            bstack1ll11l1111l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11l1111l_opy_[command.method]:
                            bstack1ll11l1111l_opy_[command.method][command.name] = list()
                        bstack1ll11l1111l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11l1111l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll11llll1l_opy_(
        self,
        f: bstack1llll11l111_opy_,
        exec: Tuple[bstack1llll1ll1ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll111ll11l_opy_, bstack1llll111111_opy_) and method_name != bstack11ll11_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᆇ"):
            return
        if bstack1111111ll1_opy_.bstack1lllll1l111_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l111ll_opy_):
            return
        if f.bstack1ll11lllll1_opy_(method_name, *args):
            bstack1ll111lllll_opy_ = False
            desired_capabilities = f.bstack1ll11llllll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11lll1ll_opy_(instance)
                platform_index = f.bstack1lllll1l1ll_opy_(instance, bstack1llll11l111_opy_.bstack1ll1l11111l_opy_, 0)
                bstack1ll11ll1l11_opy_ = datetime.now()
                r = self.bstack1ll11ll1ll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1ll1l1l1l1_opy_(bstack11ll11_opy_ (u"ࠣࡩࡵࡴࡨࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᆈ"), datetime.now() - bstack1ll11ll1l11_opy_)
                bstack1ll111lllll_opy_ = r.success
            else:
                self.logger.error(bstack11ll11_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡨࡪࡹࡩࡳࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࡀࠦᆉ") + str(desired_capabilities) + bstack11ll11_opy_ (u"ࠥࠦᆊ"))
            f.bstack1llllllllll_opy_(instance, bstack1llll1ll111_opy_.bstack1ll11l111ll_opy_, bstack1ll111lllll_opy_)
    def bstack1ll1lllll_opy_(self, test_tags):
        bstack1ll11ll1ll1_opy_ = self.config.get(bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᆋ"))
        if not bstack1ll11ll1ll1_opy_:
            return True
        try:
            include_tags = bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᆌ")] if bstack11ll11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᆍ") in bstack1ll11ll1ll1_opy_ and isinstance(bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᆎ")], list) else []
            exclude_tags = bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᆏ")] if bstack11ll11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᆐ") in bstack1ll11ll1ll1_opy_ and isinstance(bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᆑ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᆒ") + str(error))
        return False
    def bstack1ll1ll111_opy_(self, caps):
        try:
            bstack1ll1l1l111l_opy_ = caps.get(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᆓ"), {}).get(bstack11ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᆔ"), caps.get(bstack11ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᆕ"), bstack11ll11_opy_ (u"ࠨࠩᆖ")))
            if bstack1ll1l1l111l_opy_:
                self.logger.warning(bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᆗ"))
                return False
            browser = caps.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᆘ"), bstack11ll11_opy_ (u"ࠫࠬᆙ")).lower()
            if browser != bstack11ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᆚ"):
                self.logger.warning(bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᆛ"))
                return False
            bstack1ll1l111lll_opy_ = bstack1ll11l11l11_opy_
            if not self.config.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᆜ")) or self.config.get(bstack11ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᆝ")):
                bstack1ll1l111lll_opy_ = bstack1ll11l1ll11_opy_
            browser_version = caps.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᆞ"))
            if not browser_version:
                browser_version = caps.get(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᆟ"), {}).get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᆠ"), bstack11ll11_opy_ (u"ࠬ࠭ᆡ"))
            if browser_version and browser_version != bstack11ll11_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᆢ") and int(browser_version.split(bstack11ll11_opy_ (u"ࠧ࠯ࠩᆣ"))[0]) <= bstack1ll1l111lll_opy_:
                self.logger.warning(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥᆤ") + str(bstack1ll1l111lll_opy_) + bstack11ll11_opy_ (u"ࠤ࠱ࠦᆥ"))
                return False
            bstack1ll11l1lll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᆦ"), {}).get(bstack11ll11_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᆧ"))
            if not bstack1ll11l1lll1_opy_:
                bstack1ll11l1lll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᆨ"), {})
            if bstack1ll11l1lll1_opy_ and bstack11ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᆩ") in bstack1ll11l1lll1_opy_.get(bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᆪ"), []):
                self.logger.warning(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᆫ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᆬ") + str(error))
            return False
    def bstack1ll11l11111_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll111ll1ll_opy_ = {
            bstack11ll11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᆭ"): test_uuid,
        }
        bstack1ll11l1l11l_opy_ = {}
        if result.success:
            bstack1ll11l1l11l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1l11l111_opy_(bstack1ll111ll1ll_opy_, bstack1ll11l1l11l_opy_)
    def bstack1ll1l1l111_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11ll111l_opy_ = None
        try:
            self.bstack1ll1l1l1111_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll11_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᆮ")
            req.script_name = bstack11ll11_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᆯ")
            r = self.bstack1llll1l1l11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11ll11_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᆰ") + str(r.error) + bstack11ll11_opy_ (u"ࠢࠣᆱ"))
            else:
                bstack1ll111ll1ll_opy_ = self.bstack1ll11l11111_opy_(test_uuid, r)
                bstack1ll1l11l11l_opy_ = r.script
            self.logger.debug(bstack11ll11_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᆲ") + str(bstack1ll111ll1ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l11l11l_opy_:
                self.logger.debug(bstack11ll11_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᆳ") + str(framework_name) + bstack11ll11_opy_ (u"ࠥࠤࠧᆴ"))
                return
            bstack1ll11ll111l_opy_ = bstack1ll1l1ll1l1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1ll1l1111l1_opy_.value)
            self.bstack1ll1l11lll1_opy_(driver, bstack1ll1l11l11l_opy_, bstack1ll111ll1ll_opy_, framework_name)
            self.logger.info(bstack11ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᆵ"))
            bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1ll1l1111l1_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᆶ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᆷ"), True, None, command=bstack11ll11_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᆸ"),test_name=name)
        except Exception as bstack1ll11l111l1_opy_:
            self.logger.error(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᆹ") + bstack11ll11_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧᆺ") + bstack11ll11_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᆻ") + str(bstack1ll11l111l1_opy_))
            bstack1ll1l1ll1l1_opy_.end(EVENTS.bstack1ll1l1111l1_opy_.value, bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᆼ"), bstack1ll11ll111l_opy_+bstack11ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᆽ"), False, bstack1ll11l111l1_opy_, command=bstack11ll11_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᆾ"),test_name=name)
    def bstack1ll1l11lll1_opy_(self, driver, bstack1ll1l11l11l_opy_, bstack1ll111ll1ll_opy_, framework_name):
        if framework_name == bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᆿ"):
            self.bstack1ll111ll11l_opy_.bstack1ll1l11llll_opy_(driver, bstack1ll1l11l11l_opy_, bstack1ll111ll1ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l11l11l_opy_, bstack1ll111ll1ll_opy_))
    def _1ll111llll1_opy_(self, instance: bstack1llll111l11_opy_, args: Tuple) -> list:
        bstack11ll11_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧᇀ")
        if bstack11ll11_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᇁ") in instance.bstack1ll11l11l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack11ll11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᇂ")) else []
        if hasattr(args[0], bstack11ll11_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩᇃ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll111ll1l1_opy_(self, tags, capabilities):
        return self.bstack1ll1lllll_opy_(tags) and self.bstack1ll1ll111_opy_(capabilities)