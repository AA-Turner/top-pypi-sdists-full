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
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.sdk_cli.automation_framework import (
    AutomationFrameworkState,
    HookState,
    bstack1l111l1l_opy_,
    AutomationFrameworkBrowser,
)
from browserstack_sdk.sdk_cli.selenium_framework import SeleniumFramework
from browserstack_sdk.sdk_cli.bstack1l1ll1l1_opy_ import bstack111ll111_opy_
from browserstack_sdk.sdk_cli.tracked_instance import bstack1l11ll1l1l1_opy_
from typing import Tuple, Dict, Any, List, Callable
from browserstack_sdk.sdk_cli.module_base import BaseModule
from browserstack_sdk.browserstack_helper import BrowserStackHelper
import weakref
class bstack11l1l1lllll_opy_(BaseModule):
    bstack11l1ll11111_opy_: str
    frameworks: List[str]
    drivers: Dict[str, Tuple[Callable, AutomationFrameworkBrowser]]
    pages: Dict[str, Tuple[Callable, AutomationFrameworkBrowser]]
    bstack11l1llll1ll_opy_ = bstack1l1llll_opy_ (u"ࠥࡦࡸࡺࡡࡤ࡭ࡢࡳࡼࡴࡥࡳࡡࡷࡩࡸࡺ࡟ࡳࡧࡩࠦᦍ")
    bstack11l1ll11l1l_opy_ = (bstack1l1llll_opy_ (u"ࠦࡨࡲࡡࡴࡵࠥᦎ"), bstack1l1llll_opy_ (u"ࠧࡳ࡯ࡥࡷ࡯ࡩࠧᦏ"), bstack1l1llll_opy_ (u"ࠨࡰࡢࡥ࡮ࡥ࡬࡫ࠢᦐ"), bstack1l1llll_opy_ (u"ࠢࡴࡧࡶࡷ࡮ࡵ࡮ࠣᦑ"))
    def __init__(self, bstack11l1ll11111_opy_: str, frameworks: List[str]):
        super().__init__()
        self.drivers = dict()
        self.pages = dict()
        self.bstack11l1llll1l1_opy_ = dict()
        self.bstack11l1ll11111_opy_ = bstack11l1ll11111_opy_
        self.frameworks = frameworks
        bstack111ll111_opy_.set_hook_callback((AutomationFrameworkState.CREATE, HookState.POST), self.__11l1lll1lll_opy_)
        if any(SeleniumFramework.NAME in f.lower().strip() for f in frameworks):
            SeleniumFramework.set_hook_callback(
                (AutomationFrameworkState.EXECUTE, HookState.PRE), self.__11l1ll1l1l1_opy_
            )
            SeleniumFramework.set_hook_callback(
                (AutomationFrameworkState.QUIT, HookState.POST), self.__11l1ll1111l_opy_
            )
    def __11l1lll1lll_opy_(
        self,
        f: bstack111ll111_opy_,
        bstack11l1ll1ll11_opy_: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        try:
            instance, method_name = exec
            if method_name != bstack1l1llll_opy_ (u"ࠣࡰࡨࡻࡤࡶࡡࡨࡧࠥᦒ"):
                return
            if result is not None and hasattr(result, bstack1l1llll_opy_ (u"ࠤࡨࡺࡦࡲࡵࡢࡶࡨࠦᦓ")):
                self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡗࡹࡵࡲࡪࡰࡪࠤࡹ࡮ࡥࠡࡰࡨࡻࠥࡶࡡࡨࡧࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࠥ࠮ࡦࡳࡱࡰࠤࡳ࡫ࡷࡠࡲࡤ࡫ࡪࠦࡲࡦࡵࡸࡰࡹ࠯ࠢᦔ"))
                self.pages[instance.ref()] = weakref.ref(result), instance
                bstack1l111l1l_opy_.set_state(instance, self.bstack11l1ll11111_opy_, True)
                return
            browser = getattr(bstack11l1ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧᦕ"), None)
            if browser is not None:
                contexts = browser.contexts
            else:
                contexts = getattr(bstack11l1ll1ll11_opy_, bstack1l1llll_opy_ (u"ࠧࡩ࡯࡯ࡶࡨࡼࡹࡹࠢᦖ"), None)
            if contexts:
                for context in contexts:
                    if context.pages:
                        for page in context.pages:
                            if bstack1l1llll_opy_ (u"ࠨࡡࡣࡱࡸࡸ࠿ࡨ࡬ࡢࡰ࡮ࠦᦗ") in page.url:
                                self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡔࡶࡲࡶ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡴࡥࡸࠢࡳࡥ࡬࡫ࠠࡪࡰࡶࡸࡦࡴࡣࡦࠤᦘ"))
                                self.pages[instance.ref()] = weakref.ref(page), instance
                                bstack1l111l1l_opy_.set_state(instance, self.bstack11l1ll11111_opy_, True)
                                self.logger.debug(bstack1l1llll_opy_ (u"ࠣࡡࡢࡳࡳࡥࡰࡢࡩࡨࡣ࡮ࡴࡩࡵ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࠨᦙ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠤࠥᦚ"))
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡸࡩ࡯ࡩࠣࡲࡪࡽࠠࡱࡣࡪࡩࠥࡀࠢᦛ"),e)
    def __11l1ll1l1l1_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if instance.ref() in self.drivers or bstack1l111l1l_opy_.get_state(instance, self.bstack11l1ll11111_opy_, False):
            return
        label = BrowserStackHelper.get_driver_label()
        bstack1l11lll1l1l_opy_ = None
        if label:
            if bstack1l1llll_opy_ (u"ࠦࠨࠨᦜ") in label:
                suffix = label.rsplit(bstack1l1llll_opy_ (u"ࠧࠩࠢᦝ"), 1)[-1]
                if suffix.isdigit():
                    bstack1l11lll1l1l_opy_ = suffix
                else:
                    self.logger.debug(
                        bstack1l11lll11ll_opy_ (u"ࠨࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡥࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࡳࡶࡨࡩ࡭ࡽࠦࠧࡼࡵࡸࡪ࡫࡯ࡸࡾࠩࠣ࡭ࡳࠦ࡬ࡢࡤࡨࡰࠥ࠭ࡻ࡭ࡣࡥࡩࡱࢃࠧ࠼ࠢࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡳࡻ࡭ࡦࡴ࡬ࡧࠥࡸࡡ࡯࡭࠱ࠦᦞ")
                    )
            else:
                self.logger.debug(
                    bstack1l11lll11ll_opy_ (u"ࠢࡅࡴ࡬ࡺࡪࡸࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨࠢࡧࡳࡪࡹࠠ࡯ࡱࡷࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥ࠭ࠣࠨ࠽ࠣࡷࡰ࡯ࡰࡱ࡫ࡱ࡫ࠥࡸࡡ࡯࡭ࠣࡥࡸࡹࡩࡨࡰࡰࡩࡳࡺ࠮ࠣᦟ")
                )
        if bstack1l11lll1l1l_opy_ is not None:
            bstack1l11lll1l1l_opy_ = label.split(bstack1l1llll_opy_ (u"ࠣࠥࠥᦠ"))[-1]
            instance.data[bstack1l1llll_opy_ (u"ࠤࡵࡥࡳࡱࠢᦡ")] = bstack1l11lll1l1l_opy_
        self.logger.debug(bstack1l1llll_opy_ (u"ࠥࡣࡤࡵ࡮ࡠࡵࡨࡰࡪࡴࡩࡶ࡯ࡢ࡭ࡳ࡯ࡴ࠻ࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡁࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡳࡧࡩࠬ࠮ࢃࠠࡸ࡫ࡷ࡬ࠥࡪࡡࡵࡣࡀࠦᦢ") + str(instance.data) + bstack1l1llll_opy_ (u"ࠦࠧᦣ"))
        if not f.bstack11ll11111l1_opy_(f.hub_url(driver)):
            self.bstack11l1llll1l1_opy_[instance.ref()] = weakref.ref(driver), instance
            self.__11l1ll1llll_opy_(instance)
            bstack1l111l1l_opy_.set_state(instance, self.bstack11l1ll11111_opy_, True)
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡥ࡟ࡰࡰࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࡤ࡯࡮ࡪࡶ࠽ࠤࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡥࡴ࡬ࡺࡪࡸࠠࡪࡰࡶࡸࡦࡴࡣࡦ࠿ࠥᦤ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠨࠢᦥ"))
            return
        if label is not None:
            BrowserStackHelper.clear_driver_label()
        self.drivers[instance.ref()] = weakref.ref(driver), instance
        self.__11l1ll1llll_opy_(instance)
        bstack1l111l1l_opy_.set_state(instance, self.bstack11l1ll11111_opy_, True)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡠࡡࡲࡲࡤࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࡟ࡪࡰ࡬ࡸ࠿ࠦࡩ࡯ࡵࡷࡥࡳࡩࡥ࠾ࠤᦦ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠣࠤᦧ"))
    def __11l1ll1111l_opy_(
        self,
        f: SeleniumFramework,
        driver: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ):
        instance, _ = exec
        if not instance.ref() in self.drivers:
            return
        self.bstack11l1llll11l_opy_(instance)
        self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡢࡣࡴࡴ࡟ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡴࡹ࡮ࡺ࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࠦᦨ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠥࠦᦩ"))
    def __11l1ll1llll_opy_(self, instance: AutomationFrameworkBrowser):
        try:
            bstack11l1ll11lll_opy_ = self.__11l1ll111ll_opy_(instance.context)
            owner = None
            if bstack11l1ll11lll_opy_ is not None and not self.__11l1ll1ll1l_opy_(bstack11l1ll11lll_opy_):
                owner = bstack11l1ll11lll_opy_.ref()
            bstack1l111l1l_opy_.set_state(instance, self.bstack11l1llll1ll_opy_, owner)
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡤࡥࡴࡢࡩࡢࡳࡼࡴࡥࡳࡡࡷࡩࡸࡺࠠࡧࡣ࡬ࡰࡪࡪࠠࡧࡱࡵࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡾ࠼ࠣࡿࢂࠨᦪ").format(instance.ref(), e))
    def __11l1ll111ll_opy_(self, context: bstack1l11ll1l1l1_opy_):
        try:
            from browserstack_sdk.sdk_cli.test_framework import TestFramework
            tests = TestFramework.get_context_instances(context, reverse=True)
            if tests:
                return tests[0]
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠧࡥ࡟ࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡩ࡯ࡵࡷࡥࡳࡩࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡨࡲࡶࠥࡩ࡯࡯ࡶࡨࡼࡹࡃࡻࡾ࠼ࠣࡿࢂࠨᦫ").format(context, e))
        return None
    def __11l1ll1l111_opy_(self, context: bstack1l11ll1l1l1_opy_):
        test = self.__11l1ll111ll_opy_(context)
        return test.ref() if test is not None else None
    def __11l1ll1ll1l_opy_(self, bstack11l1ll11lll_opy_) -> bool:
        try:
            from browserstack_sdk.sdk_cli.test_framework import TestFramework
            from browserstack_sdk.sdk_cli.bstack1l11l111l1l_opy_ import bstack1l1111ll11l_opy_
            fixtures = TestFramework.get_state(bstack11l1ll11lll_opy_, bstack1l1111ll11l_opy_.bstack11l1ll1l1ll_opy_, {}) or {}
            bstack11l1lll11l1_opy_ = None
            bstack11l1ll1lll1_opy_ = None
            for bstack11l1ll11ll1_opy_ in fixtures.values():
                if not isinstance(bstack11l1ll11ll1_opy_, dict):
                    continue
                started = bstack11l1ll11ll1_opy_.get(TestFramework.KEY_EVENT_STARTED_AT)
                bstack11l1ll111l1_opy_ = bstack11l1ll11ll1_opy_.get(TestFramework.KEY_EVENT_ENDED_AT)
                if started is not None and bstack11l1ll111l1_opy_ is None:
                    if bstack11l1ll1lll1_opy_ is None or started > bstack11l1ll1lll1_opy_:
                        bstack11l1ll1lll1_opy_ = started
                        bstack11l1lll11l1_opy_ = bstack11l1ll11ll1_opy_.get(bstack1l1llll_opy_ (u"ࠨࡳࡤࡱࡳࡩࠧ᦬"))
            return bstack11l1lll11l1_opy_ in self.bstack11l1ll11l1l_opy_
        except Exception as e:
            self.logger.debug(bstack1l1llll_opy_ (u"ࠢࡠࡡࡦࡶࡪࡧࡴࡦࡦࡢࡹࡳࡪࡥࡳࡡࡶ࡬ࡦࡸࡥࡥࡡࡩ࡭ࡽࡺࡵࡳࡧࠣࡪࡦ࡯࡬ࡦࡦ࠽ࠤࢀࢃࠢ᦭").format(e))
            return False
    def __11l1lll111l_opy_(self, instance: AutomationFrameworkBrowser, bstack11l1lll1111_opy_) -> bool:
        owner = bstack1l111l1l_opy_.get_state(instance, self.bstack11l1llll1ll_opy_, None)
        if owner is None or bstack11l1lll1111_opy_ is None:
            return True
        return owner == bstack11l1lll1111_opy_
    def bstack11l1lllll11_opy_(self, context: bstack1l11ll1l1l1_opy_):
        return self.__11l1ll1l111_opy_(context)
    def bstack11l1lll11ll_opy_(self, context: bstack1l11ll1l1l1_opy_, reverse=True, _11l1llll111_opy_=None) -> List[Tuple[Callable, AutomationFrameworkBrowser]]:
        matches = []
        bstack11l1lll1111_opy_ = _11l1llll111_opy_ if _11l1llll111_opy_ is not None else self.__11l1ll1l111_opy_(context)
        if self.pages:
            for data in self.pages.values():
                if data[1].bstack11l1lll1l1l_opy_(context) and self.__11l1lll111l_opy_(data[1], bstack11l1lll1111_opy_):
                    matches.append(data)
        if self.drivers:
            for data in self.drivers.values():
                if (
                    SeleniumFramework.bstack11l1ll1l11l_opy_(data[1])
                    and data[1].bstack11l1lll1l1l_opy_(context)
                    and getattr(data[0](), bstack1l1llll_opy_ (u"ࠣࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠧ᦮"), False)
                    and self.__11l1lll111l_opy_(data[1], bstack11l1lll1111_opy_)
                ):
                    matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l11ll11ll1_opy_, reverse=reverse)
    def bstack11l1lll1l11_opy_(self, context: bstack1l11ll1l1l1_opy_, reverse=True, _11l1llll111_opy_=None) -> List[Tuple[Callable, AutomationFrameworkBrowser]]:
        matches = []
        bstack11l1lll1111_opy_ = _11l1llll111_opy_ if _11l1llll111_opy_ is not None else self.__11l1ll1l111_opy_(context)
        for data in self.bstack11l1llll1l1_opy_.values():
            if (
                data[1].bstack11l1lll1l1l_opy_(context)
                and getattr(data[0](), bstack1l1llll_opy_ (u"ࠤࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩࠨ᦯"), False)
                and self.__11l1lll111l_opy_(data[1], bstack11l1lll1111_opy_)
            ):
                matches.append(data)
        return sorted(matches, key=lambda d: d[1].bstack1l11ll11ll1_opy_, reverse=reverse)
    def bstack11l1ll11l11_opy_(self, instance: AutomationFrameworkBrowser) -> bool:
        return instance and instance.ref() in self.drivers
    def bstack11l1llll11l_opy_(self, instance: AutomationFrameworkBrowser) -> bool:
        if self.bstack11l1ll11l11_opy_(instance):
            self.drivers.pop(instance.ref())
            bstack1l111l1l_opy_.set_state(instance, self.bstack11l1ll11111_opy_, False)
            return True
        return False