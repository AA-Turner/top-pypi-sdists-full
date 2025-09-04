# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lllll1ll1l_opy_ import (
    bstack1lllll11111_opy_,
    bstack1llll1lllll_opy_,
    bstack1llllllll11_opy_,
    bstack1llllllll1l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll1l1ll1ll_opy_ import bstack1lll1l111ll_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_, bstack1lll1l1ll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1ll1llll11l_opy_ import bstack1lll1lll111_opy_
from browserstack_sdk.sdk_cli.bstack1llll111l1l_opy_ import bstack1llll11lll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll111l111_opy_ import bstack1lll11111l1_opy_
from browserstack_sdk.sdk_cli.bstack1ll1ll11l1l_opy_ import bstack1ll1lll1lll_opy_
from bstack_utils.helper import bstack1ll11lll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack1lllll1ll_opy_ import bstack1lll11111ll_opy_
import grpc
import traceback
import json
class bstack1lll111ll1l_opy_(bstack1lll1lll111_opy_):
    bstack1ll111ll1ll_opy_ = False
    bstack1ll11l111ll_opy_ = bstack1111l1l_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᆃ")
    bstack1ll111ll1l1_opy_ = bstack1111l1l_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᆄ")
    bstack1ll11lll1ll_opy_ = bstack1111l1l_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥᆅ")
    bstack1ll11ll11l1_opy_ = bstack1111l1l_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦᆆ")
    bstack1ll1l11l111_opy_ = bstack1111l1l_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣᆇ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1ll1l1l1l11_opy_, bstack1lll1l11111_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1ll11l11l11_opy_ = False
        self.bstack1ll1111lll1_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1ll11llll1l_opy_ = bstack1lll1l11111_opy_
        bstack1ll1l1l1l11_opy_.bstack1ll111lll1l_opy_((bstack1lllll11111_opy_.bstack1llll1lll11_opy_, bstack1llll1lllll_opy_.PRE), self.bstack1ll1l111l1l_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.PRE), self.bstack1ll1111l1l1_opy_)
        TestFramework.bstack1ll111lll1l_opy_((bstack1lll1lllll1_opy_.TEST, bstack1ll1llll1ll_opy_.POST), self.bstack1ll11llll11_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1ll1111l1l1_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11ll1ll1_opy_(instance, args)
        test_framework = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111lll11_opy_)
        if self.bstack1ll11l11l11_opy_:
            self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣᆈ")] = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        if bstack1111l1l_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᆉ") in instance.bstack1ll11ll1111_opy_:
            platform_index = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll11l1ll1l_opy_)
            self.accessibility = self.bstack1ll111l1l1l_opy_(tags, self.config[bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᆊ")][platform_index])
        else:
            capabilities = self.bstack1ll11llll1l_opy_.bstack1ll11l1llll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᆋ") + str(kwargs) + bstack1111l1l_opy_ (u"ࠧࠨᆌ"))
                return
            self.accessibility = self.bstack1ll111l1l1l_opy_(tags, capabilities)
        if self.bstack1ll11llll1l_opy_.pages and self.bstack1ll11llll1l_opy_.pages.values():
            bstack1ll111l11ll_opy_ = list(self.bstack1ll11llll1l_opy_.pages.values())
            if bstack1ll111l11ll_opy_ and isinstance(bstack1ll111l11ll_opy_[0], (list, tuple)) and bstack1ll111l11ll_opy_[0]:
                bstack1ll111lllll_opy_ = bstack1ll111l11ll_opy_[0][0]
                if callable(bstack1ll111lllll_opy_):
                    page = bstack1ll111lllll_opy_()
                    def bstack111l11ll1_opy_():
                        self.get_accessibility_results(page, bstack1111l1l_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᆍ"))
                    def bstack1ll11ll1l11_opy_():
                        self.get_accessibility_results_summary(page, bstack1111l1l_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᆎ"))
                    setattr(page, bstack1111l1l_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᆏ"), bstack111l11ll1_opy_)
                    setattr(page, bstack1111l1l_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᆐ"), bstack1ll11ll1l11_opy_)
        self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᆑ") + str(self.accessibility) + bstack1111l1l_opy_ (u"ࠦࠧᆒ"))
    def bstack1ll1l111l1l_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        driver: object,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        bstack1lllll11ll1_opy_: Tuple[bstack1lllll11111_opy_, bstack1llll1lllll_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll1l1lll_opy_ = datetime.now()
            self.bstack1ll111l1lll_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᆓ"), datetime.now() - bstack1ll1l1lll_opy_)
            if (
                not f.bstack1ll111l111l_opy_(method_name)
                or f.bstack1ll1l111ll1_opy_(method_name, *args)
                or f.bstack1ll1l111lll_opy_(method_name, *args)
            ):
                return
            if not f.bstack1lllll1l11l_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll11lll1ll_opy_, False):
                if not bstack1lll111ll1l_opy_.bstack1ll111ll1ll_opy_:
                    self.logger.warning(bstack1111l1l_opy_ (u"ࠨ࡛ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࠤᆔ") + str(f.platform_index) + bstack1111l1l_opy_ (u"ࠢ࡞ࠢࡤ࠵࠶ࡿࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠦࡨࡢࡸࡨࠤࡳࡵࡴࠡࡤࡨࡩࡳࠦࡳࡦࡶࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡹࡥࡴࡵ࡬ࡳࡳࠨᆕ"))
                    bstack1lll111ll1l_opy_.bstack1ll111ll1ll_opy_ = True
                return
            bstack1ll11l1l11l_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1ll11l1l11l_opy_:
                platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_, 0)
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡ࡬ࡲࡩ࡫ࡸ࠾ࡽࡳࡰࡦࡺࡦࡰࡴࡰࡣ࡮ࡴࡤࡦࡺࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᆖ") + str(f.framework_name) + bstack1111l1l_opy_ (u"ࠤࠥᆗ"))
                return
            command_name = f.bstack1ll111llll1_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡱ࡮ࡹࡳࡪࡰࡪࠤࡨࡵ࡭࡮ࡣࡱࡨࡤࡴࡡ࡮ࡧࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࠧᆘ") + str(method_name) + bstack1111l1l_opy_ (u"ࠦࠧᆙ"))
                return
            bstack1ll11ll11ll_opy_ = f.bstack1lllll1l11l_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll1l11l111_opy_, False)
            if command_name == bstack1111l1l_opy_ (u"ࠧ࡭ࡥࡵࠤᆚ") and not bstack1ll11ll11ll_opy_:
                f.bstack1lllllllll1_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll1l11l111_opy_, True)
                bstack1ll11ll11ll_opy_ = True
            if not bstack1ll11ll11ll_opy_ and not self.bstack1ll11l11l11_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨ࡮ࡰࠢࡘࡖࡑࠦ࡬ࡰࡣࡧࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᆛ") + str(command_name) + bstack1111l1l_opy_ (u"ࠢࠣᆜ"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡰࡲࠤࡦ࠷࠱ࡺࠢࡶࡧࡷ࡯ࡰࡵࡵࠣࡪࡴࡸࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᆝ") + str(command_name) + bstack1111l1l_opy_ (u"ࠤࠥᆞ"))
                return
            self.logger.info(bstack1111l1l_opy_ (u"ࠥࡶࡺࡴ࡮ࡪࡰࡪࠤࢀࡲࡥ࡯ࠪࡶࡧࡷ࡯ࡰࡵࡵࡢࡸࡴࡥࡲࡶࡰࠬࢁࠥࡹࡣࡳ࡫ࡳࡸࡸࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࡁࠧᆟ") + str(command_name) + bstack1111l1l_opy_ (u"ࠦࠧᆠ"))
            scripts = [(s, bstack1ll11l1l11l_opy_[s]) for s in scripts_to_run if s in bstack1ll11l1l11l_opy_]
            for script_name, bstack1ll11ll1lll_opy_ in scripts:
                try:
                    bstack1ll1l1lll_opy_ = datetime.now()
                    if script_name == bstack1111l1l_opy_ (u"ࠧࡹࡣࡢࡰࠥᆡ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                    instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡡ࠲࠳ࡼ࠾ࠧᆢ") + script_name, datetime.now() - bstack1ll1l1lll_opy_)
                    if isinstance(result, dict) and not result.get(bstack1111l1l_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᆣ"), True):
                        self.logger.warning(bstack1111l1l_opy_ (u"ࠣࡵ࡮࡭ࡵࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡵࡩࡲࡧࡩ࡯࡫ࡱ࡫ࠥࡹࡣࡳ࡫ࡳࡸࡸࡀࠠࠣᆤ") + str(result) + bstack1111l1l_opy_ (u"ࠤࠥᆥ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1111l1l_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠢࡨࡼࡪࡩࡵࡵ࡫ࡱ࡫ࠥࡹࡣࡳ࡫ࡳࡸࡂࢁࡳࡤࡴ࡬ࡴࡹࡥ࡮ࡢ࡯ࡨࢁࠥ࡫ࡲࡳࡱࡵࡁࠧᆦ") + str(e) + bstack1111l1l_opy_ (u"ࠦࠧᆧ"))
        except Exception as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡵ࡮ࡠࡤࡨࡪࡴࡸࡥࡠࡧࡻࡩࡨࡻࡴࡦࠢࡨࡶࡷࡵࡲ࠾ࠤᆨ") + str(e) + bstack1111l1l_opy_ (u"ࠨࠢᆩ"))
    def bstack1ll11llll11_opy_(
        self,
        f: TestFramework,
        instance: bstack1lll1l1ll1l_opy_,
        bstack1lllll11ll1_opy_: Tuple[bstack1lll1lllll1_opy_, bstack1ll1llll1ll_opy_],
        *args,
        **kwargs,
    ):
        tags = self._1ll11ll1ll1_opy_(instance, args)
        capabilities = self.bstack1ll11llll1l_opy_.bstack1ll11l1llll_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        self.accessibility = self.bstack1ll111l1l1l_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡩࡳࡧࡢ࡭ࡧࡧࠦᆪ"))
            return
        driver = self.bstack1ll11llll1l_opy_.bstack1ll1l11l11l_opy_(f, instance, bstack1lllll11ll1_opy_, *args, **kwargs)
        test_name = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll111l1l11_opy_)
        if not test_name:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣࡱࡱࡣࡦ࡬ࡴࡦࡴࡢࡸࡪࡹࡴ࠻ࠢࡰ࡭ࡸࡹࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡰࡤࡱࡪࠨᆫ"))
            return
        test_uuid = f.bstack1lllll1l11l_opy_(instance, TestFramework.bstack1ll1111ll1l_opy_)
        if not test_uuid:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡲࡲࡤࡧࡦࡵࡧࡵࡣࡹ࡫ࡳࡵ࠼ࠣࡱ࡮ࡹࡳࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡸࡹ࡮ࡪࠢᆬ"))
            return
        if isinstance(self.bstack1ll11llll1l_opy_, bstack1lll11111l1_opy_):
            framework_name = bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᆭ")
        else:
            framework_name = bstack1111l1l_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᆮ")
        self.bstack11ll1l11_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1ll11ll1l1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࠨᆯ"))
            return
        bstack1ll1l1lll_opy_ = datetime.now()
        bstack1ll11ll1lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1111l1l_opy_ (u"ࠨࡳࡤࡣࡱࠦᆰ"), None)
        if not bstack1ll11ll1lll_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠢࡱࡧࡵࡪࡴࡸ࡭ࡠࡵࡦࡥࡳࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡶࡧࡦࡴࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᆱ") + str(framework_name) + bstack1111l1l_opy_ (u"ࠣࠢࠥᆲ"))
            return
        if self.bstack1ll11l11l11_opy_:
            arg = dict()
            arg[bstack1111l1l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᆳ")] = method if method else bstack1111l1l_opy_ (u"ࠥࠦᆴ")
            arg[bstack1111l1l_opy_ (u"ࠦࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠦᆵ")] = self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᆶ")]
            arg[bstack1111l1l_opy_ (u"ࠨࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠦᆷ")] = self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠢࡵࡧࡶࡸ࡭ࡻࡢࡠࡤࡸ࡭ࡱࡪ࡟ࡶࡷ࡬ࡨࠧᆸ")]
            arg[bstack1111l1l_opy_ (u"ࠣࡣࡸࡸ࡭ࡎࡥࡢࡦࡨࡶࠧᆹ")] = self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠢᆺ")]
            arg[bstack1111l1l_opy_ (u"ࠥࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠢᆻ")] = self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᆼ")]
            arg[bstack1111l1l_opy_ (u"ࠧࡹࡣࡢࡰࡗ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠧᆽ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1ll11l111l1_opy_ = bstack1ll11ll1lll_opy_ % json.dumps(arg)
            driver.execute_script(bstack1ll11l111l1_opy_)
            return
        instance = bstack1llllllll11_opy_.bstack1lllll1111l_opy_(driver)
        if instance:
            if not bstack1llllllll11_opy_.bstack1lllll1l11l_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll11ll11l1_opy_, False):
                bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll11ll11l1_opy_, True)
            else:
                self.logger.info(bstack1111l1l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦࡡ࡭ࡴࡨࡥࡩࡿࠠࡪࡰࠣࡴࡷࡵࡧࡳࡧࡶࡷࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾࠢࡰࡩࡹ࡮࡯ࡥ࠿ࠥᆾ") + str(method) + bstack1111l1l_opy_ (u"ࠢࠣᆿ"))
                return
        self.logger.info(bstack1111l1l_opy_ (u"ࠣࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴ࠺ࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᇀ") + str(method) + bstack1111l1l_opy_ (u"ࠤࠥᇁ"))
        if framework_name == bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᇂ"):
            result = self.bstack1ll11llll1l_opy_.bstack1ll11llllll_opy_(driver, bstack1ll11ll1lll_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1lll_opy_, {bstack1111l1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᇃ"): method if method else bstack1111l1l_opy_ (u"ࠧࠨᇄ")})
        bstack1lll11111ll_opy_.end(EVENTS.bstack1ll11ll1l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᇅ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᇆ"), True, None, command=method)
        if instance:
            bstack1llllllll11_opy_.bstack1lllllllll1_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll11ll11l1_opy_, False)
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠣࡣ࠴࠵ࡾࡀࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲࠧᇇ"), datetime.now() - bstack1ll1l1lll_opy_)
        return result
        def bstack1ll111l1111_opy_(self, driver: object, framework_name, bstack1ll11l11l_opy_: str):
            self.bstack1ll1l1111ll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1ll11lll111_opy_ = self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠤࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠤᇈ")]
            req.bstack1ll11l11l_opy_ = bstack1ll11l11l_opy_
            req.session_id = self.bin_session_id
            try:
                r = self.bstack1ll1ll11l11_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥ࡬ࡲࡰ࡯ࠣࡷࡪࡸࡶࡦࡴ࠽ࠤࠧᇉ") + str(r) + bstack1111l1l_opy_ (u"ࠦࠧᇊ"))
                else:
                    bstack1ll11l11111_opy_ = json.loads(r.bstack1ll1111llll_opy_.decode(bstack1111l1l_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᇋ")))
                    if bstack1ll11l11l_opy_ == bstack1111l1l_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪᇌ"):
                        return bstack1ll11l11111_opy_.get(bstack1111l1l_opy_ (u"ࠢࡥࡣࡷࡥࠧᇍ"), [])
                    else:
                        return bstack1ll11l11111_opy_.get(bstack1111l1l_opy_ (u"ࠣࡦࡤࡸࡦࠨᇎ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1111l1l_opy_ (u"ࠤࡵࡴࡨ࠳ࡥࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡵࡶ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࠠࡧࡴࡲࡱࠥࡩ࡬ࡪ࠼ࠣࠦᇏ") + str(e) + bstack1111l1l_opy_ (u"ࠥࠦᇐ"))
    @measure(event_name=EVENTS.bstack1l1l11ll1l_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴ࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨᇑ"))
            return
        if self.bstack1ll11l11l11_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡦࡶࡰࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᇒ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll111l1111_opy_(driver, framework_name, bstack1111l1l_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᇓ"))
        bstack1ll11ll1lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1111l1l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࠦᇔ"), None)
        if not bstack1ll11ll1lll_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᇕ") + str(framework_name) + bstack1111l1l_opy_ (u"ࠤࠥᇖ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1l1lll_opy_ = datetime.now()
        if framework_name == bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᇗ"):
            result = self.bstack1ll11llll1l_opy_.bstack1ll11llllll_opy_(driver, bstack1ll11ll1lll_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1lll_opy_)
        instance = bstack1llllllll11_opy_.bstack1lllll1111l_opy_(driver)
        if instance:
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹࠢᇘ"), datetime.now() - bstack1ll1l1lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l11l111ll_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠧ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡵࡩࡸࡻ࡬ࡵࡵࡢࡷࡺࡳ࡭ࡢࡴࡼ࠾ࠥࡧ࠱࠲ࡻࠣࡲࡴࡺࠠࡦࡰࡤࡦࡱ࡫ࡤࠣᇙ"))
            return
        if self.bstack1ll11l11l11_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1ll111l1111_opy_(driver, framework_name, bstack1111l1l_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠪᇚ"))
        bstack1ll11ll1lll_opy_ = self.scripts.get(framework_name, {}).get(bstack1111l1l_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦᇛ"), None)
        if not bstack1ll11ll1lll_opy_:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠣ࡯࡬ࡷࡸ࡯࡮ࡨࠢࠪ࡫ࡪࡺࡒࡦࡵࡸࡰࡹࡹࡓࡶ࡯ࡰࡥࡷࡿࠧࠡࡵࡦࡶ࡮ࡶࡴࠡࡨࡲࡶࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᇜ") + str(framework_name) + bstack1111l1l_opy_ (u"ࠤࠥᇝ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1l1lll_opy_ = datetime.now()
        if framework_name == bstack1111l1l_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᇞ"):
            result = self.bstack1ll11llll1l_opy_.bstack1ll11llllll_opy_(driver, bstack1ll11ll1lll_opy_)
        else:
            result = driver.execute_async_script(bstack1ll11ll1lll_opy_)
        instance = bstack1llllllll11_opy_.bstack1lllll1111l_opy_(driver)
        if instance:
            instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࡹ࡟ࡴࡷࡰࡱࡦࡸࡹࠣᇟ"), datetime.now() - bstack1ll1l1lll_opy_)
        return result
    @measure(event_name=EVENTS.bstack1ll11lllll1_opy_, stage=STAGE.bstack1l1111l1ll_opy_)
    def bstack1ll11ll1l1l_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1ll1l1111ll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        try:
            r = self.bstack1ll1ll11l11_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᇠ") + str(r) + bstack1111l1l_opy_ (u"ࠨࠢᇡ"))
            else:
                self.bstack1ll11lll1l1_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1111l1l_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᇢ") + str(e) + bstack1111l1l_opy_ (u"ࠣࠤᇣ"))
            traceback.print_exc()
            raise e
    def bstack1ll11lll1l1_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᇤ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1ll11l11l11_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᇥ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1ll1111lll1_opy_[bstack1111l1l_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᇦ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1ll1111lll1_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1ll1111l11l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1ll11l111ll_opy_ and command.module == self.bstack1ll111ll1l1_opy_:
                        if command.method and not command.method in bstack1ll1111l11l_opy_:
                            bstack1ll1111l11l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1ll1111l11l_opy_[command.method]:
                            bstack1ll1111l11l_opy_[command.method][command.name] = list()
                        bstack1ll1111l11l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1ll1111l11l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1ll111l1lll_opy_(
        self,
        f: bstack1lll1l111ll_opy_,
        exec: Tuple[bstack1llllllll1l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1ll11llll1l_opy_, bstack1lll11111l1_opy_) and method_name != bstack1111l1l_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᇧ"):
            return
        if bstack1llllllll11_opy_.bstack1llll1l11ll_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll11lll1ll_opy_):
            return
        if f.bstack1ll11ll111l_opy_(method_name, *args):
            bstack1ll11l11ll1_opy_ = False
            desired_capabilities = f.bstack1ll1111l1ll_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1ll11l11l1l_opy_(instance)
                platform_index = f.bstack1lllll1l11l_opy_(instance, bstack1lll1l111ll_opy_.bstack1ll11l1ll1l_opy_, 0)
                bstack1ll111ll111_opy_ = datetime.now()
                r = self.bstack1ll11ll1l1l_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11l11lll_opy_(bstack1111l1l_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᇨ"), datetime.now() - bstack1ll111ll111_opy_)
                bstack1ll11l11ll1_opy_ = r.success
            else:
                self.logger.error(bstack1111l1l_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤᇩ") + str(desired_capabilities) + bstack1111l1l_opy_ (u"ࠣࠤᇪ"))
            f.bstack1lllllllll1_opy_(instance, bstack1lll111ll1l_opy_.bstack1ll11lll1ll_opy_, bstack1ll11l11ll1_opy_)
    def bstack11l111ll_opy_(self, test_tags):
        bstack1ll11ll1l1l_opy_ = self.config.get(bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇫ"))
        if not bstack1ll11ll1l1l_opy_:
            return True
        try:
            include_tags = bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᇬ")] if bstack1111l1l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᇭ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᇮ")], list) else []
            exclude_tags = bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᇯ")] if bstack1111l1l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᇰ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack1111l1l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᇱ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᇲ") + str(error))
        return False
    def bstack1l1lll1lll_opy_(self, caps):
        try:
            if self.bstack1ll11l11l11_opy_:
                bstack1ll11l1l1ll_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᇳ"))
                if bstack1ll11l1l1ll_opy_ is not None and str(bstack1ll11l1l1ll_opy_).lower() == bstack1111l1l_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᇴ"):
                    bstack1ll11l1l111_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᇵ")) or caps.get(bstack1111l1l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᇶ"))
                    if bstack1ll11l1l111_opy_ is not None and int(bstack1ll11l1l111_opy_) < 11:
                        self.logger.warning(bstack1111l1l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡂࡰࡧࡶࡴ࡯ࡤࠡ࠳࠴ࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫࠮ࠡࡅࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠢᇷ") + str(bstack1ll11l1l111_opy_) + bstack1111l1l_opy_ (u"ࠣࠤᇸ"))
                        return False
                return True
            bstack1ll11l1l1l1_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᇹ"), {}).get(bstack1111l1l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᇺ"), caps.get(bstack1111l1l_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᇻ"), bstack1111l1l_opy_ (u"ࠬ࠭ᇼ")))
            if bstack1ll11l1l1l1_opy_:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᇽ"))
                return False
            browser = caps.get(bstack1111l1l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᇾ"), bstack1111l1l_opy_ (u"ࠨࠩᇿ")).lower()
            if browser != bstack1111l1l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩሀ"):
                self.logger.warning(bstack1111l1l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨሁ"))
                return False
            bstack1ll1111ll11_opy_ = bstack1ll1l111l11_opy_
            if not self.config.get(bstack1111l1l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ሂ")) or self.config.get(bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩሃ")):
                bstack1ll1111ll11_opy_ = bstack1ll11l11lll_opy_
            browser_version = caps.get(bstack1111l1l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧሄ"))
            if not browser_version:
                browser_version = caps.get(bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨህ"), {}).get(bstack1111l1l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩሆ"), bstack1111l1l_opy_ (u"ࠩࠪሇ"))
            if browser_version and browser_version != bstack1111l1l_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪለ") and int(browser_version.split(bstack1111l1l_opy_ (u"ࠫ࠳࠭ሉ"))[0]) <= bstack1ll1111ll11_opy_:
                self.logger.warning(bstack1111l1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࠢሊ") + str(bstack1ll1111ll11_opy_) + bstack1111l1l_opy_ (u"ࠨ࠮ࠣላ"))
                return False
            bstack1ll111ll11l_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨሌ"), {}).get(bstack1111l1l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨል"))
            if not bstack1ll111ll11l_opy_:
                bstack1ll111ll11l_opy_ = caps.get(bstack1111l1l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧሎ"), {})
            if bstack1ll111ll11l_opy_ and bstack1111l1l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧሏ") in bstack1ll111ll11l_opy_.get(bstack1111l1l_opy_ (u"ࠫࡦࡸࡧࡴࠩሐ"), []):
                self.logger.warning(bstack1111l1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢሑ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣሒ") + str(error))
            return False
    def bstack1ll111l11l1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1ll1l11111l_opy_ = {
            bstack1111l1l_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧሓ"): test_uuid,
        }
        bstack1ll11l1111l_opy_ = {}
        if result.success:
            bstack1ll11l1111l_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1ll11lll11l_opy_(bstack1ll1l11111l_opy_, bstack1ll11l1111l_opy_)
    def bstack11ll1l11_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1ll111l1ll1_opy_ = None
        try:
            self.bstack1ll1l1111ll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1111l1l_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣሔ")
            req.script_name = bstack1111l1l_opy_ (u"ࠤࡶࡥࡻ࡫ࡒࡦࡵࡸࡰࡹࡹࠢሕ")
            r = self.bstack1ll1ll11l11_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠥࡶࡪࡩࡥࡪࡸࡨࡨࠥࡪࡲࡪࡸࡨࡶࠥ࡫ࡸࡦࡥࡸࡸࡪࠦࡰࡢࡴࡤࡱࡸࠦࡦࡳࡱࡰࠤࡸ࡫ࡲࡷࡧࡵ࠾ࠥࠨሖ") + str(r.error) + bstack1111l1l_opy_ (u"ࠦࠧሗ"))
            else:
                bstack1ll1l11111l_opy_ = self.bstack1ll111l11l1_opy_(test_uuid, r)
                bstack1ll11ll1lll_opy_ = r.script
            self.logger.debug(bstack1111l1l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨመ") + str(bstack1ll1l11111l_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1ll11ll1lll_opy_:
                self.logger.debug(bstack1111l1l_opy_ (u"ࠨࡰࡦࡴࡩࡳࡷࡳ࡟ࡴࡥࡤࡲ࠿ࠦ࡭ࡪࡵࡶ࡭ࡳ࡭ࠠࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨሙ") + str(framework_name) + bstack1111l1l_opy_ (u"ࠢࠡࠤሚ"))
                return
            bstack1ll111l1ll1_opy_ = bstack1lll11111ll_opy_.bstack1ll1l111111_opy_(EVENTS.bstack1ll1l1111l1_opy_.value)
            self.bstack1ll11l1lll1_opy_(driver, bstack1ll11ll1lll_opy_, bstack1ll1l11111l_opy_, framework_name)
            self.logger.info(bstack1111l1l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦማ"))
            bstack1lll11111ll_opy_.end(EVENTS.bstack1ll1l1111l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤሜ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠥ࠾ࡪࡴࡤࠣም"), True, None, command=bstack1111l1l_opy_ (u"ࠫࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠩሞ"),test_name=name)
        except Exception as bstack1ll11l1ll11_opy_:
            self.logger.error(bstack1111l1l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢሟ") + bstack1111l1l_opy_ (u"ࠨࡳࡵࡴࠫࡴࡦࡺࡨࠪࠤሠ") + bstack1111l1l_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤሡ") + str(bstack1ll11l1ll11_opy_))
            bstack1lll11111ll_opy_.end(EVENTS.bstack1ll1l1111l1_opy_.value, bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣሢ"), bstack1ll111l1ll1_opy_+bstack1111l1l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢሣ"), False, bstack1ll11l1ll11_opy_, command=bstack1111l1l_opy_ (u"ࠪࡷࡦࡼࡥࡓࡧࡶࡹࡱࡺࡳࠨሤ"),test_name=name)
    def bstack1ll11l1lll1_opy_(self, driver, bstack1ll11ll1lll_opy_, bstack1ll1l11111l_opy_, framework_name):
        if framework_name == bstack1111l1l_opy_ (u"ࠫࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨሥ"):
            self.bstack1ll11llll1l_opy_.bstack1ll11llllll_opy_(driver, bstack1ll11ll1lll_opy_, bstack1ll1l11111l_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1ll11ll1lll_opy_, bstack1ll1l11111l_opy_))
    def _1ll11ll1ll1_opy_(self, instance: bstack1lll1l1ll1l_opy_, args: Tuple) -> list:
        bstack1111l1l_opy_ (u"ࠧࠨࠢࡆࡺࡷࡶࡦࡩࡴࠡࡶࡤ࡫ࡸࠦࡢࡢࡵࡨࡨࠥࡵ࡮ࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠴ࠢࠣࠤሦ")
        if bstack1111l1l_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠪሧ") in instance.bstack1ll11ll1111_opy_:
            return args[2].tags if hasattr(args[2], bstack1111l1l_opy_ (u"ࠧࡵࡣࡪࡷࠬረ")) else []
        if hasattr(args[0], bstack1111l1l_opy_ (u"ࠨࡱࡺࡲࡤࡳࡡࡳ࡭ࡨࡶࡸ࠭ሩ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1ll111l1l1l_opy_(self, tags, capabilities):
        return self.bstack11l111ll_opy_(tags) and self.bstack1l1lll1lll_opy_(capabilities)