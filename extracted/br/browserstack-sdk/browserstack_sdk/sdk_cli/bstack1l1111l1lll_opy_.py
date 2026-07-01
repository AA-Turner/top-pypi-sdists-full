# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import json
import os
import grpc
import copy
import asyncio
import threading
from browserstack_sdk import sdk_pb2 as structs
from packaging import version
import traceback
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    AutomationFrameworkBrowser,
)
from bstack_utils.constants import *
from typing import Any, List, Union, Dict
from pathlib import Path
from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
from datetime import datetime
from typing import Tuple, Any
from bstack_utils.messages import bstack1llll1llll1_opy_
from bstack_utils.helper import is_bstack_automation
import threading
import os
import urllib.parse
class bstack1l11l11l111_opy_(BaseModule):
    @staticmethod
    def bstack11l11ll1ll1_opy_(bstack11l1ll11_opy_: dict) -> bool:
        browser_name = (
            bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᧇ"))
            or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᧈ"))
            or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡥࡧࡩࡥࡺࡲࡴࡃࡴࡲࡻࡸ࡫ࡲࡕࡻࡳࡩࠬᧉ"))
            or bstack1l1llll_opy_ (u"ࠨࠩ᧊")
        ).lower()
        return browser_name in bstack1llll1lll11_opy_
    def __init__(self, module_automation_framework_test):
        super().__init__()
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.CREATE, HookState.PRE), self.bstack11l1l111111_opy_)
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.CREATE, HookState.PRE), self.bstack11l11ll1l11_opy_)
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.bstack1l11llll1l1_opy_, HookState.PRE), self.bstack11l1l11lll1_opy_)
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.EXECUTE, HookState.PRE), self.bstack11l1l11l111_opy_)
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.CREATE, HookState.PRE), self.bstack11l11lllll1_opy_)
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.QUIT, HookState.PRE), self.on_close)
        self.module_automation_framework_test = module_automation_framework_test
    def is_enabled(self) -> bool:
        return True
    def bstack11l1l111111_opy_(
        self,
        f: bstack111ll111_opy_,
        bstack11l11l1lll1_opy_: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤ᧋"):
            return
        if not is_bstack_automation():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡖࡪࡺࡵࡳࡰ࡬ࡲ࡬ࠦࡩ࡯ࠢ࡯ࡥࡺࡴࡣࡩࠢࡰࡩࡹ࡮࡯ࡥ࠮ࠣࡲࡴࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࠦࡳࡦࡵࡶ࡭ࡴࡴࠢ᧌"))
            return
        def wrapped(bstack11l11l1lll1_opy_, launch, *args, **kwargs):
            _11l11ll111l_opy_ = int(threading.current_thread().name) if threading.current_thread().name.isdigit() else f.platform_index
            _1lll1ll1ll_opy_ = (
                os.environ.get(bstack1lll1l11111_opy_, bstack1l1llll_opy_ (u"ࠫࠬ᧍")).lower() == bstack1l1llll_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ᧎")
                and bool(os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡋࡓࡔࡑࡓࠨ᧏")))
            )
            if _1lll1ll1ll_opy_:
                bstack1l1llll1_opy_ = str(os.getpid()) + str(threading.get_ident())
                bstack11l11lll1l1_opy_ = str(hash(bstack1l1llll1_opy_))
            else:
                bstack11l11lll1l1_opy_ = instance.ref()
            response = self.bstack11l11llllll_opy_(_11l11ll111l_opy_, bstack11l11lll1l1_opy_, json.dumps({bstack1l1llll_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭᧐"): True}).encode(bstack1l1llll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢ᧑")))
            if response is not None and response.capabilities:
                if not is_bstack_automation():
                    browser = launch(bstack11l11l1lll1_opy_)
                    return browser
                bstack11l1ll11_opy_ = json.loads(response.capabilities.decode(bstack1l1llll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣ᧒")))
                if not bstack11l1ll11_opy_: # empty caps bstack11l11lll11l_opy_ bstack11l1l11l1l1_opy_ bstack11l1l1l11l1_opy_ bstack11l11ll1111_opy_ or error in processing
                    return
                bstack1l1l111lll_opy_ = bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᧓"), {})
                bstack11l1l1111l1_opy_ = bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᧔"), False) or bstack1l1l111lll_opy_.get(bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᧕"), False)
                bstack11l1l11l11l_opy_ = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡡ࠲࠳ࡼࡉࡳࡧࡢ࡭ࡧࡧࠫ᧖"), True)
                if bstack11l1l1111l1_opy_ and not bstack11l1l11l11l_opy_:
                    self.logger.info(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡣࡱࡧࡵ࡯ࡥ࡫࠾ࠥࡺࡡࡨࠢࡩ࡭ࡱࡺࡥࡳࠢࡨࡼࡨࡲࡵࡥࡧࡧࠤࡆ࠷࠱ࡺࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠦ⠔ࠡࡵࡷࡶ࡮ࡶࡰࡪࡰࡪࠤࡆ࠷࠱ࡺࠢࡦࡥࡵࡹࠢ᧗"))
                    bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᧘")] = False
                    bstack11l1l11ll11_opy_ = [bstack11l1l1111ll_opy_ for bstack11l1l1111ll_opy_ in bstack11l1ll11_opy_ if bstack11l1l1111ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᧙"))]
                    for bstack11l1l1111ll_opy_ in bstack11l1l11ll11_opy_:
                        del bstack11l1ll11_opy_[bstack11l1l1111ll_opy_]
                    bstack11l1l1111l1_opy_ = False
                if bstack11l1l1111l1_opy_:
                    bstack11ll1ll11l1_opy_ = (bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᧚"))
                                     or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᧛"))
                                     or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᧜"), {}).get(bstack1l1llll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᧝"), {}))
                    bstack1l1ll1lll_opy_ = bstack11ll1ll11l1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ᧞"), []) if isinstance(bstack11ll1ll11l1_opy_, dict) else []
                    if isinstance(bstack1l1ll1lll_opy_, list) and any(
                        isinstance(arg, str) and (arg == bstack1l1llll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬ᧟") or arg == bstack1l1llll_opy_ (u"ࠩ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫ᧠")
                                                  or (arg.startswith(bstack1l1llll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽ࠨ᧡")) and arg != bstack1l1llll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࡰࡨࡻࠬ᧢")))
                        for arg in bstack1l1ll1lll_opy_
                    ):
                        self.logger.warning(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡡ࡯ࡥࡺࡴࡣࡩ࠼ࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡪࡥࡵࡧࡦࡸࡪࡪࠠ⠕ࠢࡄ࠵࠶ࡿࠠࡦࡺࡷࡩࡳࡹࡩࡰࡰࠣࡧࡦࡴ࡮ࡰࡶࠣࡰࡴࡧࡤ࠼ࠢࡶࡸࡷ࡯ࡰࡱ࡫ࡱ࡫ࠥࡇ࠱࠲ࡻࠣࡧࡦࡶࡳࠡࡶࡲࠤࡷࡻ࡮ࠡࡣࡶࠤࡵࡲࡡࡪࡰࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࠨ᧣"))
                        bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᧤")] = False
                        bstack11l1l11ll11_opy_ = [bstack11l1l1111ll_opy_ for bstack11l1l1111ll_opy_ in bstack11l1ll11_opy_ if bstack11l1l1111ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᧥"))]
                        for bstack11l1l1111ll_opy_ in bstack11l1l11ll11_opy_:
                            del bstack11l1ll11_opy_[bstack11l1l1111ll_opy_]
                        bstack11l1l1111l1_opy_ = False
                        threading.current_thread().a11yEnabled = False
                if bstack11l1l1111l1_opy_:
                    browser_version = (bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᧦"))
                                       or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᧧"))
                                       or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᧨"), {}).get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᧩"), bstack1l1llll_opy_ (u"ࠬ࠭᧪")))
                    bstack11ll1lll1ll_opy_ = str(browser_version).lower() if browser_version else bstack1l1llll_opy_ (u"࠭ࠧ᧫")
                    if bstack11ll1lll1ll_opy_ and not bstack11ll1lll1ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ᧬")):
                        try:
                            if int(bstack11ll1lll1ll_opy_.split(bstack1l1llll_opy_ (u"ࠨ࠰ࠪ᧭"))[0]) <= MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION:
                                self.logger.warning(bstack1l1llll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂ࠴ࠢ᧮").format(MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION))
                                bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᧯")] = False
                                bstack11l1l11ll11_opy_ = [bstack11l1l1111ll_opy_ for bstack11l1l1111ll_opy_ in bstack11l1ll11_opy_ if bstack11l1l1111ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᧰"))]
                                for bstack11l1l1111ll_opy_ in bstack11l1l11ll11_opy_:
                                    del bstack11l1ll11_opy_[bstack11l1l1111ll_opy_]
                                bstack11l1l1111l1_opy_ = False
                                threading.current_thread().a11yEnabled = False
                        except (ValueError, IndexError):
                            pass
                if bstack11l1l1111l1_opy_:
                    if self.bstack11l11ll1ll1_opy_(bstack11l1ll11_opy_):
                        bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᧱")] = True
                        threading.current_thread().a11yPlatform = True
                        self.logger.info(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡢࡰࡦࡻ࡮ࡤࡪ࠽ࠤࡆ࠷࠱ࡺࠢࡨࡲࡦࡨ࡬ࡦࡦࠣࡪࡴࡸࠠࡄࡪࡵࡳࡲ࡯ࡵ࡮ࠢࡥࡶࡴࡽࡳࡦࡴ࠽ࠤࢀࢃࠢ᧲").format(
                            bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᧳")) or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᧴"))))
                    else:
                        self.logger.info(bstack1l1llll_opy_ (u"ࠤࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡥ࡬ࡢࡷࡱࡧ࡭ࡀࠠࡓࡧࡰࡳࡻ࡯࡮ࡨࠢࡄ࠵࠶ࡿࠠࡤࡣࡳࡷࠥ࡬࡯ࡳࠢࡱࡳࡳ࠳ࡃࡩࡴࡲࡱ࡮ࡻ࡭ࠡࡤࡵࡳࡼࡹࡥࡳ࠼ࠣࡿࢂࠨ᧵").format(
                            bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᧶")) or bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬ᧷"))))
                        bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᧸")] = False
                        bstack11l1l11ll11_opy_ = [bstack11l1l1111ll_opy_ for bstack11l1l1111ll_opy_ in bstack11l1ll11_opy_ if bstack11l1l1111ll_opy_.startswith(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᧹"))]
                        for bstack11l1l1111ll_opy_ in bstack11l1l11ll11_opy_:
                            del bstack11l1ll11_opy_[bstack11l1l1111ll_opy_]
                bstack11l1l111l1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack11l1ll11_opy_))
                f.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, bstack11l1l111l1l_opy_)
                f.set_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, bstack11l1ll11_opy_)
                f.set_state(instance, bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࡟ࡵࡪࡵࡩࡦࡪ࡟ࡪࡦࠪ᧺"), threading.get_ident())
                threading.current_thread()._bstack_driver_init_done = True
                try:
                    threading.current_thread()._bstack_internal_connect = True
                    browser = bstack11l11l1lll1_opy_.connect(bstack11l1l111l1l_opy_)
                finally:
                    threading.current_thread()._bstack_internal_connect = False
                return browser
        return wrapped
    def bstack11l1l11lll1_opy_(
        self,
        f: bstack111ll111_opy_,
        Connection: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠣࡦ࡬ࡷࡵࡧࡴࡤࡪࠥ᧻"):
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣ᧼"))
            return
        if not is_bstack_automation():
            return
        def wrapped(Connection, dispatch, *args, **kwargs):
            data = args[0]
            try:
                bstack11l1l111l11_opy_ = None
                if args and isinstance(args[0], dict):
                    bstack11l1l111l11_opy_ = args[0].get(bstack1l1llll_opy_ (u"ࠪࡴࡦࡸࡡ࡮ࡵࠪ᧽"), {}).get(bstack1l1llll_opy_ (u"ࠫࡧࡹࡐࡢࡴࡤࡱࡸ࠭᧾"))
                    if not bstack11l1l111l11_opy_:
                        bstack11l1l111l11_opy_ = args[0].get(bstack1l1llll_opy_ (u"ࠬࡨࡓࡵࡣࡦ࡯ࡕࡧࡲࡢ࡯ࡶࠫ᧿"))
                        if bstack11l1l111l11_opy_:
                            data = dict(args[0])
                            data.pop(bstack1l1llll_opy_ (u"࠭ࡢࡔࡶࡤࡧࡰࡖࡡࡳࡣࡰࡷࠬᨀ"), None)
                            args = (data,) + args[1:]
                if bstack11l1l111l11_opy_:
                    session_id = bstack11l1l111l11_opy_.get(bstack1l1llll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡊࡦࠥᨁ"))
                    if session_id:
                        _11l1l11ll1l_opy_ = threading.get_ident()
                        f.set_state(instance, bstack111ll111_opy_.bstack111lllll_opy_, session_id)
                        f.set_state(instance, bstack111ll111_opy_.bstack11l11lll111_opy_, _11l1l11ll1l_opy_)
                        try:
                            for bstack11l1l11111l_opy_ in list(bstack111ll111_opy_.instances.values()):
                                hub_url = bstack111ll111_opy_.get_state(bstack11l1l11111l_opy_, bstack111ll111_opy_.bstack11lll111_opy_, None)
                                if not hub_url:
                                    continue
                                if bstack111ll111_opy_.get_state(bstack11l1l11111l_opy_, bstack111ll111_opy_.bstack111lllll_opy_, None):
                                    continue
                                bstack1l1ll111_opy_ = bstack111ll111_opy_.get_state(bstack11l1l11111l_opy_, bstack111ll111_opy_.bstack11l11lll111_opy_, None)
                                if bstack1l1ll111_opy_ is not None and bstack1l1ll111_opy_ != _11l1l11ll1l_opy_:
                                    continue
                                bstack111ll111_opy_.set_state(bstack11l1l11111l_opy_, bstack111ll111_opy_.bstack111lllll_opy_, session_id)
                                bstack111ll111_opy_.set_state(bstack11l1l11111l_opy_, bstack111ll111_opy_.bstack11l11lll111_opy_, _11l1l11ll1l_opy_)
                        except Exception as _11l1l111ll1_opy_:
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡱࡱࡣࡨࡵ࡮࡯ࡧࡦࡸ࡮ࡵ࡮ࡠࡦ࡬ࡷࡵࡧࡴࡤࡪ࠽ࠤࡨࡸ࡯ࡴࡵ࠰࡭ࡳࡹࡴࡢࡰࡦࡩࠥࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠢࡳࡶࡴࡶࡡࡨࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪ࠺ࠡࡽࢀࠦᨂ").format(_11l1l111ll1_opy_))
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡦ࡬ࡷࡵࡧࡴࡤࡪࠣࡱࡪࡺࡨࡰࡦ࠽ࠤࠧᨃ"), e)
            dispatch(Connection, *args)
        return wrapped
    def bstack11l11lllll1_opy_(
        self,
        f: bstack111ll111_opy_,
        bstack11l11l1lll1_opy_: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᨄ"):
            return
        if not is_bstack_automation():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡗ࡫ࡴࡶࡴࡱ࡭ࡳ࡭ࠠࡪࡰࠣࡧࡴࡴ࡮ࡦࡥࡷࠤࡲ࡫ࡴࡩࡱࡧ࠰ࠥࡴ࡯ࡵࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡵࡨࡷࡸ࡯࡯࡯ࠤᨅ"))
            return
        def wrapped(bstack11l11l1lll1_opy_, connect, *args, **kwargs):
            if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡩ࡯ࡶࡨࡶࡳࡧ࡬ࡠࡥࡲࡲࡳ࡫ࡣࡵࠩᨆ"), False):
                bstack11l1l111l1l_opy_ = args[0] if args else bstack1l1llll_opy_ (u"࠭ࠧᨇ")
                try:
                    encoded = bstack11l1l111l1l_opy_.replace(PLAYWRIGHT_HUB_URL, bstack1l1llll_opy_ (u"ࠧࠨᨈ"), 1)
                    bstack11l1ll11_opy_ = json.loads(urllib.parse.unquote(encoded))
                except Exception:
                    bstack11l1ll11_opy_ = {}
                f.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, bstack11l1l111l1l_opy_)
                f.set_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, bstack11l1ll11_opy_)
                if bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨉ"), False):
                    threading.current_thread().a11yPlatform = True
                    browser = bstack11l11l1lll1_opy_.connect_over_cdp(bstack11l1l111l1l_opy_)
                    self._11l11llll11_opy_()
                    return browser
                return connect(bstack11l11l1lll1_opy_, *args, **kwargs)
            _11l11ll111l_opy_ = int(threading.current_thread().name) if threading.current_thread().name.isdigit() else f.platform_index
            _1lll1ll1ll_opy_ = (
                os.environ.get(bstack1lll1l11111_opy_, bstack1l1llll_opy_ (u"ࠩࠪᨊ")).lower() == bstack1l1llll_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪᨋ")
                and bool(os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ᨌ")))
            )
            if _1lll1ll1ll_opy_:
                bstack1l1llll1_opy_ = str(os.getpid()) + str(threading.get_ident())
                bstack11l11lll1l1_opy_ = str(hash(bstack1l1llll1_opy_))
            else:
                bstack11l11lll1l1_opy_ = instance.ref()
            _11l11llll1l_opy_ = type(bstack11l11l1lll1_opy_).__name__ == bstack1l1llll_opy_ (u"ࠬࡇ࡮ࡥࡴࡲ࡭ࡩ࠭ᨍ")
            bstack11l11lll1ll_opy_ = {bstack1l1llll_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᨎ"): True}
            if _11l11llll1l_opy_:
                bstack11l11lll1ll_opy_[bstack1l1llll_opy_ (u"ࠧࡪࡵࡄࡲࡩࡸ࡯ࡪࡦࠪᨏ")] = True
            response = self.bstack11l11llllll_opy_(_11l11ll111l_opy_, bstack11l11lll1l1_opy_, json.dumps(bstack11l11lll1ll_opy_).encode(bstack1l1llll_opy_ (u"ࠣࡷࡷࡪ࠲࠾ࠢᨐ")))
            if response is not None and response.capabilities:
                bstack11l1ll11_opy_ = json.loads(response.capabilities.decode(bstack1l1llll_opy_ (u"ࠤࡸࡸ࡫࠳࠸ࠣᨑ")))
                if not bstack11l1ll11_opy_:
                    return
                if _1lll1ll1ll_opy_:
                    bstack11l1ll11_opy_[bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᨒ")] = False
                    bstack11l1l11ll11_opy_ = [bstack11l1l1111ll_opy_ for bstack11l1l1111ll_opy_ in bstack11l1ll11_opy_ if bstack11l1l1111ll_opy_.startswith(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᨓ"))]
                    for bstack11l1l1111ll_opy_ in bstack11l1l11ll11_opy_:
                        del bstack11l1ll11_opy_[bstack11l1l1111ll_opy_]
                    threading.current_thread().a11yEnabled = False
                bstack11l1l111l1l_opy_ = PLAYWRIGHT_HUB_URL + urllib.parse.quote(json.dumps(bstack11l1ll11_opy_))
                f.set_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, bstack11l1l111l1l_opy_)
                f.set_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, bstack11l1ll11_opy_)
                f.set_state(instance, bstack1l1llll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡺࡨࡳࡧࡤࡨࡤ࡯ࡤࠨᨔ"), threading.get_ident())
                if not _1lll1ll1ll_opy_ and bstack11l1ll11_opy_.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨕ"), False) \
                        and bstack1l11l11l111_opy_.bstack11l11ll1ll1_opy_(bstack11l1ll11_opy_):
                    threading.current_thread().a11yPlatform = True
                    browser = bstack11l11l1lll1_opy_.connect_over_cdp(bstack11l1l111l1l_opy_)
                    self._11l11llll11_opy_()
                    return browser
                args = list(args)
                kwargs.pop(bstack1l1llll_opy_ (u"ࠧࡸࡵࡢࡩࡳࡪࡰࡰ࡫ࡱࡸࠬᨖ"), None)
                if not args:
                    args.append(bstack11l1l111l1l_opy_)
                else:
                    args[0] = bstack11l1l111l1l_opy_
                return connect(bstack11l11l1lll1_opy_, *args, **kwargs)
        return wrapped
    def bstack11l11ll1l11_opy_(
        self,
        f: bstack111ll111_opy_,
        bstack11l1ll1ll11_opy_: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᨗ"):
            return
        if not is_bstack_automation():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡕࡩࡹࡻࡲ࡯࡫ࡱ࡫ࠥ࡯࡮ࠡࡰࡨࡻࡤࡶࡡࡨࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ᨘࠣ"))
            return
        def wrapped(bstack11l1ll1ll11_opy_, bstack11l1l11l1ll_opy_, *args, **kwargs):
            a11y = getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᨙ"), False)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟࡯ࡧࡺࡣࡵࡧࡧࡦ࠰ࡺࡶࡦࡶࡰࡦࡦ࠽ࠤࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࡀࡿࢂࠦࡴࡩࡴࡨࡥࡩࡃࡻࡾࠤᨚ").format(a11y, threading.current_thread().name))
            if not a11y:
                return bstack11l1l11l1ll_opy_(bstack11l1ll1ll11_opy_, *args, **kwargs)
            try:
                browser = bstack11l1ll1ll11_opy_.browser
                if browser is None:
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡰࡨࡻࡤࡶࡡࡨࡧ࠽ࠤࡧࡸ࡯ࡸࡵࡨࡶࠥ࡯ࡳࠡࡐࡲࡲࡪ࠲ࠠࡧࡣ࡯ࡰ࡮ࡴࡧࠡࡤࡤࡧࡰࠨᨛ"))
                    return bstack11l1l11l1ll_opy_(bstack11l1ll1ll11_opy_, *args, **kwargs)
                contexts = browser.contexts
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨ࡯࡯ࡡࡱࡩࡼࡥࡰࡢࡩࡨ࠾ࠥࡩ࡯࡯ࡶࡨࡼࡹࡹࠠࡤࡱࡸࡲࡹࡃࡻࡾࠤ᨜").format(len(contexts) if contexts else 0))
                if contexts:
                    bstack11l1l1l111l_opy_ = contexts[0]
                    pages = bstack11l1l1l111l_opy_.pages
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡰࡰࡢࡲࡪࡽ࡟ࡱࡣࡪࡩ࠿ࠦࡰࡢࡩࡨࡷࠥ࡯࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࡵ࡞࠴ࡢࡃࡻࡾࠤ᨝").format([p.url for p in pages]))
                    for p in pages:
                        if bstack1l1llll_opy_ (u"ࠨࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰ࠭᨞") in p.url or p.url == bstack1l1llll_opy_ (u"ࠩࠪ᨟"):
                            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡳࡳࡥ࡮ࡦࡹࡢࡴࡦ࡭ࡥ࠻ࠢࡵࡩࡺࡹࡩ࡯ࡩࠣࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠡࡲࡤ࡫ࡪࠦࡦࡰࡴࠣࡅ࠶࠷ࡹࠡࠪࡶ࡭ࡳ࡭࡬ࡦࠢࡺ࡭ࡳࡪ࡯ࡸࠫࠥᨠ"))
                            bstack1l11l11l111_opy_._11l11ll11l1_opy_(p, self.logger)
                            return p
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟࡯ࡧࡺࡣࡵࡧࡧࡦ࠼ࠣࡲࡴࠦࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠤ࡫ࡵࡵ࡯ࡦ࠯ࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦ࡮ࡦࡹࠣࡴࡦ࡭ࡥࠡ࡫ࡱࠤࡈࡊࡐࠡࡥࡲࡲࡹ࡫ࡸࡵࠤᨡ"))
                    bstack11l1l1l1111_opy_ = bstack11l1l11l1ll_opy_(bstack11l1l1l111l_opy_, *args, **kwargs)
                    bstack1l11l11l111_opy_._11l11ll11l1_opy_(bstack11l1l1l1111_opy_, self.logger)
                    return bstack11l1l1l1111_opy_
            except Exception as e:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡵ࡮ࡠࡰࡨࡻࡤࡶࡡࡨࡧ࠽ࠤࡪࡸࡲࡰࡴ࠯ࠤ࡫ࡧ࡬࡭࡫ࡱ࡫ࠥࡨࡡࡤ࡭࠽ࠤࢀࢃࠢᨢ").format(e))
            return bstack11l1l11l1ll_opy_(bstack11l1ll1ll11_opy_, *args, **kwargs)
        return wrapped
    @staticmethod
    def _11l11ll11l1_opy_(page, logger):
        bstack1l1llll_opy_ (u"ࠨࠢࠣࡄ࡬ࡲࡦࡸࡹࠡࡈ࡯ࡳࡼࠦࡁ࠲࠳ࡼࠤࡵࡧࡧࡦࠢࡺࡶࡦࡶࡰࡪࡰࡪ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡗࡳࡣࡳࡷࠥࡖࡡࡨࡧࠣࡥࡨࡺࡩࡰࡰࠣࡱࡪࡺࡨࡰࡦࡶࠤ࠭࡭࡯ࡵࡱ࠯ࠤࡨࡲࡩࡤ࡭࠯ࠤ࡫࡯࡬࡭࠮ࠣ࠲࠳࠴ࠩࠡࡵࡲࠤࡹ࡮ࡡࡵࠢࡤࡪࡹ࡫ࡲࠡࡧࡤࡧ࡭ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡤࡣ࡯ࡰࠥࡽࡥࠡ࡫ࡱࡺࡴࡱࡥࠡ࡯ࡲࡨࡺࡲࡥࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹ࠯ࡲࡨࡶ࡫ࡵࡲ࡮ࡡࡶࡧࡦࡴࠨࡱࡣࡪࡩ࠱ࠦ࡭ࡦࡶ࡫ࡳࡩࡃࡣ࡮ࡦࡢࡲࡦࡳࡥ࠭ࠌࠣࠤࠥࠦࠠࠡࠢࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࡁࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠩࠬ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࡕࡴࡧࡧࠤࡧࡿࠠࡃࡑࡗࡌ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢ࠰ࠤࡤ࡯࡮ࡴࡶࡤࡰࡱࡥࡡ࠲࠳ࡼࡣࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡥࡸࡡࡳࡥ࡬࡫࡟ࡱࡣࡷࡧ࡭࠴࡟ࡢ࠳࠴ࡽࡤࡴࡥࡸࡡࡳࡥ࡬࡫ࠠࠩࡄࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡥࡰࡢࡩࡨ࠭ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡ࠯ࠣࡳࡳࡥ࡮ࡦࡹࡢࡴࡦ࡭ࡥ࠯ࡹࡵࡥࡵࡶࡥࡥࠢࠫࡆࡷࡵࡷࡴࡧࡵࡇࡴࡴࡴࡦࡺࡷ࠲ࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦ⠔ࠡࡲࡼࡸࡪࡹࡴ࠮ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡶࡡࡵࡪࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥ࡝ࡩࡵࡪࡲࡹࡹࠦࡴࡩ࡫ࡶࠤࡴࡴࠠࡵࡪࡨࠤࡇࡸ࡯ࡸࡵࡨࡶࡈࡵ࡮ࡵࡧࡻࡸ࠳ࡴࡥࡸࡡࡳࡥ࡬࡫ࠠࡱࡣࡷ࡬࠱ࠦࡰࡺࡶࡨࡷࡹ࠳ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠍࠤࠥࠦࠠࠡࠢࠣࠤ࡫࡯ࡸࡵࡷࡵࡩࡸࠦࠨࡸࡪ࡬ࡧ࡭ࠦࡡ࡭ࡹࡤࡽࡸࠦࡣࡢ࡮࡯ࠤࡨࡵ࡮ࡵࡧࡻࡸ࠳ࡴࡥࡸࡡࡳࡥ࡬࡫ࠨࠪࠫࠣ࡫ࡪࡺࠠࡵࡪࡨࠎࠥࠦࠠࠡࠢࠣࠤࠥࡇ࠱࠲ࡻ࠰ࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳ࠳ࡥ࡯ࡣࡥࡰࡪࡪࠠࡢࡤࡲࡹࡹࡀࡢ࡭ࡣࡱ࡯ࠥࡶࡡࡨࡧࠣࡦࡺࡺࠠ࡯ࡧࡹࡩࡷࠦࡴࡳ࡫ࡪ࡫ࡪࡸࠠࡴࡥࡤࡲࡸࠦࡢࡦࡥࡤࡹࡸ࡫ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡣࡦࡸ࡮ࡵ࡮ࠡ࡯ࡨࡸ࡭ࡵࡤࡴࠢࡤࡶࡪࡴࠧࡵࠢࡺࡶࡦࡶࡰࡦࡦ࠱ࠤࡘ࡫ࡳࡴ࡫ࡲࡲࠥࡸࡥࡢࡥ࡫ࡩࡸࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡨࡵࡵࠢࡱࡳࠥࡇ࠱࠲ࡻࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡧࡲࡦࠢࡦࡥࡵࡺࡵࡳࡧࡧ࠲ࠏࠦࠠࠡࠢࠣࠤࠥࠦࠢࠣࠤᨣ")
        if page is None:
            return
        if getattr(page, bstack1l1llll_opy_ (u"ࠧࡠࡤࡶࡸࡦࡩ࡫ࡠࡣ࠴࠵ࡾࡥࡷࡳࡣࡳࡴࡪࡪࠧᨤ"), False):
            return
        try:
            from browserstack_sdk.playwright_driver_wrapper_direct import PlaywrightDriverWrapperDirect
            class bstack11l11ll1lll_opy_:
                def __init__(self, page_ref, bstack11l11l1llll_opy_):
                    self._page = page_ref
                    self._a11y_module = bstack11l11l1llll_opy_
                    self.bstackA11yShouldScan = True
                def execute_async_script(self, script, *args):
                    cmd_name = None
                    if args and isinstance(args[0], dict):
                        cmd_name = args[0].get(bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᨥ"))
                    if cmd_name and self._a11y_module:
                        _thread = threading.current_thread()
                        if getattr(_thread, bstack1l1llll_opy_ (u"ࠩࡢࡦࡸࡺࡡࡤ࡭ࡢࡥ࠶࠷ࡹࡠࡵࡦࡥࡳࡥࡩ࡯ࡡࡳࡶࡴ࡭ࡲࡦࡵࡶࠫᨦ"), False):
                            return None
                        _thread._bstack_a11y_scan_in_progress = True
                        try:
                            return self._a11y_module.perform_scan(
                                self._page,
                                method=cmd_name,
                                framework_name=bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᨧ")
                            )
                        finally:
                            _thread._bstack_a11y_scan_in_progress = False
                    return None
            a11y_module = None
            try:
                from browserstack_sdk.sdk_cli.cli import cli
                a11y_module = getattr(cli, bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᨨ"), None)
            except Exception:
                pass
            if a11y_module:
                wrapper = bstack11l11ll1lll_opy_(page, a11y_module)
                PlaywrightDriverWrapperDirect._wrap_page_for_a11y(page, wrapper, a11y_module)
                setattr(page, bstack1l1llll_opy_ (u"ࠬࡥࡢࡴࡶࡤࡧࡰࡥࡡ࠲࠳ࡼࡣࡼࡸࡡࡱࡲࡨࡨࠬᨩ"), True)
                logger.debug(bstack1l1llll_opy_ (u"ࠨ࡟ࡸࡴࡤࡴࡤࡶࡡࡨࡧࡢࡪࡴࡸ࡟ࡣ࡫ࡱࡥࡷࡿ࡟ࡢ࠳࠴ࡽࡤࡹࡣࡢࡰ࠽ࠤࡼࡸࡡࡱࡲࡨࡨࠥࡶࡡࡨࡧࠣࡥࡨࡺࡩࡰࡰࠣࡱࡪࡺࡨࡰࡦࡶࠤ࡫ࡵࡲࠡࡃ࠴࠵ࡾࠦࡳࡤࡣࡱࡲ࡮ࡴࡧࠣᨪ"))
            else:
                logger.debug(bstack1l1llll_opy_ (u"ࠢࡠࡹࡵࡥࡵࡥࡰࡢࡩࡨࡣ࡫ࡵࡲࡠࡤ࡬ࡲࡦࡸࡹࡠࡣ࠴࠵ࡾࡥࡳࡤࡣࡱ࠾ࠥࡴ࡯ࠡࡣ࠴࠵ࡾࠦ࡭ࡰࡦࡸࡰࡪࠦ࡯࡯ࠢࡦࡰ࡮ࠦࡳࡪࡰࡪࡰࡪࡺ࡯࡯࠮ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡽࡲࡢࡲࠥᨫ"))
        except Exception as _11l11ll11ll_opy_:
            logger.debug(bstack1l1llll_opy_ (u"ࠣࡡࡺࡶࡦࡶ࡟ࡱࡣࡪࡩࡤ࡬࡯ࡳࡡࡥ࡭ࡳࡧࡲࡺࡡࡤ࠵࠶ࡿ࡟ࡴࡥࡤࡲ࠿ࠦࡰࡢࡩࡨࠤࡼࡸࡡࡱࡲ࡬ࡲ࡬ࠦࡥࡳࡴࡲࡶ࠿ࠦࡻࡾࠤᨬ").format(_11l11ll11ll_opy_))
    def _11l11llll11_opy_(self):
        bstack1l1llll_opy_ (u"ࠤࠥࠦࠏࠦࠠࠡࠢࠣࠤࠥࠦࡂࡪࡰࡤࡶࡾࠦࡆ࡭ࡱࡺࠤࡆ࠷࠱ࡺ࠼ࠣࡴࡦࡺࡣࡩࠢࡖࡽࡳࡩࡂࡳࡱࡺࡷࡪࡸ࠮࡯ࡧࡺࡣࡵࡧࡧࡦࠢࡷࡳࠥࡸࡥࡶࡵࡨࠤࡹ࡮ࡥࠡࡧࡻ࡭ࡸࡺࡩ࡯ࡩࠣࡥࡧࡵࡵࡵ࠼ࡥࡰࡦࡴ࡫ࠋࠢࠣࠤࠥࠦࠠࠡࠢࡳࡥ࡬࡫ࠠࠩࡹ࡫࡭ࡨ࡮ࠠࡩࡣࡶࠤࡹ࡮ࡥࠡࡃ࠴࠵ࡾࠦࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࠢࡤࡰࡷ࡫ࡡࡥࡻࠣࡰࡴࡧࡤࡦࡦࠬࠤ࡮ࡴࡳࡵࡧࡤࡨࠥࡵࡦࠡࡱࡳࡩࡳ࡯࡮ࡨࠢࡤࠤࡳ࡫ࡷࠡࡶࡤࡦ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡘࡪࡨࡲࠥࡩ࡯࡯ࡰࡨࡧࡹࡥ࡯ࡷࡧࡵࡣࡨࡪࡰࠡ࡫ࡶࠤࡺࡹࡥࡥ࠮ࠣࡸ࡭࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡣ࡯ࡶࡪࡧࡤࡺࠢ࡫ࡥࡸࠦࡡࠡࡦࡨࡪࡦࡻ࡬ࡵࠢࡦࡳࡳࡺࡥࡹࡶࠣࡻ࡮ࡺࡨࠡࡣࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥ࠯ࠢࡆࡥࡱࡲࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵ࠲ࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠮ࠩࠡࡰࡲࡶࡲࡧ࡬࡭ࡻࠣࡧࡷ࡫ࡡࡵࡧࡶࠤࡦࠦࡎࡆ࡙ࠣࡧࡴࡴࡴࡦࡺࡷࠤࡦࡴࡤࠋࠢࠣࠤࠥࠦࠠࠡࠢࡤࠤࡓࡋࡗࠡࡶࡤࡦࠥ⠚ࠠࡵࡪ࡬ࡷࠥ࡯ࡳࠡࡶ࡫ࡩࠥࡹࡥࡤࡱࡱࡨࠥࡽࡩ࡯ࡦࡲࡻࠥࡺࡨࡦࠢࡸࡷࡪࡸࠠࡴࡧࡨࡷ࠳ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡕࡪ࡬ࡷࠥࡶࡡࡵࡥ࡫ࠤ࡮ࡴࡴࡦࡴࡦࡩࡵࡺࡳࠡࡄࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡥࡰࡢࡩࡨࠤࡦࡺࠠࡵࡪࡨࠤࡨࡲࡡࡴࡵࠣࡰࡪࡼࡥ࡭ࠢࠫ࡫ࡺࡧࡲࡥࡧࡧࠤࡧࡿࠊࠡࠢࠣࠤࠥࠦࠠࠡࡡࡥࡷࡹࡧࡣ࡬ࡡࡱࡩࡼࡥࡰࡢࡩࡨࡣࡵࡧࡴࡤࡪࡨࡨࠥࡹ࡯ࠡ࡫ࡷࠤࡴࡴ࡬ࡺࠢࡵࡹࡳࡹࠠࡰࡰࡦࡩ࠮࠲ࠠࡤࡪࡨࡧࡰࡹࠠࡵࡪࡵࡩࡦࡪ࠮ࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠲ࠊࠡࠢࠣࠤࠥࠦࠠࠡࡣࡱࡨࠥࡸࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡩࡽ࡯ࡳࡵ࡫ࡱ࡫ࠥࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠣࡴࡦ࡭ࡥࠡ࡫ࡱࡷࡹ࡫ࡡࡥ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࡒ࡯ࡲࡳࡱࡵࡷࠥࡥࡰࡢࡶࡦ࡬ࡪࡪ࡟࡯ࡧࡺࡣࡵࡧࡧࡦࠢ࡬ࡲࠥࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠰ࡳࡽࠥ࠮ࡄࡪࡴࡨࡧࡹࠦࡆ࡭ࡱࡺࠤࡪࡷࡵࡪࡸࡤࡰࡪࡴࡴࠪ࠰ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠧࠨࠢᨭ")
        try:
            from playwright.sync_api import Browser as bstack11lllll1l1_opy_
            if hasattr(bstack11lllll1l1_opy_, bstack1l1llll_opy_ (u"ࠪࡣࡧࡹࡴࡢࡥ࡮ࡣࡳ࡫ࡷࡠࡲࡤ࡫ࡪࡥࡰࡢࡶࡦ࡬ࡪࡪࠧᨮ")):
                return
            _1l1lll11lll_opy_ = bstack11lllll1l1_opy_.new_page
            _log = self.logger
            _11l11ll1l1l_opy_ = self
            def _11l1l111lll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_):
                page = None
                if getattr(threading.current_thread(), bstack1l1llll_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᨯ"), None):
                    try:
                        bstack1ll1111111l_opy_ = bstack11l11l1lll_opy_.contexts[0] if bstack11l11l1lll_opy_.contexts else None
                        if bstack1ll1111111l_opy_ and bstack1ll1111111l_opy_.pages:
                            for _1l1lll1ll11_opy_ in bstack1ll1111111l_opy_.pages:
                                if bstack1l1llll_opy_ (u"ࠬࡧࡢࡰࡷࡷ࠾ࡧࡲࡡ࡯࡭ࠪᨰ") in _1l1lll1ll11_opy_.url:
                                    _log.debug(bstack1l1llll_opy_ (u"ࠨࡡ࠲࠳ࡼࡣࡳ࡫ࡷࡠࡲࡤ࡫ࡪࡀࠠࡳࡧࡸࡷ࡮ࡴࡧࠡࡣࡥࡳࡺࡺ࠺ࡣ࡮ࡤࡲࡰࠦࡰࡢࡩࡨࠤ࠭ࡨࡩ࡯ࡣࡵࡽࠥ࡬࡬ࡰࡹࠬࠦᨱ"))
                                    page = _1l1lll1ll11_opy_
                                    break
                            if not page:
                                page = bstack1ll1111111l_opy_.new_page(*bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                        elif bstack1ll1111111l_opy_:
                            page = bstack1ll1111111l_opy_.new_page(*bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                    except Exception as _e:
                        _log.debug(bstack1l1llll_opy_ (u"ࠢࡢ࠳࠴ࡽࡤࡴࡥࡸࡡࡳࡥ࡬࡫࠺ࠡࡨࡤࡰࡱࡨࡡࡤ࡭ࠣࡨࡺ࡫ࠠࡵࡱ࠽ࠤࢀࢃࠢᨲ").format(_e))
                if not page:
                    page = _1l1lll11lll_opy_(bstack11l11l1lll_opy_, *bstack1l11l1ll1l_opy_, **bstack11ll111l1l_opy_)
                bstack1l11l11l111_opy_._11l11ll11l1_opy_(page, _log)
                return page
            bstack11lllll1l1_opy_.new_page = _11l1l111lll_opy_
            bstack11lllll1l1_opy_._bstack_new_page_patched = True
            self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡡ࡬ࡲࡸࡺࡡ࡭࡮ࡢࡥ࠶࠷ࡹࡠࡤࡵࡳࡼࡹࡥࡳࡡࡱࡩࡼࡥࡰࡢࡩࡨࡣࡵࡧࡴࡤࡪ࠽ࠤࡘࡿ࡮ࡤࡄࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࡥࡰࡢࡩࡨࠤࡵࡧࡴࡤࡪࡨࡨࠥ࡬࡯ࡳࠢࡅ࡭ࡳࡧࡲࡺࠢࡉࡰࡴࡽࠠࡂ࠳࠴ࡽࠧᨳ"))
        except Exception as _e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡢ࡭ࡳࡹࡴࡢ࡮࡯ࡣࡦ࠷࠱ࡺࡡࡥࡶࡴࡽࡳࡦࡴࡢࡲࡪࡽ࡟ࡱࡣࡪࡩࡤࡶࡡࡵࡥ࡫࠾ࠥࡶࡡࡵࡥ࡫ࠤ࡫ࡧࡩ࡭ࡧࡧ࠾ࠥࢁࡽࠣᨴ").format(_e))
    def bstack11l11llllll_opy_(self, platform_index: int, ref, user_input_params: bytes):
        req = structs.DriverInitRequest()
        req.bin_session_id = self.bin_session_id
        req.platform_index = platform_index
        req.user_input_params = user_input_params
        req.ref = ref
        req.client_worker_id = bstack1l1llll_opy_ (u"ࠥࡿࢂ࠳ࡻࡾࠤᨵ").format(threading.get_ident(), os.getpid())
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡷ࡫ࡧࡪࡵࡷࡩࡷࡥࡷࡦࡤࡧࡶ࡮ࡼࡥࡳࡡ࡬ࡲ࡮ࡺ࠺ࠡࠤᨶ") + str(req) + bstack1l1llll_opy_ (u"ࠧࠨᨷ"))
        try:
            r = self.cli_service.DriverInit(req)
            if not r.success:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡲࡦࡥࡨ࡭ࡻ࡫ࡤࠡࡨࡵࡳࡲࠦࡳࡦࡴࡹࡩࡷࡀࠠࡴࡷࡦࡧࡪࡹࡳ࠾ࠤᨸ") + str(r.success) + bstack1l1llll_opy_ (u"ࠢࠣᨹ"))
            return r
        except grpc.RpcError as e:
            self.logger.error(bstack1l1llll_opy_ (u"ࠣࡴࡳࡧ࠲࡫ࡲࡳࡱࡵ࠾ࠥࠨᨺ") + str(e) + bstack1l1llll_opy_ (u"ࠤࠥᨻ"))
            traceback.print_exc()
            raise e
    def bstack11l1l11l111_opy_(
        self,
        f: bstack111ll111_opy_,
        Connection: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠥࡣࡸ࡫࡮ࡥࡡࡰࡩࡸࡹࡡࡨࡧࡢࡸࡴࡥࡳࡦࡴࡹࡩࡷࠨᨼ"):
            return
        if not is_bstack_automation():
            return
        def wrapped(Connection, bstack11l1l11llll_opy_, *args, **kwargs):
            return bstack11l1l11llll_opy_(Connection, *args, **kwargs)
        return wrapped
    def on_close(
        self,
        f: bstack111ll111_opy_,
        bstack11l11l1lll1_opy_: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, method_name = exec
        if method_name != bstack1l1llll_opy_ (u"ࠦࡨࡲ࡯ࡴࡧࠥᨽ"):
            return
        if not is_bstack_automation():
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡘࡥࡵࡷࡵࡲ࡮ࡴࡧࠡ࡫ࡱࠤࡨࡲ࡯ࡴࡧࠣࡱࡪࡺࡨࡰࡦ࠯ࠤࡳࡵࡴࠡࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠣᨾ"))
            return
        def wrapped(Connection, close, *args, **kwargs):
            return close(Connection)
        return wrapped