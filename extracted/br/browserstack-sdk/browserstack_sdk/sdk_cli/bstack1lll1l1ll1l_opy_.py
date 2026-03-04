# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1ll1lll11ll_opy_ import bstack1ll1ll1l1ll_opy_, bstack1ll1ll11lll_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1ll1llll111_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1lll1l_opy_ (u"ࠧࡎ࡯ࡰ࡭ࡖࡸࡦࡺࡥ࠯ࡽࢀࠦቐ").format(self.name)
class bstack1ll1l1l11ll_opy_(Enum):
    NONE = 0
    bstack1ll1lllll11_opy_ = 1
    bstack1ll1l1ll111_opy_ = 3
    bstack1ll1lll11l1_opy_ = 4
    bstack1ll1ll111ll_opy_ = 5
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
        return bstack1lll1l_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࡘࡺࡡࡵࡧ࠱ࡿࢂࠨቑ").format(self.name)
class bstack1ll1llll11l_opy_(bstack1ll1ll1l1ll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1ll1l1l11ll_opy_
    previous_state: bstack1ll1l1l11ll_opy_
    bstack1ll1lll1111_opy_: datetime
    bstack1ll1ll1lll1_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll11lll_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1ll1l1l11ll_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1ll1l1l11ll_opy_.NONE
        self.bstack1ll1lll1111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1l11lll_opy_(self, bstack1ll1l1ll1ll_opy_: bstack1ll1l1l11ll_opy_):
        bstack1ll1lll1lll_opy_ = bstack1ll1l1l11ll_opy_(bstack1ll1l1ll1ll_opy_).name
        if not bstack1ll1lll1lll_opy_:
            return False
        if bstack1ll1l1ll1ll_opy_ == self.state:
            return False
        if self.state == bstack1ll1l1l11ll_opy_.bstack1ll1l1ll111_opy_: # bstack1ll1ll11l11_opy_ bstack1ll1l1ll1l1_opy_ for bstack1ll1ll1llll_opy_ in bstack1ll1ll11l1l_opy_, it bstack1ll1lll111l_opy_ bstack1ll1ll111l1_opy_ bstack1ll1lll1l11_opy_ times bstack1ll1ll11ll1_opy_ a new state
            return True
        if (
            bstack1ll1l1ll1ll_opy_ == bstack1ll1l1l11ll_opy_.NONE
            or (self.state != bstack1ll1l1l11ll_opy_.NONE and bstack1ll1l1ll1ll_opy_ == bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_)
            or (self.state < bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_ and bstack1ll1l1ll1ll_opy_ == bstack1ll1l1l11ll_opy_.bstack1ll1lll11l1_opy_)
            or (self.state < bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_ and bstack1ll1l1ll1ll_opy_ == bstack1ll1l1l11ll_opy_.QUIT)
        ):
            raise ValueError(bstack1lll1l_opy_ (u"ࠢࡪࡰࡹࡥࡱ࡯ࡤࠡࡵࡷࡥࡹ࡫ࠠࡵࡴࡤࡲࡸ࡯ࡴࡪࡱࡱ࠾ࠥࠨቒ") + str(self.state) + bstack1lll1l_opy_ (u"ࠣࠢࡀࡂࠥࠨቓ") + str(bstack1ll1l1ll1ll_opy_))
        self.previous_state = self.state
        self.state = bstack1ll1l1ll1ll_opy_
        self.bstack1ll1ll1lll1_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1lll1111l11_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lll1l1111l_opy_: Dict[str, bstack1ll1llll11l_opy_] = dict()
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
    def bstack1ll1ll11111_opy_(self, instance: bstack1ll1llll11l_opy_, method_name: str, bstack1ll1l1l1l11_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll1lll1ll1_opy_(
        self, method_name, previous_state: bstack1ll1l1l11ll_opy_, *args, **kwargs
    ) -> bstack1ll1l1l11ll_opy_:
        return
    @abc.abstractmethod
    def bstack1ll1l1lllll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1llll11l_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1l1l11ll_opy_, bstack1ll1llll111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll1l1l1111_opy_(self, bstack1ll1l1lll11_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1ll1l1lll11_opy_:
                bstack1ll1ll1l111_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1ll1ll1l111_opy_):
                    self.logger.warning(bstack1lll1l_opy_ (u"ࠤࡸࡲࡵࡧࡴࡤࡪࡨࡨࠥࡳࡥࡵࡪࡲࡨ࠿ࠦࠢቔ") + str(method_name) + bstack1lll1l_opy_ (u"ࠥࠦቕ"))
                    continue
                bstack1ll1ll1ll11_opy_ = self.bstack1ll1lll1ll1_opy_(
                    method_name, previous_state=bstack1ll1l1l11ll_opy_.NONE
                )
                bstack1ll1ll1l1l1_opy_ = self.bstack1ll1ll1111l_opy_(
                    method_name,
                    (bstack1ll1ll1ll11_opy_ if bstack1ll1ll1ll11_opy_ else bstack1ll1l1l11ll_opy_.NONE),
                    bstack1ll1ll1l111_opy_,
                )
                if not callable(bstack1ll1ll1l1l1_opy_):
                    self.logger.warning(bstack1lll1l_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠤࡳࡵࡴࠡࡲࡤࡸࡨ࡮ࡥࡥ࠼ࠣࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࠬࢀࡹࡥ࡭ࡨ࠱ࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࢁ࠿ࠦࠢቖ") + str(self.framework_version) + bstack1lll1l_opy_ (u"ࠧ࠯ࠢ቗"))
                    continue
                setattr(clazz, method_name, bstack1ll1ll1l1l1_opy_)
    def bstack1ll1ll1111l_opy_(
        self,
        method_name: str,
        bstack1ll1ll1ll11_opy_: bstack1ll1l1l11ll_opy_,
        bstack1ll1ll1l111_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1l11ll1_opy_ = datetime.now()
            (bstack1ll1ll1ll11_opy_,) = wrapped.__vars__
            bstack1ll1ll1ll11_opy_ = (
                bstack1ll1ll1ll11_opy_
                if bstack1ll1ll1ll11_opy_ and bstack1ll1ll1ll11_opy_ != bstack1ll1l1l11ll_opy_.NONE
                else self.bstack1ll1lll1ll1_opy_(method_name, previous_state=bstack1ll1ll1ll11_opy_, *args, **kwargs)
            )
            if bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.bstack1ll1lllll11_opy_:
                ctx = bstack1ll1ll1l1ll_opy_.create_context(self.bstack1ll1ll1l11l_opy_(target))
                if not self.bstack1ll1l1llll1_opy_() or ctx.id not in bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_:
                    bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_[ctx.id] = bstack1ll1llll11l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1ll1ll1ll11_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1ll1l1l1lll_opy_ = None
                    if label:
                        if bstack1lll1l_opy_ (u"ࠨࠣࠣቘ") in label:
                            suffix = label.rsplit(bstack1lll1l_opy_ (u"ࠢࠤࠤ቙"), 1)[-1]
                            if suffix.isdigit():
                                bstack1ll1l1l1lll_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1ll1l1ll11l_opy_ (u"ࠣࡋࡱࡺࡦࡲࡩࡥࠢࡧࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬ࠡࡵࡸࡪ࡫࡯ࡸࠡࠩࡾࡷࡺ࡬ࡦࡪࡺࢀࠫࠥ࡯࡮ࠡ࡮ࡤࡦࡪࡲࠠࠨࡽ࡯ࡥࡧ࡫࡬ࡾࠩ࠾ࠤࡪࡾࡰࡦࡥࡷࡩࡩࠦ࡮ࡶ࡯ࡨࡶ࡮ࡩࠠࡳࡣࡱ࡯࠳ࠨቚ")
                                )
                        else:
                            self.logger.debug(
                                bstack1ll1l1ll11l_opy_ (u"ࠤࡇࡶ࡮ࡼࡥࡳࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡰࡦࡨࡥ࡭ࡿࠪࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡣࡰࡰࡷࡥ࡮ࡴࠠࠨࠥࠪ࠿ࠥࡹ࡫ࡪࡲࡳ࡭ࡳ࡭ࠠࡳࡣࡱ࡯ࠥࡧࡳࡴ࡫ࡪࡲࡲ࡫࡮ࡵ࠰ࠥቛ")
                            )
                    self.logger.debug(bstack1lll1l_opy_ (u"ࠥࡧࡷ࡫ࡡࡵࡧࡧࠤࡳ࡫ࡷࠡࡶࡵࡥࡨࡱࡥࡥࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹ࠰࡬ࡨࢂࠦࡲࡢࡰ࡮ࡁࢀࡸࡡ࡯࡭ࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣቜ") + str(bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.keys()) + bstack1lll1l_opy_ (u"ࠦࠧቝ"))
                    bstack1ll1l1l11l1_opy_ = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(self.bstack1ll1ll1l11l_opy_(target))
                    bstack1ll1l1l11l1_opy_.data[bstack1lll1l_opy_ (u"ࠬࡸࡡ࡯࡭ࠪ቞")] = bstack1ll1l1l1lll_opy_
                self.logger.debug(bstack1lll1l_opy_ (u"ࠨࡷࡳࡣࡳࡴࡪࡪࠠ࡮ࡧࡷ࡬ࡴࡪࠠࡤࡴࡨࡥࡹ࡫ࡤ࠻ࠢࡾࡸࡦࡸࡧࡦࡶ࠱ࡣࡤࡩ࡬ࡢࡵࡶࡣࡤࢃࠠ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࡂࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽ࠴ࡩࡥࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢ቟") + str(bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.keys()) + bstack1lll1l_opy_ (u"ࠢࠣበ"))
            else:
                self.logger.debug(bstack1lll1l_opy_ (u"ࠣࡹࡵࡥࡵࡶࡥࡥࠢࡰࡩࡹ࡮࡯ࡥࠢ࡬ࡲࡻࡵ࡫ࡦࡦ࠽ࠤࢀࡺࡡࡳࡩࡨࡸ࠳ࡥ࡟ࡤ࡮ࡤࡷࡸࡥ࡟ࡾࠢࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫࠽ࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡩ࡯ࡵࡷࡥࡳࡩࡥࡴ࠿ࠥቡ") + str(bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.keys()) + bstack1lll1l_opy_ (u"ࠤࠥቢ"))
            instance = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(self.bstack1ll1ll1l11l_opy_(target))
            if bstack1ll1ll1ll11_opy_ == bstack1ll1l1l11ll_opy_.NONE or not instance:
                ctx = bstack1ll1ll1l1ll_opy_.create_context(self.bstack1ll1ll1l11l_opy_(target))
                self.logger.warning(bstack1lll1l_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡺࡴࡴࡳࡣࡦ࡯ࡪࡪ࠺ࠡࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡤࡶࡻࡁࢀࡩࡴࡹࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢባ") + str(bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.keys()) + bstack1lll1l_opy_ (u"ࠦࠧቤ"))
                return bstack1ll1ll1l111_opy_(target, *args, **kwargs)
            bstack1ll1llll1ll_opy_ = self.bstack1ll1l1lllll_opy_(
                target,
                (instance, method_name),
                (bstack1ll1ll1ll11_opy_, bstack1ll1llll111_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lll1l11lll_opy_(bstack1ll1ll1ll11_opy_):
                self.logger.debug(bstack1lll1l_opy_ (u"ࠧࡧࡰࡱ࡮࡬ࡩࡩࠦࡳࡵࡣࡷࡩ࠲ࡺࡲࡢࡰࡶ࡭ࡹ࡯࡯࡯࠼ࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡰࡳࡧࡹ࡭ࡴࡻࡳࡠࡵࡷࡥࡹ࡫ࡽࠡ࠿ࡁࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡴࡶࡤࡸࡪࢃࠠࠩࡽࡷࡽࡵ࡫ࠨࡵࡣࡵ࡫ࡪࡺࠩࡾ࠰ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡾࡥࡷ࡭ࡳࡾࠫࠣ࡟ࠧብ") + str(instance.ref()) + bstack1lll1l_opy_ (u"ࠨ࡝ࠣቦ"))
            result = (
                bstack1ll1llll1ll_opy_(target, bstack1ll1ll1l111_opy_, *args, **kwargs)
                if callable(bstack1ll1llll1ll_opy_)
                else bstack1ll1ll1l111_opy_(target, *args, **kwargs)
            )
            bstack1ll1l1lll1l_opy_ = self.bstack1ll1l1lllll_opy_(
                target,
                (instance, method_name),
                (bstack1ll1ll1ll11_opy_, bstack1ll1llll111_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll1ll11111_opy_(instance, method_name, datetime.now() - bstack1l1l11ll1_opy_, *args, **kwargs)
            return bstack1ll1l1lll1l_opy_ if bstack1ll1l1lll1l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1ll1ll1ll11_opy_,)
        return wrapped
    @staticmethod
    def bstack1ll1l1l111l_opy_(target: object, strict=True):
        ctx = bstack1ll1ll1l1ll_opy_.create_context(target)
        instance = bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1llll1l1_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll1lll1l1l_opy_(
        ctx: bstack1ll1ll11lll_opy_, state: bstack1ll1l1l11ll_opy_, reverse=True
    ) -> List[bstack1ll1llll11l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1lll1111l11_opy_.bstack1lll1l1111l_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1lll1111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1l1l1l_opy_(instance: bstack1ll1llll11l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll111l1l1_opy_(instance: bstack1ll1llll11l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1l11lll_opy_(instance: bstack1ll1llll11l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1lll1111l11_opy_.logger.debug(bstack1lll1l_opy_ (u"ࠢࡴࡧࡷࡣࡸࡺࡡࡵࡧ࠽ࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡃࡻࡪࡰࡶࡸࡦࡴࡣࡦ࠰ࡵࡩ࡫࠮ࠩࡾࠢ࡮ࡩࡾࡃࡻ࡬ࡧࡼࢁࠥࡼࡡ࡭ࡷࡨࡁࠧቧ") + str(value) + bstack1lll1l_opy_ (u"ࠣࠤቨ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(target, strict)
        return bstack1lll1111l11_opy_.bstack1lll111l1l1_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1lll1111l11_opy_.bstack1ll1l1l111l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1ll1l1llll1_opy_(self):
        return self.framework_name == bstack1lll1l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ቩ")
    def bstack1ll1ll1l11l_opy_(self, target):
        return target if not self.bstack1ll1l1llll1_opy_() else self.bstack1ll1l1l1ll1_opy_()
    @staticmethod
    def bstack1ll1l1l1ll1_opy_():
        return str(os.getpid()) + str(threading.get_ident())