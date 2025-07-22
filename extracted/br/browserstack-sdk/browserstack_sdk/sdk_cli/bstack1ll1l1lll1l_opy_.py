# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1llll1lll1l_opy_ import (
    bstack1lllllll11l_opy_,
    bstack1llllll1111_opy_,
    bstack11111111ll_opy_,
    bstack1lllll1ll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1llll1l1111_opy_ import bstack1lll1l11l11_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_, bstack1lll1lllll1_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1lll1l1111l_opy_ import bstack1llll1l1l11_opy_
from browserstack_sdk.sdk_cli.bstack1lll1l1llll_opy_ import bstack1ll1ll1ll1l_opy_
from browserstack_sdk.sdk_cli.bstack1llll1l111l_opy_ import bstack1ll1lll111l_opy_
from browserstack_sdk.sdk_cli.bstack1llll111ll1_opy_ import bstack1ll1llll11l_opy_
from bstack_utils.helper import bstack1ll11l1l111_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
import grpc
import traceback
import json
class bstack1lll11ll11l_opy_(bstack1llll1l1l11_opy_):
    bstack1ll111lll1l_opy_ = False
    bstack1ll11ll11l1_opy_ = bstack111l111_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴࠥᅷ")
    bstack1ll11l1l1l1_opy_ = bstack111l111_opy_ (u"ࠨࡲࡦ࡯ࡲࡸࡪ࠴ࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࠤᅸ")
    bstack1ll111l1ll1_opy_ = bstack111l111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡪࡰ࡬ࡸࠧᅹ")
    bstack1ll1l11ll11_opy_ = bstack111l111_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠ࡫ࡶࡣࡸࡩࡡ࡯ࡰ࡬ࡲ࡬ࠨᅺ")
    bstack1ll11lll1l1_opy_ = bstack111l111_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳࡡ࡫ࡥࡸࡥࡵࡳ࡮ࠥᅻ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1lll1l1ll1l_opy_, bstack1ll1ll1ll11_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll1111llll_opy_ = False
        self.bstack1ll1l11111l_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11ll11ll_opy_ = bstack1ll1ll1ll11_opy_
        bstack1lll1l1ll1l_opy_.bstack1ll11l1l11l_opy_((bstack1lllllll11l_opy_.bstack1llllll11ll_opy_, bstack1llllll1111_opy_.PRE), self.bstack1ll1l11l1ll_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll11l1l11l_opy_((bstack1ll1lll1lll_opy_.TEST, bstack1lll111llll_opy_.POST), self.bstack1ll111lll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1l111l1l_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1111lll1_opy_(instance, args)
        test_framework = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111ll1l1_opy_)
        if self.bstack1ll1111llll_opy_:
            self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᅼ")] = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
        if bstack111l111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᅽ") in instance.bstack1ll11l11ll1_opy_:
            platform_index = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l1lll1_opy_)
            self.accessibility = self.bstack1ll11l11lll_opy_(tags, self.config[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᅾ")][platform_index])
        else:
            capabilities = self.bstack1ll11ll11ll_opy_.bstack1ll1l1111ll_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack111l111_opy_ (u"ࠨ࡯࡯ࡡࡥࡩ࡫ࡵࡲࡦࡡࡷࡩࡸࡺ࠺ࠡࡰࡲࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠣࡪࡴࡻ࡮ࡥࠢࡩࡳࡷࠦࡨࡰࡱ࡮ࡣ࡮ࡴࡦࡰ࠿ࡾ࡬ࡴࡵ࡫ࡠ࡫ࡱࡪࡴࢃࠠࡢࡴࡪࡷࡂࢁࡡࡳࡩࡶࢁࠥࡱࡷࡢࡴࡪࡷࡂࠨᅿ") + str(kwargs) + bstack111l111_opy_ (u"ࠢࠣᆀ"))
                return
            self.accessibility = self.bstack1ll11l11lll_opy_(tags, capabilities)
        if self.bstack1ll11ll11ll_opy_.pages and self.bstack1ll11ll11ll_opy_.pages.values():
            bstack1ll1l111ll1_opy_ = list(self.bstack1ll11ll11ll_opy_.pages.values())
            if bstack1ll1l111ll1_opy_ and isinstance(bstack1ll1l111ll1_opy_[0], (list, tuple)) and bstack1ll1l111ll1_opy_[0]:
                bstack1ll11l11111_opy_ = bstack1ll1l111ll1_opy_[0][0]
                if callable(bstack1ll11l11111_opy_):
                    page = bstack1ll11l11111_opy_()
                    def bstack11l1ll1l1_opy_():
                        self.get_accessibility_results(page, bstack111l111_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᆁ"))
                    def bstack1ll111lllll_opy_():
                        self.get_accessibility_results_summary(page, bstack111l111_opy_ (u"ࠤࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨᆂ"))
                    setattr(page, bstack111l111_opy_ (u"ࠥ࡫ࡪࡺࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡘࡥࡴࡷ࡯ࡸࡸࠨᆃ"), bstack11l1ll1l1_opy_)
                    setattr(page, bstack111l111_opy_ (u"ࠦ࡬࡫ࡴࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡒࡦࡵࡸࡰࡹ࡙ࡵ࡮࡯ࡤࡶࡾࠨᆄ"), bstack1ll111lllll_opy_)
        self.logger.debug(bstack111l111_opy_ (u"ࠧࡹࡨࡰࡷ࡯ࡨࠥࡸࡵ࡯ࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱࡻࡥ࠾ࠤᆅ") + str(self.accessibility) + bstack111l111_opy_ (u"ࠨࠢᆆ"))
    def bstack1ll1l11l1ll_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        driver: object,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        bstack1llllll111l_opy_: Tuple[bstack1lllllll11l_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1l1111lll_opy_ = datetime.now()
            self.bstack1ll11lll11l_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠢࡢ࠳࠴ࡽ࠿࡯࡮ࡪࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡧࡴࡴࡦࡪࡩࠥᆇ"), datetime.now() - bstack1l1111lll_opy_)
            if (
                not f.bstack1ll11l1111l_opy_(method_name)
                or f.bstack1ll111l1111_opy_(method_name, *args)
                or f.bstack1ll11ll1111_opy_(method_name, *args)
            ):
                return
            if not f.bstack1111111l1l_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll111l1ll1_opy_, False):
                if not bstack1lll11ll11l_opy_.bstack1ll111lll1l_opy_:
                    self.logger.warning(bstack111l111_opy_ (u"ࠣ࡝ࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࠦᆈ") + str(f.platform_index) + bstack111l111_opy_ (u"ࠤࡠࠤࡦ࠷࠱ࡺࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡪࡤࡺࡪࠦ࡮ࡰࡶࠣࡦࡪ࡫࡮ࠡࡵࡨࡸࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᆉ"))
                    bstack1lll11ll11l_opy_.bstack1ll111lll1l_opy_ = True
                return
            bstack1ll11ll1ll1_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11ll1ll1_opy_:
                platform_index = f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_, 0)
                self.logger.debug(bstack111l111_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࡀࡿࡵࡲࡡࡵࡨࡲࡶࡲࡥࡩ࡯ࡦࡨࡼࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣᆊ") + str(f.framework_name) + bstack111l111_opy_ (u"ࠦࠧᆋ"))
                return
            bstack1ll1l11l111_opy_ = f.bstack1ll11llllll_opy_(*args)
            if not bstack1ll1l11l111_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠧࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࠢᆌ") + str(method_name) + bstack111l111_opy_ (u"ࠨࠢᆍ"))
                return
            bstack1ll1l111l11_opy_ = f.bstack1111111l1l_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll11lll1l1_opy_, False)
            if bstack1ll1l11l111_opy_ == bstack111l111_opy_ (u"ࠢࡨࡧࡷࠦᆎ") and not bstack1ll1l111l11_opy_:
                f.bstack1111111111_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll11lll1l1_opy_, True)
                bstack1ll1l111l11_opy_ = True
            if not bstack1ll1l111l11_opy_ and not self.bstack1ll1111llll_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠣࡰࡲࠤ࡚ࡘࡌࠡ࡮ࡲࡥࡩ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᆏ") + str(bstack1ll1l11l111_opy_) + bstack111l111_opy_ (u"ࠤࠥᆐ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(bstack1ll1l11l111_opy_, [])
            if not scripts_to_run:
                self.logger.debug(bstack111l111_opy_ (u"ࠥࡲࡴࠦࡡ࠲࠳ࡼࠤࡸࡩࡲࡪࡲࡷࡷࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࡿ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡࡥࡲࡱࡲࡧ࡮ࡥࡡࡱࡥࡲ࡫࠽ࠣᆑ") + str(bstack1ll1l11l111_opy_) + bstack111l111_opy_ (u"ࠦࠧᆒ"))
                return
            self.logger.info(bstack111l111_opy_ (u"ࠧࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡻ࡭ࡧࡱࠬࡸࡩࡲࡪࡲࡷࡷࡤࡺ࡯ࡠࡴࡸࡲ࠮ࢃࠠࡴࡥࡵ࡭ࡵࡺࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᆓ") + str(bstack1ll1l11l111_opy_) + bstack111l111_opy_ (u"ࠨࠢᆔ"))
            scripts = [(s, bstack1ll11ll1ll1_opy_[s]) for s in scripts_to_run if s in bstack1ll11ll1ll1_opy_]
            for script_name, bstack1ll11ll1l11_opy_ in scripts:
                try:
                    bstack1l1111lll_opy_ = datetime.now()
                    if script_name == bstack111l111_opy_ (u"ࠢࡴࡥࡤࡲࠧᆕ"):
                        result = self.perform_scan(driver, method=bstack1ll1l11l111_opy_, framework_name=f.framework_name)
                    instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࠢᆖ") + script_name, datetime.now() - bstack1l1111lll_opy_)
                    if isinstance(result, dict) and not result.get(bstack111l111_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᆗ"), True):
                        self.logger.warning(bstack111l111_opy_ (u"ࠥࡷࡰ࡯ࡰࠡࡧࡻࡩࡨࡻࡴࡪࡰࡪࠤࡷ࡫࡭ࡢ࡫ࡱ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺࡳ࠻ࠢࠥᆘ") + str(result) + bstack111l111_opy_ (u"ࠦࠧᆙ"))
                        break
                except Exception as e:
                    self.logger.error(bstack111l111_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤࡪࡾࡥࡤࡷࡷ࡭ࡳ࡭ࠠࡴࡥࡵ࡭ࡵࡺ࠽ࡼࡵࡦࡶ࡮ࡶࡴࡠࡰࡤࡱࡪࢃࠠࡦࡴࡵࡳࡷࡃࠢᆚ") + str(e) + bstack111l111_opy_ (u"ࠨࠢᆛ"))
        except Exception as e:
            self.logger.error(bstack111l111_opy_ (u"ࠢࡰࡰࡢࡦࡪ࡬࡯ࡳࡧࡢࡩࡽ࡫ࡣࡶࡶࡨࠤࡪࡸࡲࡰࡴࡀࠦᆜ") + str(e) + bstack111l111_opy_ (u"ࠣࠤᆝ"))
    def bstack1ll111lll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1lllll1_opy_,
        bstack1llllll111l_opy_: Tuple[bstack1ll1lll1lll_opy_, bstack1lll111llll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll1111lll1_opy_(instance, args)
        capabilities = self.bstack1ll11ll11ll_opy_.bstack1ll1l1111ll_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll11l11lll_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᆞ"))
            return
        driver = self.bstack1ll11ll11ll_opy_.bstack1ll11lll111_opy_(f, instance, bstack1llllll111l_opy_, *args, **kwargs)
        test_name = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll111l111l_opy_)
        if not test_name:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡳࡳࡥࡡࡧࡶࡨࡶࡤࡺࡥࡴࡶ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡲࡦࡳࡥࠣᆟ"))
            return
        test_uuid = f.bstack1111111l1l_opy_(instance, TestFramework.bstack1ll11l11l1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡴࡴ࡟ࡢࡨࡷࡩࡷࡥࡴࡦࡵࡷ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡺࡻࡩࡥࠤᆠ"))
            return
        if isinstance(self.bstack1ll11ll11ll_opy_, bstack1ll1lll111l_opy_):
            framework_name = bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᆡ")
        else:
            framework_name = bstack111l111_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨᆢ")
        self.bstack1llllll11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1l1l1lll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࠣᆣ"))
            return
        bstack1l1111lll_opy_ = datetime.now()
        bstack1ll11ll1l11_opy_ = self.scripts.get(framework_name, {}).get(bstack111l111_opy_ (u"ࠣࡵࡦࡥࡳࠨᆤ"), None)
        if not bstack1ll11ll1l11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࠫࡸࡩࡡ࡯ࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᆥ") + str(framework_name) + bstack111l111_opy_ (u"ࠥࠤࠧᆦ"))
            return
        if self.bstack1ll1111llll_opy_:
            arg = dict()
            arg[bstack111l111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᆧ")] = method if method else bstack111l111_opy_ (u"ࠧࠨᆨ")
            arg[bstack111l111_opy_ (u"ࠨࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩࠨᆩ")] = self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠢࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠢᆪ")]
            arg[bstack111l111_opy_ (u"ࠣࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩࠨᆫ")] = self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠤࡷࡩࡸࡺࡨࡶࡤࡢࡦࡺ࡯࡬ࡥࡡࡸࡹ࡮ࡪࠢᆬ")]
            arg[bstack111l111_opy_ (u"ࠥࡥࡺࡺࡨࡉࡧࡤࡨࡪࡸࠢᆭ")] = self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠦࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠤᆮ")]
            arg[bstack111l111_opy_ (u"ࠧࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠤᆯ")] = self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠨࡴࡩࡡ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠧᆰ")]
            arg[bstack111l111_opy_ (u"ࠢࡴࡥࡤࡲ࡙࡯࡭ࡦࡵࡷࡥࡲࡶࠢᆱ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11l11l11_opy_ = bstack1ll11ll1l11_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11l11l11_opy_)
            return
        instance = bstack11111111ll_opy_.bstack1lllll11l1l_opy_(driver)
        if instance:
            if not bstack11111111ll_opy_.bstack1111111l1l_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll1l11ll11_opy_, False):
                bstack11111111ll_opy_.bstack1111111111_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll1l11ll11_opy_, True)
            else:
                self.logger.info(bstack111l111_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡬ࡲࠥࡶࡲࡰࡩࡵࡩࡸࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀࠤࡲ࡫ࡴࡩࡱࡧࡁࠧᆲ") + str(method) + bstack111l111_opy_ (u"ࠤࠥᆳ"))
                return
        self.logger.info(bstack111l111_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࠽ࠣᆴ") + str(method) + bstack111l111_opy_ (u"ࠦࠧᆵ"))
        if framework_name == bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᆶ"):
            result = self.bstack1ll11ll11ll_opy_.bstack1ll111l1lll_opy_(driver, bstack1ll11ll1l11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1l11_opy_, {bstack111l111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᆷ"): method if method else bstack111l111_opy_ (u"ࠢࠣᆸ")})
        bstack1llll1111l1_opy_.end(EVENTS.bstack1l1l1lll1_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᆹ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᆺ"), True, None, command=method)
        if instance:
            bstack11111111ll_opy_.bstack1111111111_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll1l11ll11_opy_, False)
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠢᆻ"), datetime.now() - bstack1l1111lll_opy_)
        return result
        def bstack1ll11l111ll_opy_(self, driver: object, framework_name, bstack1lll1l1l1l_opy_: str):
            self.bstack1ll111l1l11_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll1l1111l1_opy_ = self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠦࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠦᆼ")]
            req.bstack1lll1l1l1l_opy_ = bstack1lll1l1l1l_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1lll1l11l1l_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack111l111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᆽ") + str(r) + bstack111l111_opy_ (u"ࠨࠢᆾ"))
                else:
                    bstack1ll1l11lll1_opy_ = json.loads(r.bstack1ll11l111l1_opy_.decode(bstack111l111_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ᆿ")))
                    if bstack1lll1l1l1l_opy_ == bstack111l111_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠬᇀ"):
                        return bstack1ll1l11lll1_opy_.get(bstack111l111_opy_ (u"ࠤࡧࡥࡹࡧࠢᇁ"), [])
                    else:
                        return bstack1ll1l11lll1_opy_.get(bstack111l111_opy_ (u"ࠥࡨࡦࡺࡡࠣᇂ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack111l111_opy_ (u"ࠦࡷࡶࡣ࠮ࡧࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡰࡱࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࠢࡩࡶࡴࡳࠠࡤ࡮࡬࠾ࠥࠨᇃ") + str(e) + bstack111l111_opy_ (u"ࠧࠨᇄ"))
    @measure(event_name=EVENTS.bstack11ll1ll111_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack111l111_opy_ (u"ࠨࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡶࡪࡹࡵ࡭ࡶࡶ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᇅ"))
            return
        if self.bstack1ll1111llll_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡡࡱࡲࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᇆ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l111ll_opy_(driver, framework_name, bstack111l111_opy_ (u"ࠣࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࠧᇇ"))
        bstack1ll11ll1l11_opy_ = self.scripts.get(framework_name, {}).get(bstack111l111_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸࠨᇈ"), None)
        if not bstack1ll11ll1l11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᇉ") + str(framework_name) + bstack111l111_opy_ (u"ࠦࠧᇊ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1111lll_opy_ = datetime.now()
        if framework_name == bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᇋ"):
            result = self.bstack1ll11ll11ll_opy_.bstack1ll111l1lll_opy_(driver, bstack1ll11ll1l11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1l11_opy_)
        instance = bstack11111111ll_opy_.bstack1lllll11l1l_opy_(driver)
        if instance:
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࠤᇌ"), datetime.now() - bstack1l1111lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1111l1111_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack111l111_opy_ (u"ࠢࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡷ࡫ࡳࡶ࡮ࡷࡷࡤࡹࡵ࡮࡯ࡤࡶࡾࡀࠠࡢ࠳࠴ࡽࠥࡴ࡯ࡵࠢࡨࡲࡦࡨ࡬ࡦࡦࠥᇍ"))
            return
        if self.bstack1ll1111llll_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll11l111ll_opy_(driver, framework_name, bstack111l111_opy_ (u"ࠨࡩࡨࡸࡗ࡫ࡳࡶ࡮ࡷࡷࡘࡻ࡭࡮ࡣࡵࡽࠬᇎ"))
        bstack1ll11ll1l11_opy_ = self.scripts.get(framework_name, {}).get(bstack111l111_opy_ (u"ࠤࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾࠨᇏ"), None)
        if not bstack1ll11ll1l11_opy_:
            self.logger.debug(bstack111l111_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩࠣࡷࡨࡸࡩࡱࡶࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࠤᇐ") + str(framework_name) + bstack111l111_opy_ (u"ࠦࠧᇑ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1l1111lll_opy_ = datetime.now()
        if framework_name == bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩᇒ"):
            result = self.bstack1ll11ll11ll_opy_.bstack1ll111l1lll_opy_(driver, bstack1ll11ll1l11_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1l11_opy_)
        instance = bstack11111111ll_opy_.bstack1lllll11l1l_opy_(driver)
        if instance:
            instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻࠥᇓ"), datetime.now() - bstack1l1111lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll1l11ll1l_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1ll11ll1l1l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll111l1l11_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1lll1l11l1l_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠢࡳࡧࡦࡩ࡮ࡼࡥࡥࠢࡩࡶࡴࡳࠠࡴࡧࡵࡺࡪࡸ࠺ࠡࠤᇔ") + str(r) + bstack111l111_opy_ (u"ࠣࠤᇕ"))
            else:
                self.bstack1ll11l1llll_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack111l111_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶ࠿ࠦࠢᇖ") + str(e) + bstack111l111_opy_ (u"ࠥࠦᇗ"))
            traceback.print_exc()
            raise e
    def bstack1ll11l1llll_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡱࡵࡡࡥࡡࡦࡳࡳ࡬ࡩࡨ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡬࡯ࡶࡰࡧࠦᇘ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll1111llll_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᇙ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll1l11111l_opy_[bstack111l111_opy_ (u"ࠨࡴࡩࡡ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠧᇚ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll1l11111l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll11lllll1_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11ll11l1_opy_ and command.module == self.bstack1ll11l1l1l1_opy_:
                        if command.method and not command.method in bstack1ll11lllll1_opy_:
                            bstack1ll11lllll1_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll11lllll1_opy_[command.method]:
                            bstack1ll11lllll1_opy_[command.method][command.name] = list()
                        bstack1ll11lllll1_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll11lllll1_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll11lll11l_opy_(
        self,
        f: bstack1lll1l11l11_opy_,
        exec: Tuple[bstack1lllll1ll1l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11ll11ll_opy_, bstack1ll1lll111l_opy_) and method_name != bstack111l111_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࠨᇛ"):
            return
        if bstack11111111ll_opy_.bstack1lllll1l111_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll111l1ll1_opy_):
            return
        if f.bstack1ll1l11l11l_opy_(method_name, *args):
            bstack1ll11ll1lll_opy_ = False
            desired_capabilities = f.bstack1ll111ll1ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll1l111lll_opy_(instance)
                platform_index = f.bstack1111111l1l_opy_(instance, bstack1lll1l11l11_opy_.bstack1ll11l1lll1_opy_, 0)
                bstack1ll11l1ll1l_opy_ = datetime.now()
                r = self.bstack1ll11ll1l1l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack111111l1_opy_(bstack111l111_opy_ (u"ࠣࡩࡵࡴࡨࡀࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡣࡰࡰࡩ࡭࡬ࠨᇜ"), datetime.now() - bstack1ll11l1ll1l_opy_)
                bstack1ll11ll1lll_opy_ = r.success
            else:
                self.logger.error(bstack111l111_opy_ (u"ࠤࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡨࡪࡹࡩࡳࡧࡧࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࡀࠦᇝ") + str(desired_capabilities) + bstack111l111_opy_ (u"ࠥࠦᇞ"))
            f.bstack1111111111_opy_(instance, bstack1lll11ll11l_opy_.bstack1ll111l1ll1_opy_, bstack1ll11ll1lll_opy_)
    def bstack11ll111lll_opy_(self, test_tags):
        bstack1ll11ll1l1l_opy_ = self.config.get(bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᇟ"))
        if not bstack1ll11ll1l1l_opy_:
            return True
        try:
            include_tags = bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᇠ")] if bstack111l111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᇡ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᇢ")], list) else []
            exclude_tags = bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᇣ")] if bstack111l111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᇤ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᇥ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack111l111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᇦ") + str(error))
        return False
    def bstack1l11llll1l_opy_(self, caps):
        try:
            if self.bstack1ll1111llll_opy_:
                bstack1ll11llll1l_opy_ = caps.get(bstack111l111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᇧ"))
                if bstack1ll11llll1l_opy_ is not None and str(bstack1ll11llll1l_opy_).lower() == bstack111l111_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢᇨ"):
                    bstack1ll111l1l1l_opy_ = caps.get(bstack111l111_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᇩ")) or caps.get(bstack111l111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᇪ"))
                    if bstack1ll111l1l1l_opy_ is not None and int(bstack1ll111l1l1l_opy_) < 11:
                        self.logger.warning(bstack111l111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡄࡲࡩࡸ࡯ࡪࡦࠣ࠵࠶ࠦࡡ࡯ࡦࠣࡥࡧࡵࡶࡦ࠰ࠣࡇࡺࡸࡲࡦࡰࡷࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠ࠾ࠤᇫ") + str(bstack1ll111l1l1l_opy_) + bstack111l111_opy_ (u"ࠥࠦᇬ"))
                        return False
                return True
            bstack1ll11l1l1ll_opy_ = caps.get(bstack111l111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᇭ"), {}).get(bstack111l111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᇮ"), caps.get(bstack111l111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᇯ"), bstack111l111_opy_ (u"ࠧࠨᇰ")))
            if bstack1ll11l1l1ll_opy_:
                self.logger.warning(bstack111l111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᇱ"))
                return False
            browser = caps.get(bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᇲ"), bstack111l111_opy_ (u"ࠪࠫᇳ")).lower()
            if browser != bstack111l111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᇴ"):
                self.logger.warning(bstack111l111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᇵ"))
                return False
            bstack1ll1l11l1l1_opy_ = bstack1ll111l11ll_opy_
            if not self.config.get(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᇶ")) or self.config.get(bstack111l111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫᇷ")):
                bstack1ll1l11l1l1_opy_ = bstack1ll11lll1ll_opy_
            browser_version = caps.get(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᇸ"))
            if not browser_version:
                browser_version = caps.get(bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᇹ"), {}).get(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᇺ"), bstack111l111_opy_ (u"ࠫࠬᇻ"))
            if browser_version and browser_version != bstack111l111_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᇼ") and int(browser_version.split(bstack111l111_opy_ (u"࠭࠮ࠨᇽ"))[0]) <= bstack1ll1l11l1l1_opy_:
                self.logger.warning(bstack111l111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࠤᇾ") + str(bstack1ll1l11l1l1_opy_) + bstack111l111_opy_ (u"ࠣ࠰ࠥᇿ"))
                return False
            bstack1ll111ll111_opy_ = caps.get(bstack111l111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪሀ"), {}).get(bstack111l111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪሁ"))
            if not bstack1ll111ll111_opy_:
                bstack1ll111ll111_opy_ = caps.get(bstack111l111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩሂ"), {})
            if bstack1ll111ll111_opy_ and bstack111l111_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩሃ") in bstack1ll111ll111_opy_.get(bstack111l111_opy_ (u"࠭ࡡࡳࡩࡶࠫሄ"), []):
                self.logger.warning(bstack111l111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤህ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack111l111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥሆ") + str(error))
            return False
    def bstack1ll1l111111_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll111ll11l_opy_ = {
            bstack111l111_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩሇ"): test_uuid,
        }
        bstack1ll11l1ll11_opy_ = {}
        if result.success:
            bstack1ll11l1ll11_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll11l1l111_opy_(bstack1ll111ll11l_opy_, bstack1ll11l1ll11_opy_)
    def bstack1llllll11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll11llll11_opy_ = None
        try:
            self.bstack1ll111l1l11_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack111l111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥለ")
            req.script_name = bstack111l111_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤሉ")
            r = self.bstack1lll1l11l1l_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack111l111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡥࡴ࡬ࡺࡪࡸࠠࡦࡺࡨࡧࡺࡺࡥࠡࡲࡤࡶࡦࡳࡳࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࠣሊ") + str(r.error) + bstack111l111_opy_ (u"ࠨࠢላ"))
            else:
                bstack1ll111ll11l_opy_ = self.bstack1ll1l111111_opy_(test_uuid, r)
                bstack1ll11ll1l11_opy_ = r.script
            self.logger.debug(bstack111l111_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪሌ") + str(bstack1ll111ll11l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11ll1l11_opy_:
                self.logger.debug(bstack111l111_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨࠢࡶࡧࡷ࡯ࡰࡵࠢࡩࡳࡷࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࠣል") + str(framework_name) + bstack111l111_opy_ (u"ࠤࠣࠦሎ"))
                return
            bstack1ll11llll11_opy_ = bstack1llll1111l1_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1ll11ll111l_opy_.value)
            self.bstack1ll111l11l1_opy_(driver, bstack1ll11ll1l11_opy_, bstack1ll111ll11l_opy_, framework_name)
            self.logger.info(bstack111l111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨሏ"))
            bstack1llll1111l1_opy_.end(EVENTS.bstack1ll11ll111l_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦሐ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥሑ"), True, None, command=bstack111l111_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫሒ"),test_name=name)
        except Exception as bstack1ll1111ll1l_opy_:
            self.logger.error(bstack111l111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤሓ") + bstack111l111_opy_ (u"ࠣࡵࡷࡶ࠭ࡶࡡࡵࡪࠬࠦሔ") + bstack111l111_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦሕ") + str(bstack1ll1111ll1l_opy_))
            bstack1llll1111l1_opy_.end(EVENTS.bstack1ll11ll111l_opy_.value, bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥሖ"), bstack1ll11llll11_opy_+bstack111l111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤሗ"), False, bstack1ll1111ll1l_opy_, command=bstack111l111_opy_ (u"ࠬࡹࡡࡷࡧࡕࡩࡸࡻ࡬ࡵࡵࠪመ"),test_name=name)
    def bstack1ll111l11l1_opy_(self, driver, bstack1ll11ll1l11_opy_, bstack1ll111ll11l_opy_, framework_name):
        if framework_name == bstack111l111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪሙ"):
            self.bstack1ll11ll11ll_opy_.bstack1ll111l1lll_opy_(driver, bstack1ll11ll1l11_opy_, bstack1ll111ll11l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11ll1l11_opy_, bstack1ll111ll11l_opy_))
    def _1ll1111lll1_opy_(self, instance: bstack1lll1lllll1_opy_, args: Tuple) -> list:
        bstack111l111_opy_ (u"ࠢࠣࠤࡈࡼࡹࡸࡡࡤࡶࠣࡸࡦ࡭ࡳࠡࡤࡤࡷࡪࡪࠠࡰࡰࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫࠯ࠤࠥࠦሚ")
        if bstack111l111_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠬማ") in instance.bstack1ll11l11ll1_opy_:
            return args[2].tags if hasattr(args[2], bstack111l111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧሜ")) else []
        if hasattr(args[0], bstack111l111_opy_ (u"ࠪࡳࡼࡴ࡟࡮ࡣࡵ࡯ࡪࡸࡳࠨም")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll11l11lll_opy_(self, tags, capabilities):
        return self.bstack11ll111lll_opy_(tags) and self.bstack1l11llll1l_opy_(capabilities)