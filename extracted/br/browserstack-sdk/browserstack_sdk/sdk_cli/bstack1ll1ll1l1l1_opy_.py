# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1llllll1111_opy_ import (
    bstack1111111111_opy_,
    bstack11111l1ll1_opy_,
    bstack1111111l11_opy_,
    bstack1llllll111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1lll1l11_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll11lllll_opy_, bstack1lllll1111l_opy_, bstack1lll1111l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1lll11l1_opy_ import bstack1lll1l11ll1_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1111_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l1l1_opy_ import bstack1lll1lllll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llllll1_opy_ import bstack1llll11lll1_opy_
from bstack_utils.helper import bstack1ll1l1lllll_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
import grpc
import traceback
import json
class bstack1lll111l111_opy_(bstack1lll1l11ll1_opy_):
    bstack1ll11lllll1_opy_ = False
    bstack1ll1l11l1l1_opy_ = bstack111lll_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᄯ")
    bstack1ll1l111l11_opy_ = bstack111lll_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᄰ")
    bstack1ll1l1llll1_opy_ = bstack111lll_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥᄱ")
    bstack1ll11ll1lll_opy_ = bstack111lll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦᄲ")
    bstack1ll11l1llll_opy_ = bstack111lll_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣᄳ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1ll1llll_opy_, bstack1lll1llllll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll1l1lll1l_opy_ = bstack1lll1llllll_opy_
        bstack1ll1ll1llll_opy_.bstack1ll11ll1l1l_opy_((bstack1111111111_opy_.bstack111111lll1_opy_, bstack11111l1ll1_opy_.PRE), self.bstack1ll1l1ll1l1_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.PRE), self.bstack1ll1ll11111_opy_)
        TestFramework.bstack1ll11ll1l1l_opy_((bstack1lll11lllll_opy_.TEST, bstack1lllll1111l_opy_.POST), self.bstack1ll11ll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11lll1_opy_(instance, args)
        test_framework = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11ll11ll_opy_)
        if bstack111lll_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬᄴ") in instance.bstack1ll11l1ll1l_opy_:
            platform_index = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l11ll1l_opy_)
            self.accessibility = self.bstack1ll11l1l11l_opy_(tags, self.config[bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᄵ")][platform_index])
        else:
            capabilities = self.bstack1ll1l1lll1l_opy_.bstack1ll11llllll_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack111lll_opy_ (u"ࠥࡳࡳࡥࡢࡦࡨࡲࡶࡪࡥࡴࡦࡵࡷ࠾ࠥࡴ࡯ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࡃࡻࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࢀࠤࡦࡸࡧࡴ࠿ࡾࡥࡷ࡭ࡳࡾࠢ࡮ࡻࡦࡸࡧࡴ࠿ࠥᄶ") + str(kwargs) + bstack111lll_opy_ (u"ࠦࠧᄷ"))
                return
            self.accessibility = self.bstack1ll11l1l11l_opy_(tags, capabilities)
        if self.bstack1ll1l1lll1l_opy_.pages and self.bstack1ll1l1lll1l_opy_.pages.values():
            bstack1ll1l1lll11_opy_ = list(self.bstack1ll1l1lll1l_opy_.pages.values())
            if bstack1ll1l1lll11_opy_ and isinstance(bstack1ll1l1lll11_opy_[0], (list, tuple)) and bstack1ll1l1lll11_opy_[0]:
                bstack1ll1l111ll1_opy_ = bstack1ll1l1lll11_opy_[0][0]
                if callable(bstack1ll1l111ll1_opy_):
                    page = bstack1ll1l111ll1_opy_()
                    def bstack11llll11l_opy_():
                        self.get_accessibility_results(page, bstack111lll_opy_ (u"ࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤᄸ"))
                    def bstack1ll11l1ll11_opy_():
                        self.get_accessibility_results_summary(page, bstack111lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᄹ"))
                    setattr(page, bstack111lll_opy_ (u"ࠢࡨࡧࡷࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡕࡩࡸࡻ࡬ࡵࡵࠥᄺ"), bstack11llll11l_opy_)
                    setattr(page, bstack111lll_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡖࡹࡲࡳࡡࡳࡻࠥᄻ"), bstack1ll11l1ll11_opy_)
        self.logger.debug(bstack111lll_opy_ (u"ࠤࡶ࡬ࡴࡻ࡬ࡥࠢࡵࡹࡳࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮ࡸࡩࡂࠨᄼ") + str(self.accessibility) + bstack111lll_opy_ (u"ࠥࠦᄽ"))
    def bstack1ll1l1ll1l1_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1llllll111l_opy_, str],
        bstack11111l1l11_opy_: Tuple[bstack1111111111_opy_, bstack11111l1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack11ll1ll1_opy_ = datetime.now()
            self.bstack1ll1l111111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼࡬ࡲ࡮ࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᄾ"), datetime.now() - bstack11ll1ll1_opy_)
            if (
                not f.bstack1ll11l1l1l1_opy_(method_name)
                or f.bstack1ll1l111l1l_opy_(method_name, *args)
                or f.bstack1ll1l11llll_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllll1l1l_opy_(instance, bstack1lll111l111_opy_.bstack1ll1l1llll1_opy_, False):
                if not bstack1lll111l111_opy_.bstack1ll11lllll1_opy_:
                    self.logger.warning(bstack111lll_opy_ (u"ࠧࡡࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࠣᄿ") + str(f.platform_index) + bstack111lll_opy_ (u"ࠨ࡝ࠡࡣ࠴࠵ࡾࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠥ࡮ࡡࡷࡧࠣࡲࡴࡺࠠࡣࡧࡨࡲࠥࡹࡥࡵࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠧᅀ"))
                    bstack1lll111l111_opy_.bstack1ll11lllll1_opy_ = True
                return
            bstack1ll1l1ll11l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l1ll11l_opy_:
                platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_, 0)
                self.logger.debug(bstack111lll_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾ࠽ࡼࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅁ") + str(f.framework_name) + bstack111lll_opy_ (u"ࠣࠤᅂ"))
                return
            bstack1ll1l11111l_opy_ = f.bstack1ll1l111lll_opy_(*args)
            if not bstack1ll1l11111l_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡧࡴࡳ࡭ࡢࡰࡧࡣࡳࡧ࡭ࡦࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࠦᅃ") + str(method_name) + bstack111lll_opy_ (u"ࠥࠦᅄ"))
                return
            bstack1ll1l1l11ll_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll111l111_opy_.bstack1ll11l1llll_opy_, False)
            if bstack1ll1l11111l_opy_ == bstack111lll_opy_ (u"ࠦ࡬࡫ࡴࠣᅅ") and not bstack1ll1l1l11ll_opy_:
                f.bstack11111ll111_opy_(instance, bstack1lll111l111_opy_.bstack1ll11l1llll_opy_, True)
                bstack1ll1l1l11ll_opy_ = True
            if not bstack1ll1l1l11ll_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠧࡴ࡯ࠡࡗࡕࡐࠥࡲ࡯ࡢࡦࡨࡨࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᅆ") + str(bstack1ll1l11111l_opy_) + bstack111lll_opy_ (u"ࠨࠢᅇ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l11111l_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack111lll_opy_ (u"ࠢ࡯ࡱࠣࡥ࠶࠷ࡹࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᅈ") + str(bstack1ll1l11111l_opy_) + bstack111lll_opy_ (u"ࠣࠤᅉ"))
                return
            self.logger.info(bstack111lll_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠣࡿࡱ࡫࡮ࠩࡵࡦࡶ࡮ࡶࡴࡴࡡࡷࡳࡤࡸࡵ࡯ࠫࢀࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࡀࠦᅊ") + str(bstack1ll1l11111l_opy_) + bstack111lll_opy_ (u"ࠥࠦᅋ"))
            scripts = [(s, bstack1ll1l1ll11l_opy_[s]) for s in scripts_to_run if s in bstack1ll1l1ll11l_opy_]
            for script_name, bstack1ll11ll1111_opy_ in scripts:
                try:
                    bstack11ll1ll1_opy_ = datetime.now()
                    if script_name == bstack111lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᅌ"):
                        result = self.perform_scan(driver, method=bstack1ll1l11111l_opy_, framework_name=f.framework_name)
                    instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽ࠦᅍ") + script_name, datetime.now() - bstack11ll1ll1_opy_)
                    if isinstance(result, dict) and not result.get(bstack111lll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᅎ"), True):
                        self.logger.warning(bstack111lll_opy_ (u"ࠢࡴ࡭࡬ࡴࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡴࡨࡱࡦ࡯࡮ࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡷ࠿ࠦࠢᅏ") + str(result) + bstack111lll_opy_ (u"ࠣࠤᅐ"))
                        break
                except Exception as e:
                    self.logger.error(bstack111lll_opy_ (u"ࠤࡨࡶࡷࡵࡲࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡸࡩࡲࡪࡲࡷࡁࢀࡹࡣࡳ࡫ࡳࡸࡤࡴࡡ࡮ࡧࢀࠤࡪࡸࡲࡰࡴࡀࠦᅑ") + str(e) + bstack111lll_opy_ (u"ࠥࠦᅒ"))
        except Exception as e:
            self.logger.error(bstack111lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡦࡺࡨࡧࡺࡺࡥࠡࡧࡵࡶࡴࡸ࠽ࠣᅓ") + str(e) + bstack111lll_opy_ (u"ࠧࠨᅔ"))
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1111l1l_opy_,
        bstack11111l1l11_opy_: Tuple[bstack1lll11lllll_opy_, bstack1lllll1111l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l11lll1_opy_(instance, args)
        capabilities = self.bstack1ll1l1lll1l_opy_.bstack1ll11llllll_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll11l1l11l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᅕ"))
            return
        driver = self.bstack1ll1l1lll1l_opy_.bstack1ll1l1111l1_opy_(f, instance, bstack11111l1l11_opy_, *args, **kwargs)
        test_name = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11l1l1ll_opy_)
        if not test_name:
            self.logger.debug(bstack111lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠ࡯ࡣࡰࡩࠧᅖ"))
            return
        test_uuid = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11lll11l_opy_)
        if not test_uuid:
            self.logger.debug(bstack111lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡷࡸ࡭ࡩࠨᅗ"))
            return
        if isinstance(self.bstack1ll1l1lll1l_opy_, bstack1lll1lllll1_opy_):
            framework_name = bstack111lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᅘ")
        else:
            framework_name = bstack111lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᅙ")
        self.bstack1ll1ll1l11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1ll1l1l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࠧᅚ"))
            return
        bstack11ll1ll1_opy_ = datetime.now()
        bstack1ll11ll1111_opy_ = self.scripts.get(framework_name, {}).get(bstack111lll_opy_ (u"ࠧࡹࡣࡢࡰࠥᅛ"), None)
        if not bstack1ll11ll1111_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡦࡥࡳ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᅜ") + str(framework_name) + bstack111lll_opy_ (u"ࠢࠡࠤᅝ"))
            return
        instance = bstack1111111l11_opy_.bstack11111l11l1_opy_(driver)
        if instance:
            if not bstack1111111l11_opy_.bstack1llllll1l1l_opy_(instance, bstack1lll111l111_opy_.bstack1ll11ll1lll_opy_, False):
                bstack1111111l11_opy_.bstack11111ll111_opy_(instance, bstack1lll111l111_opy_.bstack1ll11ll1lll_opy_, True)
            else:
                self.logger.info(bstack111lll_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡲࠥࡶࡲࡰࡩࡵࡩࡸࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᅞ") + str(method) + bstack111lll_opy_ (u"ࠤࠥᅟ"))
                return
        self.logger.info(bstack111lll_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᅠ") + str(method) + bstack111lll_opy_ (u"ࠦࠧᅡ"))
        if framework_name == bstack111lll_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᅢ"):
            result = self.bstack1ll1l1lll1l_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll11ll1111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1111_opy_, {bstack111lll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᅣ"): method if method else bstack111lll_opy_ (u"ࠢࠣᅤ")})
        bstack1llll1l1l11_opy_.end(EVENTS.bstack1ll1l1l1_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᅥ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᅦ"), True, None, command=method)
        if instance:
            bstack1111111l11_opy_.bstack11111ll111_opy_(instance, bstack1lll111l111_opy_.bstack1ll11ll1lll_opy_, False)
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢᅧ"), datetime.now() - bstack11ll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l111111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack111lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᅨ"))
            return
        bstack1ll11ll1111_opy_ = self.scripts.get(framework_name, {}).get(bstack111lll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᅩ"), None)
        if not bstack1ll11ll1111_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅪ") + str(framework_name) + bstack111lll_opy_ (u"ࠢࠣᅫ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll1ll1_opy_ = datetime.now()
        if framework_name == bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᅬ"):
            result = self.bstack1ll1l1lll1l_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll11ll1111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1111_opy_)
        instance = bstack1111111l11_opy_.bstack11111l11l1_opy_(driver)
        if instance:
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࠧᅭ"), datetime.now() - bstack11ll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1lll_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack111lll_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᅮ"))
            return
        bstack1ll11ll1111_opy_ = self.scripts.get(framework_name, {}).get(bstack111lll_opy_ (u"ࠦ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠣᅯ"), None)
        if not bstack1ll11ll1111_opy_:
            self.logger.debug(bstack111lll_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᅰ") + str(framework_name) + bstack111lll_opy_ (u"ࠨࠢᅱ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll1ll1_opy_ = datetime.now()
        if framework_name == bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᅲ"):
            result = self.bstack1ll1l1lll1l_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll11ll1111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1111_opy_)
        instance = bstack1111111l11_opy_.bstack11111l11l1_opy_(driver)
        if instance:
            instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽࠧᅳ"), datetime.now() - bstack11ll1ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1l1ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1ll11l1l111_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11ll1l11_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1ll1l11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᅴ") + str(r) + bstack111lll_opy_ (u"ࠥࠦᅵ"))
            else:
                self.bstack1ll11ll1ll1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111lll_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸ࠺ࠡࠤᅶ") + str(e) + bstack111lll_opy_ (u"ࠧࠨᅷ"))
            traceback.print_exc()
            raise e
    def bstack1ll11ll1ll1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack111lll_opy_ (u"ࠨ࡬ࡰࡣࡧࡣࡨࡵ࡮ࡧ࡫ࡪ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᅸ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l1111ll_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll1l11l1l1_opy_ and command.module == self.bstack1ll1l111l11_opy_:
                        if command.method and not command.method in bstack1ll1l1111ll_opy_:
                            bstack1ll1l1111ll_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l1111ll_opy_[command.method]:
                            bstack1ll1l1111ll_opy_[command.method][command.name] = list()
                        bstack1ll1l1111ll_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l1111ll_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1l111111_opy_(
        self,
        f: bstack1llll111lll_opy_,
        exec: Tuple[bstack1llllll111l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll1l1lll1l_opy_, bstack1lll1lllll1_opy_) and method_name != bstack111lll_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᅹ"):
            return
        if bstack1111111l11_opy_.bstack11111111ll_opy_(instance, bstack1lll111l111_opy_.bstack1ll1l1llll1_opy_):
            return
        if f.bstack1ll1l11l111_opy_(method_name, *args):
            bstack1ll11lll1ll_opy_ = False
            desired_capabilities = f.bstack1ll1l11l11l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1l1l11l1_opy_(instance)
                platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1llll111lll_opy_.bstack1ll1l11ll1l_opy_, 0)
                bstack1ll1l1l1l11_opy_ = datetime.now()
                r = self.bstack1ll11l1l111_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1lllll1l1l_opy_(bstack111lll_opy_ (u"ࠣࡩࡵࡴࡨࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᅺ"), datetime.now() - bstack1ll1l1l1l11_opy_)
                bstack1ll11lll1ll_opy_ = r.success
            else:
                self.logger.error(bstack111lll_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡨࡪࡹࡩࡳࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࡀࠦᅻ") + str(desired_capabilities) + bstack111lll_opy_ (u"ࠥࠦᅼ"))
            f.bstack11111ll111_opy_(instance, bstack1lll111l111_opy_.bstack1ll1l1llll1_opy_, bstack1ll11lll1ll_opy_)
    def bstack11lllllll1_opy_(self, test_tags):
        bstack1ll11l1l111_opy_ = self.config.get(bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᅽ"))
        if not bstack1ll11l1l111_opy_:
            return True
        try:
            include_tags = bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅾ")] if bstack111lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᅿ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᆀ")], list) else []
            exclude_tags = bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᆁ")] if bstack111lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᆂ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᆃ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack111lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᆄ") + str(error))
        return False
    def bstack111l1111l_opy_(self, caps):
        try:
            bstack1ll1l11l1ll_opy_ = caps.get(bstack111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᆅ"), {}).get(bstack111lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᆆ"), caps.get(bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᆇ"), bstack111lll_opy_ (u"ࠨࠩᆈ")))
            if bstack1ll1l11l1ll_opy_:
                self.logger.warning(bstack111lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᆉ"))
                return False
            browser = caps.get(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᆊ"), bstack111lll_opy_ (u"ࠫࠬᆋ")).lower()
            if browser != bstack111lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᆌ"):
                self.logger.warning(bstack111lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᆍ"))
                return False
            bstack1ll1l1l111l_opy_ = bstack1ll1l1ll111_opy_
            if not self.config.get(bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᆎ")) or self.config.get(bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᆏ")):
                bstack1ll1l1l111l_opy_ = bstack1ll1l1l1111_opy_
            browser_version = caps.get(bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᆐ"))
            if not browser_version:
                browser_version = caps.get(bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᆑ"), {}).get(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᆒ"), bstack111lll_opy_ (u"ࠬ࠭ᆓ"))
            if browser_version and browser_version != bstack111lll_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᆔ") and int(browser_version.split(bstack111lll_opy_ (u"ࠧ࠯ࠩᆕ"))[0]) <= bstack1ll1l1l111l_opy_:
                self.logger.warning(bstack111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥᆖ") + str(bstack1ll1l1l111l_opy_) + bstack111lll_opy_ (u"ࠤ࠱ࠦᆗ"))
                return False
            bstack1ll1l1ll1ll_opy_ = caps.get(bstack111lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᆘ"), {}).get(bstack111lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᆙ"))
            if not bstack1ll1l1ll1ll_opy_:
                bstack1ll1l1ll1ll_opy_ = caps.get(bstack111lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᆚ"), {})
            if bstack1ll1l1ll1ll_opy_ and bstack111lll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᆛ") in bstack1ll1l1ll1ll_opy_.get(bstack111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᆜ"), []):
                self.logger.warning(bstack111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᆝ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᆞ") + str(error))
            return False
    def bstack1ll11lll1l1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l1l1lll_opy_ = {
            bstack111lll_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᆟ"): test_uuid,
        }
        bstack1ll1l11ll11_opy_ = {}
        if result.success:
            bstack1ll1l11ll11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1l1lllll_opy_(bstack1ll1l1l1lll_opy_, bstack1ll1l11ll11_opy_)
    def bstack1ll1ll1l11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11llll11_opy_ = None
        try:
            self.bstack1ll11ll1l11_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111lll_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦᆠ")
            req.script_name = bstack111lll_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥᆡ")
            r = self.bstack1lll1ll1l11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack111lll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᆢ") + str(r.error) + bstack111lll_opy_ (u"ࠢࠣᆣ"))
            else:
                bstack1ll1l1l1lll_opy_ = self.bstack1ll11lll1l1_opy_(test_uuid, r)
                bstack1ll11ll1111_opy_ = r.script
            self.logger.debug(bstack111lll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫᆤ") + str(bstack1ll1l1l1lll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11ll1111_opy_:
                self.logger.debug(bstack111lll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᆥ") + str(framework_name) + bstack111lll_opy_ (u"ࠥࠤࠧᆦ"))
                return
            bstack1ll11llll11_opy_ = bstack1llll1l1l11_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1ll11lll111_opy_.value)
            self.bstack1ll11llll1l_opy_(driver, bstack1ll11ll1111_opy_, bstack1ll1l1l1lll_opy_, framework_name)
            self.logger.info(bstack111lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᆧ"))
            bstack1llll1l1l11_opy_.end(EVENTS.bstack1ll11lll111_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᆨ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᆩ"), True, None, command=bstack111lll_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᆪ"),test_name=name)
        except Exception as bstack1ll11l1lll1_opy_:
            self.logger.error(bstack111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᆫ") + bstack111lll_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧᆬ") + bstack111lll_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᆭ") + str(bstack1ll11l1lll1_opy_))
            bstack1llll1l1l11_opy_.end(EVENTS.bstack1ll11lll111_opy_.value, bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᆮ"), bstack1ll11llll11_opy_+bstack111lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᆯ"), False, bstack1ll11l1lll1_opy_, command=bstack111lll_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᆰ"),test_name=name)
    def bstack1ll11llll1l_opy_(self, driver, bstack1ll11ll1111_opy_, bstack1ll1l1l1lll_opy_, framework_name):
        if framework_name == bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᆱ"):
            self.bstack1ll1l1lll1l_opy_.bstack1ll11ll11l1_opy_(driver, bstack1ll11ll1111_opy_, bstack1ll1l1l1lll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11ll1111_opy_, bstack1ll1l1l1lll_opy_))
    def _1ll1l11lll1_opy_(self, instance: bstack1lll1111l1l_opy_, args: Tuple) -> list:
        bstack111lll_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧᆲ")
        if bstack111lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᆳ") in instance.bstack1ll11l1ll1l_opy_:
            return args[2].tags if hasattr(args[2], bstack111lll_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᆴ")) else []
        if hasattr(args[0], bstack111lll_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩᆵ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll11l1l11l_opy_(self, tags, capabilities):
        return self.bstack11lllllll1_opy_(tags) and self.bstack111l1111l_opy_(capabilities)