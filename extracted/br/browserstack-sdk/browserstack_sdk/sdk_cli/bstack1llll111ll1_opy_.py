# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllll111ll_opy_ import (
    bstack1llllllllll_opy_,
    bstack1llllllll1l_opy_,
    bstack1llll1lll11_opy_,
    bstack11111111l1_opy_,
)
from browserstack_sdk.sdk_cli.bstack1lll11lll11_opy_ import bstack1ll1l1lll11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_, bstack1ll1ll11l1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1l1l1ll1_opy_ import bstack1ll1l1ll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lll1l_opy_ import bstack1lll11l1ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1lllll1_opy_ import bstack1lll1lll1ll_opy_
from browserstack_sdk.sdk_cli.bstack1ll1l1lllll_opy_ import bstack1ll1lllll1l_opy_
from bstack_utils.helper import bstack1ll111lll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
import grpc
import traceback
import json
class bstack1lll111ll11_opy_(bstack1ll1l1ll1ll_opy_):
    bstack1ll111l11l1_opy_ = False
    bstack1ll111lll11_opy_ = bstackl_opy_ (u"ࠨࡳࡦ࡮ࡨࡲ࡮ࡻ࡭࠯ࡹࡨࡦࡩࡸࡩࡷࡧࡵࠦᅸ")
    bstack1ll1l11l111_opy_ = bstackl_opy_ (u"ࠢࡳࡧࡰࡳࡹ࡫࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᅹ")
    bstack1ll11lllll1_opy_ = bstackl_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡱ࡭ࡹࠨᅺ")
    bstack1ll111lllll_opy_ = bstackl_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡ࡬ࡷࡤࡹࡣࡢࡰࡱ࡭ࡳ࡭ࠢᅻ")
    bstack1ll111l1l1l_opy_ = bstackl_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴࡢ࡬ࡦࡹ࡟ࡶࡴ࡯ࠦᅼ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll1l11ll1_opy_, bstack1lll1ll11ll_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll111l11ll_opy_ = False
        self.bstack1ll11l1l1l1_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11l1l1ll_opy_ = bstack1lll1ll11ll_opy_
        bstack1lll1l11ll1_opy_.bstack1ll1l11ll1l_opy_((bstack1llllllllll_opy_.bstack1llllll1l11_opy_, bstack1llllllll1l_opy_.PRE), self.bstack1ll11l11l11_opy_)
        TestFramework.bstack1ll1l11ll1l_opy_((bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.PRE), self.bstack1ll11l1111l_opy_)
        TestFramework.bstack1ll1l11ll1l_opy_((bstack1lll1l11l1l_opy_.TEST, bstack1lll111l111_opy_.POST), self.bstack1ll11ll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll11l1111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11ll1lll_opy_(instance, args)
        test_framework = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l1111l1_opy_)
        if self.bstack1ll111l11ll_opy_:
            self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᅽ")] = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
        if bstackl_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠩᅾ") in instance.bstack1ll1l11111l_opy_:
            platform_index = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll111ll1l1_opy_)
            self.accessibility = self.bstack1ll111l1ll1_opy_(tags, self.config[bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᅿ")][platform_index])
        else:
            capabilities = self.bstack1ll11l1l1ll_opy_.bstack1ll11ll11l1_opy_(f, instance, bstack1lllll1l1ll_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstackl_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡸࡪࡹࡴ࠻ࠢࡱࡳࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠤ࡫ࡵࡵ࡯ࡦࠣࡪࡴࡸࠠࡩࡱࡲ࡯ࡤ࡯࡮ࡧࡱࡀࡿ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵࡽࠡࡣࡵ࡫ࡸࡃࡻࡢࡴࡪࡷࢂࠦ࡫ࡸࡣࡵ࡫ࡸࡃࠢᆀ") + str(kwargs) + bstackl_opy_ (u"ࠣࠤᆁ"))
                return
            self.accessibility = self.bstack1ll111l1ll1_opy_(tags, capabilities)
        if self.bstack1ll11l1l1ll_opy_.pages and self.bstack1ll11l1l1ll_opy_.pages.values():
            bstack1ll11lll1ll_opy_ = list(self.bstack1ll11l1l1ll_opy_.pages.values())
            if bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[0], (list, tuple)) and bstack1ll11lll1ll_opy_[0]:
                bstack1ll11ll1l1l_opy_ = bstack1ll11lll1ll_opy_[0][0]
                if callable(bstack1ll11ll1l1l_opy_):
                    page = bstack1ll11ll1l1l_opy_()
                    def bstack1ll1l1llll_opy_():
                        self.get_accessibility_results(page, bstackl_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᆂ"))
                    def bstack1ll1l11l1ll_opy_():
                        self.get_accessibility_results_summary(page, bstackl_opy_ (u"ࠥࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠢᆃ"))
                    setattr(page, bstackl_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹࡹࠢᆄ"), bstack1ll1l1llll_opy_)
                    setattr(page, bstackl_opy_ (u"ࠧ࡭ࡥࡵࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡓࡧࡶࡹࡱࡺࡓࡶ࡯ࡰࡥࡷࡿࠢᆅ"), bstack1ll1l11l1ll_opy_)
        self.logger.debug(bstackl_opy_ (u"ࠨࡳࡩࡱࡸࡰࡩࠦࡲࡶࡰࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡺࡦࡲࡵࡦ࠿ࠥᆆ") + str(self.accessibility) + bstackl_opy_ (u"ࠢࠣᆇ"))
    def bstack1ll11l11l11_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        driver: object,
        exec: Tuple[bstack11111111l1_opy_, str],
        bstack1lllll1l1ll_opy_: Tuple[bstack1llllllllll_opy_, bstack1llllllll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1ll11l1_opy_ = datetime.now()
            self.bstack1ll11ll1111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡩ࡯࡫ࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᆈ"), datetime.now() - bstack1l1ll11l1_opy_)
            if (
                not f.bstack1ll111l1111_opy_(method_name)
                or f.bstack1ll11l1l11l_opy_(method_name, *args)
                or f.bstack1ll1111llll_opy_(method_name, *args)
            ):
                return
            if not f.bstack1llllll1l1l_opy_(instance, bstack1lll111ll11_opy_.bstack1ll11lllll1_opy_, False):
                if not bstack1lll111ll11_opy_.bstack1ll111l11l1_opy_:
                    self.logger.warning(bstackl_opy_ (u"ࠤ࡞ࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࠧᆉ") + str(f.platform_index) + bstackl_opy_ (u"ࠥࡡࠥࡧ࠱࠲ࡻࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠢ࡫ࡥࡻ࡫ࠠ࡯ࡱࡷࠤࡧ࡫ࡥ࡯ࠢࡶࡩࡹࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᆊ"))
                    bstack1lll111ll11_opy_.bstack1ll111l11l1_opy_ = True
                return
            bstack1ll11l111l1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11l111l1_opy_:
                platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_, 0)
                self.logger.debug(bstackl_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࡁࢀࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡪࡰࡧࡩࡽࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᆋ") + str(f.framework_name) + bstackl_opy_ (u"ࠧࠨᆌ"))
                return
            bstack1ll11l1llll_opy_ = f.bstack1ll11l1ll1l_opy_(*args)
            if not bstack1ll11l1llll_opy_:
                self.logger.debug(bstackl_opy_ (u"ࠨ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࠣᆍ") + str(method_name) + bstackl_opy_ (u"ࠢࠣᆎ"))
                return
            bstack1ll111l1l11_opy_ = f.bstack1llllll1l1l_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111l1l1l_opy_, False)
            if bstack1ll11l1llll_opy_ == bstackl_opy_ (u"ࠣࡩࡨࡸࠧᆏ") and not bstack1ll111l1l11_opy_:
                f.bstack1lllllllll1_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111l1l1l_opy_, True)
                bstack1ll111l1l11_opy_ = True
            if not bstack1ll111l1l11_opy_ and not self.bstack1ll111l11ll_opy_:
                self.logger.debug(bstackl_opy_ (u"ࠤࡱࡳ࡛ࠥࡒࡍࠢ࡯ࡳࡦࡪࡥࡥࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᆐ") + str(bstack1ll11l1llll_opy_) + bstackl_opy_ (u"ࠥࠦᆑ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll11l1llll_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstackl_opy_ (u"ࠦࡳࡵࠠࡢ࠳࠴ࡽࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡦࡳࡲࡳࡡ࡯ࡦࡢࡲࡦࡳࡥ࠾ࠤᆒ") + str(bstack1ll11l1llll_opy_) + bstackl_opy_ (u"ࠧࠨᆓ"))
                return
            self.logger.info(bstackl_opy_ (u"ࠨࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡼ࡮ࡨࡲ࠭ࡹࡣࡳ࡫ࡳࡸࡸࡥࡴࡰࡡࡵࡹࡳ࠯ࡽࠡࡵࡦࡶ࡮ࡶࡴࡴࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᆔ") + str(bstack1ll11l1llll_opy_) + bstackl_opy_ (u"ࠢࠣᆕ"))
            scripts = [(s, bstack1ll11l111l1_opy_[s]) for s in scripts_to_run if s in bstack1ll11l111l1_opy_]
            for script_name, bstack1ll11lll1l1_opy_ in scripts:
                try:
                    bstack1l1ll11l1_opy_ = datetime.now()
                    if script_name == bstackl_opy_ (u"ࠣࡵࡦࡥࡳࠨᆖ"):
                        result = self.perform_scan(driver, method=bstack1ll11l1llll_opy_, framework_name=f.framework_name)
                    instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠤࡤ࠵࠶ࡿ࠺ࠣᆗ") + script_name, datetime.now() - bstack1l1ll11l1_opy_)
                    if isinstance(result, dict) and not result.get(bstackl_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦᆘ"), True):
                        self.logger.warning(bstackl_opy_ (u"ࠦࡸࡱࡩࡱࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡸࡥ࡮ࡣ࡬ࡲ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴࡴ࠼ࠣࠦᆙ") + str(result) + bstackl_opy_ (u"ࠧࠨᆚ"))
                        break
                except Exception as e:
                    self.logger.error(bstackl_opy_ (u"ࠨࡥࡳࡴࡲࡶࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡴࡧࠡࡵࡦࡶ࡮ࡶࡴ࠾ࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽࠡࡧࡵࡶࡴࡸ࠽ࠣᆛ") + str(e) + bstackl_opy_ (u"ࠢࠣᆜ"))
        except Exception as e:
            self.logger.error(bstackl_opy_ (u"ࠣࡱࡱࡣࡧ࡫ࡦࡰࡴࡨࡣࡪࡾࡥࡤࡷࡷࡩࠥ࡫ࡲࡳࡱࡵࡁࠧᆝ") + str(e) + bstackl_opy_ (u"ࠤࠥᆞ"))
    def bstack1ll11ll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll1ll11l1l_opy_,
        bstack1lllll1l1ll_opy_: Tuple[bstack1lll1l11l1l_opy_, bstack1lll111l111_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11ll1lll_opy_(instance, args)
        capabilities = self.bstack1ll11l1l1ll_opy_.bstack1ll11ll11l1_opy_(f, instance, bstack1lllll1l1ll_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll111l1ll1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstackl_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᆟ"))
            return
        driver = self.bstack1ll11l1l1ll_opy_.bstack1ll11ll1ll1_opy_(f, instance, bstack1lllll1l1ll_opy_, *args, **kwargs)
        test_name = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll1l111l1l_opy_)
        if not test_name:
            self.logger.debug(bstackl_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡳࡧ࡭ࡦࠤᆠ"))
            return
        test_uuid = f.bstack1llllll1l1l_opy_(instance, TestFramework.bstack1ll11l11lll_opy_)
        if not test_uuid:
            self.logger.debug(bstackl_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡻࡵࡪࡦࠥᆡ"))
            return
        if isinstance(self.bstack1ll11l1l1ll_opy_, bstack1lll1lll1ll_opy_):
            framework_name = bstackl_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᆢ")
        else:
            framework_name = bstackl_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᆣ")
        self.bstack11ll11111l_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack11ll11l11_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstackl_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࠤᆤ"))
            return
        bstack1l1ll11l1_opy_ = datetime.now()
        bstack1ll11lll1l1_opy_ = self.scripts.get(framework_name, {}).get(bstackl_opy_ (u"ࠤࡶࡧࡦࡴࠢᆥ"), None)
        if not bstack1ll11lll1l1_opy_:
            self.logger.debug(bstackl_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࠬࡹࡣࡢࡰࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᆦ") + str(framework_name) + bstackl_opy_ (u"ࠦࠥࠨᆧ"))
            return
        if self.bstack1ll111l11ll_opy_:
            arg = dict()
            arg[bstackl_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᆨ")] = method if method else bstackl_opy_ (u"ࠨࠢᆩ")
            arg[bstackl_opy_ (u"ࠢࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠢᆪ")] = self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣᆫ")]
            arg[bstackl_opy_ (u"ࠤࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠢᆬ")] = self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᆭ")]
            arg[bstackl_opy_ (u"ࠦࡦࡻࡴࡩࡊࡨࡥࡩ࡫ࡲࠣᆮ")] = self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠥᆯ")]
            arg[bstackl_opy_ (u"ࠨࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠥᆰ")] = self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨᆱ")]
            arg[bstackl_opy_ (u"ࠣࡵࡦࡥࡳ࡚ࡩ࡮ࡧࡶࡸࡦࡳࡰࠣᆲ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll111ll1ll_opy_ = bstack1ll11lll1l1_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll111ll1ll_opy_)
            return
        instance = bstack1llll1lll11_opy_.bstack1111111111_opy_(driver)
        if instance:
            if not bstack1llll1lll11_opy_.bstack1llllll1l1l_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111lllll_opy_, False):
                bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111lllll_opy_, True)
            else:
                self.logger.info(bstackl_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᆳ") + str(method) + bstackl_opy_ (u"ࠥࠦᆴ"))
                return
        self.logger.info(bstackl_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᆵ") + str(method) + bstackl_opy_ (u"ࠧࠨᆶ"))
        if framework_name == bstackl_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᆷ"):
            result = self.bstack1ll11l1l1ll_opy_.bstack1ll11l1lll1_opy_(driver, bstack1ll11lll1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11lll1l1_opy_, {bstackl_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᆸ"): method if method else bstackl_opy_ (u"ࠣࠤᆹ")})
        bstack1lll11lll1l_opy_.end(EVENTS.bstack11ll11l11_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᆺ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᆻ"), True, None, command=method)
        if instance:
            bstack1llll1lll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lll111ll11_opy_.bstack1ll111lllll_opy_, False)
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᆼ"), datetime.now() - bstack1l1ll11l1_opy_)
        return result
        def bstack1ll11llll11_opy_(self, driver: object, framework_name, bstack1lll11l1l1_opy_: str):
            self.bstack1ll111llll1_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll1l1111ll_opy_ = self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᆽ")]
            req.bstack1lll11l1l1_opy_ = bstack1lll11l1l1_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll1l1l1ll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstackl_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣᆾ") + str(r) + bstackl_opy_ (u"ࠢࠣᆿ"))
                else:
                    bstack1ll11lll111_opy_ = json.loads(r.bstack1ll11l11l1l_opy_.decode(bstackl_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᇀ")))
                    if bstack1lll11l1l1_opy_ == bstackl_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ᇁ"):
                        return bstack1ll11lll111_opy_.get(bstackl_opy_ (u"ࠥࡨࡦࡺࡡࠣᇂ"), [])
                    else:
                        return bstack1ll11lll111_opy_.get(bstackl_opy_ (u"ࠦࡩࡧࡴࡢࠤᇃ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstackl_opy_ (u"ࠧࡸࡰࡤ࠯ࡨࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡱࡲࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࠣࡪࡷࡵ࡭ࠡࡥ࡯࡭࠿ࠦࠢᇄ") + str(e) + bstackl_opy_ (u"ࠨࠢᇅ"))
    @measure(event_name=EVENTS.bstack1l11ll1l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstackl_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᇆ"))
            return
        if self.bstack1ll111l11ll_opy_:
            self.logger.debug(bstackl_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡢࡲࡳࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᇇ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11llll11_opy_(driver, framework_name, bstackl_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᇈ"))
        bstack1ll11lll1l1_opy_ = self.scripts.get(framework_name, {}).get(bstackl_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠢᇉ"), None)
        if not bstack1ll11lll1l1_opy_:
            self.logger.debug(bstackl_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᇊ") + str(framework_name) + bstackl_opy_ (u"ࠧࠨᇋ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1ll11l1_opy_ = datetime.now()
        if framework_name == bstackl_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᇌ"):
            result = self.bstack1ll11l1l1ll_opy_.bstack1ll11l1lll1_opy_(driver, bstack1ll11lll1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11lll1l1_opy_)
        instance = bstack1llll1lll11_opy_.bstack1111111111_opy_(driver)
        if instance:
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࠥᇍ"), datetime.now() - bstack1l1ll11l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack111l1l11l_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstackl_opy_ (u"ࠣࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᇎ"))
            return
        if self.bstack1ll111l11ll_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11llll11_opy_(driver, framework_name, bstackl_opy_ (u"ࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ᇏ"))
        bstack1ll11lll1l1_opy_ = self.scripts.get(framework_name, {}).get(bstackl_opy_ (u"ࠥ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠢᇐ"), None)
        if not bstack1ll11lll1l1_opy_:
            self.logger.debug(bstackl_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪࠤࡸࡩࡲࡪࡲࡷࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࠥᇑ") + str(framework_name) + bstackl_opy_ (u"ࠧࠨᇒ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1ll11l1_opy_ = datetime.now()
        if framework_name == bstackl_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᇓ"):
            result = self.bstack1ll11l1l1ll_opy_.bstack1ll11l1lll1_opy_(driver, bstack1ll11lll1l1_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11lll1l1_opy_)
        instance = bstack1llll1lll11_opy_.bstack1111111111_opy_(driver)
        if instance:
            instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼࠦᇔ"), datetime.now() - bstack1l1ll11l1_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll111ll111_opy_, stage=STAGE.bstack1l1111ll1_opy_)
    def bstack1ll11l1l111_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll111llll1_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1l1l1ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstackl_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡪࡷࡵ࡭ࠡࡵࡨࡶࡻ࡫ࡲ࠻ࠢࠥᇕ") + str(r) + bstackl_opy_ (u"ࠤࠥᇖ"))
            else:
                self.bstack1ll11l11111_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstackl_opy_ (u"ࠥࡶࡵࡩ࠭ࡦࡴࡵࡳࡷࡀࠠࠣᇗ") + str(e) + bstackl_opy_ (u"ࠦࠧᇘ"))
            traceback.print_exc()
            raise e
    def bstack1ll11l11111_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstackl_opy_ (u"ࠧࡲ࡯ࡢࡦࡢࡧࡴࡴࡦࡪࡩ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡦࡰࡷࡱࡨࠧᇙ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll111l11ll_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠨࡴࡦࡵࡷ࡬ࡺࡨ࡟ࡣࡷ࡬ࡰࡩࡥࡵࡶ࡫ࡧࠦᇚ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll11l1l1l1_opy_[bstackl_opy_ (u"ࠢࡵࡪࡢ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳࠨᇛ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll11l1l1l1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1l11ll11_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll111lll11_opy_ and command.module == self.bstack1ll1l11l111_opy_:
                        if command.method and not command.method in bstack1ll1l11ll11_opy_:
                            bstack1ll1l11ll11_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1l11ll11_opy_[command.method]:
                            bstack1ll1l11ll11_opy_[command.method][command.name] = list()
                        bstack1ll1l11ll11_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1l11ll11_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll11ll1111_opy_(
        self,
        f: bstack1ll1l1lll11_opy_,
        exec: Tuple[bstack11111111l1_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11l1l1ll_opy_, bstack1lll1lll1ll_opy_) and method_name != bstackl_opy_ (u"ࠨࡥࡲࡲࡳ࡫ࡣࡵࠩᇜ"):
            return
        if bstack1llll1lll11_opy_.bstack1lllll11111_opy_(instance, bstack1lll111ll11_opy_.bstack1ll11lllll1_opy_):
            return
        if f.bstack1ll1111ll1l_opy_(method_name, *args):
            bstack1ll1l11l11l_opy_ = False
            desired_capabilities = f.bstack1ll111l111l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1l111l11_opy_(instance)
                platform_index = f.bstack1llllll1l1l_opy_(instance, bstack1ll1l1lll11_opy_.bstack1ll111ll1l1_opy_, 0)
                bstack1ll1l111ll1_opy_ = datetime.now()
                r = self.bstack1ll11l1l111_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack1l11ll11ll_opy_(bstackl_opy_ (u"ࠤࡪࡶࡵࡩ࠺ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡤࡱࡱࡪ࡮࡭ࠢᇝ"), datetime.now() - bstack1ll1l111ll1_opy_)
                bstack1ll1l11l11l_opy_ = r.success
            else:
                self.logger.error(bstackl_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡩ࡫ࡳࡪࡴࡨࡨࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࡁࠧᇞ") + str(desired_capabilities) + bstackl_opy_ (u"ࠦࠧᇟ"))
            f.bstack1lllllllll1_opy_(instance, bstack1lll111ll11_opy_.bstack1ll11lllll1_opy_, bstack1ll1l11l11l_opy_)
    def bstack1l111lll_opy_(self, test_tags):
        bstack1ll11l1l111_opy_ = self.config.get(bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᇠ"))
        if not bstack1ll11l1l111_opy_:
            return True
        try:
            include_tags = bstack1ll11l1l111_opy_[bstackl_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᇡ")] if bstackl_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᇢ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstackl_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᇣ")], list) else []
            exclude_tags = bstack1ll11l1l111_opy_[bstackl_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᇤ")] if bstackl_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᇥ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstackl_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᇦ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstackl_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᇧ") + str(error))
        return False
    def bstack1lll1l111l_opy_(self, caps):
        try:
            if self.bstack1ll111l11ll_opy_:
                bstack1ll11llll1l_opy_ = caps.get(bstackl_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᇨ"))
                if bstack1ll11llll1l_opy_ is not None and str(bstack1ll11llll1l_opy_).lower() == bstackl_opy_ (u"ࠢࡢࡰࡧࡶࡴ࡯ࡤࠣᇩ"):
                    bstack1ll111l1lll_opy_ = caps.get(bstackl_opy_ (u"ࠣࡣࡳࡴ࡮ࡻ࡭࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᇪ")) or caps.get(bstackl_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᇫ"))
                    if bstack1ll111l1lll_opy_ is not None and int(bstack1ll111l1lll_opy_) < 11:
                        self.logger.warning(bstackl_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡅࡳࡪࡲࡰ࡫ࡧࠤ࠶࠷ࠠࡢࡰࡧࠤࡦࡨ࡯ࡷࡧ࠱ࠤࡈࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡ࠿ࠥᇬ") + str(bstack1ll111l1lll_opy_) + bstackl_opy_ (u"ࠦࠧᇭ"))
                        return False
                return True
            bstack1ll111ll11l_opy_ = caps.get(bstackl_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᇮ"), {}).get(bstackl_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᇯ"), caps.get(bstackl_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᇰ"), bstackl_opy_ (u"ࠨࠩᇱ")))
            if bstack1ll111ll11l_opy_:
                self.logger.warning(bstackl_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᇲ"))
                return False
            browser = caps.get(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᇳ"), bstackl_opy_ (u"ࠫࠬᇴ")).lower()
            if browser != bstackl_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᇵ"):
                self.logger.warning(bstackl_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᇶ"))
                return False
            bstack1ll11l11ll1_opy_ = bstack1ll1l111111_opy_
            if not self.config.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᇷ")) or self.config.get(bstackl_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬᇸ")):
                bstack1ll11l11ll1_opy_ = bstack1ll11l111ll_opy_
            browser_version = caps.get(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᇹ"))
            if not browser_version:
                browser_version = caps.get(bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᇺ"), {}).get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᇻ"), bstackl_opy_ (u"ࠬ࠭ᇼ"))
            if browser_version and browser_version != bstackl_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᇽ") and int(browser_version.split(bstackl_opy_ (u"ࠧ࠯ࠩᇾ"))[0]) <= bstack1ll11l11ll1_opy_:
                self.logger.warning(bstackl_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥᇿ") + str(bstack1ll11l11ll1_opy_) + bstackl_opy_ (u"ࠤ࠱ࠦሀ"))
                return False
            bstack1ll11ll11ll_opy_ = caps.get(bstackl_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫሁ"), {}).get(bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫሂ"))
            if not bstack1ll11ll11ll_opy_:
                bstack1ll11ll11ll_opy_ = caps.get(bstackl_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪሃ"), {})
            if bstack1ll11ll11ll_opy_ and bstackl_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪሄ") in bstack1ll11ll11ll_opy_.get(bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬህ"), []):
                self.logger.warning(bstackl_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥሆ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstackl_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦሇ") + str(error))
            return False
    def bstack1ll1111ll11_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l111lll_opy_ = {
            bstackl_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪለ"): test_uuid,
        }
        bstack1ll11l1ll11_opy_ = {}
        if result.success:
            bstack1ll11l1ll11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll111lll1l_opy_(bstack1ll1l111lll_opy_, bstack1ll11l1ll11_opy_)
    def bstack11ll11111l_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11lll11l_opy_ = None
        try:
            self.bstack1ll111llll1_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstackl_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠦሉ")
            req.script_name = bstackl_opy_ (u"ࠧࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠥሊ")
            r = self.bstack1lll1l1l1ll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstackl_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤላ") + str(r.error) + bstackl_opy_ (u"ࠢࠣሌ"))
            else:
                bstack1ll1l111lll_opy_ = self.bstack1ll1111ll11_opy_(test_uuid, r)
                bstack1ll11lll1l1_opy_ = r.script
            self.logger.debug(bstackl_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫል") + str(bstack1ll1l111lll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11lll1l1_opy_:
                self.logger.debug(bstackl_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤሎ") + str(framework_name) + bstackl_opy_ (u"ࠥࠤࠧሏ"))
                return
            bstack1ll11lll11l_opy_ = bstack1lll11lll1l_opy_.bstack1ll11llllll_opy_(EVENTS.bstack1ll11ll1l11_opy_.value)
            self.bstack1ll1l11l1l1_opy_(driver, bstack1ll11lll1l1_opy_, bstack1ll1l111lll_opy_, framework_name)
            self.logger.info(bstackl_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢሐ"))
            bstack1lll11lll1l_opy_.end(EVENTS.bstack1ll11ll1l11_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧሑ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠨ࠺ࡦࡰࡧࠦሒ"), True, None, command=bstackl_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬሓ"),test_name=name)
        except Exception as bstack1ll1111lll1_opy_:
            self.logger.error(bstackl_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥሔ") + bstackl_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧሕ") + bstackl_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧሖ") + str(bstack1ll1111lll1_opy_))
            bstack1lll11lll1l_opy_.end(EVENTS.bstack1ll11ll1l11_opy_.value, bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦሗ"), bstack1ll11lll11l_opy_+bstackl_opy_ (u"ࠧࡀࡥ࡯ࡦࠥመ"), False, bstack1ll1111lll1_opy_, command=bstackl_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫሙ"),test_name=name)
    def bstack1ll1l11l1l1_opy_(self, driver, bstack1ll11lll1l1_opy_, bstack1ll1l111lll_opy_, framework_name):
        if framework_name == bstackl_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫሚ"):
            self.bstack1ll11l1l1ll_opy_.bstack1ll11l1lll1_opy_(driver, bstack1ll11lll1l1_opy_, bstack1ll1l111lll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11lll1l1_opy_, bstack1ll1l111lll_opy_))
    def _1ll11ll1lll_opy_(self, instance: bstack1ll1ll11l1l_opy_, args: Tuple) -> list:
        bstackl_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧማ")
        if bstackl_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ሜ") in instance.bstack1ll1l11111l_opy_:
            return args[2].tags if hasattr(args[2], bstackl_opy_ (u"ࠪࡸࡦ࡭ࡳࠨም")) else []
        if hasattr(args[0], bstackl_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩሞ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll111l1ll1_opy_(self, tags, capabilities):
        return self.bstack1l111lll_opy_(tags) and self.bstack1lll1l111l_opy_(capabilities)