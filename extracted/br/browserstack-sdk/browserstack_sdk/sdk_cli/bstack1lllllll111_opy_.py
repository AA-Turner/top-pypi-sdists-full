# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack11111111l1_opy_ import (
    bstack111111lll1_opy_,
    bstack111111l1l1_opy_,
    bstack111111l11l_opy_,
    bstack11111111ll_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l11ll_opy_ import bstack1lll1lll1l1_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_, bstack1lll1lllll1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll11lll1l_opy_ import bstack1llll111111_opy_
from browserstack_sdk.sdk_cli.bstack1lll1ll11l1_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.bstack1llll1ll1ll_opy_ import bstack1lll11llll1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1llll1ll_opy_ import bstack1lll111ll11_opy_
from bstack_utils.helper import bstack1ll1l1l1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
import grpc
import traceback
import json
class bstack1lll11l1ll1_opy_(bstack1llll111111_opy_):
    bstack1ll1ll1111l_opy_ = False
    bstack1ll11llll11_opy_ = bstack1l11lll_opy_ (u"ࠦࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤჿ")
    bstack1ll1l11lll1_opy_ = bstack1l11lll_opy_ (u"ࠧࡸࡥ࡮ࡱࡷࡩ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᄀ")
    bstack1ll1l1l1l11_opy_ = bstack1l11lll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩ࡯࡫ࡷࠦᄁ")
    bstack1ll1l1l111l_opy_ = bstack1l11lll_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡵࡢࡷࡨࡧ࡮࡯࡫ࡱ࡫ࠧᄂ")
    bstack1ll1l1lllll_opy_ = bstack1l11lll_opy_ (u"ࠣࡦࡵ࡭ࡻ࡫ࡲࡠࡪࡤࡷࡤࡻࡲ࡭ࠤᄃ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1lllll1l_opy_, bstack1lll1ll1lll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        if not self.is_enabled():
            return
        self.bstack1ll11lllll1_opy_ = bstack1lll1ll1lll_opy_
        bstack1ll1lllll1l_opy_.bstack1ll1ll11l1l_opy_((bstack111111lll1_opy_.bstack1111l11ll1_opy_, bstack111111l1l1_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.PRE), self.bstack1ll1ll1ll11_opy_)
        TestFramework.bstack1ll1ll11l1l_opy_((bstack1llll1111ll_opy_.TEST, bstack1lll1l1l11l_opy_.POST), self.bstack1ll1ll11111_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1ll1ll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1ll111ll_opy_(instance, args)
        test_framework = f.bstack1111111111_opy_(instance, TestFramework.bstack1ll1l1ll111_opy_)
        if bstack1l11lll_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᄄ") in instance.bstack1ll1l11ll11_opy_:
            platform_index = f.bstack1111111111_opy_(instance, TestFramework.bstack1ll1l111lll_opy_)
            self.accessibility = self.bstack1ll1ll1llll_opy_(tags, self.config[bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᄅ")][platform_index])
        else:
            capabilities = self.bstack1ll11lllll1_opy_.bstack1ll1l1ll1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᄆ") + str(kwargs) + bstack1l11lll_opy_ (u"ࠧࠨᄇ"))
                return
            self.accessibility = self.bstack1ll1ll1llll_opy_(tags, capabilities)
        if self.bstack1ll11lllll1_opy_.pages and self.bstack1ll11lllll1_opy_.pages.values():
            bstack1ll1l1111ll_opy_ = list(self.bstack1ll11lllll1_opy_.pages.values())
            if bstack1ll1l1111ll_opy_ and isinstance(bstack1ll1l1111ll_opy_[0], (list, tuple)) and bstack1ll1l1111ll_opy_[0]:
                bstack1ll1ll1ll1l_opy_ = bstack1ll1l1111ll_opy_[0][0]
                if callable(bstack1ll1ll1ll1l_opy_):
                    page = bstack1ll1ll1ll1l_opy_()
                    def bstack11lll1111l_opy_():
                        self.get_accessibility_results(page, bstack1l11lll_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᄈ"))
                    def bstack1ll1l1l11l1_opy_():
                        self.get_accessibility_results_summary(page, bstack1l11lll_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᄉ"))
                    setattr(page, bstack1l11lll_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᄊ"), bstack11lll1111l_opy_)
                    setattr(page, bstack1l11lll_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᄋ"), bstack1ll1l1l11l1_opy_)
        self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᄌ") + str(self.accessibility) + bstack1l11lll_opy_ (u"ࠦࠧᄍ"))
    def bstack1ll1l111l1l_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        driver: object,
        exec: Tuple[bstack11111111ll_opy_, str],
        bstack11111l11ll_opy_: Tuple[bstack111111lll1_opy_, bstack111111l1l1_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll1ll11ll_opy_ = datetime.now()
            self.bstack1ll1l11l11l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᄎ"), datetime.now() - bstack1ll1ll11ll_opy_)
            if (
                not f.bstack1ll1l1ll1l1_opy_(method_name)
                or f.bstack1ll1ll11ll1_opy_(method_name, *args)
                or f.bstack1ll11lll1l1_opy_(method_name, *args)
            ):
                return
            if not f.bstack1111111111_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1l1l11_opy_, False):
                if not bstack1lll11l1ll1_opy_.bstack1ll1ll1111l_opy_:
                    self.logger.warning(bstack1l11lll_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᄏ") + str(f.platform_index) + bstack1l11lll_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᄐ"))
                    bstack1lll11l1ll1_opy_.bstack1ll1ll1111l_opy_ = True
                return
            bstack1ll1l111l11_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll1l111l11_opy_:
                platform_index = f.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1ll1l111lll_opy_, 0)
                self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᄑ") + str(f.framework_name) + bstack1l11lll_opy_ (u"ࠤࠥᄒ"))
                return
            bstack1ll11lll11l_opy_ = f.bstack1ll1l111111_opy_(*args)
            if not bstack1ll11lll11l_opy_:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧᄓ") + str(method_name) + bstack1l11lll_opy_ (u"ࠦࠧᄔ"))
                return
            bstack1ll1l11111l_opy_ = f.bstack1111111111_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1lllll_opy_, False)
            if bstack1ll11lll11l_opy_ == bstack1l11lll_opy_ (u"ࠧ࡭ࡥࡵࠤᄕ") and not bstack1ll1l11111l_opy_:
                f.bstack1111l111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1lllll_opy_, True)
                bstack1ll1l11111l_opy_ = True
            if not bstack1ll1l11111l_opy_:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡮ࡰࠢࡘࡖࡑࠦ࡬ࡰࡣࡧࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᄖ") + str(bstack1ll11lll11l_opy_) + bstack1l11lll_opy_ (u"ࠢࠣᄗ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll11lll11l_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᄘ") + str(bstack1ll11lll11l_opy_) + bstack1l11lll_opy_ (u"ࠤࠥᄙ"))
                return
            self.logger.info(bstack1l11lll_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡶࡧࡷ࡯ࡰࡵࡵࡢࡸࡴࡥࡲࡶࡰࠬࢁࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᄚ") + str(bstack1ll11lll11l_opy_) + bstack1l11lll_opy_ (u"ࠦࠧᄛ"))
            scripts = [(s, bstack1ll1l111l11_opy_[s]) for s in scripts_to_run if s in bstack1ll1l111l11_opy_]
            for script_name, bstack1ll1l1llll1_opy_ in scripts:
                try:
                    bstack1ll1ll11ll_opy_ = datetime.now()
                    if script_name == bstack1l11lll_opy_ (u"ࠧࡹࡣࡢࡰࠥᄜ"):
                        result = self.perform_scan(driver, method=bstack1ll11lll11l_opy_, framework_name=f.framework_name)
                    instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࠧᄝ") + script_name, datetime.now() - bstack1ll1ll11ll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1l11lll_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᄞ"), True):
                        self.logger.warning(bstack1l11lll_opy_ (u"ࠣࡵ࡮࡭ࡵࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡵࡩࡲࡧࡩ࡯࡫ࡱ࡫ࠥࡹࡣࡳ࡫ࡳࡸࡸࡀࠠࠣᄟ") + str(result) + bstack1l11lll_opy_ (u"ࠤࠥᄠ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1l11lll_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡹࡣࡳ࡫ࡳࡸࡂࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁࠥ࡫ࡲࡳࡱࡵࡁࠧᄡ") + str(e) + bstack1l11lll_opy_ (u"ࠦࠧᄢ"))
        except Exception as e:
            self.logger.error(bstack1l11lll_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦࠢࡨࡶࡷࡵࡲ࠾ࠤᄣ") + str(e) + bstack1l11lll_opy_ (u"ࠨࠢᄤ"))
    def bstack1ll1ll11111_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack11111l11ll_opy_: Tuple[bstack1llll1111ll_opy_, bstack1lll1l1l11l_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1ll111ll_opy_(instance, args)
        capabilities = self.bstack1ll11lllll1_opy_.bstack1ll1l1ll1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll1ll1llll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᄥ"))
            return
        driver = self.bstack1ll11lllll1_opy_.bstack1ll1ll1l1ll_opy_(f, instance, bstack11111l11ll_opy_, *args, **kwargs)
        test_name = f.bstack1111111111_opy_(instance, TestFramework.bstack1ll1ll111l1_opy_)
        if not test_name:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᄦ"))
            return
        test_uuid = f.bstack1111111111_opy_(instance, TestFramework.bstack1ll1ll11lll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢᄧ"))
            return
        if isinstance(self.bstack1ll11lllll1_opy_, bstack1lll11llll1_opy_):
            framework_name = bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᄨ")
        else:
            framework_name = bstack1l11lll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᄩ")
        self.bstack1l111l11l1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack1111l11ll_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࠨᄪ"))
            return
        bstack1ll1ll11ll_opy_ = datetime.now()
        bstack1ll1l1llll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᄫ"), None)
        if not bstack1ll1l1llll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡧࡦࡴࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᄬ") + str(framework_name) + bstack1l11lll_opy_ (u"ࠣࠢࠥᄭ"))
            return
        instance = bstack111111l11l_opy_.bstack1111111l1l_opy_(driver)
        if instance:
            if not bstack111111l11l_opy_.bstack1111111111_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1l111l_opy_, False):
                bstack111111l11l_opy_.bstack1111l111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1l111l_opy_, True)
            else:
                self.logger.info(bstack1l11lll_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᄮ") + str(method) + bstack1l11lll_opy_ (u"ࠥࠦᄯ"))
                return
        self.logger.info(bstack1l11lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᄰ") + str(method) + bstack1l11lll_opy_ (u"ࠧࠨᄱ"))
        if framework_name == bstack1l11lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᄲ"):
            result = self.bstack1ll11lllll1_opy_.bstack1ll1l11l1ll_opy_(driver, bstack1ll1l1llll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1llll1_opy_, {bstack1l11lll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᄳ"): method if method else bstack1l11lll_opy_ (u"ࠣࠤᄴ")})
        bstack1ll1llll111_opy_.end(EVENTS.bstack1111l11ll_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᄵ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᄶ"), True, None, command=method)
        if instance:
            bstack111111l11l_opy_.bstack1111l111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1l111l_opy_, False)
            instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᄷ"), datetime.now() - bstack1ll1ll11ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack11l1llll11_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᄸ"))
            return
        bstack1ll1l1llll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11lll_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᄹ"), None)
        if not bstack1ll1l1llll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᄺ") + str(framework_name) + bstack1l11lll_opy_ (u"ࠣࠤᄻ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1ll11ll_opy_ = datetime.now()
        if framework_name == bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᄼ"):
            result = self.bstack1ll11lllll1_opy_.bstack1ll1l11l1ll_opy_(driver, bstack1ll1l1llll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1llll1_opy_)
        instance = bstack111111l11l_opy_.bstack1111111l1l_opy_(driver)
        if instance:
            instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᄽ"), datetime.now() - bstack1ll1ll11ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll111lll_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᄾ"))
            return
        bstack1ll1l1llll1_opy_ = self.scripts.get(framework_name, {}).get(bstack1l11lll_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠤᄿ"), None)
        if not bstack1ll1l1llll1_opy_:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᅀ") + str(framework_name) + bstack1l11lll_opy_ (u"ࠢࠣᅁ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1ll11ll_opy_ = datetime.now()
        if framework_name == bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᅂ"):
            result = self.bstack1ll11lllll1_opy_.bstack1ll1l11l1ll_opy_(driver, bstack1ll1l1llll1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll1l1llll1_opy_)
        instance = bstack111111l11l_opy_.bstack1111111l1l_opy_(driver)
        if instance:
            instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࠨᅃ"), datetime.now() - bstack1ll1ll11ll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l1111l1_opy_, stage=STAGE.bstack1l1ll11ll1_opy_)
    def bstack1ll11lll1ll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1ll1l11l_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1ll11ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᅄ") + str(r) + bstack1l11lll_opy_ (u"ࠦࠧᅅ"))
            else:
                self.bstack1ll1l1l11ll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l11lll_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲ࠻ࠢࠥᅆ") + str(e) + bstack1l11lll_opy_ (u"ࠨࠢᅇ"))
            traceback.print_exc()
            raise e
    def bstack1ll1l1l11ll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠢ࡭ࡱࡤࡨࡤࡩ࡯࡯ࡨ࡬࡫࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡨࡲࡹࡳࡪࠢᅈ"))
            return False
        if result.accessibility.options:
            options = result.accessibility.options
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l11ll1l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11llll11_opy_ and command.module == self.bstack1ll1l11lll1_opy_:
                        if command.method and not command.method in bstack1ll1l11ll1l_opy_:
                            bstack1ll1l11ll1l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l11ll1l_opy_[command.method]:
                            bstack1ll1l11ll1l_opy_[command.method][command.name] = list()
                        bstack1ll1l11ll1l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l11ll1l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll1l11l11l_opy_(
        self,
        f: bstack1lll1lll1l1_opy_,
        exec: Tuple[bstack11111111ll_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11lllll1_opy_, bstack1lll11llll1_opy_) and method_name != bstack1l11lll_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᅉ"):
            return
        if bstack111111l11l_opy_.bstack11111ll11l_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1l1l11_opy_):
            return
        if not f.bstack1ll1ll1l1l1_opy_(instance):
            if not bstack1lll11l1ll1_opy_.bstack1ll1ll1111l_opy_:
                self.logger.warning(bstack1l11lll_opy_ (u"ࠤࡤ࠵࠶ࡿࠠࡧ࡮ࡲࡻࠥࡪࡩࡴࡣࡥࡰࡪࡪࠠࡧࡱࡵࠤࡳࡵ࡮࠮ࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡪࡰࡩࡶࡦࠨᅊ"))
                bstack1lll11l1ll1_opy_.bstack1ll1ll1111l_opy_ = True
            return
        if f.bstack1ll1l1ll11l_opy_(method_name, *args):
            bstack1ll1l1lll1l_opy_ = False
            desired_capabilities = f.bstack1ll1l11l111_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11llllll_opy_(instance)
                platform_index = f.bstack1111111111_opy_(instance, bstack1lll1lll1l1_opy_.bstack1ll1l111lll_opy_, 0)
                bstack1ll1l1l1lll_opy_ = datetime.now()
                r = self.bstack1ll11lll1ll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l11111ll1_opy_(bstack1l11lll_opy_ (u"ࠥ࡫ࡷࡶࡣ࠻ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᅋ"), datetime.now() - bstack1ll1l1l1lll_opy_)
                bstack1ll1l1lll1l_opy_ = r.success
            else:
                self.logger.error(bstack1l11lll_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡪࡥࡴ࡫ࡵࡩࡩࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࡂࠨᅌ") + str(desired_capabilities) + bstack1l11lll_opy_ (u"ࠧࠨᅍ"))
            f.bstack1111l111ll_opy_(instance, bstack1lll11l1ll1_opy_.bstack1ll1l1l1l11_opy_, bstack1ll1l1lll1l_opy_)
    def bstack111ll1l1l_opy_(self, test_tags):
        bstack1ll11lll1ll_opy_ = self.config.get(bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᅎ"))
        if not bstack1ll11lll1ll_opy_:
            return True
        try:
            include_tags = bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᅏ")] if bstack1l11lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᅐ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᅑ")], list) else []
            exclude_tags = bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᅒ")] if bstack1l11lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᅓ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᅔ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᅕ") + str(error))
        return False
    def bstack11l1ll1l1l_opy_(self, caps):
        try:
            bstack1ll1ll11l11_opy_ = caps.get(bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᅖ"), {}).get(bstack1l11lll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᅗ"), caps.get(bstack1l11lll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᅘ"), bstack1l11lll_opy_ (u"ࠪࠫᅙ")))
            if bstack1ll1ll11l11_opy_:
                self.logger.warning(bstack1l11lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᅚ"))
                return False
            browser = caps.get(bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᅛ"), bstack1l11lll_opy_ (u"࠭ࠧᅜ")).lower()
            if browser != bstack1l11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᅝ"):
                self.logger.warning(bstack1l11lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᅞ"))
                return False
            browser_version = caps.get(bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᅟ"))
            if browser_version and browser_version != bstack1l11lll_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᅠ") and int(browser_version.split(bstack1l11lll_opy_ (u"ࠫ࠳࠭ᅡ"))[0]) <= 98:
                self.logger.warning(bstack1l11lll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦ࠹࠹࠰ࠥᅢ"))
                return False
            bstack1ll1l11llll_opy_ = caps.get(bstack1l11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᅣ"), {}).get(bstack1l11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᅤ"))
            if bstack1ll1l11llll_opy_ and bstack1l11lll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᅥ") in bstack1ll1l11llll_opy_.get(bstack1l11lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᅦ"), []):
                self.logger.warning(bstack1l11lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᅧ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨᅨ") + str(error))
            return False
    def bstack1ll1ll1lll1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll11llll1l_opy_ = {
            bstack1l11lll_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᅩ"): test_uuid,
        }
        bstack1ll1l1lll11_opy_ = {}
        if result.success:
            bstack1ll1l1lll11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll1l1l1l1l_opy_(bstack1ll11llll1l_opy_, bstack1ll1l1lll11_opy_)
    def bstack1l111l11l1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll1ll1l111_opy_ = None
        try:
            self.bstack1ll1ll1l11l_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1l11lll_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠨᅪ")
            req.script_name = bstack1l11lll_opy_ (u"ࠢࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠧᅫ")
            r = self.bstack1lll1ll11ll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᅬ") + str(r.error) + bstack1l11lll_opy_ (u"ࠤࠥᅭ"))
            else:
                bstack1ll11llll1l_opy_ = self.bstack1ll1ll1lll1_opy_(test_uuid, r)
                bstack1ll1l1llll1_opy_ = r.script
            self.logger.debug(bstack1l11lll_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᅮ") + str(bstack1ll11llll1l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll1l1llll1_opy_:
                self.logger.debug(bstack1l11lll_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᅯ") + str(framework_name) + bstack1l11lll_opy_ (u"ࠧࠦࠢᅰ"))
                return
            bstack1ll1ll1l111_opy_ = bstack1ll1llll111_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack1ll1l1l1ll1_opy_.value)
            self.bstack1ll1l11l1l1_opy_(driver, bstack1ll1l1llll1_opy_, bstack1ll11llll1l_opy_, framework_name)
            self.logger.info(bstack1l11lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᅱ"))
            bstack1ll1llll111_opy_.end(EVENTS.bstack1ll1l1l1ll1_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᅲ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᅳ"), True, None, command=bstack1l11lll_opy_ (u"ࠩࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠧᅴ"),test_name=name)
        except Exception as bstack1ll1l111ll1_opy_:
            self.logger.error(bstack1l11lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᅵ") + bstack1l11lll_opy_ (u"ࠦࡸࡺࡲࠩࡲࡤࡸ࡭࠯ࠢᅶ") + bstack1l11lll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᅷ") + str(bstack1ll1l111ll1_opy_))
            bstack1ll1llll111_opy_.end(EVENTS.bstack1ll1l1l1ll1_opy_.value, bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᅸ"), bstack1ll1ll1l111_opy_+bstack1l11lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᅹ"), False, bstack1ll1l111ll1_opy_, command=bstack1l11lll_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ᅺ"),test_name=name)
    def bstack1ll1l11l1l1_opy_(self, driver, bstack1ll1l1llll1_opy_, bstack1ll11llll1l_opy_, framework_name):
        if framework_name == bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᅻ"):
            self.bstack1ll11lllll1_opy_.bstack1ll1l11l1ll_opy_(driver, bstack1ll1l1llll1_opy_, bstack1ll11llll1l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll1l1llll1_opy_, bstack1ll11llll1l_opy_))
    def _1ll1ll111ll_opy_(self, instance: bstack1lll1lllll1_opy_, args: Tuple) -> list:
        bstack1l11lll_opy_ (u"ࠥࠦࠧࡋࡸࡵࡴࡤࡧࡹࠦࡴࡢࡩࡶࠤࡧࡧࡳࡦࡦࠣࡳࡳࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࠲ࠧࠨࠢᅼ")
        if bstack1l11lll_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᅽ") in instance.bstack1ll1l11ll11_opy_:
            return args[2].tags if hasattr(args[2], bstack1l11lll_opy_ (u"ࠬࡺࡡࡨࡵࠪᅾ")) else []
        if hasattr(args[0], bstack1l11lll_opy_ (u"࠭࡯ࡸࡰࡢࡱࡦࡸ࡫ࡦࡴࡶࠫᅿ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll1ll1llll_opy_(self, tags, capabilities):
        return self.bstack111ll1l1l_opy_(tags) and self.bstack11l1ll1l1l_opy_(capabilities)