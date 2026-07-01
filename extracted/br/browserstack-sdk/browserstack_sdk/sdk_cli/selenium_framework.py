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
from bstack_utils.performance_tester import PerformanceTester
from bstack_utils.constants import EVENTS
class SeleniumFramework(bstack1l111l1l_opy_):
    bstack111ll1l1l1l_opy_ = bstack1l1llll_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠦᶡ")
    NAME = bstack1l1llll_opy_ (u"ࠧࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠢᶢ")
    bstack11lll111_opy_ = bstack1l1llll_opy_ (u"ࠨࡨࡶࡤࡢࡹࡷࡲࠢᶣ")
    bstack111lllll_opy_ = bstack1l1llll_opy_ (u"ࠢࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡪࡹࡳࡪࡱࡱࡣ࡮ࡪࠢᶤ")
    bstack111l111lll1_opy_ = bstack1l1llll_opy_ (u"ࠣ࡫ࡱࡴࡺࡺ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸࠨᶥ")
    bstack1l111lll_opy_ = bstack1l1llll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠣᶦ")
    bstack111lll11l1l_opy_ = bstack1l1llll_opy_ (u"ࠥ࡭ࡸࡥࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡮ࡵࡣࠤᶧ")
    bstack111l11l11l1_opy_ = bstack1l1llll_opy_ (u"ࠦࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠣᶨ")
    bstack111l11l1l11_opy_ = bstack1l1llll_opy_ (u"ࠧ࡫࡮ࡥࡧࡧࡣࡦࡺࠢᶩ")
    KEY_PLATFORM_INDEX = bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠ࡫ࡱࡨࡪࡾࠢᶪ")
    bstack111llll1111_opy_ = bstack1l1llll_opy_ (u"ࠢ࡯ࡧࡺࡷࡪࡹࡳࡪࡱࡱࠦᶫ")
    bstack111l111l1ll_opy_ = bstack1l1llll_opy_ (u"ࠣࡩࡨࡸࠧᶬ")
    COMMAND_SCREENSHOT = bstack1l1llll_opy_ (u"ࠤࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࠨᶭ")
    bstack111ll1ll11l_opy_ = bstack1l1llll_opy_ (u"ࠥࡻ࠸ࡩࡥࡹࡧࡦࡹࡹ࡫ࡳࡤࡴ࡬ࡴࡹࠨᶮ")
    bstack111ll1ll1l1_opy_ = bstack1l1llll_opy_ (u"ࠦࡼ࠹ࡣࡦࡺࡨࡧࡺࡺࡥࡴࡥࡵ࡭ࡵࡺࡡࡴࡻࡱࡧࠧᶯ")
    bstack111l11l1l1l_opy_ = bstack1l1llll_opy_ (u"ࠧࡷࡵࡪࡶࠥᶰ")
    hook_regsitry: Dict[str, List[Callable]] = dict()
    bstack111llll1l1l_opy_: str
    platform_index: int
    options: Any
    desired_capabilities: Any
    bstack1l11l11l1l1_opy_: Any
    bstack111ll1l11l1_opy_: Dict
    def __init__(
        self,
        bstack111llll1l1l_opy_: str,
        platform_index: int,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
        bstack1l11l11l1l1_opy_: Dict[str, Any],
        methods=[bstack1l1llll_opy_ (u"ࠨ࡟ࡠ࡫ࡱ࡭ࡹࡥ࡟ࠣᶱ"), bstack1l1llll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢᶲ"), bstack1l1llll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤᶳ"), bstack1l1llll_opy_ (u"ࠤࡴࡹ࡮ࡺࠢᶴ")],
    ):
        super().__init__(
            framework_name,
            framework_version,
            classes,
        )
        self.bstack111llll1l1l_opy_ = bstack111llll1l1l_opy_
        self.platform_index = platform_index
        self.bstack1l11lll11l1_opy_(methods)
        self.bstack1l11l11l1l1_opy_ = bstack1l11l11l1l1_opy_
    @staticmethod
    def session_id(target: object, strict=True):
        return bstack1l111l1l_opy_.get_data(SeleniumFramework.bstack111lllll_opy_, target, strict)
    @staticmethod
    def hub_url(target: object, strict=True):
        return bstack1l111l1l_opy_.get_data(SeleniumFramework.bstack11lll111_opy_, target, strict)
    @staticmethod
    def bstack111l11l11ll_opy_(target: object, strict=True):
        return bstack1l111l1l_opy_.get_data(SeleniumFramework.bstack111l111lll1_opy_, target, strict)
    @staticmethod
    def capabilities(target: object, strict=True):
        return bstack1l111l1l_opy_.get_data(SeleniumFramework.bstack1l111lll_opy_, target, strict)
    @staticmethod
    def bstack11l1ll1l11l_opy_(instance: AutomationFrameworkBrowser) -> bool:
        return bstack1l111l1l_opy_.get_state(instance, SeleniumFramework.bstack111lll11l1l_opy_, False)
    @staticmethod
    def bstack11ll1l11l1l_opy_(instance: AutomationFrameworkBrowser, default_value=None):
        return bstack1l111l1l_opy_.get_state(instance, SeleniumFramework.bstack11lll111_opy_, default_value)
    @staticmethod
    def bstack11lll111l11_opy_(instance: AutomationFrameworkBrowser, default_value=None):
        return bstack1l111l1l_opy_.get_state(instance, SeleniumFramework.bstack1l111lll_opy_, default_value)
    @staticmethod
    def bstack11ll11111l1_opy_(hub_url: str, bstack111l11l111l_opy_=bstack1l1llll_opy_ (u"ࠥ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠢᶵ")):
        try:
            bstack111l111ll11_opy_ = str(urlparse(hub_url).netloc) if hub_url else None
            return bstack111l111ll11_opy_.endswith(bstack111l11l111l_opy_)
        except Exception as e:
            from bstack_utils import logger_utils
            logger_utils.get_logger(__name__).debug(bstack1l1llll_opy_ (u"ࠦ࡮ࡹ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡨࡶࡤࠣࡹࡷࡲࠠࡱࡣࡵࡷࡪࠦࡦࡢ࡫࡯ࡩࡩࡀࠠࡼࡿ࠽ࠤࢀࢃࠢᶶ").format(type(e).__name__, e), exc_info=True)
        return False
    @staticmethod
    def is_execute_request(method_name: str):
        return method_name == bstack1l1llll_opy_ (u"ࠧ࡫ࡸࡦࡥࡸࡸࡪࠨᶷ")
    @staticmethod
    def bstack11ll111ll1l_opy_(method_name: str, *args):
        return (
            SeleniumFramework.is_execute_request(method_name)
            and SeleniumFramework.bstack111lll1l1ll_opy_(*args) == SeleniumFramework.bstack111llll1111_opy_
        )
    @staticmethod
    def bstack11ll11ll111_opy_(method_name: str, *args):
        if not SeleniumFramework.is_execute_request(method_name):
            return False
        if not SeleniumFramework.bstack111ll1ll11l_opy_ in SeleniumFramework.bstack111lll1l1ll_opy_(*args):
            return False
        bstack11ll1111ll1_opy_ = SeleniumFramework.bstack11ll1111l1l_opy_(*args)
        return bstack11ll1111ll1_opy_ and bstack1l1llll_opy_ (u"ࠨࡳࡤࡴ࡬ࡴࡹࠨᶸ") in bstack11ll1111ll1_opy_ and bstack1l1llll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᶹ") in bstack11ll1111ll1_opy_[bstack1l1llll_opy_ (u"ࠣࡵࡦࡶ࡮ࡶࡴࠣᶺ")]
    @staticmethod
    def bstack11ll11l1111_opy_(method_name: str, *args):
        if not SeleniumFramework.is_execute_request(method_name):
            return False
        if not SeleniumFramework.bstack111ll1ll11l_opy_ in SeleniumFramework.bstack111lll1l1ll_opy_(*args):
            return False
        bstack11ll1111ll1_opy_ = SeleniumFramework.bstack11ll1111l1l_opy_(*args)
        return (
            bstack11ll1111ll1_opy_
            and bstack1l1llll_opy_ (u"ࠤࡶࡧࡷ࡯ࡰࡵࠤᶻ") in bstack11ll1111ll1_opy_
            and bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡥࡳࡤࡴ࡬ࡴࡹࠨᶼ") in bstack11ll1111ll1_opy_[bstack1l1llll_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࠦᶽ")]
        )
    @staticmethod
    def bstack111lll1l1ll_opy_(*args):
        return str(SeleniumFramework.parse_command_name(*args)).lower()
    @staticmethod
    def parse_command_name(*args):
        return args[0] if args and type(args) in [list, tuple] and isinstance(args[0], str) else None
    @staticmethod
    def bstack11ll1111l1l_opy_(*args):
        return args[1] if len(args) > 1 and isinstance(args[1], dict) else None
    @staticmethod
    def bstack1l1l111ll11_opy_(driver):
        command_executor = getattr(driver, bstack1l1llll_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࡥࡥࡹࡧࡦࡹࡹࡵࡲࠣᶾ"), None)
        if not command_executor:
            return None
        hub_url = str(command_executor) if isinstance(command_executor, (str, bytes)) else None
        hub_url = str(command_executor._url) if not hub_url and getattr(command_executor, bstack1l1llll_opy_ (u"ࠨ࡟ࡶࡴ࡯ࠦᶿ"), None) else None
        if not hub_url:
            client_config = getattr(command_executor, bstack1l1llll_opy_ (u"ࠢࡠࡥ࡯࡭ࡪࡴࡴࡠࡥࡲࡲ࡫࡯ࡧࠣ᷀"), None)
            if not client_config:
                return None
            hub_url = getattr(client_config, bstack1l1llll_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡠࡵࡨࡶࡻ࡫ࡲࡠࡣࡧࡨࡷࠨ᷁"), None)
        return hub_url
    def bstack111lll1llll_opy_(self, instance, driver, hub_url: str):
        result = False
        if not hub_url:
            return result
        command_executor = getattr(driver, bstack1l1llll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ᷂ࠧ"), None)
        if command_executor:
            if isinstance(command_executor, (str, bytes)):
                setattr(driver, bstack1l1llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡣࡪࡾࡥࡤࡷࡷࡳࡷࠨ᷃"), hub_url)
                result = True
            elif hasattr(command_executor, bstack1l1llll_opy_ (u"ࠦࡤࡻࡲ࡭ࠤ᷄")):
                setattr(command_executor, bstack1l1llll_opy_ (u"ࠧࡥࡵࡳ࡮ࠥ᷅"), hub_url)
                result = True
        if result:
            self.bstack111llll1l1l_opy_ = hub_url
            SeleniumFramework.set_state(instance, SeleniumFramework.bstack11lll111_opy_, hub_url)
            SeleniumFramework.set_state(
                instance, SeleniumFramework.bstack111lll11l1l_opy_, SeleniumFramework.bstack11ll11111l1_opy_(hub_url)
            )
        return result
    @staticmethod
    def hook_info_to_registry_key(hook_info: Tuple[AutomationFrameworkState, HookState]):
        return bstack1l1llll_opy_ (u"ࠨ࠺ࠣ᷆").join((AutomationFrameworkState(hook_info[0]).name, HookState(hook_info[1]).name))
    @staticmethod
    def set_hook_callback(hook_info: Tuple[AutomationFrameworkState, HookState], callback: Callable):
        hook_registry_key = SeleniumFramework.hook_info_to_registry_key(hook_info)
        if not hook_registry_key in SeleniumFramework.hook_regsitry:
            SeleniumFramework.hook_regsitry[hook_registry_key] = []
        SeleniumFramework.hook_regsitry[hook_registry_key].append(callback)
    def bstack1l11ll1l111_opy_(self, instance: AutomationFrameworkBrowser, method_name: str, bstack1l11ll11l1l_opy_: timedelta, *args, **kwargs):
        if not instance or method_name in (bstack1l1llll_opy_ (u"ࠢࡴࡶࡤࡶࡹࡥࡳࡦࡵࡶ࡭ࡴࡴࠢ᷇")):
            return
        cmd = args[0] if method_name == bstack1l1llll_opy_ (u"ࠣࡧࡻࡩࡨࡻࡴࡦࠤ᷈") and args and type(args) in [list, tuple] and isinstance(args[0], str) else None
        bstack111l111llll_opy_ = bstack1l1llll_opy_ (u"ࠤ࠽ࠦ᷉").join(map(str, filter(None, [method_name, cmd])))
        instance.add_benchmark(bstack1l1llll_opy_ (u"ࠥࡨࡷ࡯ࡶࡦࡴ࠽᷊ࠦ") + bstack111l111llll_opy_, bstack1l11ll11l1l_opy_)
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
        hook_registry_key = SeleniumFramework.hook_info_to_registry_key(hook_info)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡴࡴ࡟ࡩࡱࡲ࡯࠿ࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡭ࡵ࡯࡬ࡡ࡬ࡲ࡫ࡵ࠽ࡼࡪࡲࡳࡰࡥࡩ࡯ࡨࡲࢁࠥࡧࡲࡨࡵࡀࡿࡦࡸࡧࡴࡿࠣ࡯ࡼࡧࡲࡨࡵࡀࠦ᷋") + str(kwargs) + bstack1l1llll_opy_ (u"ࠧࠨ᷌"))
        if bstack1l11llll11l_opy_ == AutomationFrameworkState.QUIT:
            if bstack111ll1l1ll1_opy_ == HookState.PRE:
                random_label = PerformanceTester.mark_start(EVENTS.bstack111l111ll1l_opy_.value)
                bstack1l111l1l_opy_.set_state(instance, EVENTS.bstack111l111ll1l_opy_.value, random_label)
                self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࡽࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠣ࡬ࡴࡵ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡿࠥ᷍").format(instance, method_name, bstack1l11llll11l_opy_, bstack111ll1l1ll1_opy_))
            if bstack111ll1l1ll1_opy_ == HookState.POST:
                random_label = PerformanceTester.mark_start(EVENTS.bstack111l11l1111_opy_.value)
                bstack1l111l1l_opy_.set_state(instance, EVENTS.bstack111l11l1111_opy_.value, random_label)
        if bstack1l11llll11l_opy_ == AutomationFrameworkState.CREATE:
            if bstack111ll1l1ll1_opy_ == HookState.POST and not SeleniumFramework.bstack111lllll_opy_ in instance.data:
                session_id = getattr(target, bstack1l1llll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࡠ࡫ࡧ᷎ࠦ"), None)
                if session_id:
                    instance.data[SeleniumFramework.bstack111lllll_opy_] = session_id
        elif (
            bstack1l11llll11l_opy_ == AutomationFrameworkState.EXECUTE
            and SeleniumFramework.bstack111lll1l1ll_opy_(*args) == SeleniumFramework.bstack111llll1111_opy_
        ):
            if bstack111ll1l1ll1_opy_ == HookState.PRE:
                hub_url = SeleniumFramework.bstack1l1l111ll11_opy_(target)
                if hub_url:
                    instance.data.update(
                        {
                            SeleniumFramework.bstack11lll111_opy_: hub_url,
                            SeleniumFramework.bstack111lll11l1l_opy_: SeleniumFramework.bstack11ll11111l1_opy_(hub_url),
                            SeleniumFramework.KEY_PLATFORM_INDEX: int(
                                os.environ.get(bstack1l1llll_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘ᷏ࠣ"), str(self.platform_index))
                            ),
                        }
                    )
                bstack11ll1111ll1_opy_ = SeleniumFramework.bstack11ll1111l1l_opy_(*args)
                bstack111l11l11ll_opy_ = bstack11ll1111ll1_opy_.get(bstack1l1llll_opy_ (u"ࠤࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ᷐ࠣ"), None) if bstack11ll1111ll1_opy_ else None
                if isinstance(bstack111l11l11ll_opy_, dict):
                    instance.data[SeleniumFramework.bstack111l111lll1_opy_] = copy.deepcopy(bstack111l11l11ll_opy_)
                    instance.data[SeleniumFramework.bstack1l111lll_opy_] = bstack111l11l11ll_opy_
            elif bstack111ll1l1ll1_opy_ == HookState.POST:
                if isinstance(result, dict):
                    framework_session_id = result.get(bstack1l1llll_opy_ (u"ࠥࡺࡦࡲࡵࡦࠤ᷑"), dict()).get(bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡳࡴ࡫ࡲࡲࡎࡪࠢ᷒"), None)
                    if framework_session_id:
                        instance.data.update(
                            {
                                SeleniumFramework.bstack111lllll_opy_: framework_session_id,
                                SeleniumFramework.bstack111l11l11l1_opy_: datetime.now(tz=timezone.utc),
                            }
                        )
        elif (
            bstack1l11llll11l_opy_ == AutomationFrameworkState.EXECUTE
            and SeleniumFramework.bstack111lll1l1ll_opy_(*args) == SeleniumFramework.bstack111l11l1l1l_opy_
            and bstack111ll1l1ll1_opy_ == HookState.POST
        ):
            instance.data[SeleniumFramework.bstack111l11l1l11_opy_] = datetime.now(tz=timezone.utc)
        if hook_registry_key in SeleniumFramework.hook_regsitry:
            bstack111ll1l1l11_opy_ = None
            for callback in SeleniumFramework.hook_regsitry[hook_registry_key]:
                try:
                    bstack111ll1l11ll_opy_ = callback(self, target, exec, hook_info, result, *args, **kwargs)
                    if bstack111ll1l1l11_opy_ == None:
                        bstack111ll1l1l11_opy_ = bstack111ll1l11ll_opy_
                except Exception as e:
                    self.logger.error(bstack1l1llll_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠤ࡮ࡴࡶࡰ࡭࡬ࡲ࡬ࠦࡣࡢ࡮࡯ࡦࡦࡩ࡫࠻ࠢࠥᷓ") + str(e) + bstack1l1llll_opy_ (u"ࠨࠢᷔ"))
                    traceback.print_exc()
            if bstack1l11llll11l_opy_ == AutomationFrameworkState.QUIT:
                if bstack111ll1l1ll1_opy_ == HookState.PRE:
                    random_label = bstack1l111l1l_opy_.get_state(instance, EVENTS.bstack111l111ll1l_opy_.value)
                    if random_label!=None:
                        PerformanceTester.end(EVENTS.bstack111l111ll1l_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᷕ"), random_label+bstack1l1llll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᷖ"), True, None)
                if bstack111ll1l1ll1_opy_ == HookState.POST:
                    random_label = bstack1l111l1l_opy_.get_state(instance, EVENTS.bstack111l11l1111_opy_.value)
                    if random_label!=None:
                        PerformanceTester.end(EVENTS.bstack111l11l1111_opy_.value, random_label+bstack1l1llll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᷗ"), random_label+bstack1l1llll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᷘ"), True, None)
            if bstack111ll1l1ll1_opy_ == HookState.PRE and callable(bstack111ll1l1l11_opy_):
                return bstack111ll1l1l11_opy_
            elif bstack111ll1l1ll1_opy_ == HookState.POST and bstack111ll1l1l11_opy_:
                return bstack111ll1l1l11_opy_
    def bstack1l11ll1ll1l_opy_(
        self, method_name, previous_state: AutomationFrameworkState, *args, **kwargs
    ) -> AutomationFrameworkState:
        if method_name == bstack1l1llll_opy_ (u"ࠦࡤࡥࡩ࡯࡫ࡷࡣࡤࠨᷙ") or method_name == bstack1l1llll_opy_ (u"ࠧࡹࡴࡢࡴࡷࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠧᷚ"):
            return AutomationFrameworkState.CREATE
        if method_name == bstack1l1llll_opy_ (u"ࠨࡱࡶ࡫ࡷࠦᷛ"):
            return AutomationFrameworkState.QUIT
        if method_name == bstack1l1llll_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࠣᷜ"):
            if previous_state != AutomationFrameworkState.NONE:
                command_name = SeleniumFramework.bstack111lll1l1ll_opy_(*args)
                if command_name == SeleniumFramework.bstack111llll1111_opy_:
                    return AutomationFrameworkState.CREATE
            return AutomationFrameworkState.EXECUTE
        return AutomationFrameworkState.NONE