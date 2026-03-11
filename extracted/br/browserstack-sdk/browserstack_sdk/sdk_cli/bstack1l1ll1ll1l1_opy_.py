# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
from datetime import datetime
import os
import threading
from browserstack_sdk.sdk_cli.bstack1lll11111ll_opy_ import (
    bstack1ll1l1l11l1_opy_,
    bstack1ll1l11ll1l_opy_,
    bstack1ll1lllllll_opy_,
    bstack1ll1l1l111l_opy_,
)
from browserstack_sdk.sdk_cli.bstack1ll111llll1_opy_ import bstack1ll11lll111_opy_
from browserstack_sdk.sdk_cli.test_framework import TestFramework, TestFrameworkState, TestHookState, bstack1ll11l1ll1l_opy_
from typing import Tuple, Dict, Any, List, Union
from browserstack_sdk import sdk_pb2 as structs
from browserstack_sdk.sdk_cli.bstack1l1llllllll_opy_ import bstack1ll11111l11_opy_
from browserstack_sdk.sdk_cli.bstack1ll111ll111_opy_ import bstack1ll111l1lll_opy_
from browserstack_sdk.sdk_cli.bstack1l1ll1ll11l_opy_ import bstack1ll11111ll1_opy_
from browserstack_sdk.sdk_cli.bstack1lll1111l11_opy_ import bstack1lll111l1l1_opy_
from bstack_utils.helper import bstack1l1l11111l1_opy_
from bstack_utils.measure import measure
from bstack_utils.constants import *
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from bstack_utils import logger_utils
import grpc
import traceback
import json
class bstack1ll11l11lll_opy_(bstack1ll11111l11_opy_):
    bstack1l1l1l111l1_opy_ = False
    bstack1l1l11lllll_opy_ = bstack1ll111_opy_ (u"ࠥࡷࡪࡲࡥ࡯࡫ࡸࡱ࠳ࡽࡥࡣࡦࡵ࡭ࡻ࡫ࡲࠣᏝ")
    bstack1l1l11l111l_opy_ = bstack1ll111_opy_ (u"ࠦࡷ࡫࡭ࡰࡶࡨ࠲ࡼ࡫ࡢࡥࡴ࡬ࡺࡪࡸࠢᏞ")
    bstack1l1l1111l1l_opy_ = bstack1ll111_opy_ (u"ࠧࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤ࡯࡮ࡪࡶࠥᏟ")
    bstack1l11lll1l11_opy_ = bstack1ll111_opy_ (u"ࠨࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡩࡴࡡࡶࡧࡦࡴ࡮ࡪࡰࡪࠦᏠ")
    bstack1l1l1l1l11l_opy_ = bstack1ll111_opy_ (u"ࠢࡥࡴ࡬ࡺࡪࡸ࡟ࡩࡣࡶࡣࡺࡸ࡬ࠣᏡ")
    scripts: Dict[str, Dict[str, str]]
    commands: Dict[str, Dict[str, Dict[str, List[str]]]]
    def __init__(self, bstack1l1ll1l1lll_opy_, bstack1l1lllllll1_opy_):
        super().__init__()
        self.scripts = dict()
        self.commands = dict()
        self.accessibility = False
        self.bstack1l1l1l11111_opy_ = False
        self.bstack1l1l11l1l1l_opy_ = dict()
        self.bstack1l11llll_opy_ = logger_utils.bstack1111l1ll1_opy_(__name__)
        self.bstack1l1l11ll11l_opy_ = False
        self.bstack1l11lll11ll_opy_ = dict()
        if not self.is_enabled():
            return
        self.bstack1l1l11l1111_opy_ = bstack1l1lllllll1_opy_
        bstack1l1ll1l1lll_opy_.bstack1l1l1111111_opy_((bstack1ll1l1l11l1_opy_.bstack1ll1l11l11l_opy_, bstack1ll1l11ll1l_opy_.PRE), self.bstack1l1l111l1ll_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.PRE), self.bstack1l1l11ll1ll_opy_)
        TestFramework.bstack1l1l1111111_opy_((TestFrameworkState.TEST, TestHookState.POST), self.bstack1l11lll111l_opy_)
    def is_enabled(self) -> bool:
        return True
    def bstack1l1l11ll1ll_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        tags = self._1l1l1l11lll_opy_(instance, args)
        test_framework = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l11llllll1_opy_)
        if self.bstack1l1l1l11111_opy_:
            self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠣࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠣᏢ")] = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_)
        if bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭Ꮳ") in instance.bstack1l11lll1l1l_opy_:
            platform_index = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1l1ll11_opy_)
            self.accessibility = self.bstack1l11lll11l1_opy_(tags, self.config[bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭Ꮴ")][platform_index])
        else:
            capabilities = self.bstack1l1l11l1111_opy_.bstack1l11ll1lll1_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
            if not capabilities:
                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡴࡴ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡵࡧࡶࡸ࠿ࠦ࡮ࡰࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠡࡨࡲࡹࡳࡪࠠࡧࡱࡵࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦᏥ") + str(kwargs) + bstack1ll111_opy_ (u"ࠧࠨᏦ"))
                return
            self.accessibility = self.bstack1l11lll11l1_opy_(tags, capabilities)
        if self.bstack1l1l11l1111_opy_.pages and self.bstack1l1l11l1111_opy_.pages.values():
            bstack1l1l1ll1111_opy_ = list(self.bstack1l1l11l1111_opy_.pages.values())
            if bstack1l1l1ll1111_opy_ and isinstance(bstack1l1l1ll1111_opy_[0], (list, tuple)) and bstack1l1l1ll1111_opy_[0]:
                bstack1l11lllllll_opy_ = bstack1l1l1ll1111_opy_[0][0]
                if callable(bstack1l11lllllll_opy_):
                    page = bstack1l11lllllll_opy_()
                    def bstack111111l1_opy_():
                        self.get_accessibility_results(page, bstack1ll111_opy_ (u"ࠨࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠥᏧ"))
                    def bstack1l1l1l1ll1l_opy_():
                        self.get_accessibility_results_summary(page, bstack1ll111_opy_ (u"ࠢࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦᏨ"))
                    setattr(page, bstack1ll111_opy_ (u"ࠣࡩࡨࡸࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡖࡪࡹࡵ࡭ࡶࡶࠦᏩ"), bstack111111l1_opy_)
                    setattr(page, bstack1ll111_opy_ (u"ࠤࡪࡩࡹࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡗ࡫ࡳࡶ࡮ࡷࡗࡺࡳ࡭ࡢࡴࡼࠦᏪ"), bstack1l1l1l1ll1l_opy_)
        self.logger.debug(bstack1ll111_opy_ (u"ࠥࡷ࡭ࡵࡵ࡭ࡦࠣࡶࡺࡴࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯ࡹࡪࡃࠢᏫ") + str(self.accessibility) + bstack1ll111_opy_ (u"ࠦࠧᏬ"))
    def bstack1l1l111l1ll_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        driver: object,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        bstack1ll1l1l1l1l_opy_: Tuple[bstack1ll1l1l11l1_opy_, bstack1ll1l11ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            bstack1ll1l1l111_opy_ = datetime.now()
            self.bstack1l11llll111_opy_(f, exec, *args, **kwargs)
            instance, method_name = exec
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠧࡧ࠱࠲ࡻ࠽࡭ࡳ࡯ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡥࡲࡲ࡫࡯ࡧࠣᏭ"), datetime.now() - bstack1ll1l1l111_opy_)
            bstack1ll1l11111l_opy_ = instance.data.get(bstack1ll111_opy_ (u"࠭ࡲࡢࡰ࡮ࠫᏮ"), None)
            if (
                not f.bstack1l1l111111l_opy_(method_name)
                or f.bstack1l1l1l1111l_opy_(method_name, *args)
                or f.bstack1l1l11l11l1_opy_(method_name, *args)
                or (bstack1ll1l11111l_opy_ and int(bstack1ll1l11111l_opy_)>1)
            ):
                return
            if not f.bstack1lll111lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l1l1111l1l_opy_, False):
                if not bstack1ll11l11lll_opy_.bstack1l1l1l111l1_opy_:
                    self.logger.warning(bstack1ll111_opy_ (u"ࠢ࡜ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࠥᏯ") + str(f.platform_index) + bstack1ll111_opy_ (u"ࠣ࡟ࠣࡥ࠶࠷ࡹࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠠࡩࡣࡹࡩࠥࡴ࡯ࡵࠢࡥࡩࡪࡴࠠࡴࡧࡷࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡳࡦࡵࡶ࡭ࡴࡴࠢᏰ"))
                    bstack1ll11l11lll_opy_.bstack1l1l1l111l1_opy_ = True
                return
            bstack1l11lllll11_opy_ = self.scripts.get(f.framework_name, {})
            if not bstack1l11lllll11_opy_:
                platform_index = f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_, 0)
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢ࡭ࡳࡪࡥࡹ࠿ࡾࡴࡱࡧࡴࡧࡱࡵࡱࡤ࡯࡮ࡥࡧࡻࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࡃࠢᏱ") + str(f.framework_name) + bstack1ll111_opy_ (u"ࠥࠦᏲ"))
                return
            command_name = f.bstack1l1l11l1l11_opy_(*args)
            if not command_name:
                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥࡩ࡯࡮࡯ࡤࡲࡩࡥ࡮ࡢ࡯ࡨࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࠨᏳ") + str(method_name) + bstack1ll111_opy_ (u"ࠧࠨᏴ"))
                return
            bstack1l1l111l111_opy_ = f.bstack1lll111lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l1l1l1l11l_opy_, False)
            if command_name == bstack1ll111_opy_ (u"ࠨࡧࡦࡶࠥᏵ") and not bstack1l1l111l111_opy_:
                f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l1l1l1l11l_opy_, True)
                bstack1l1l111l111_opy_ = True
            if not bstack1l1l111l111_opy_ and not self.bstack1l1l1l11111_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡯ࡱ࡙ࠣࡗࡒࠠ࡭ࡱࡤࡨࡪࡪࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨ᏶") + str(command_name) + bstack1ll111_opy_ (u"ࠣࠤ᏷"))
                return
            scripts_to_run = self.commands.get(f.framework_name, {}).get(method_name, {}).get(command_name, [])
            if not scripts_to_run:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡱࡳࠥࡧ࠱࠲ࡻࠣࡷࡨࡸࡩࡱࡶࡶࠤ࡫ࡵࡲࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪ࠳࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪࢃࠠࡤࡱࡰࡱࡦࡴࡤࡠࡰࡤࡱࡪࡃࠢᏸ") + str(command_name) + bstack1ll111_opy_ (u"ࠥࠦᏹ"))
                return
            self.logger.info(bstack1ll111_opy_ (u"ࠦࡷࡻ࡮࡯࡫ࡱ࡫ࠥࢁ࡬ࡦࡰࠫࡷࡨࡸࡩࡱࡶࡶࡣࡹࡵ࡟ࡳࡷࡱ࠭ࢂࠦࡳࡤࡴ࡬ࡴࡹࡹࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥ࠾ࡽࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࠦࡣࡰ࡯ࡰࡥࡳࡪ࡟࡯ࡣࡰࡩࡂࠨᏺ") + str(command_name) + bstack1ll111_opy_ (u"ࠧࠨᏻ"))
            scripts = [(s, bstack1l11lllll11_opy_[s]) for s in scripts_to_run if s in bstack1l11lllll11_opy_]
            for script_name, bstack1l1l1ll11l1_opy_ in scripts:
                try:
                    bstack1ll1l1l111_opy_ = datetime.now()
                    if script_name == bstack1ll111_opy_ (u"ࠨࡳࡤࡣࡱࠦᏼ"):
                        result = self.perform_scan(driver, method=command_name, framework_name=f.framework_name)
                        try:
                            bstack1ll1l111l1_opy_ = {
                                bstack1ll111_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᏽ"): {
                                    bstack1ll111_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤ᏾"): bstack1ll111_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡅࡄࡒࠧ᏿"),
                                    bstack1ll111_opy_ (u"ࠥࡴࡦࡸࡡ࡮ࡧࡷࡩࡷࡹࠢ᐀"): [
                                        {
                                            bstack1ll111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᐁ"): command_name
                                        }
                                    ]
                                },
                                bstack1ll111_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᐂ"): {
                                    bstack1ll111_opy_ (u"ࠨࡢࡰࡦࡼࠦᐃ"): {
                                        bstack1ll111_opy_ (u"ࠢ࡮ࡵࡪࠦᐄ"): result.get(bstack1ll111_opy_ (u"ࠣ࡯ࡶ࡫ࠧᐅ"), bstack1ll111_opy_ (u"ࠤࠥᐆ")) if isinstance(result, dict) else bstack1ll111_opy_ (u"ࠥࠦᐇ"),
                                        bstack1ll111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᐈ"): result.get(bstack1ll111_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᐉ"), True) if isinstance(result, dict) else True
                                    }
                                }
                            }
                            self.bstack1l11llll_opy_.info(json.dumps(bstack1ll1l111l1_opy_, separators=(bstack1ll111_opy_ (u"ࠨࠬࠣᐊ"), bstack1ll111_opy_ (u"ࠢ࠻ࠤᐋ"))))
                        except Exception as bstack111ll1ll1l_opy_:
                            self.logger.debug(bstack1ll111_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡦࡥࡳࠦࡤࡢࡶࡤ࠾ࠥࠨᐌ") + str(bstack111ll1ll1l_opy_) + bstack1ll111_opy_ (u"ࠤࠥᐍ"))
                    instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࠤᐎ") + script_name, datetime.now() - bstack1ll1l1l111_opy_)
                    if isinstance(result, dict) and not result.get(bstack1ll111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧᐏ"), True):
                        self.logger.warning(bstack1ll111_opy_ (u"ࠧࡹ࡫ࡪࡲࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡲ࡬ࠦࡲࡦ࡯ࡤ࡭ࡳ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵࡵ࠽ࠤࠧᐐ") + str(result) + bstack1ll111_opy_ (u"ࠨࠢᐑ"))
                        break
                except Exception as e:
                    self.logger.error(bstack1ll111_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡥࡹࡧࡦࡹࡹ࡯࡮ࡨࠢࡶࡧࡷ࡯ࡰࡵ࠿ࡾࡷࡨࡸࡩࡱࡶࡢࡲࡦࡳࡥࡾࠢࡨࡶࡷࡵࡲ࠾ࠤᐒ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᐓ"))
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠤࡲࡲࡤࡨࡥࡧࡱࡵࡩࡤ࡫ࡸࡦࡥࡸࡸࡪࠦࡥࡳࡴࡲࡶࡂࠨᐔ") + str(e) + bstack1ll111_opy_ (u"ࠥࠦᐕ"))
    def bstack1l11lll111l_opy_(
        self,
        f: TestFramework,
        instance: bstack1ll11l1ll1l_opy_,
        bstack1ll1l1l1l1l_opy_: Tuple[TestFrameworkState, TestHookState],
        *args,
        **kwargs,
    ):
        if bstack1ll111_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠨᐖ") not in instance.bstack1l11lll1l1l_opy_:
            tags = self._1l1l1l11lll_opy_(instance, args)
            capabilities = self.bstack1l1l11l1111_opy_.bstack1l11ll1lll1_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
            self.accessibility = self.bstack1l11lll11l1_opy_(tags, capabilities)
        if not self.accessibility:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡵ࡮ࡠࡣࡩࡸࡪࡸ࡟ࡵࡧࡶࡸ࠿ࠦࡡ࠲࠳ࡼࠤࡳࡵࡴࠡࡧࡱࡥࡧࡲࡥࡥࠤᐗ"))
            return
        driver = self.bstack1l1l11l1111_opy_.bstack1l1l11l11ll_opy_(f, instance, bstack1ll1l1l1l1l_opy_, *args, **kwargs)
        test_name = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l11llll1_opy_)
        if not test_name:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨ࡯࡯ࡡࡤࡪࡹ࡫ࡲࡠࡶࡨࡷࡹࡀࠠ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡶࡨࡷࡹࠦ࡮ࡢ࡯ࡨࠦᐘ"))
            return
        test_uuid = f.bstack1lll111lll1_opy_(instance, TestFramework.bstack1l1l1ll11ll_opy_)
        if not test_uuid:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢࡰࡰࡢࡥ࡫ࡺࡥࡳࡡࡷࡩࡸࡺ࠺ࠡ࡯࡬ࡷࡸ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡶࡷ࡬ࡨࠧᐙ"))
            return
        if isinstance(self.bstack1l1l11l1111_opy_, bstack1ll11111ll1_opy_):
            framework_name = bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᐚ")
        else:
            framework_name = bstack1ll111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᐛ")
        self.bstack11lll1lll1_opy_(driver, test_name, framework_name, test_uuid)
    def perform_scan(self, driver: object, method: Union[None, str], framework_name: str):
        bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1ll1l11ll1_opy_.value)
        if not self.accessibility:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡣࡸࡩࡡ࡯࠼ࠣࡥ࠶࠷ࡹࠡࡰࡲࡸࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࡿࠣࠦᐜ"))
            return
        bstack1ll1l1l111_opy_ = datetime.now()
        bstack1l1l1ll11l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᐝ"), None)
        if not bstack1l1l1ll11l1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠧࡶࡥࡳࡨࡲࡶࡲࡥࡳࡤࡣࡱ࠾ࠥࡳࡩࡴࡵ࡬ࡲ࡬ࠦࠧࡴࡥࡤࡲࠬࠦࡳࡤࡴ࡬ࡴࡹࠦࡦࡰࡴࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠧᐞ") + str(framework_name) + bstack1ll111_opy_ (u"ࠨࠠࠣᐟ"))
            return
        if self.bstack1l1l1l11111_opy_:
            arg = dict()
            arg[bstack1ll111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᐠ")] = method if method else bstack1ll111_opy_ (u"ࠣࠤᐡ")
            arg[bstack1ll111_opy_ (u"ࠤࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠤᐢ")] = self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠥᐣ")]
            arg[bstack1ll111_opy_ (u"ࠦࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠤᐤ")] = self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶ࡫ࡹࡧࡥࡢࡶ࡫࡯ࡨࡤࡻࡵࡪࡦࠥᐥ")]
            arg[bstack1ll111_opy_ (u"ࠨࡡࡶࡶ࡫ࡌࡪࡧࡤࡦࡴࠥᐦ")] = self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠧᐧ")]
            arg[bstack1ll111_opy_ (u"ࠣࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠧᐨ")] = self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠤࡷ࡬ࡤࡰࡷࡵࡡࡷࡳࡰ࡫࡮ࠣᐩ")]
            arg[bstack1ll111_opy_ (u"ࠥࡷࡨࡧ࡮ࡕ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥᐪ")] = str(int(datetime.now().timestamp() * 1000))
            bstack1l11lll1111_opy_ = self.bstack1l1l11ll1l1_opy_(bstack1ll111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᐫ"), self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᐬ")])
            if bstack1ll111_opy_ (u"ࠨࡣࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠤᐭ") in bstack1l11lll1111_opy_:
                bstack1l11lll1111_opy_ = bstack1l11lll1111_opy_.copy()
                bstack1l11lll1111_opy_[bstack1ll111_opy_ (u"ࠢࡤࡧࡱࡸࡷࡧ࡬ࡂࡷࡷ࡬ࡍ࡫ࡡࡥࡧࡵࠦᐮ")] = bstack1l11lll1111_opy_.pop(bstack1ll111_opy_ (u"ࠣࡥࡨࡲࡹࡸࡡ࡭ࡃࡸࡸ࡭࡚࡯࡬ࡧࡱࠦᐯ"))
            arg = bstack1l1l11111l1_opy_(arg, bstack1l11lll1111_opy_)
            bstack1l1l11lll1l_opy_ = bstack1l1l1ll11l1_opy_ % json.dumps(arg)
            driver.execute_script(bstack1l1l11lll1l_opy_)
            return
        instance = bstack1ll1lllllll_opy_.bstack1ll1l1ll1l1_opy_(driver)
        if instance:
            if not bstack1ll1lllllll_opy_.bstack1lll111lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l11lll1l11_opy_, False):
                bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l11lll1l11_opy_, True)
            else:
                self.logger.info(bstack1ll111_opy_ (u"ࠤࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮࠻ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡳࠦࡰࡳࡱࡪࡶࡪࡹࡳࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁࠥࡳࡥࡵࡪࡲࡨࡂࠨᐰ") + str(method) + bstack1ll111_opy_ (u"ࠥࠦᐱ"))
                return
        self.logger.info(bstack1ll111_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽࠡ࡯ࡨࡸ࡭ࡵࡤ࠾ࠤᐲ") + str(method) + bstack1ll111_opy_ (u"ࠧࠨᐳ"))
        if framework_name == bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᐴ"):
            result = self.bstack1l1l11l1111_opy_.bstack1l11lll1lll_opy_(driver, bstack1l1l1ll11l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1ll11l1_opy_, {bstack1ll111_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᐵ"): method if method else bstack1ll111_opy_ (u"ࠣࠤᐶ")})
        bstack111ll11111_opy_.end(EVENTS.bstack1ll1l11ll1_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᐷ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᐸ"), True, None, command=method)
        if instance:
            bstack1ll1lllllll_opy_.bstack1ll1ll1lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l11lll1l11_opy_, False)
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠦࡦ࠷࠱ࡺ࠼ࡳࡩࡷ࡬࡯ࡳ࡯ࡢࡷࡨࡧ࡮ࠣᐹ"), datetime.now() - bstack1ll1l1l111_opy_)
        return result
        def bstack1l1l1l1llll_opy_(self, driver: object, framework_name, result_type: str):
            self.bstack1l11ll1llll_opy_()
            req = structs.AccessibilityResultRequest()
            req.bin_session_id = self.bin_session_id
            req.bstack1l1l1111l11_opy_ = self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠧࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠧᐺ")]
            req.result_type = result_type
            req.session_id = self.bin_session_id
            req.platform_index = str(os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᐻ"), bstack1ll111_opy_ (u"ࠧ࠱ࠩᐼ")))
            req.client_worker_id = bstack1ll111_opy_ (u"ࠣࡽࢀ࠱ࢀࢃࠢᐽ").format(threading.get_ident(), os.getpid())
            try:
                r = self.bstack1ll1lll11ll_opy_.AccessibilityResult(req)
                if not r.success:
                    self.logger.debug(bstack1ll111_opy_ (u"ࠤࡵࡩࡨ࡫ࡩࡷࡧࡧࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᐾ") + str(r) + bstack1ll111_opy_ (u"ࠥࠦᐿ"))
                else:
                    bstack1l1l111l1l1_opy_ = json.loads(r.bstack1l1l111l11l_opy_.decode(bstack1ll111_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪᑀ")))
                    if result_type == bstack1ll111_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠩᑁ"):
                        return bstack1l1l111l1l1_opy_.get(bstack1ll111_opy_ (u"ࠨࡤࡢࡶࡤࠦᑂ"), [])
                    else:
                        return bstack1l1l111l1l1_opy_.get(bstack1ll111_opy_ (u"ࠢࡥࡣࡷࡥࠧᑃ"), {})
            except grpc.RpcError as e:
                self.logger.error(bstack1ll111_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡴࡵࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡲࡦࡵࡸࡰࡹࠦࡦࡳࡱࡰࠤࡨࡲࡩ࠻ࠢࠥᑄ") + str(e) + bstack1ll111_opy_ (u"ࠤࠥᑅ"))
    @measure(event_name=EVENTS.bstack1ll1l11111_opy_, stage=STAGE.bstack11ll1111_opy_)
    def get_accessibility_results(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll111_opy_ (u"ࠥ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡳࡧࡶࡹࡱࡺࡳ࠻ࠢࡤ࠵࠶ࡿࠠ࡯ࡱࡷࠤࡪࡴࡡࡣ࡮ࡨࡨࠧᑆ"))
            return
        if self.bstack1l1l1l11111_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡥࡵࡶࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᑇ"))
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1l1llll_opy_(driver, framework_name, bstack1ll111_opy_ (u"ࠧ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࠤᑈ"))
        bstack1l1l1ll11l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll111_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥᑉ"), None)
        if not bstack1l1l1ll11l1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᑊ") + str(framework_name) + bstack1ll111_opy_ (u"ࠣࠤᑋ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1l1l111_opy_ = datetime.now()
        if framework_name == bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᑌ"):
            result = self.bstack1l1l11l1111_opy_.bstack1l11lll1lll_opy_(driver, bstack1l1l1ll11l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1ll11l1_opy_)
        instance = bstack1ll1lllllll_opy_.bstack1ll1l1ll1l1_opy_(driver)
        if instance:
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࠨᑍ"), datetime.now() - bstack1ll1l1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1ll1ll11_opy_, stage=STAGE.bstack11ll1111_opy_)
    def get_accessibility_results_summary(self, driver: object, framework_name):
        if not self.accessibility:
            self.logger.debug(bstack1ll111_opy_ (u"ࠦ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡴࡨࡷࡺࡲࡴࡴࡡࡶࡹࡲࡳࡡࡳࡻ࠽ࠤࡦ࠷࠱ࡺࠢࡱࡳࡹࠦࡥ࡯ࡣࡥࡰࡪࡪࠢᑎ"))
            return
        if self.bstack1l1l1l11111_opy_:
            self.perform_scan(driver, method=None, framework_name=framework_name)
            return self.bstack1l1l1l1llll_opy_(driver, framework_name, bstack1ll111_opy_ (u"ࠬ࡭ࡥࡵࡔࡨࡷࡺࡲࡴࡴࡕࡸࡱࡲࡧࡲࡺࠩᑏ"))
        bstack1l1l1ll11l1_opy_ = self.scripts.get(framework_name, {}).get(bstack1ll111_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࡖࡹࡲࡳࡡࡳࡻࠥᑐ"), None)
        if not bstack1l1l1ll11l1_opy_:
            self.logger.debug(bstack1ll111_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࠩࡪࡩࡹࡘࡥࡴࡷ࡯ࡸࡸ࡙ࡵ࡮࡯ࡤࡶࡾ࠭ࠠࡴࡥࡵ࡭ࡵࡺࠠࡧࡱࡵࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࡂࠨᑑ") + str(framework_name) + bstack1ll111_opy_ (u"ࠣࠤᑒ"))
            return
        self.perform_scan(driver, method=None, framework_name=framework_name)
        bstack1ll1l1l111_opy_ = datetime.now()
        if framework_name == bstack1ll111_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ᑓ"):
            result = self.bstack1l1l11l1111_opy_.bstack1l11lll1lll_opy_(driver, bstack1l1l1ll11l1_opy_)
        else:
            result = driver.execute_async_script(bstack1l1l1ll11l1_opy_)
        instance = bstack1ll1lllllll_opy_.bstack1ll1l1ll1l1_opy_(driver)
        if instance:
            instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠥࡥ࠶࠷ࡹ࠻ࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡸࡥࡴࡷ࡯ࡸࡸࡥࡳࡶ࡯ࡰࡥࡷࡿࠢᑔ"), datetime.now() - bstack1ll1l1l111_opy_)
        return result
    @measure(event_name=EVENTS.bstack1l1l11lll11_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack1l1l1l1l1ll_opy_(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        hub_url: str,
    ):
        self.bstack1l11ll1llll_opy_()
        req = structs.AccessibilityConfigRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.framework_name = framework_name
        req.framework_version = framework_version
        req.hub_url = hub_url
        req.client_worker_id = bstack1ll111_opy_ (u"ࠦࢀࢃ࠭ࡼࡿࠥᑕ").format(threading.get_ident(), os.getpid())
        try:
            r = self.bstack1ll1lll11ll_opy_.AccessibilityConfig(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠧࡸࡥࡤࡧ࡬ࡺࡪࡪࠠࡧࡴࡲࡱࠥࡹࡥࡳࡸࡨࡶ࠿ࠦࠢᑖ") + str(r) + bstack1ll111_opy_ (u"ࠨࠢᑗ"))
            else:
                self.bstack1l1l1l11l1l_opy_(framework_name, r)
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠢࡳࡲࡦ࠱ࡪࡸࡲࡰࡴ࠽ࠤࠧᑘ") + str(e) + bstack1ll111_opy_ (u"ࠣࠤᑙ"))
            traceback.print_exc()
            raise e
    def bstack1l1l1l11l1l_opy_(self, framework_name: str, result: structs.AccessibilityConfigResponse) -> bool:
        if not result.success or not result.accessibility.success:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤ࡯ࡳࡦࡪ࡟ࡤࡱࡱࡪ࡮࡭࠺ࠡࡣ࠴࠵ࡾࠦ࡮ࡰࡶࠣࡪࡴࡻ࡮ࡥࠤᑚ"))
            return False
        if result.accessibility.is_app_accessibility:
            self.bstack1l1l1l11111_opy_ = result.accessibility.is_app_accessibility
        if result.testhub.build_hashed_id:
            self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠥࡸࡪࡹࡴࡩࡷࡥࡣࡧࡻࡩ࡭ࡦࡢࡹࡺ࡯ࡤࠣᑛ")] = result.testhub.build_hashed_id
        if result.testhub.jwt:
            self.bstack1l1l11l1l1l_opy_[bstack1ll111_opy_ (u"ࠦࡹ࡮࡟࡫ࡹࡷࡣࡹࡵ࡫ࡦࡰࠥᑜ")] = result.testhub.jwt
        if result.accessibility.options:
            options = result.accessibility.options
            if options.capabilities:
                for caps in options.capabilities:
                    self.bstack1l1l11l1l1l_opy_[caps.name] = caps.value
            if options.scripts:
                self.scripts[framework_name] = {row.name: row.command for row in options.scripts}
            if options.commands_to_wrap and options.commands_to_wrap.commands:
                scripts_to_run = [s for s in options.commands_to_wrap.scripts_to_run]
                if not scripts_to_run:
                    return False
                bstack1l1l1ll111l_opy_ = dict()
                for command in options.commands_to_wrap.commands:
                    if command.library == self.bstack1l1l11lllll_opy_ and command.module == self.bstack1l1l11l111l_opy_:
                        if command.method and not command.method in bstack1l1l1ll111l_opy_:
                            bstack1l1l1ll111l_opy_[command.method] = dict()
                        if command.name and not command.name in bstack1l1l1ll111l_opy_[command.method]:
                            bstack1l1l1ll111l_opy_[command.method][command.name] = list()
                        bstack1l1l1ll111l_opy_[command.method][command.name].extend(scripts_to_run)
                self.commands[framework_name] = bstack1l1l1ll111l_opy_
        return bool(self.commands.get(framework_name, None))
    def bstack1l11llll111_opy_(
        self,
        f: bstack1ll11lll111_opy_,
        exec: Tuple[bstack1ll1l1l111l_opy_, str],
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if isinstance(self.bstack1l1l11l1111_opy_, bstack1ll11111ll1_opy_) and method_name != bstack1ll111_opy_ (u"ࠬࡩ࡯࡯ࡰࡨࡧࡹ࠭ᑝ"):
            return
        if bstack1ll1lllllll_opy_.bstack1ll1l1lllll_opy_(instance, bstack1ll11l11lll_opy_.bstack1l1l1111l1l_opy_):
            return
        if f.bstack1l1l11l1ll1_opy_(method_name, *args):
            bstack1l1l11ll111_opy_ = False
            desired_capabilities = f.bstack1l11lllll1l_opy_(instance)
            if isinstance(desired_capabilities, dict):
                hub_url = f.bstack1l1l111ll1l_opy_(instance)
                platform_index = f.bstack1lll111lll1_opy_(instance, bstack1ll11lll111_opy_.bstack1l1l1l1ll11_opy_, 0)
                bstack1l1l111llll_opy_ = datetime.now()
                r = self.bstack1l1l1l1l1ll_opy_(platform_index, f.framework_name, f.framework_version, hub_url)
                instance.bstack11l11l1ll1_opy_(bstack1ll111_opy_ (u"ࠨࡧࡳࡲࡦ࠾ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡨࡵ࡮ࡧ࡫ࡪࠦᑞ"), datetime.now() - bstack1l1l111llll_opy_)
                bstack1l1l11ll111_opy_ = r.success
            else:
                self.logger.error(bstack1ll111_opy_ (u"ࠢ࡮࡫ࡶࡷ࡮ࡴࡧࠡࡦࡨࡷ࡮ࡸࡥࡥࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠾ࠤᑟ") + str(desired_capabilities) + bstack1ll111_opy_ (u"ࠣࠤᑠ"))
            f.bstack1ll1ll1lll1_opy_(instance, bstack1ll11l11lll_opy_.bstack1l1l1111l1l_opy_, bstack1l1l11ll111_opy_)
    def bstack11l1llll11_opy_(self, test_tags):
        bstack1l1l1l1l1ll_opy_ = self.config.get(bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᑡ"))
        if not bstack1l1l1l1l1ll_opy_:
            return True
        try:
            include_tags = bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᑢ")] if bstack1ll111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᑣ") in bstack1l1l1l1l1ll_opy_ and isinstance(bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᑤ")], list) else []
            exclude_tags = bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᑥ")] if bstack1ll111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᑦ") in bstack1l1l1l1l1ll_opy_ and isinstance(bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᑧ")], list) else []
            excluded = any(tag in exclude_tags for tag in test_tags)
            included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
            return not excluded and included
        except Exception as error:
            self.logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᑨ") + str(error))
        return False
    def bstack1l1l1l1l1l_opy_(self, caps):
        try:
            if self.bstack1l1l1l11111_opy_:
                bstack1l1l1l11ll1_opy_ = caps.get(bstack1ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᑩ"))
                if bstack1l1l1l11ll1_opy_ is not None and str(bstack1l1l1l11ll1_opy_).lower() == bstack1ll111_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᑪ"):
                    bstack1l1l1111lll_opy_ = caps.get(bstack1ll111_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᑫ")) or caps.get(bstack1ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᑬ"))
                    if bstack1l1l1111lll_opy_ is not None and int(bstack1l1l1111lll_opy_) < 11:
                        self.logger.warning(bstack1ll111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡂࡰࡧࡶࡴ࡯ࡤࠡ࠳࠴ࠤࡦࡴࡤࠡࡣࡥࡳࡻ࡫࠮ࠡࡅࡸࡶࡷ࡫࡮ࡵࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡃࠢᑭ") + str(bstack1l1l1111lll_opy_) + bstack1ll111_opy_ (u"ࠣࠤᑮ"))
                        return False
                return True
            bstack1l11llll1ll_opy_ = caps.get(bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᑯ"), {}).get(bstack1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᑰ"), caps.get(bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᑱ"), bstack1ll111_opy_ (u"ࠬ࠭ᑲ")))
            if bstack1l11llll1ll_opy_:
                self.logger.warning(bstack1ll111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᑳ"))
                return False
            browser = caps.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᑴ"), bstack1ll111_opy_ (u"ࠨࠩᑵ")).lower()
            if browser != bstack1ll111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᑶ"):
                self.logger.warning(bstack1ll111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᑷ"))
                return False
            bstack1l1l1l1l111_opy_ = bstack1l1l1l1l1l1_opy_
            if not self.config.get(bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᑸ")) or self.config.get(bstack1ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩᑹ")):
                bstack1l1l1l1l111_opy_ = bstack1l1l1111ll1_opy_
            browser_version = caps.get(bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᑺ"))
            if not browser_version:
                browser_version = caps.get(bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑻ"), {}).get(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᑼ"), bstack1ll111_opy_ (u"ࠩࠪᑽ"))
            bstack1l1l111ll11_opy_ = str(browser_version).lower() if browser_version is not None else bstack1ll111_opy_ (u"ࠪࠫᑾ")
            if bstack1l1l111ll11_opy_:
                if bstack1l1l111ll11_opy_.startswith(bstack1ll111_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᑿ")):
                    if bstack1l1l111ll11_opy_.startswith(bstack1ll111_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸ࠲࠭ᒀ")):
                        bstack1l11llll11l_opy_ = bstack1l1l111ll11_opy_[len(bstack1ll111_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠳ࠧᒁ")):]
                        if bstack1l11llll11l_opy_ and not bstack1l11llll11l_opy_.isdigit():
                            self.logger.warning(bstack1ll111_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣࡪࡴࡸ࡭ࡢࡶࠣࠫࠧᒂ") + str(browser_version) + bstack1ll111_opy_ (u"ࠣࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦࠧ࡭ࡣࡷࡩࡸࡺࠧࠡࡱࡵࠤࠬࡲࡡࡵࡧࡶࡸ࠲ࡂ࡮ࡶ࡯ࡥࡩࡷࡄࠧ࠯ࠤᒃ"))
                            return False
                else:
                    try:
                        if int(bstack1l1l111ll11_opy_.split(bstack1ll111_opy_ (u"ࠩ࠱ࠫᒄ"))[0]) <= bstack1l1l1l1l111_opy_:
                            self.logger.warning(bstack1ll111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࠧᒅ") + str(bstack1l1l1l1l111_opy_) + bstack1ll111_opy_ (u"ࠦ࠳ࠨᒆ"))
                            return False
                    except (ValueError, IndexError) as e:
                        self.logger.debug(bstack1ll111_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࠪࡿࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࢃࠧ࠻ࠢࠥᒇ") + str(e) + bstack1ll111_opy_ (u"ࠨࠢᒈ"))
            bstack1l1l1l1lll1_opy_ = caps.get(bstack1ll111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᒉ"), {}).get(bstack1ll111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᒊ"))
            if not bstack1l1l1l1lll1_opy_:
                bstack1l1l1l1lll1_opy_ = caps.get(bstack1ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᒋ"), {})
            if bstack1l1l1l1lll1_opy_ and bstack1ll111_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᒌ") in bstack1l1l1l1lll1_opy_.get(bstack1ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩᒍ"), []):
                self.logger.warning(bstack1ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᒎ"))
                return False
            return True
        except Exception as error:
            self.logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᒏ") + str(error))
            return False
    def bstack1l1l111lll1_opy_(self, test_uuid: str, result: structs.FetchDriverExecuteParamsEventResponse):
        bstack1l1l1l111ll_opy_ = {
            bstack1ll111_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᒐ"): test_uuid,
        }
        bstack1l11lll1ll1_opy_ = {}
        if result.success:
            bstack1l11lll1ll1_opy_ = json.loads(result.accessibility_execute_params)
        return bstack1l1l11111l1_opy_(bstack1l1l1l111ll_opy_, bstack1l11lll1ll1_opy_)
    def bstack1l1l11ll1l1_opy_(self, script_name: str, test_uuid: str) -> dict:
        bstack1ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࠠࠡࠢࠣࠤࠥࡌࡥࡵࡥ࡫ࠤࡨ࡫࡮ࡵࡴࡤࡰࠥࡧࡵࡵࡪࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡪࡴࡸࠠࡵࡪࡨࠤ࡬࡯ࡶࡦࡰࠣࡷࡨࡸࡩࡱࡶࠣࡲࡦࡳࡥ࠯ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡨࡧࡣࡩࡧࡧࠤࡨࡵ࡮ࡧ࡫ࡪࠤ࡮࡬ࠠࡢ࡮ࡵࡩࡦࡪࡹࠡࡨࡨࡸࡨ࡮ࡥࡥ࠮ࠣࡳࡹ࡮ࡥࡳࡹ࡬ࡷࡪࠦ࡬ࡰࡣࡧࡷࠥࡧ࡮ࡥࠢࡦࡥࡨ࡮ࡥࡴࠢ࡬ࡸ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡂࡴࡪࡷ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸࡩࡲࡪࡲࡷࡣࡳࡧ࡭ࡦ࠼ࠣࡒࡦࡳࡥࠡࡱࡩࠤࡹ࡮ࡥࠡࡵࡦࡶ࡮ࡶࡴࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡧࡴࡴࡦࡪࡩࠣࡪࡴࡸࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡺࡥࡴࡶࡢࡹࡺ࡯ࡤ࠻ࠢࡘ࡙ࡎࡊࠠࡰࡨࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡷࡩ࡫ࡦ࡬ࠥࡺ࡯ࠡࡨࡨࡸࡨ࡮ࠠࡤࡱࡱࡪ࡮࡭ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡔࡨࡸࡺࡸ࡮ࡴ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡦ࡬ࡧࡹࡀࠠࡄࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡥ࡫ࡦࡸ࡮ࡵ࡮ࡢࡴࡼ࠰ࠥ࡫࡭ࡱࡶࡼࠤࡩ࡯ࡣࡵࠢ࡬ࡪࠥ࡫ࡲࡳࡱࡵࠤࡴࡩࡣࡶࡴࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠨࠢࠣᒑ")
        try:
            if self.bstack1l1l11ll11l_opy_:
                return self.bstack1l11lll11ll_opy_
            self.bstack1l11ll1llll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll111_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᒒ")
            req.script_name = script_name
            req.platform_index = str(os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᒓ"), bstack1ll111_opy_ (u"ࠫ࠵࠭ᒔ")))
            req.client_worker_id = bstack1ll111_opy_ (u"ࠧࢁࡽ࠮ࡽࢀࠦᒕ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1lll11ll_opy_.FetchDriverExecuteParamsEvent(req)
            if r.success:
                self.bstack1l11lll11ll_opy_ = self.bstack1l1l111lll1_opy_(test_uuid, r)
                self.bstack1l1l11ll11l_opy_ = True
            else:
                self.logger.error(bstack1ll111_opy_ (u"ࠨࡦࡦࡶࡦ࡬ࡈ࡫࡮ࡵࡴࡤࡰࡆࡻࡴࡩࡃ࠴࠵ࡾࡉ࡯࡯ࡨ࡬࡫࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡩࡩࡹࡩࡨࠡࡦࡵ࡭ࡻ࡫ࡲࠡࡧࡻࡩࡨࡻࡴࡦࠢࡳࡥࡷࡧ࡭ࡴࠢࡩࡳࡷࠦࡻࡴࡥࡵ࡭ࡵࡺ࡟࡯ࡣࡰࡩࢂࡀࠠࠣᒖ") + str(r.error) + bstack1ll111_opy_ (u"ࠢࠣᒗ"))
                self.bstack1l11lll11ll_opy_ = dict()
            return self.bstack1l11lll11ll_opy_
        except Exception as e:
            self.logger.error(bstack1ll111_opy_ (u"ࠣࡨࡨࡸࡨ࡮ࡃࡦࡰࡷࡶࡦࡲࡁࡶࡶ࡫ࡅ࠶࠷ࡹࡄࡱࡱࡪ࡮࡭࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤ࡫࡫ࡴࡤࡪࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡵࡲࠡࡽࡶࡧࡷ࡯ࡰࡵࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᒘ") + str(traceback.format_exc()) + bstack1ll111_opy_ (u"ࠤࠥᒙ"))
            return dict()
    def bstack11lll1lll1_opy_(self, driver: object, name: str, framework_name: str, test_uuid: str):
        bstack1l1l1l111_opy_ = None
        try:
            self.bstack1l11ll1llll_opy_()
            req = structs.FetchDriverExecuteParamsEventRequest()
            req.bin_session_id = self.bin_session_id
            req.product = bstack1ll111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥᒚ")
            req.script_name = bstack1ll111_opy_ (u"ࠦࡸࡧࡶࡦࡔࡨࡷࡺࡲࡴࡴࠤᒛ")
            req.platform_index = str(os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬᒜ"), bstack1ll111_opy_ (u"࠭࠰ࠨᒝ")))
            req.client_worker_id = bstack1ll111_opy_ (u"ࠢࡼࡿ࠰ࡿࢂࠨᒞ").format(threading.get_ident(), os.getpid())
            r = self.bstack1ll1lll11ll_opy_.FetchDriverExecuteParamsEvent(req)
            if not r.success:
                self.logger.debug(bstack1ll111_opy_ (u"ࠣࡴࡨࡧࡪ࡯ࡶࡦࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡩࡽ࡫ࡣࡶࡶࡨࠤࡵࡧࡲࡢ࡯ࡶࠤ࡫ࡸ࡯࡮ࠢࡶࡩࡷࡼࡥࡳ࠼ࠣࠦᒟ") + str(r.error) + bstack1ll111_opy_ (u"ࠤࠥᒠ"))
            else:
                bstack1l1l1l111ll_opy_ = self.bstack1l1l111lll1_opy_(test_uuid, r)
                bstack1l1l1ll11l1_opy_ = r.script
            self.logger.debug(bstack1ll111_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᒡ") + str(bstack1l1l1l111ll_opy_))
            self.perform_scan(driver, name, framework_name=framework_name)
            if not bstack1l1l1ll11l1_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡤࡹࡣࡢࡰ࠽ࠤࡲ࡯ࡳࡴ࡫ࡱ࡫ࠥ࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫࠥࡹࡣࡳ࡫ࡳࡸࠥ࡬࡯ࡳࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࡀࠦᒢ") + str(framework_name) + bstack1ll111_opy_ (u"ࠧࠦࠢᒣ"))
                return
            bstack1l1l1l111_opy_ = bstack111ll11111_opy_.bstack111l11l11_opy_(EVENTS.bstack1l1l11l1lll_opy_.value)
            self.bstack1l11llll1l1_opy_(driver, bstack1l1l1ll11l1_opy_, bstack1l1l1l111ll_opy_, framework_name)
            try:
                bstack1l1l1l11l11_opy_ = {
                    bstack1ll111_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢᒤ"): {
                        bstack1ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᒥ"): bstack1ll111_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᒦ"),
                    },
                    bstack1ll111_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᒧ"): {
                        bstack1ll111_opy_ (u"ࠥࡦࡴࡪࡹࠣᒨ"): {
                            bstack1ll111_opy_ (u"ࠦࡲࡹࡧࠣᒩ"): bstack1ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᒪ"),
                            bstack1ll111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᒫ"): True
                        }
                    }
                }
                self.bstack1l11llll_opy_.info(json.dumps(bstack1l1l1l11l11_opy_, separators=(bstack1ll111_opy_ (u"ࠧ࠭ࠩᒬ"), bstack1ll111_opy_ (u"ࠨ࠼ࠪᒭ"))))
            except Exception as bstack111ll1ll1l_opy_:
                self.logger.debug(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣᒮ") + str(bstack111ll1ll1l_opy_) + bstack1ll111_opy_ (u"ࠥࠦᒯ"))
            self.logger.info(bstack1ll111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᒰ"))
            bstack111ll11111_opy_.end(EVENTS.bstack1l1l11l1lll_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᒱ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᒲ"), True, None, command=bstack1ll111_opy_ (u"ࠧࡴࡣࡹࡩࡗ࡫ࡳࡶ࡮ࡷࡷࠬᒳ"),test_name=name)
        except Exception as bstack1l1l11111ll_opy_:
            self.logger.error(bstack1ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᒴ") + bstack1ll111_opy_ (u"ࠤࡶࡸࡷ࠮ࡰࡢࡶ࡫࠭ࠧᒵ") + bstack1ll111_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᒶ") + str(bstack1l1l11111ll_opy_))
            bstack111ll11111_opy_.end(EVENTS.bstack1l1l11l1lll_opy_.value, bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᒷ"), bstack1l1l1l111_opy_+bstack1ll111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᒸ"), False, bstack1l1l11111ll_opy_, command=bstack1ll111_opy_ (u"࠭ࡳࡢࡸࡨࡖࡪࡹࡵ࡭ࡶࡶࠫᒹ"),test_name=name)
    def bstack1l11llll1l1_opy_(self, driver, bstack1l1l1ll11l1_opy_, bstack1l1l1l111ll_opy_, framework_name):
        if framework_name == bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠫᒺ"):
            self.bstack1l1l11l1111_opy_.bstack1l11lll1lll_opy_(driver, bstack1l1l1ll11l1_opy_, bstack1l1l1l111ll_opy_)
        else:
            self.logger.debug(driver.execute_async_script(bstack1l1l1ll11l1_opy_, bstack1l1l1l111ll_opy_))
    def _1l1l1l11lll_opy_(self, instance: bstack1ll11l1ll1l_opy_, args: Tuple) -> list:
        bstack1ll111_opy_ (u"ࠣࠤࠥࡉࡽࡺࡲࡢࡥࡷࠤࡹࡧࡧࡴࠢࡥࡥࡸ࡫ࡤࠡࡱࡱࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࠥࠦࠧᒻ")
        if bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᒼ") in instance.bstack1l11lll1l1l_opy_:
            return args[2].tags if hasattr(args[2], bstack1ll111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᒽ")) else []
        if hasattr(args[0], bstack1ll111_opy_ (u"ࠫࡴࡽ࡮ࡠ࡯ࡤࡶࡰ࡫ࡲࡴࠩᒾ")):
            return [marker.name for marker in args[0].own_markers]
        return []
    def bstack1l11lll11l1_opy_(self, tags, capabilities):
        return self.bstack11l1llll11_opy_(tags) and self.bstack1l1l1l1l1l_opy_(capabilities)