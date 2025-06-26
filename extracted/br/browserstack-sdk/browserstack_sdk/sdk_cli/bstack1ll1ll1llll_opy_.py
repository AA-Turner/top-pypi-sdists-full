# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1111111ll1_opy_ import (
    bstack1lllll1ll11_opy_,
    bstack1llllll1ll1_opy_,
    bstack1llllll1111_opy_,
    bstack1111111l1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll1l111l1_opy_ import bstack1ll1lllllll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_, bstack1ll1l1lll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll1ll1l1_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l11lll_opy_ import bstack1lll111l1l1_opy_
from browserstack_sdk.sdk_cli.bstack1llll11l11l_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1lllll1l_opy_ import bstack1lll111111l_opy_
from bstack_utils.helper import bstack1ll1l11111l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
import grpc
import traceback
import json
class bstack1lll11l1ll1_opy_(bstack1lll1ll1l1l_opy_):
    bstack1ll1l11ll11_opy_ = False
    bstack1ll111l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᄾ")
    bstack1ll1l111l11_opy_ = bstack11ll1l1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᄿ")
    bstack1ll1l11l1ll_opy_ = bstack11ll1l1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᅀ")
    bstack1ll1l111lll_opy_ = bstack11ll1l1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᅁ")
    bstack1ll11l11111_opy_ = bstack11ll1l1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᅂ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1l1ll1l1_opy_, bstack1ll1ll1ll1l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll11l1l111_opy_ = False
        self.bstack1ll11ll1111_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11lll11l_opy_ = bstack1ll1ll1ll1l_opy_
        bstack1ll1l1ll1l1_opy_.bstack1ll11l11lll_opy_((bstack1lllll1ll11_opy_.bstack1llllllll11_opy_, bstack1llllll1ll1_opy_.PRE), self.bstack1ll11l1ll11_opy_)
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.PRE), self.bstack1ll111l11ll_opy_)
        TestFramework.bstack1ll11l11lll_opy_((bstack1lll1ll111l_opy_.TEST, bstack1lll1111l1l_opy_.POST), self.bstack1ll11lllll1_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll111l11ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll111l11l1_opy_(instance, args)
        test_framework = f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11lll111_opy_)
        if self.bstack1ll11l1l111_opy_:
            self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᅃ")] = f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11l11l11_opy_)
        if bstack11ll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᅄ") in instance.bstack1ll11l1l1ll_opy_:
            platform_index = f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll111ll11l_opy_)
            self.accessibility = self.bstack1ll11l1ll1l_opy_(tags, self.config[bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᅅ")][platform_index])
        else:
            capabilities = self.bstack1ll11lll11l_opy_.bstack1ll11ll1ll1_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡶࡨࡷࡹࡀࠠ࡯ࡱࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢࡩࡳࡺࡴࡤࠡࡨࡲࡶࠥ࡮࡯ࡰ࡭ࡢ࡭ࡳ࡬࡯࠾ࡽ࡫ࡳࡴࡱ࡟ࡪࡰࡩࡳࢂࠦࡡࡳࡩࡶࡁࢀࡧࡲࡨࡵࢀࠤࡰࡽࡡࡳࡩࡶࡁࠧᅆ") + str(kwargs) + bstack11ll1l1_opy_ (u"ࠨࠢᅇ"))
                return
            self.accessibility = self.bstack1ll11l1ll1l_opy_(tags, capabilities)
        if self.bstack1ll11lll11l_opy_.pages and self.bstack1ll11lll11l_opy_.pages.values():
            bstack1ll1l11l111_opy_ = list(self.bstack1ll11lll11l_opy_.pages.values())
            if bstack1ll1l11l111_opy_ and isinstance(bstack1ll1l11l111_opy_[0], (list, tuple)) and bstack1ll1l11l111_opy_[0]:
                bstack1ll1l1111l1_opy_ = bstack1ll1l11l111_opy_[0][0]
                if callable(bstack1ll1l1111l1_opy_):
                    page = bstack1ll1l1111l1_opy_()
                    def bstack1llllllll_opy_():
                        self.get_accessibility_results(page, bstack11ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᅈ"))
                    def bstack1ll11ll1lll_opy_():
                        self.get_accessibility_results_summary(page, bstack11ll1l1_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᅉ"))
                    setattr(page, bstack11ll1l1_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡷࠧᅊ"), bstack1llllllll_opy_)
                    setattr(page, bstack11ll1l1_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡘࡻ࡭࡮ࡣࡵࡽࠧᅋ"), bstack1ll11ll1lll_opy_)
        self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡸ࡮࡯ࡶ࡮ࡧࠤࡷࡻ࡮ࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰࡺ࡫࠽ࠣᅌ") + str(self.accessibility) + bstack11ll1l1_opy_ (u"ࠧࠨᅍ"))
    def bstack1ll11l1ll11_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        driver: object,
        exec: Tuple[bstack1111111l1l_opy_, str],
        bstack1llllllllll_opy_: Tuple[bstack1lllll1ll11_opy_, bstack1llllll1ll1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack11ll11ll1_opy_ = datetime.now()
            self.bstack1ll111l1lll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡮ࡴࡩࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡦࡳࡳ࡬ࡩࡨࠤᅎ"), datetime.now() - bstack11ll11ll1_opy_)
            if (
                not f.bstack1ll11l1lll1_opy_(method_name)
                or f.bstack1ll1l111l1l_opy_(method_name, *args)
                or f.bstack1ll11llll1l_opy_(method_name, *args)
            ):
                return
            if not f.bstack11111111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l11l1ll_opy_, False):
                if not bstack1lll11l1ll1_opy_.bstack1ll1l11ll11_opy_:
                    self.logger.warning(bstack11ll1l1_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᅏ") + str(f.platform_index) + bstack11ll1l1_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᅐ"))
                    bstack1lll11l1ll1_opy_.bstack1ll1l11ll11_opy_ = True
                return
            bstack1ll11l11l1l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11l11l1l_opy_:
                platform_index = f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_, 0)
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᅑ") + str(f.framework_name) + bstack11ll1l1_opy_ (u"ࠥࠦᅒ"))
                return
            bstack1ll1l11lll1_opy_ = f.bstack1ll1l111ll1_opy_(*args)
            if not bstack1ll1l11lll1_opy_:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᅓ") + str(method_name) + bstack11ll1l1_opy_ (u"ࠧࠨᅔ"))
                return
            bstack1ll111l111l_opy_ = f.bstack11111111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll11l11111_opy_, False)
            if bstack1ll1l11lll1_opy_ == bstack11ll1l1_opy_ (u"ࠨࡧࡦࡶࠥᅕ") and not bstack1ll111l111l_opy_:
                f.bstack1lllll1ll1l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll11l11111_opy_, True)
                bstack1ll111l111l_opy_ = True
            if not bstack1ll111l111l_opy_ and not self.bstack1ll11l1l111_opy_:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᅖ") + str(bstack1ll1l11lll1_opy_) + bstack11ll1l1_opy_ (u"ࠣࠤᅗ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l11lll1_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᅘ") + str(bstack1ll1l11lll1_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦᅙ"))
                return
            self.logger.info(bstack11ll1l1_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᅚ") + str(bstack1ll1l11lll1_opy_) + bstack11ll1l1_opy_ (u"ࠧࠨᅛ"))
            scripts = [(s, bstack1ll11l11l1l_opy_[s]) for s in scripts_to_run if s in bstack1ll11l11l1l_opy_]
            for script_name, bstack1ll1l111111_opy_ in scripts:
                try:
                    bstack11ll11ll1_opy_ = datetime.now()
                    if script_name == bstack11ll1l1_opy_ (u"ࠨࡳࡤࡣࡱࠦᅜ"):
                        result = self.perform_scan(driver, method=bstack1ll1l11lll1_opy_, framework_name=f.framework_name)
                    instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿ࠨᅝ") + script_name, datetime.now() - bstack11ll11ll1_opy_)
                    if isinstance(result, dict) and not result.get(bstack11ll1l1_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᅞ"), True):
                        self.logger.warning(bstack11ll1l1_opy_ (u"ࠤࡶ࡯࡮ࡶࠠࡦࡺࡨࡧࡺࡺࡩ࡯ࡩࠣࡶࡪࡳࡡࡪࡰ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡹ࠺ࠡࠤᅟ") + str(result) + bstack11ll1l1_opy_ (u"ࠥࠦᅠ"))
                        break
                except Exception as e:
                    self.logger.error(bstack11ll1l1_opy_ (u"ࠦࡪࡸࡲࡰࡴࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡳࡤࡴ࡬ࡴࡹࡃࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࠦࡥࡳࡴࡲࡶࡂࠨᅡ") + str(e) + bstack11ll1l1_opy_ (u"ࠧࠨᅢ"))
        except Exception as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡨࡼࡪࡩࡵࡵࡧࠣࡩࡷࡸ࡯ࡳ࠿ࠥᅣ") + str(e) + bstack11ll1l1_opy_ (u"ࠢࠣᅤ"))
    def bstack1ll11lllll1_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1l1lll1l_opy_,
        bstack1llllllllll_opy_: Tuple[bstack1lll1ll111l_opy_, bstack1lll1111l1l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll111l11l1_opy_(instance, args)
        capabilities = self.bstack1ll11lll11l_opy_.bstack1ll11ll1ll1_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll11l1ll1l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᅥ"))
            return
        driver = self.bstack1ll11lll11l_opy_.bstack1ll11ll11ll_opy_(f, instance, bstack1llllllllll_opy_, *args, **kwargs)
        test_name = f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11ll11l1_opy_)
        if not test_name:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡱࡥࡲ࡫ࠢᅦ"))
            return
        test_uuid = f.bstack11111111ll_opy_(instance, TestFramework.bstack1ll11l11l11_opy_)
        if not test_uuid:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡹࡺ࡯ࡤࠣᅧ"))
            return
        if isinstance(self.bstack1ll11lll11l_opy_, bstack1lll1l111ll_opy_):
            framework_name = bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᅨ")
        else:
            framework_name = bstack11ll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᅩ")
        self.bstack11l1l1l1l1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack1ll1ll111l_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࠢᅪ"))
            return
        bstack11ll11ll1_opy_ = datetime.now()
        bstack1ll1l111111_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᅫ"), None)
        if not bstack1ll1l111111_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡨࡧ࡮ࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᅬ") + str(framework_name) + bstack11ll1l1_opy_ (u"ࠤࠣࠦᅭ"))
            return
        if self.bstack1ll11l1l111_opy_:
            arg = dict()
            arg[bstack11ll1l1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᅮ")] = method if method else bstack11ll1l1_opy_ (u"ࠦࠧᅯ")
            arg[bstack11ll1l1_opy_ (u"ࠧࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠧᅰ")] = self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩࠨᅱ")]
            arg[bstack11ll1l1_opy_ (u"ࠢࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠧᅲ")] = self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠣࡶࡨࡷࡹ࡮ࡵࡣࡡࡥࡹ࡮ࡲࡤࡠࡷࡸ࡭ࡩࠨᅳ")]
            arg[bstack11ll1l1_opy_ (u"ࠤࡤࡹࡹ࡮ࡈࡦࡣࡧࡩࡷࠨᅴ")] = self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠣᅵ")]
            arg[bstack11ll1l1_opy_ (u"ࠦࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠣᅶ")] = self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦᅷ")]
            arg[bstack11ll1l1_opy_ (u"ࠨࡳࡤࡣࡱࡘ࡮ࡳࡥࡴࡶࡤࡱࡵࠨᅸ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11lll1ll_opy_ = bstack1ll1l111111_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11lll1ll_opy_)
            return
        instance = bstack1llllll1111_opy_.bstack1lllll11111_opy_(driver)
        if instance:
            if not bstack1llllll1111_opy_.bstack11111111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l111lll_opy_, False):
                bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l111lll_opy_, True)
            else:
                self.logger.info(bstack11ll1l1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࡮ࡵࡩࡦࡪࡹࠡ࡫ࡱࠤࡵࡸ࡯ࡨࡴࡨࡷࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࡱࡪࡺࡨࡰࡦࡀࠦᅹ") + str(method) + bstack11ll1l1_opy_ (u"ࠣࠤᅺ"))
                return
        self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡃࠢᅻ") + str(method) + bstack11ll1l1_opy_ (u"ࠥࠦᅼ"))
        if framework_name == bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᅽ"):
            result = self.bstack1ll11lll11l_opy_.bstack1ll111llll1_opy_(driver, bstack1ll1l111111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l111111_opy_, {bstack11ll1l1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᅾ"): method if method else bstack11ll1l1_opy_ (u"ࠨࠢᅿ")})
        bstack1llll11lll1_opy_.end(EVENTS.bstack1ll1ll111l_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᆀ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᆁ"), True, None, command=method)
        if instance:
            bstack1llllll1111_opy_.bstack1lllll1ll1l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l111lll_opy_, False)
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࠨᆂ"), datetime.now() - bstack11ll11ll1_opy_)
        return result
        def bstack1ll111lll1l_opy_(self, driver: object, framework_name, bstack111111l11_opy_: str):
            self.bstack1ll11llllll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll111l1111_opy_ = self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᆃ")]
            req.bstack111111l11_opy_ = bstack111111l11_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll1l1ll1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨᆄ") + str(r) + bstack11ll1l1_opy_ (u"ࠧࠨᆅ"))
                else:
                    bstack1ll11ll111l_opy_ = json.loads(r.bstack1ll111lll11_opy_.decode(bstack11ll1l1_opy_ (u"࠭ࡵࡵࡨ࠰࠼ࠬᆆ")))
                    if bstack111111l11_opy_ == bstack11ll1l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠫᆇ"):
                        return bstack1ll11ll111l_opy_.get(bstack11ll1l1_opy_ (u"ࠣࡦࡤࡸࡦࠨᆈ"), [])
                    else:
                        return bstack1ll11ll111l_opy_.get(bstack11ll1l1_opy_ (u"ࠤࡧࡥࡹࡧࠢᆉ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack11ll1l1_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡶࡰࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࠡࡨࡵࡳࡲࠦࡣ࡭࡫࠽ࠤࠧᆊ") + str(e) + bstack11ll1l1_opy_ (u"ࠦࠧᆋ"))
    @measure(event_name=EVENTS.bstack1l1l111ll1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᆌ"))
            return
        if self.bstack1ll11l1l111_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡧࡰࡱࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᆍ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll111lll1l_opy_(driver, framework_name, bstack11ll1l1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᆎ"))
        bstack1ll1l111111_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll1l1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᆏ"), None)
        if not bstack1ll1l111111_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᆐ") + str(framework_name) + bstack11ll1l1_opy_ (u"ࠥࠦᆑ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll11ll1_opy_ = datetime.now()
        if framework_name == bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᆒ"):
            result = self.bstack1ll11lll11l_opy_.bstack1ll111llll1_opy_(driver, bstack1ll1l111111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l111111_opy_)
        instance = bstack1llllll1111_opy_.bstack1lllll11111_opy_(driver)
        if instance:
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࠣᆓ"), datetime.now() - bstack11ll11ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l1l11l1_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶࡣࡸࡻ࡭࡮ࡣࡵࡽ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᆔ"))
            return
        if self.bstack1ll11l1l111_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll111lll1l_opy_(driver, framework_name, bstack11ll1l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫᆕ"))
        bstack1ll1l111111_opy_ = self.scripts.get(framework_name, {}).get(bstack11ll1l1_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠧᆖ"), None)
        if not bstack1ll1l111111_opy_:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫ࡬࡫ࡴࡓࡧࡶࡹࡱࡺࡳࡔࡷࡰࡱࡦࡸࡹࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᆗ") + str(framework_name) + bstack11ll1l1_opy_ (u"ࠥࠦᆘ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack11ll11ll1_opy_ = datetime.now()
        if framework_name == bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᆙ"):
            result = self.bstack1ll11lll11l_opy_.bstack1ll111llll1_opy_(driver, bstack1ll1l111111_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l111111_opy_)
        instance = bstack1llllll1111_opy_.bstack1lllll11111_opy_(driver)
        if instance:
            instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳࡠࡵࡸࡱࡲࡧࡲࡺࠤᆚ"), datetime.now() - bstack11ll11ll1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll111l1l11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1ll11l1l1l1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11llllll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1l1ll1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆛ") + str(r) + bstack11ll1l1_opy_ (u"ࠢࠣᆜ"))
            else:
                self.bstack1ll111lllll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᆝ") + str(e) + bstack11ll1l1_opy_ (u"ࠤࠥᆞ"))
            traceback.print_exc()
            raise e
    def bstack1ll111lllll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡰࡴࡧࡤࡠࡥࡲࡲ࡫࡯ࡧ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤ࡫ࡵࡵ࡯ࡦࠥᆟ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll11l1l111_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡪࡸࡦࡤࡨࡵࡪ࡮ࡧࡣࡺࡻࡩࡥࠤᆠ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠧࡺࡨࡠ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠦᆡ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll11ll1111_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l11l11l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll111l1l1l_opy_ and command.module == self.bstack1ll1l111l11_opy_:
                        if command.method and not command.method in bstack1ll1l11l11l_opy_:
                            bstack1ll1l11l11l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l11l11l_opy_[command.method]:
                            bstack1ll1l11l11l_opy_[command.method][command.name] = list()
                        bstack1ll1l11l11l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l11l11l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll111l1lll_opy_(
        self,
        f: bstack1ll1lllllll_opy_,
        exec: Tuple[bstack1111111l1l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11lll11l_opy_, bstack1lll1l111ll_opy_) and method_name != bstack11ll1l1_opy_ (u"࠭ࡣࡰࡰࡱࡩࡨࡺࠧᆢ"):
            return
        if bstack1llllll1111_opy_.bstack1lllll1l111_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l11l1ll_opy_):
            return
        if f.bstack1ll11l1111l_opy_(method_name, *args):
            bstack1ll1l11llll_opy_ = False
            desired_capabilities = f.bstack1ll11l1llll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1l1111ll_opy_(instance)
                platform_index = f.bstack11111111ll_opy_(instance, bstack1ll1lllllll_opy_.bstack1ll111ll11l_opy_, 0)
                bstack1ll1l1l1111_opy_ = datetime.now()
                r = self.bstack1ll11l1l1l1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11l111ll_opy_(bstack11ll1l1_opy_ (u"ࠢࡨࡴࡳࡧ࠿ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡩ࡯࡯ࡨ࡬࡫ࠧᆣ"), datetime.now() - bstack1ll1l1l1111_opy_)
                bstack1ll1l11llll_opy_ = r.success
            else:
                self.logger.error(bstack11ll1l1_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡧࡩࡸ࡯ࡲࡦࡦࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠿ࠥᆤ") + str(desired_capabilities) + bstack11ll1l1_opy_ (u"ࠤࠥᆥ"))
            f.bstack1lllll1ll1l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l11l1ll_opy_, bstack1ll1l11llll_opy_)
    def bstack1lll11l1l1_opy_(self, test_tags):
        bstack1ll11l1l1l1_opy_ = self.config.get(bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᆦ"))
        if not bstack1ll11l1l1l1_opy_:
            return True
        try:
            include_tags = bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᆧ")] if bstack11ll1l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᆨ") in bstack1ll11l1l1l1_opy_ and isinstance(bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᆩ")], list) else []
            exclude_tags = bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᆪ")] if bstack11ll1l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᆫ") in bstack1ll11l1l1l1_opy_ and isinstance(bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᆬ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᆭ") + str(error))
        return False
    def bstack11l11l1l1l_opy_(self, caps):
        try:
            if self.bstack1ll11l1l111_opy_:
                bstack1ll11llll11_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᆮ"))
                if bstack1ll11llll11_opy_ is not None and str(bstack1ll11llll11_opy_).lower() == bstack11ll1l1_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᆯ"):
                    bstack1ll111ll1l1_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᆰ")) or caps.get(bstack11ll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᆱ"))
                    if bstack1ll111ll1l1_opy_ is not None and int(bstack1ll111ll1l1_opy_) < 11:
                        self.logger.warning(bstack11ll1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡃࡱࡨࡷࡵࡩࡥࠢ࠴࠵ࠥࡧ࡮ࡥࠢࡤࡦࡴࡼࡥ࠯ࠢࡆࡹࡷࡸࡥ࡯ࡶࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦ࠽ࠣᆲ") + str(bstack1ll111ll1l1_opy_) + bstack11ll1l1_opy_ (u"ࠤࠥᆳ"))
                        return False
                return True
            bstack1ll1l11ll1l_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᆴ"), {}).get(bstack11ll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᆵ"), caps.get(bstack11ll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᆶ"), bstack11ll1l1_opy_ (u"࠭ࠧᆷ")))
            if bstack1ll1l11ll1l_opy_:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᆸ"))
                return False
            browser = caps.get(bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᆹ"), bstack11ll1l1_opy_ (u"ࠩࠪᆺ")).lower()
            if browser != bstack11ll1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᆻ"):
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᆼ"))
                return False
            bstack1ll1l11l1l1_opy_ = bstack1ll11ll1l11_opy_
            if not self.config.get(bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᆽ")) or self.config.get(bstack11ll1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪᆾ")):
                bstack1ll1l11l1l1_opy_ = bstack1ll11lll1l1_opy_
            browser_version = caps.get(bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᆿ"))
            if not browser_version:
                browser_version = caps.get(bstack11ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᇀ"), {}).get(bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᇁ"), bstack11ll1l1_opy_ (u"ࠪࠫᇂ"))
            if browser_version and browser_version != bstack11ll1l1_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᇃ") and int(browser_version.split(bstack11ll1l1_opy_ (u"ࠬ࠴ࠧᇄ"))[0]) <= bstack1ll1l11l1l1_opy_:
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࠣᇅ") + str(bstack1ll1l11l1l1_opy_) + bstack11ll1l1_opy_ (u"ࠢ࠯ࠤᇆ"))
                return False
            bstack1ll11ll1l1l_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᇇ"), {}).get(bstack11ll1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇈ"))
            if not bstack1ll11ll1l1l_opy_:
                bstack1ll11ll1l1l_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᇉ"), {})
            if bstack1ll11ll1l1l_opy_ and bstack11ll1l1_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᇊ") in bstack1ll11ll1l1l_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᇋ"), []):
                self.logger.warning(bstack11ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᇌ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᇍ") + str(error))
            return False
    def bstack1ll11l111l1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll111ll111_opy_ = {
            bstack11ll1l1_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨᇎ"): test_uuid,
        }
        bstack1ll1l1l111l_opy_ = {}
        if result.success:
            bstack1ll1l1l111l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1l11111l_opy_(bstack1ll111ll111_opy_, bstack1ll1l1l111l_opy_)
    def bstack11l1l1l1l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11l111ll_opy_ = None
        try:
            self.bstack1ll11llllll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack11ll1l1_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᇏ")
            req.script_name = bstack11ll1l1_opy_ (u"ࠥࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠣᇐ")
            r = self.bstack1lll1l1ll1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠦࡷ࡫ࡣࡦ࡫ࡹࡩࡩࠦࡤࡳ࡫ࡹࡩࡷࠦࡥࡹࡧࡦࡹࡹ࡫ࠠࡱࡣࡵࡥࡲࡹࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᇑ") + str(r.error) + bstack11ll1l1_opy_ (u"ࠧࠨᇒ"))
            else:
                bstack1ll111ll111_opy_ = self.bstack1ll11l111l1_opy_(test_uuid, r)
                bstack1ll1l111111_opy_ = r.script
            self.logger.debug(bstack11ll1l1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᇓ") + str(bstack1ll111ll111_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l111111_opy_:
                self.logger.debug(bstack11ll1l1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᇔ") + str(framework_name) + bstack11ll1l1_opy_ (u"ࠣࠢࠥᇕ"))
                return
            bstack1ll11l111ll_opy_ = bstack1llll11lll1_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack1ll11l1l11l_opy_.value)
            self.bstack1ll11l11ll1_opy_(driver, bstack1ll1l111111_opy_, bstack1ll111ll111_opy_, framework_name)
            self.logger.info(bstack11ll1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᇖ"))
            bstack1llll11lll1_opy_.end(EVENTS.bstack1ll11l1l11l_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᇗ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᇘ"), True, None, command=bstack11ll1l1_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪᇙ"),test_name=name)
        except Exception as bstack1ll111l1ll1_opy_:
            self.logger.error(bstack11ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᇚ") + bstack11ll1l1_opy_ (u"ࠢࡴࡶࡵࠬࡵࡧࡴࡩࠫࠥᇛ") + bstack11ll1l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᇜ") + str(bstack1ll111l1ll1_opy_))
            bstack1llll11lll1_opy_.end(EVENTS.bstack1ll11l1l11l_opy_.value, bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᇝ"), bstack1ll11l111ll_opy_+bstack11ll1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᇞ"), False, bstack1ll111l1ll1_opy_, command=bstack11ll1l1_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩᇟ"),test_name=name)
    def bstack1ll11l11ll1_opy_(self, driver, bstack1ll1l111111_opy_, bstack1ll111ll111_opy_, framework_name):
        if framework_name == bstack11ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᇠ"):
            self.bstack1ll11lll11l_opy_.bstack1ll111llll1_opy_(driver, bstack1ll1l111111_opy_, bstack1ll111ll111_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l111111_opy_, bstack1ll111ll111_opy_))
    def _1ll111l11l1_opy_(self, instance: bstack1ll1l1lll1l_opy_, args: Tuple) -> list:
        bstack11ll1l1_opy_ (u"ࠨࠢࠣࡇࡻࡸࡷࡧࡣࡵࠢࡷࡥ࡬ࡹࠠࡣࡣࡶࡩࡩࠦ࡯࡯ࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࠮ࠣࠤࠥᇡ")
        if bstack11ll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᇢ") in instance.bstack1ll11l1l1ll_opy_:
            return args[2].tags if hasattr(args[2], bstack11ll1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᇣ")) else []
        if hasattr(args[0], bstack11ll1l1_opy_ (u"ࠩࡲࡻࡳࡥ࡭ࡢࡴ࡮ࡩࡷࡹࠧᇤ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll11l1ll1l_opy_(self, tags, capabilities):
        return self.bstack1lll11l1l1_opy_(tags) and self.bstack11l11l1l1l_opy_(capabilities)