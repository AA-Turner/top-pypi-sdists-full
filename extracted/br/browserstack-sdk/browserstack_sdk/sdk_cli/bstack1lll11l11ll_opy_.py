# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import (
    bstack1lllll1l111_opy_,
    bstack1lllll1llll_opy_,
    bstack1llllll1lll_opy_,
    bstack1111111111_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1ll111ll_opy_ import bstack1llll111lll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_, bstack1lll1l1l1l1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1llll111111_opy_ import bstack1llll11l1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1lll1llll1l_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1lll1ll1l1l_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l11l_opy_ import bstack1ll1lllllll_opy_
from bstack_utils.helper import bstack1ll11lll111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
import grpc
import traceback
import json
class bstack1ll1lll1l11_opy_(bstack1llll11l1ll_opy_):
    bstack1ll11l1llll_opy_ = False
    bstack1ll11l1l1l1_opy_ = bstack1l1l1l1_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᄾ")
    bstack1ll11l11l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᄿ")
    bstack1ll1l11llll_opy_ = bstack1l1l1l1_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᅀ")
    bstack1ll111lll11_opy_ = bstack1l1l1l1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᅁ")
    bstack1ll11ll1l1l_opy_ = bstack1l1l1l1_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᅂ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1lll1ll1_opy_, bstack1lll1ll111l_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll11l1lll1_opy_ = bstack1lll1ll111l_opy_
        bstack1ll1lll1ll1_opy_.bstack1ll111lll1l_opy_((bstack1lllll1l111_opy_.bstack1lllll11111_opy_, bstack1lllll1llll_opy_.PRE), self.bstack1ll11llllll_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.PRE), self.bstack1ll11l1l111_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1ll1ll11l11_opy_.TEST, bstack1lll1lll111_opy_.POST), self.bstack1ll1l11ll1l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l1l111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l111lll_opy_(instance, args)
        test_framework = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11l1l1_opy_)
        if bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᅃ") in instance.bstack1ll1l111ll1_opy_:
            platform_index = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll111ll1ll_opy_)
            self.accessibility = self.bstack1ll111lllll_opy_(tags, self.config[bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᅄ")][platform_index])
        else:
            capabilities = self.bstack1ll11l1lll1_opy_.bstack1ll11ll1lll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᅅ") + str(kwargs) + bstack1l1l1l1_opy_ (u"ࠧࠨᅆ"))
                return
            self.accessibility = self.bstack1ll111lllll_opy_(tags, capabilities)
        if self.bstack1ll11l1lll1_opy_.pages and self.bstack1ll11l1lll1_opy_.pages.values():
            bstack1ll11l11l11_opy_ = list(self.bstack1ll11l1lll1_opy_.pages.values())
            if bstack1ll11l11l11_opy_ and isinstance(bstack1ll11l11l11_opy_[0], (list, tuple)) and bstack1ll11l11l11_opy_[0]:
                bstack1ll1l111111_opy_ = bstack1ll11l11l11_opy_[0][0]
                if callable(bstack1ll1l111111_opy_):
                    page = bstack1ll1l111111_opy_()
                    def bstack1ll1111111_opy_():
                        self.get_accessibility_results(page, bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᅇ"))
                    def bstack1ll11ll1ll1_opy_():
                        self.get_accessibility_results_summary(page, bstack1l1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᅈ"))
                    setattr(page, bstack1l1l1l1_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᅉ"), bstack1ll1111111_opy_)
                    setattr(page, bstack1l1l1l1_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᅊ"), bstack1ll11ll1ll1_opy_)
        self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᅋ") + str(self.accessibility) + bstack1l1l1l1_opy_ (u"ࠦࠧᅌ"))
    def bstack1ll11llllll_opy_(
        self,
        f: bstack1llll111lll_opy_,
        driver: object,
        exec: Tuple[bstack1111111111_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll1l111_opy_, bstack1lllll1llll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1ll1l1ll_opy_ = datetime.now()
            self.bstack1ll11llll11_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᅍ"), datetime.now() - bstack1l1ll1l1ll_opy_)
            if (
                not f.bstack1ll11l111ll_opy_(method_name)
                or f.bstack1ll1l11ll11_opy_(method_name, *args)
                or f.bstack1ll1l1l111l_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lllll1ll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll1l11llll_opy_, False):
                if not bstack1ll1lll1l11_opy_.bstack1ll11l1llll_opy_:
                    self.logger.warning(bstack1l1l1l1_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᅎ") + str(f.platform_index) + bstack1l1l1l1_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᅏ"))
                    bstack1ll1lll1l11_opy_.bstack1ll11l1llll_opy_ = True
                return
            bstack1ll1l11l111_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l11l111_opy_:
                platform_index = f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_, 0)
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᅐ") + str(f.framework_name) + bstack1l1l1l1_opy_ (u"ࠤࠥᅑ"))
                return
            bstack1ll11lll1l1_opy_ = f.bstack1ll11l1ll11_opy_(*args)
            if not bstack1ll11lll1l1_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧᅒ") + str(method_name) + bstack1l1l1l1_opy_ (u"ࠦࠧᅓ"))
                return
            bstack1ll11l11111_opy_ = f.bstack1lllll1ll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll11ll1l1l_opy_, False)
            if bstack1ll11lll1l1_opy_ == bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࠤᅔ") and not bstack1ll11l11111_opy_:
                f.bstack1lllll1111l_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll11ll1l1l_opy_, True)
                bstack1ll11l11111_opy_ = True
            if not bstack1ll11l11111_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡮ࡰࠢࡘࡖࡑࠦ࡬ࡰࡣࡧࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᅕ") + str(bstack1ll11lll1l1_opy_) + bstack1l1l1l1_opy_ (u"ࠢࠣᅖ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll11lll1l1_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᅗ") + str(bstack1ll11lll1l1_opy_) + bstack1l1l1l1_opy_ (u"ࠤࠥᅘ"))
                return
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡶࡧࡷ࡯ࡰࡵࡵࡢࡸࡴࡥࡲࡶࡰࠬࢁࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᅙ") + str(bstack1ll11lll1l1_opy_) + bstack1l1l1l1_opy_ (u"ࠦࠧᅚ"))
            scripts = [(s, bstack1ll1l11l111_opy_[s]) for s in scripts_to_run if s in bstack1ll1l11l111_opy_]
            for script_name, bstack1ll11l111l1_opy_ in scripts:
                try:
                    bstack1l1ll1l1ll_opy_ = datetime.now()
                    if script_name == bstack1l1l1l1_opy_ (u"ࠧࡹࡣࡢࡰࠥᅛ"):
                        result = self.perform_scan(driver, method=bstack1ll11lll1l1_opy_, framework_name=f.framework_name)
                    instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࠧᅜ") + script_name, datetime.now() - bstack1l1ll1l1ll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l1l1l1_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᅝ"), True):
                        self.logger.warning(bstack1l1l1l1_opy_ (u"ࠣࡵ࡮࡭ࡵࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡵࡩࡲࡧࡩ࡯࡫ࡱ࡫ࠥࡹࡣࡳ࡫ࡳࡸࡸࡀࠠࠣᅞ") + str(result) + bstack1l1l1l1_opy_ (u"ࠤࠥᅟ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡹࡣࡳ࡫ࡳࡸࡂࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁࠥ࡫ࡲࡳࡱࡵࡁࠧᅠ") + str(e) + bstack1l1l1l1_opy_ (u"ࠦࠧᅡ"))
        except Exception as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦࠢࡨࡶࡷࡵࡲ࠾ࠤᅢ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢᅣ"))
    def bstack1ll1l11ll1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1l1l1_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1ll1ll11l11_opy_, bstack1lll1lll111_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1l111lll_opy_(instance, args)
        capabilities = self.bstack1ll11l1lll1_opy_.bstack1ll11ll1lll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll111lllll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᅤ"))
            return
        driver = self.bstack1ll11l1lll1_opy_.bstack1ll1l1111l1_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        test_name = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll111llll1_opy_)
        if not test_name:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᅥ"))
            return
        test_uuid = f.bstack1lllll1ll11_opy_(instance, TestFramework.bstack1ll1l11lll1_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢᅦ"))
            return
        if isinstance(self.bstack1ll11l1lll1_opy_, bstack1lll1ll1l1l_opy_):
            framework_name = bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᅧ")
        else:
            framework_name = bstack1l1l1l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᅨ")
        self.bstack1ll1lll111_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1111l11l_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࠨᅩ"))
            return
        bstack1l1ll1l1ll_opy_ = datetime.now()
        bstack1ll11l111l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠨࡳࡤࡣࡱࠦᅪ"), None)
        if not bstack1ll11l111l1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡧࡦࡴࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᅫ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠣࠢࠥᅬ"))
            return
        instance = bstack1llllll1lll_opy_.bstack1llllllllll_opy_(driver)
        if instance:
            if not bstack1llllll1lll_opy_.bstack1lllll1ll11_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll111lll11_opy_, False):
                bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll111lll11_opy_, True)
            else:
                self.logger.info(bstack1l1l1l1_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᅭ") + str(method) + bstack1l1l1l1_opy_ (u"ࠥࠦᅮ"))
                return
        self.logger.info(bstack1l1l1l1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᅯ") + str(method) + bstack1l1l1l1_opy_ (u"ࠧࠨᅰ"))
        if framework_name == bstack1l1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᅱ"):
            result = self.bstack1ll11l1lll1_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll11l111l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11l111l1_opy_, {bstack1l1l1l1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᅲ"): method if method else bstack1l1l1l1_opy_ (u"ࠣࠤᅳ")})
        bstack1lll1ll11l1_opy_.end(EVENTS.bstack1111l11l_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᅴ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᅵ"), True, None, command=method)
        if instance:
            bstack1llllll1lll_opy_.bstack1lllll1111l_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll111lll11_opy_, False)
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᅶ"), datetime.now() - bstack1l1ll1l1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll111l11l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᅷ"))
            return
        bstack1ll11l111l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᅸ"), None)
        if not bstack1ll11l111l1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᅹ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠣࠤᅺ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1ll1l1ll_opy_ = datetime.now()
        if framework_name == bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᅻ"):
            result = self.bstack1ll11l1lll1_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll11l111l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11l111l1_opy_)
        instance = bstack1llllll1lll_opy_.bstack1llllllllll_opy_(driver)
        if instance:
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᅼ"), datetime.now() - bstack1l1ll1l1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l11lll1_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᅽ"))
            return
        bstack1ll11l111l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l1l1l1_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᅾ"), None)
        if not bstack1ll11l111l1_opy_:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅿ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠢࠣᆀ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1ll1l1ll_opy_ = datetime.now()
        if framework_name == bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᆁ"):
            result = self.bstack1ll11l1lll1_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll11l111l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11l111l1_opy_)
        instance = bstack1llllll1lll_opy_.bstack1llllllllll_opy_(driver)
        if instance:
            instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᆂ"), datetime.now() - bstack1l1ll1l1ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll11lll11l_opy_, stage=STAGE.bstack1l1lll1lll_opy_)
    def bstack1ll11lllll1_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll11l1l1ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1ll1ll111l1_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᆃ") + str(r) + bstack1l1l1l1_opy_ (u"ࠦࠧᆄ"))
            else:
                self.bstack1ll1l111l1l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᆅ") + str(e) + bstack1l1l1l1_opy_ (u"ࠨࠢᆆ"))
            traceback.print_exc()
            raise e
    def bstack1ll1l111l1l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᆇ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11ll1111_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11l1l1l1_opy_ and command.module == self.bstack1ll11l11l1l_opy_:
                        if command.method and not command.method in bstack1ll11ll1111_opy_:
                            bstack1ll11ll1111_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11ll1111_opy_[command.method]:
                            bstack1ll11ll1111_opy_[command.method][command.name] = list()
                        bstack1ll11ll1111_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11ll1111_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll11llll11_opy_(
        self,
        f: bstack1llll111lll_opy_,
        exec: Tuple[bstack1111111111_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11l1lll1_opy_, bstack1lll1ll1l1l_opy_) and method_name != bstack1l1l1l1_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᆈ"):
            return
        if bstack1llllll1lll_opy_.bstack1lllllll1ll_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll1l11llll_opy_):
            return
        if f.bstack1ll111ll11l_opy_(method_name, *args):
            bstack1ll1l1111ll_opy_ = False
            desired_capabilities = f.bstack1ll11l1l11l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11ll11ll_opy_(instance)
                platform_index = f.bstack1lllll1ll11_opy_(instance, bstack1llll111lll_opy_.bstack1ll111ll1ll_opy_, 0)
                bstack1ll1l11111l_opy_ = datetime.now()
                r = self.bstack1ll11lllll1_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l1l1ll111_opy_(bstack1l1l1l1_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᆉ"), datetime.now() - bstack1ll1l11111l_opy_)
                bstack1ll1l1111ll_opy_ = r.success
            else:
                self.logger.error(bstack1l1l1l1_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡩ࡫ࡳࡪࡴࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࡁࠧᆊ") + str(desired_capabilities) + bstack1l1l1l1_opy_ (u"ࠦࠧᆋ"))
            f.bstack1lllll1111l_opy_(instance, bstack1ll1lll1l11_opy_.bstack1ll1l11llll_opy_, bstack1ll1l1111ll_opy_)
    def bstack11lll1llll_opy_(self, test_tags):
        bstack1ll11lllll1_opy_ = self.config.get(bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᆌ"))
        if not bstack1ll11lllll1_opy_:
            return True
        try:
            include_tags = bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᆍ")] if bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᆎ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᆏ")], list) else []
            exclude_tags = bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᆐ")] if bstack1l1l1l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᆑ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᆒ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᆓ") + str(error))
        return False
    def bstack11ll1l1l1_opy_(self, caps):
        try:
            bstack1ll1l11l11l_opy_ = caps.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᆔ"), {}).get(bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᆕ"), caps.get(bstack1l1l1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᆖ"), bstack1l1l1l1_opy_ (u"ࠩࠪᆗ")))
            if bstack1ll1l11l11l_opy_:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᆘ"))
                return False
            browser = caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᆙ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ᆚ")).lower()
            if browser != bstack1l1l1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᆛ"):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᆜ"))
                return False
            bstack1ll1l11l1ll_opy_ = bstack1ll11ll11l1_opy_
            if not self.config.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᆝ")) or self.config.get(bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭ᆞ")):
                bstack1ll1l11l1ll_opy_ = bstack1ll11llll1l_opy_
            browser_version = caps.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᆟ"))
            if not browser_version:
                browser_version = caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᆠ"), {}).get(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᆡ"), bstack1l1l1l1_opy_ (u"࠭ࠧᆢ"))
            if browser_version and browser_version != bstack1l1l1l1_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᆣ") and int(browser_version.split(bstack1l1l1l1_opy_ (u"ࠨ࠰ࠪᆤ"))[0]) <= bstack1ll1l11l1ll_opy_:
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࠦᆥ") + str(bstack1ll1l11l1ll_opy_) + bstack1l1l1l1_opy_ (u"ࠥ࠲ࠧᆦ"))
                return False
            bstack1ll1l111l11_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᆧ"), {}).get(bstack1l1l1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᆨ"))
            if not bstack1ll1l111l11_opy_:
                bstack1ll1l111l11_opy_ = caps.get(bstack1l1l1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᆩ"), {})
            if bstack1ll1l111l11_opy_ and bstack1l1l1l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᆪ") in bstack1ll1l111l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᆫ"), []):
                self.logger.warning(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᆬ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᆭ") + str(error))
            return False
    def bstack1ll11ll1l11_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll11l11lll_opy_ = {
            bstack1l1l1l1_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᆮ"): test_uuid,
        }
        bstack1ll11l1111l_opy_ = {}
        if result.success:
            bstack1ll11l1111l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll11lll111_opy_(bstack1ll11l11lll_opy_, bstack1ll11l1111l_opy_)
    def bstack1ll1lll111_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll111ll1l1_opy_ = None
        try:
            self.bstack1ll11l1l1ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l1l1l1_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠧᆯ")
            req.script_name = bstack1l1l1l1_opy_ (u"ࠨࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠦᆰ")
            r = self.bstack1ll1ll111l1_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡧࡶ࡮ࡼࡥࡳࠢࡨࡼࡪࡩࡵࡵࡧࠣࡴࡦࡸࡡ࡮ࡵࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᆱ") + str(r.error) + bstack1l1l1l1_opy_ (u"ࠣࠤᆲ"))
            else:
                bstack1ll11l11lll_opy_ = self.bstack1ll11ll1l11_opy_(test_uuid, r)
                bstack1ll11l111l1_opy_ = r.script
            self.logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᆳ") + str(bstack1ll11l11lll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11l111l1_opy_:
                self.logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᆴ") + str(framework_name) + bstack1l1l1l1_opy_ (u"ࠦࠥࠨᆵ"))
                return
            bstack1ll111ll1l1_opy_ = bstack1lll1ll11l1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1ll11lll1ll_opy_.value)
            self.bstack1ll11l11ll1_opy_(driver, bstack1ll11l111l1_opy_, bstack1ll11l11lll_opy_, framework_name)
            self.logger.info(bstack1l1l1l1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᆶ"))
            bstack1lll1ll11l1_opy_.end(EVENTS.bstack1ll11lll1ll_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᆷ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᆸ"), True, None, command=bstack1l1l1l1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᆹ"),test_name=name)
        except Exception as bstack1ll11ll111l_opy_:
            self.logger.error(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᆺ") + bstack1l1l1l1_opy_ (u"ࠥࡷࡹࡸࠨࡱࡣࡷ࡬࠮ࠨᆻ") + bstack1l1l1l1_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᆼ") + str(bstack1ll11ll111l_opy_))
            bstack1lll1ll11l1_opy_.end(EVENTS.bstack1ll11lll1ll_opy_.value, bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᆽ"), bstack1ll111ll1l1_opy_+bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᆾ"), False, bstack1ll11ll111l_opy_, command=bstack1l1l1l1_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᆿ"),test_name=name)
    def bstack1ll11l11ll1_opy_(self, driver, bstack1ll11l111l1_opy_, bstack1ll11l11lll_opy_, framework_name):
        if framework_name == bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᇀ"):
            self.bstack1ll11l1lll1_opy_.bstack1ll1l1l1111_opy_(driver, bstack1ll11l111l1_opy_, bstack1ll11l11lll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11l111l1_opy_, bstack1ll11l11lll_opy_))
    def _1ll1l111lll_opy_(self, instance: bstack1lll1l1l1l1_opy_, args: Tuple) -> list:
        bstack1l1l1l1_opy_ (u"ࠤࠥࠦࡊࡾࡴࡳࡣࡦࡸࠥࡺࡡࡨࡵࠣࡦࡦࡹࡥࡥࠢࡲࡲࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࠱ࠦࠧࠨᇁ")
        if bstack1l1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧᇂ") in instance.bstack1ll1l111ll1_opy_:
            return args[2].tags if hasattr(args[2], bstack1l1l1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᇃ")) else []
        if hasattr(args[0], bstack1l1l1l1_opy_ (u"ࠬࡵࡷ࡯ࡡࡰࡥࡷࡱࡥࡳࡵࠪᇄ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll111lllll_opy_(self, tags, capabilities):
        return self.bstack11lll1llll_opy_(tags) and self.bstack11ll1l1l1_opy_(capabilities)