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
import os
import traceback
from typing import Dict, Tuple, Callable, Type, List, Any
from urllib.parse import urlparse
from browserstack_sdk.sdk_cli.automation_framework import (
    bstack1l111l1l_opy_,
    AutomationFrameworkBrowser,
    AutomationFrameworkState,
    HookState,
)
import copy
from datetime import datetime, timezone, timedelta
class bstack111ll111_opy_(bstack1l111l1l_opy_):
    bstack111ll1l1l1l_opy_ = bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠣᮟ")
    bstack111lllll_opy_ = bstack1l1llll_opy_ (u"ࠤࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳࡥࡩࡥࠤᮠ")
    bstack11lll111_opy_ = bstack1l1llll_opy_ (u"ࠥ࡬ࡺࡨ࡟ࡶࡴ࡯ࠦᮡ")
    bstack1l111lll_opy_ = bstack1l1llll_opy_ (u"ࠦࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠥᮢ")
    bstack11l11lll111_opy_ = bstack1l1llll_opy_ (u"ࠧࡺࡨࡳࡧࡤࡨࡤ࡯ࡤࠣᮣ")
    bstack111ll1ll11l_opy_ = bstack1l1llll_opy_ (u"ࠨࡷ࠴ࡥࡨࡼࡪࡩࡵࡵࡧࡶࡧࡷ࡯ࡰࡵࠤᮤ")
    bstack111ll1ll1l1_opy_ = bstack1l1llll_opy_ (u"ࠢࡸ࠵ࡦࡩࡽ࡫ࡣࡶࡶࡨࡷࡨࡸࡩࡱࡶࡤࡷࡾࡴࡣࠣᮥ")
    NAME = bstack1l1llll_opy_ (u"ࠣࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠧᮦ")
    bstack111ll1ll111_opy_: Dict[str, List[Callable]] = dict()
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l11l1l1_opy_: Any
    bstack111ll1l11l1_opy_: Dict
    def __init__(
        self,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        methods=[bstack1l1llll_opy_ (u"ࠤ࡯ࡥࡺࡴࡣࡩࠤᮧ"), bstack1l1llll_opy_ (u"ࠥࡧࡴࡴ࡮ࡦࡥࡷࠦᮨ"), bstack1l1llll_opy_ (u"ࠦࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠨᮩ"), bstack1l1llll_opy_ (u"ࠧࡩ࡬ࡰࡵࡨ᮪ࠦ"), bstack1l1llll_opy_ (u"ࠨࡤࡪࡵࡳࡥࡹࡩࡨ᮫ࠣ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.platform_index = platform_index
        self.bstack1l11lll11l1_opy_(methods)
    def bstack1l11ll1l111_opy_(self, instance: AutomationFrameworkBrowser, method_name: str, bstack1l11ll11l1l_opy_: timedelta, *args, **kwargs):
        pass
    def bstack1l1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable[..., Any]:
        instance, method_name = exec
        bstack1l11llll11l_opy_, bstack111ll1l1ll1_opy_ = hook_info
        hook_registry_key = bstack111ll111_opy_.hook_info_to_registry_key(hook_info)
        if hook_registry_key in bstack111ll111_opy_.bstack111ll1ll111_opy_:
            bstack111ll1l1l11_opy_ = None
            for callback in bstack111ll111_opy_.bstack111ll1ll111_opy_[hook_registry_key]:
                try:
                    bstack111ll1l11ll_opy_ = callback(self, target, exec, hook_info, result, *args, **kwargs)
                    if bstack111ll1l1l11_opy_ == None:
                        bstack111ll1l1l11_opy_ = bstack111ll1l11ll_opy_
                except Exception as e:
                    self.logger.error(bstack1l1llll_opy_ (u"ࠢࡦࡴࡵࡳࡷࠦࡩ࡯ࡸࡲ࡯࡮ࡴࡧࠡࡥࡤࡰࡱࡨࡡࡤ࡭࠽ࠤࠧᮬ") + str(e) + bstack1l1llll_opy_ (u"ࠣࠤᮭ"))
                    traceback.print_exc()
            if bstack111ll1l1ll1_opy_ == HookState.PRE and callable(bstack111ll1l1l11_opy_):
                return bstack111ll1l1l11_opy_
            elif bstack111ll1l1ll1_opy_ == HookState.POST and bstack111ll1l1l11_opy_:
                return bstack111ll1l1l11_opy_
    def bstack1l11ll1ll1l_opy_(
        self, method_name, previous_state: AutomationFrameworkState, *args, **kwargs
    ) -> AutomationFrameworkState:
        if method_name == bstack1l1llll_opy_ (u"ࠩ࡯ࡥࡺࡴࡣࡩࠩᮮ") or method_name == bstack1l1llll_opy_ (u"ࠪࡧࡴࡴ࡮ࡦࡥࡷࠫᮯ") or method_name == bstack1l1llll_opy_ (u"ࠫࡳ࡫ࡷࡠࡲࡤ࡫ࡪ࠭᮰"):
            return AutomationFrameworkState.CREATE
        if method_name == bstack1l1llll_opy_ (u"ࠬࡪࡩࡴࡲࡤࡸࡨ࡮ࠧ᮱"):
            return AutomationFrameworkState.bstack1l11llll1l1_opy_
        if method_name == bstack1l1llll_opy_ (u"࠭ࡣ࡭ࡱࡶࡩࠬ᮲"):
            return AutomationFrameworkState.QUIT
        return AutomationFrameworkState.NONE
    @staticmethod
    def hook_info_to_registry_key(hook_info: Tuple[AutomationFrameworkState, HookState]):
        return bstack1l1llll_opy_ (u"ࠢ࠻ࠤ᮳").join((AutomationFrameworkState(hook_info[0]).name, HookState(hook_info[1]).name))
    @staticmethod
    def set_hook_callback(hook_info: Tuple[AutomationFrameworkState, HookState], callback: Callable):
        hook_registry_key = bstack111ll111_opy_.hook_info_to_registry_key(hook_info)
        if not hook_registry_key in bstack111ll111_opy_.bstack111ll1ll111_opy_:
            bstack111ll111_opy_.bstack111ll1ll111_opy_[hook_registry_key] = []
        bstack111ll111_opy_.bstack111ll1ll111_opy_[hook_registry_key].append(callback)
    @staticmethod
    def is_execute_request(method_name: str):
        return True
    @staticmethod
    def bstack11ll111ll1l_opy_(method_name: str, *args) -> bool:
        command_name = bstack111ll111_opy_.bstack111lll1l1ll_opy_(*args)
        if command_name in [bstack1l1llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳ࠰ࡱࡩࡼࠦࡢࡳࡱࡺࡷࡪࡸࠢ᮴"), bstack1l1llll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴ࠱ࡧࡴࡴ࡮ࡦࡥࡷࠤࡹࡵࠠࡣࡴࡲࡻࡸ࡫ࡲࠣ᮵")]:
            return True
        return False
    @staticmethod
    def bstack11lll111l11_opy_(instance: AutomationFrameworkBrowser, default_value=None):
        return bstack1l111l1l_opy_.get_state(instance, bstack111ll111_opy_.bstack1l111lll_opy_, default_value)
    @staticmethod
    def bstack11l1ll1l11l_opy_(instance: AutomationFrameworkBrowser) -> bool:
        return True
    @staticmethod
    def bstack11ll1l11l1l_opy_(instance: AutomationFrameworkBrowser, default_value=None):
        return bstack1l111l1l_opy_.get_state(instance, bstack111ll111_opy_.bstack11lll111_opy_, default_value)
    @staticmethod
    def parse_command_name(*args):
        bstack111ll1l1lll_opy_ = None
        if args and isinstance(args, (list, tuple)):
            if len(args) > 0 and isinstance(args[0], (list, tuple)):
                if len(args[0]) > 0 and isinstance(args[0][0], str):
                    bstack111ll1l1lll_opy_ = args[0][0]
            elif isinstance(args[0], str):
                bstack111ll1l1lll_opy_ = args[0]
        if not bstack111ll1l1lll_opy_:
            return None
        return bstack111ll1l1lll_opy_.strip()
    @staticmethod
    def bstack11ll11ll111_opy_(method_name: str, *args):
        if not bstack111ll111_opy_.is_execute_request(method_name):
            return False
        bstack11ll1111ll1_opy_ = args[0][1]
        if not isinstance(bstack11ll1111ll1_opy_, dict) or bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᮶") not in bstack11ll1111ll1_opy_:
            return False
        args_list = bstack11ll1111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ᮷"), [])
        return any(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠧ᮸") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack11ll11l1111_opy_(method_name: str, *args):
        if not bstack111ll111_opy_.is_execute_request(method_name):
            return False
        bstack11ll1111ll1_opy_ = args[0][1]
        if not isinstance(bstack11ll1111ll1_opy_, dict) or bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡶࠫ᮹") not in bstack11ll1111ll1_opy_:
            return False
        args_list = bstack11ll1111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬᮺ"), [])
        return any(bstack1l1llll_opy_ (u"ࠨࡨࡸࡲࡨࡺࡩࡰࡰࠣࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࠨࠪࠩᮻ") in str(arg) for arg in args_list if arg)
    @staticmethod
    def bstack111lll1l1ll_opy_(*args):
        return str(bstack111ll111_opy_.parse_command_name(*args)).lower()