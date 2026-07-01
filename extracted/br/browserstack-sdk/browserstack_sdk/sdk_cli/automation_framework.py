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
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.tracked_instance import TrackedInstance, bstack1l11ll1l1l1_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class HookState(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1llll_opy_ (u"ࠢࡉࡱࡲ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨᛀ").format(self.name)
class AutomationFrameworkState(Enum):
    NONE = 0
    CREATE = 1
    bstack1l11llll1l1_opy_ = 3
    EXECUTE = 4
    bstack1l11lll1l11_opy_ = 5
    QUIT = 6
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.value == other.value
        return NotImplemented
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
    def __repr__(self) -> str:
        return bstack1l1llll_opy_ (u"ࠣࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣᛁ").format(self.name)
class AutomationFrameworkBrowser(TrackedInstance):
    framework_name: str
    framework_version: str
    state: AutomationFrameworkState
    previous_state: AutomationFrameworkState
    bstack1l11ll11ll1_opy_: datetime
    bstack1l11ll1111l_opy_: datetime
    def __init__(
        self,
        context: bstack1l11ll1l1l1_opy_,
        framework_name: str,
        framework_version: str,
        state=AutomationFrameworkState.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = AutomationFrameworkState.NONE
        self.bstack1l11ll11ll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1l11ll1111l_opy_ = datetime.now(tz=timezone.utc)
    def set_state(self, bstack1l11l1llll1_opy_: AutomationFrameworkState):
        bstack1l11ll11111_opy_ = AutomationFrameworkState(bstack1l11l1llll1_opy_).name
        if not bstack1l11ll11111_opy_:
            return False
        if bstack1l11l1llll1_opy_ == self.state:
            return False
        if self.state == AutomationFrameworkState.bstack1l11llll1l1_opy_: # bstack1l11l1lll1l_opy_ bstack1l11llll1ll_opy_ for bstack1l11lll1lll_opy_ in Playwright, it bstack1l11lll1ll1_opy_ called bstack1l11ll1lll1_opy_ times bstack1l11ll111ll_opy_ a new state
            return True
        if (
            bstack1l11l1llll1_opy_ == AutomationFrameworkState.NONE
            or (self.state != AutomationFrameworkState.NONE and bstack1l11l1llll1_opy_ == AutomationFrameworkState.CREATE)
            or (self.state < AutomationFrameworkState.CREATE and bstack1l11l1llll1_opy_ == AutomationFrameworkState.EXECUTE)
            or (self.state < AutomationFrameworkState.CREATE and bstack1l11l1llll1_opy_ == AutomationFrameworkState.QUIT)
        ):
            raise ValueError(bstack1l1llll_opy_ (u"ࠤ࡬ࡲࡻࡧ࡬ࡪࡦࠣࡷࡹࡧࡴࡦࠢࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࠣᛂ") + str(self.state) + bstack1l1llll_opy_ (u"ࠥࠤࡂࡄࠠࠣᛃ") + str(bstack1l11l1llll1_opy_))
        self.previous_state = self.state
        self.state = bstack1l11l1llll1_opy_
        self.bstack1l11ll1111l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1l111l1l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    instances: Dict[str, AutomationFrameworkBrowser] = dict()
    framework_name: str
    framework_version: str
    classes: List[Type]
    def __init__(
        self,
        framework_name: str,
        framework_version: str,
        classes: List[Type],
    ):
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.classes = classes
    @abc.abstractmethod
    def bstack1l11ll1l111_opy_(self, instance: AutomationFrameworkBrowser, method_name: str, bstack1l11ll11l1l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1l11ll1ll1l_opy_(
        self, method_name, previous_state: AutomationFrameworkState, *args, **kwargs
    ) -> AutomationFrameworkState:
        return
    @abc.abstractmethod
    def bstack1l1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[AutomationFrameworkBrowser, str],
        hook_info: Tuple[AutomationFrameworkState, HookState],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1l11lll11l1_opy_(self, bstack1l11ll11l11_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1l11ll11l11_opy_:
                bstack1l11ll1ll11_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1l11ll1ll11_opy_):
                    if not os.environ.get(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡇࡑࡏ࡟ࡉࡑࡒࡏࡘ࠭ᛄ")):
                        self.logger.warning(bstack1l1llll_opy_ (u"ࠧࡻ࡮ࡱࡣࡷࡧ࡭࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤ࠻ࠢࠥᛅ") + str(method_name) + bstack1l1llll_opy_ (u"ࠨࠢᛆ"))
                    continue
                bstack1l11llll11l_opy_ = self.bstack1l11ll1ll1l_opy_(
                    method_name, previous_state=AutomationFrameworkState.NONE
                )
                bstack1l11ll11lll_opy_ = self.bstack1l11llll111_opy_(
                    method_name,
                    (bstack1l11llll11l_opy_ if bstack1l11llll11l_opy_ else AutomationFrameworkState.NONE),
                    bstack1l11ll1ll11_opy_,
                )
                if not callable(bstack1l11ll11lll_opy_):
                    self.logger.warning(bstack1l1llll_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠠ࡯ࡱࡷࠤࡵࡧࡴࡤࡪࡨࡨ࠿ࠦࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࠨࡼࡵࡨࡰ࡫࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࡽ࠻ࠢࠥᛇ") + str(self.framework_version) + bstack1l1llll_opy_ (u"ࠣࠫࠥᛈ"))
                    continue
                setattr(clazz, method_name, bstack1l11ll11lll_opy_)
    def bstack1l11llll111_opy_(
        self,
        method_name: str,
        bstack1l11llll11l_opy_: AutomationFrameworkState,
        bstack1l11ll1ll11_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            time_start = datetime.now()
            (bstack1l11llll11l_opy_,) = wrapped.__vars__
            bstack1l11llll11l_opy_ = (
                bstack1l11llll11l_opy_
                if bstack1l11llll11l_opy_ and bstack1l11llll11l_opy_ != AutomationFrameworkState.NONE
                else self.bstack1l11ll1ll1l_opy_(method_name, previous_state=bstack1l11llll11l_opy_, *args, **kwargs)
            )
            if bstack1l11llll11l_opy_ == AutomationFrameworkState.CREATE:
                ctx = TrackedInstance.create_context(self.bstack1l11ll1l11l_opy_(target))
                if not self.bstack1l11ll1llll_opy_() or ctx.id not in bstack1l111l1l_opy_.instances:
                    bstack1l111l1l_opy_.instances[ctx.id] = AutomationFrameworkBrowser(
                        ctx, self.framework_name, self.framework_version, bstack1l11llll11l_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1l11lll1l1l_opy_ = None
                    if label:
                        if bstack1l1llll_opy_ (u"ࠤࠦࠦᛉ") in label:
                            suffix = label.rsplit(bstack1l1llll_opy_ (u"ࠥࠧࠧᛊ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1l11lll1l1l_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1l11lll11ll_opy_ (u"ࠦࡎࡴࡶࡢ࡮࡬ࡨࠥࡪࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯ࠤࡸࡻࡦࡧ࡫ࡻࠤࠬࢁࡳࡶࡨࡩ࡭ࡽࢃࠧࠡ࡫ࡱࠤࡱࡧࡢࡦ࡮ࠣࠫࢀࡲࡡࡣࡧ࡯ࢁࠬࡁࠠࡦࡺࡳࡩࡨࡺࡥࡥࠢࡱࡹࡲ࡫ࡲࡪࡥࠣࡶࡦࡴ࡫࠯ࠤᛋ")
                                )
                        else:
                            self.logger.debug(
                                bstack1l11lll11ll_opy_ (u"ࠧࡊࡲࡪࡸࡨࡶࠥࡲࡡࡣࡧ࡯ࠤࠬࢁ࡬ࡢࡤࡨࡰࢂ࠭ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡦࡳࡳࡺࡡࡪࡰࠣࠫࠨ࠭࠻ࠡࡵ࡮࡭ࡵࡶࡩ࡯ࡩࠣࡶࡦࡴ࡫ࠡࡣࡶࡷ࡮࡭࡮࡮ࡧࡱࡸ࠳ࠨᛌ")
                            )
                    self.logger.debug(bstack1l1llll_opy_ (u"ࠨࡣࡳࡧࡤࡸࡪࡪࠠ࡯ࡧࡺࠤࡹࡸࡡࡤ࡭ࡨࡨࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢࡵࡥࡳࡱ࠽ࡼࡴࡤࡲࡰࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᛍ") + str(bstack1l111l1l_opy_.instances.keys()) + bstack1l1llll_opy_ (u"ࠢࠣᛎ"))
                    bstack1l11lll111l_opy_ = bstack1l111l1l_opy_.get_tracked_instance(self.bstack1l11ll1l11l_opy_(target))
                    bstack1l11lll111l_opy_.data[bstack1l1llll_opy_ (u"ࠨࡴࡤࡲࡰ࠭ᛏ")] = bstack1l11lll1l1l_opy_
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡧࡷ࡫ࡡࡵࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥᛐ") + str(bstack1l111l1l_opy_.instances.keys()) + bstack1l1llll_opy_ (u"ࠥࠦᛑ"))
            else:
                self.logger.debug(bstack1l1llll_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥ࡯࡮ࡷࡱ࡮ࡩࡩࡀࠠࡼࡶࡤࡶ࡬࡫ࡴ࠯ࡡࡢࡧࡱࡧࡳࡴࡡࡢࢁࠥࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࡀࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࡂࢁࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᛒ") + str(bstack1l111l1l_opy_.instances.keys()) + bstack1l1llll_opy_ (u"ࠧࠨᛓ"))
            instance = bstack1l111l1l_opy_.get_tracked_instance(self.bstack1l11ll1l11l_opy_(target))
            if bstack1l11llll11l_opy_ == AutomationFrameworkState.NONE or not instance:
                ctx = TrackedInstance.create_context(self.bstack1l11ll1l11l_opy_(target))
                if not os.environ.get(bstack1l1llll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡉࡌࡊࡡࡋࡓࡔࡑࡓࠨᛔ")):
                    self.logger.warning(bstack1l1llll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡷࡱࡸࡷࡧࡣ࡬ࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦᛕ") + str(bstack1l111l1l_opy_.instances.keys()) + bstack1l1llll_opy_ (u"ࠣࠤᛖ"))
                return bstack1l11ll1ll11_opy_(target, *args, **kwargs)
            bstack1l11ll1l1ll_opy_ = self.bstack1l1lll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1l11llll11l_opy_, HookState.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.set_state(bstack1l11llll11l_opy_):
                self.logger.debug(bstack1l1llll_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠣࡷࡹࡧࡴࡦ࠯ࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡴࡷ࡫ࡶࡪࡱࡸࡷࡤࡹࡴࡢࡶࡨࢁࠥࡃ࠾ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡸࡺࡡࡵࡧࢀࠤ࠭ࢁࡴࡺࡲࡨࠬࡹࡧࡲࡨࡧࡷ࠭ࢂ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡻࡢࡴࡪࡷࢂ࠯ࠠ࡜ࠤᛗ") + str(instance.ref()) + bstack1l1llll_opy_ (u"ࠥࡡࠧᛘ"))
            result = (
                bstack1l11ll1l1ll_opy_(target, bstack1l11ll1ll11_opy_, *args, **kwargs)
                if callable(bstack1l11ll1l1ll_opy_)
                else bstack1l11ll1ll11_opy_(target, *args, **kwargs)
            )
            bstack1l11l1lllll_opy_ = self.bstack1l1lll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1l11llll11l_opy_, HookState.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1l11ll1l111_opy_(instance, method_name, datetime.now() - time_start, *args, **kwargs)
            return bstack1l11l1lllll_opy_ if bstack1l11l1lllll_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1l11llll11l_opy_,)
        return wrapped
    @staticmethod
    def get_tracked_instance(target: object, strict=True):
        ctx = TrackedInstance.create_context(target)
        instance = bstack1l111l1l_opy_.instances.get(ctx.id, None)
        if instance and instance.bstack1l11ll111l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def get_context_instances(
        ctx: bstack1l11ll1l1l1_opy_, state: AutomationFrameworkState, reverse=True
    ) -> List[AutomationFrameworkBrowser]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1l111l1l_opy_.instances.values(),
            ),
            key=lambda t: t.bstack1l11ll11ll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def has_state(instance: AutomationFrameworkBrowser, key: str):
        return instance and key in instance.data
    @staticmethod
    def get_state(instance: AutomationFrameworkBrowser, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def set_state(instance: AutomationFrameworkBrowser, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1l111l1l_opy_.logger.debug(bstack1l1llll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤᛙ") + str(value) + bstack1l1llll_opy_ (u"ࠧࠨᛚ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1l111l1l_opy_.get_tracked_instance(target, strict)
        return bstack1l111l1l_opy_.get_state(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1l111l1l_opy_.get_tracked_instance(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1l11ll1llll_opy_(self):
        return self.framework_name == bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪᛛ")
    def bstack1l11ll1l11l_opy_(self, target):
        return target if not self.bstack1l11ll1llll_opy_() else self.bstack1l11lll1111_opy_()
    @staticmethod
    def bstack1l11lll1111_opy_():
        return str(os.getpid()) + str(threading.get_ident())