# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1ll1l111l11_opy_ import bstack1ll11ll1111_opy_, bstack1ll11lll1ll_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack11lllll11l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack11lll1_opy_ (u"ࠦࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥጚ").format(self.name)
class bstack111ll1lll1_opy_(Enum):
    NONE = 0
    bstack1l1111ll11_opy_ = 1
    bstack1ll11llll11_opy_ = 3
    bstack1ll1l11lll1_opy_ = 4
    bstack1ll11l11lll_opy_ = 5
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
        return bstack11lll1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧጛ").format(self.name)
class bstack1ll11llllll_opy_(bstack1ll11ll1111_opy_):
    framework_name: str
    framework_version: str
    state: bstack111ll1lll1_opy_
    previous_state: bstack111ll1lll1_opy_
    bstack1ll1l111l1l_opy_: datetime
    bstack1ll11l11111_opy_: datetime
    def __init__(
        self,
        context: bstack1ll11lll1ll_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack111ll1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack111ll1lll1_opy_.NONE
        self.bstack1ll1l111l1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll11l11111_opy_ = datetime.now(tz=timezone.utc)
    def bstack1ll1ll1l1l_opy_(self, bstack1ll11l111ll_opy_: bstack111ll1lll1_opy_):
        bstack1ll11lll111_opy_ = bstack111ll1lll1_opy_(bstack1ll11l111ll_opy_).name
        if not bstack1ll11lll111_opy_:
            return False
        if bstack1ll11l111ll_opy_ == self.state:
            return False
        if self.state == bstack111ll1lll1_opy_.bstack1ll11llll11_opy_: # bstack1ll11ll1l1l_opy_ bstack1ll1l1111l1_opy_ for bstack1ll11ll11ll_opy_ in Playwright, it bstack1ll11ll1l11_opy_ bstack1ll1l11111l_opy_ bstack1ll11l1ll1l_opy_ times bstack1ll11lll11l_opy_ a new state
            return True
        if (
            bstack1ll11l111ll_opy_ == bstack111ll1lll1_opy_.NONE
            or (self.state != bstack111ll1lll1_opy_.NONE and bstack1ll11l111ll_opy_ == bstack111ll1lll1_opy_.bstack1l1111ll11_opy_)
            or (self.state < bstack111ll1lll1_opy_.bstack1l1111ll11_opy_ and bstack1ll11l111ll_opy_ == bstack111ll1lll1_opy_.bstack1ll1l11lll1_opy_)
            or (self.state < bstack111ll1lll1_opy_.bstack1l1111ll11_opy_ and bstack1ll11l111ll_opy_ == bstack111ll1lll1_opy_.QUIT)
        ):
            raise ValueError(bstack11lll1_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡶࡤࡸࡪࠦࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࠧጜ") + str(self.state) + bstack11lll1_opy_ (u"ࠢࠡ࠿ࡁࠤࠧጝ") + str(bstack1ll11l111ll_opy_))
        self.previous_state = self.state
        self.state = bstack1ll11l111ll_opy_
        self.bstack1ll11l11111_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1l1lll1111_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack11l1lll111_opy_: Dict[str, bstack1ll11llllll_opy_] = dict()
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
    def bstack1ll11l1lll1_opy_(self, instance: bstack1ll11llllll_opy_, method_name: str, bstack1ll11ll111l_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll1l1111ll_opy_(
        self, method_name, previous_state: bstack111ll1lll1_opy_, *args, **kwargs
    ) -> bstack111ll1lll1_opy_:
        return
    @abc.abstractmethod
    def bstack1ll1ll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll11llllll_opy_, str],
        bstack1ll1l111111_opy_: Tuple[bstack111ll1lll1_opy_, bstack11lllll11l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll11ll11l1_opy_(self, bstack1ll11l111l1_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1ll11l111l1_opy_:
                bstack1ll11l1ll11_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1ll11l1ll11_opy_):
                    self.logger.warning(bstack11lll1_opy_ (u"ࠣࡷࡱࡴࡦࡺࡣࡩࡧࡧࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨጞ") + str(method_name) + bstack11lll1_opy_ (u"ࠤࠥጟ"))
                    continue
                bstack1ll11l1111l_opy_ = self.bstack1ll1l1111ll_opy_(
                    method_name, previous_state=bstack111ll1lll1_opy_.NONE
                )
                bstack1ll11l1l1ll_opy_ = self.bstack1ll11l1llll_opy_(
                    method_name,
                    (bstack1ll11l1111l_opy_ if bstack1ll11l1111l_opy_ else bstack111ll1lll1_opy_.NONE),
                    bstack1ll11l1ll11_opy_,
                )
                if not callable(bstack1ll11l1l1ll_opy_):
                    self.logger.warning(bstack11lll1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠣࡲࡴࡺࠠࡱࡣࡷࡧ࡭࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࠫࡿࡸ࡫࡬ࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨጠ") + str(self.framework_version) + bstack11lll1_opy_ (u"ࠦ࠮ࠨጡ"))
                    continue
                setattr(clazz, method_name, bstack1ll11l1l1ll_opy_)
    def bstack1ll11l1llll_opy_(
        self,
        method_name: str,
        bstack1ll11l1111l_opy_: bstack111ll1lll1_opy_,
        bstack1ll11l1ll11_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack111ll1l1_opy_ = datetime.now()
            (bstack1ll11l1111l_opy_,) = wrapped.__vars__
            bstack1ll11l1111l_opy_ = (
                bstack1ll11l1111l_opy_
                if bstack1ll11l1111l_opy_ and bstack1ll11l1111l_opy_ != bstack111ll1lll1_opy_.NONE
                else self.bstack1ll1l1111ll_opy_(method_name, previous_state=bstack1ll11l1111l_opy_, *args, **kwargs)
            )
            if bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.bstack1l1111ll11_opy_:
                ctx = bstack1ll11ll1111_opy_.create_context(self.bstack1ll11ll1lll_opy_(target))
                if not self.bstack1ll11l1l1l1_opy_() or ctx.id not in bstack1l1lll1111_opy_.bstack11l1lll111_opy_:
                    bstack1l1lll1111_opy_.bstack11l1lll111_opy_[ctx.id] = bstack1ll11llllll_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1ll11l1111l_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1ll11l11ll1_opy_ = None
                    if label:
                        if bstack11lll1_opy_ (u"ࠧࠩࠢጢ") in label:
                            suffix = label.rsplit(bstack11lll1_opy_ (u"ࠨࠣࠣጣ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1ll11l11ll1_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1ll11ll1ll1_opy_ (u"ࠢࡊࡰࡹࡥࡱ࡯ࡤࠡࡦࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࡴࡷࡩࡪ࡮ࡾࠠࠨࡽࡶࡹ࡫࡬ࡩࡹࡿࠪࠤ࡮ࡴࠠ࡭ࡣࡥࡩࡱࠦࠧࡼ࡮ࡤࡦࡪࡲࡽࠨ࠽ࠣࡩࡽࡶࡥࡤࡶࡨࡨࠥࡴࡵ࡮ࡧࡵ࡭ࡨࠦࡲࡢࡰ࡮࠲ࠧጤ")
                                )
                        else:
                            self.logger.debug(
                                bstack1ll11ll1ll1_opy_ (u"ࠣࡆࡵ࡭ࡻ࡫ࡲࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩࠣࡨࡴ࡫ࡳࠡࡰࡲࡸࠥࡩ࡯࡯ࡶࡤ࡭ࡳࠦࠧࠤࠩ࠾ࠤࡸࡱࡩࡱࡲ࡬ࡲ࡬ࠦࡲࡢࡰ࡮ࠤࡦࡹࡳࡪࡩࡱࡱࡪࡴࡴ࠯ࠤጥ")
                            )
                    self.logger.debug(bstack11lll1_opy_ (u"ࠤࡦࡶࡪࡧࡴࡦࡦࠣࡲࡪࡽࠠࡵࡴࡤࡧࡰ࡫ࡤࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸ࠯࡫ࡧࢁࠥࡸࡡ࡯࡭ࡀࡿࡷࡧ࡮࡬ࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢጦ") + str(bstack1l1lll1111_opy_.bstack11l1lll111_opy_.keys()) + bstack11lll1_opy_ (u"ࠥࠦጧ"))
                    bstack1ll11l1l11l_opy_ = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(self.bstack1ll11ll1lll_opy_(target))
                    bstack1ll11l1l11l_opy_.data[bstack11lll1_opy_ (u"ࠫࡷࡧ࡮࡬ࠩጨ")] = bstack1ll11l11ll1_opy_
                self.logger.debug(bstack11lll1_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨጩ") + str(bstack1l1lll1111_opy_.bstack11l1lll111_opy_.keys()) + bstack11lll1_opy_ (u"ࠨࠢጪ"))
            else:
                self.logger.debug(bstack11lll1_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡ࡫ࡱࡺࡴࡱࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤጫ") + str(bstack1l1lll1111_opy_.bstack11l1lll111_opy_.keys()) + bstack11lll1_opy_ (u"ࠣࠤጬ"))
            instance = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(self.bstack1ll11ll1lll_opy_(target))
            if bstack1ll11l1111l_opy_ == bstack111ll1lll1_opy_.NONE or not instance:
                ctx = bstack1ll11ll1111_opy_.create_context(self.bstack1ll11ll1lll_opy_(target))
                self.logger.warning(bstack11lll1_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡹࡳࡺࡲࡢࡥ࡮ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨጭ") + str(bstack1l1lll1111_opy_.bstack11l1lll111_opy_.keys()) + bstack11lll1_opy_ (u"ࠥࠦጮ"))
                return bstack1ll11l1ll11_opy_(target, *args, **kwargs)
            bstack1ll11l11l1l_opy_ = self.bstack1ll1ll111l_opy_(
                target,
                (instance, method_name),
                (bstack1ll11l1111l_opy_, bstack11lllll11l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1ll1ll1l1l_opy_(bstack1ll11l1111l_opy_):
                self.logger.debug(bstack11lll1_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠥࡹࡴࡢࡶࡨ࠱ࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡶࡲࡦࡸ࡬ࡳࡺࡹ࡟ࡴࡶࡤࡸࡪࢃࠠ࠾ࡀࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡳࡵࡣࡷࡩࢂࠦࠨࡼࡶࡼࡴࡪ࠮ࡴࡢࡴࡪࡩࡹ࠯ࡽ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡽࡤࡶ࡬ࡹࡽࠪࠢ࡞ࠦጯ") + str(instance.ref()) + bstack11lll1_opy_ (u"ࠧࡣࠢጰ"))
            result = (
                bstack1ll11l11l1l_opy_(target, bstack1ll11l1ll11_opy_, *args, **kwargs)
                if callable(bstack1ll11l11l1l_opy_)
                else bstack1ll11l1ll11_opy_(target, *args, **kwargs)
            )
            bstack1ll11l1l111_opy_ = self.bstack1ll1ll111l_opy_(
                target,
                (instance, method_name),
                (bstack1ll11l1111l_opy_, bstack11lllll11l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll11l1lll1_opy_(instance, method_name, datetime.now() - bstack111ll1l1_opy_, *args, **kwargs)
            return bstack1ll11l1l111_opy_ if bstack1ll11l1l111_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1ll11l1111l_opy_,)
        return wrapped
    @staticmethod
    def bstack1ll11l11l11_opy_(target: object, strict=True):
        ctx = bstack1ll11ll1111_opy_.create_context(target)
        instance = bstack1l1lll1111_opy_.bstack11l1lll111_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll11lll1l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll11lllll1_opy_(
        ctx: bstack1ll11lll1ll_opy_, state: bstack111ll1lll1_opy_, reverse=True
    ) -> List[bstack1ll11llllll_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1l1lll1111_opy_.bstack11l1lll111_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l111l1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1lll1l11_opy_(instance: bstack1ll11llllll_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1ll1l1l1111_opy_(instance: bstack1ll11llllll_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1ll1ll1l1l_opy_(instance: bstack1ll11llllll_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1l1lll1111_opy_.logger.debug(bstack11lll1_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡ࡭ࡨࡽࡂࢁ࡫ࡦࡻࢀࠤࡻࡧ࡬ࡶࡧࡀࠦጱ") + str(value) + bstack11lll1_opy_ (u"ࠢࠣጲ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(target, strict)
        return bstack1l1lll1111_opy_.bstack1ll1l1l1111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1l1lll1111_opy_.bstack1ll11l11l11_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1ll11l1l1l1_opy_(self):
        return self.framework_name == bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬጳ")
    def bstack1ll11ll1lll_opy_(self, target):
        return target if not self.bstack1ll11l1l1l1_opy_() else self.bstack1ll11llll1l_opy_()
    @staticmethod
    def bstack1ll11llll1l_opy_():
        return str(os.getpid()) + str(threading.get_ident())