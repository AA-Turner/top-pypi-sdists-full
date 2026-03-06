# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1ll1ll111l1_opy_ import bstack1ll1llll1l1_opy_, bstack1ll1ll11l11_opy_
import os
import threading
from browserstack_sdk.browserstack_helper import BrowserStackHelper
class bstack1ll1l1lll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1111_opy_ (u"ࠨࡈࡰࡱ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧቑ").format(self.name)
class bstack1ll1lll1ll1_opy_(Enum):
    NONE = 0
    bstack1ll1l1l1111_opy_ = 1
    bstack1ll1ll1l11l_opy_ = 3
    bstack1ll1ll1l1l1_opy_ = 4
    bstack1ll1lll1lll_opy_ = 5
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
        return bstack1111_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡙ࡴࡢࡶࡨ࠲ࢀࢃࠢቒ").format(self.name)
class bstack1ll1ll1l111_opy_(bstack1ll1llll1l1_opy_):
    framework_name: str
    framework_version: str
    state: bstack1ll1lll1ll1_opy_
    previous_state: bstack1ll1lll1ll1_opy_
    bstack1ll1l1llll1_opy_: datetime
    bstack1ll1l1lll11_opy_: datetime
    def __init__(
        self,
        context: bstack1ll1ll11l11_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1ll1lll1ll1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1ll1lll1ll1_opy_.NONE
        self.bstack1ll1l1llll1_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1ll1l1lll11_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll1l11l1l_opy_(self, bstack1ll1lll111l_opy_: bstack1ll1lll1ll1_opy_):
        bstack1ll1lll1l1l_opy_ = bstack1ll1lll1ll1_opy_(bstack1ll1lll111l_opy_).name
        if not bstack1ll1lll1l1l_opy_:
            return False
        if bstack1ll1lll111l_opy_ == self.state:
            return False
        if self.state == bstack1ll1lll1ll1_opy_.bstack1ll1ll1l11l_opy_: # bstack1ll1l1ll111_opy_ bstack1ll1ll1l1ll_opy_ for bstack1ll1ll11111_opy_ in bstack1ll1ll111ll_opy_, it bstack1ll1ll1lll1_opy_ bstack1ll1lll1l11_opy_ bstack1ll1llll11l_opy_ times bstack1ll1lll11l1_opy_ a new state
            return True
        if (
            bstack1ll1lll111l_opy_ == bstack1ll1lll1ll1_opy_.NONE
            or (self.state != bstack1ll1lll1ll1_opy_.NONE and bstack1ll1lll111l_opy_ == bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_)
            or (self.state < bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_ and bstack1ll1lll111l_opy_ == bstack1ll1lll1ll1_opy_.bstack1ll1ll1l1l1_opy_)
            or (self.state < bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_ and bstack1ll1lll111l_opy_ == bstack1ll1lll1ll1_opy_.QUIT)
        ):
            raise ValueError(bstack1111_opy_ (u"ࠣ࡫ࡱࡺࡦࡲࡩࡥࠢࡶࡸࡦࡺࡥࠡࡶࡵࡥࡳࡹࡩࡵ࡫ࡲࡲ࠿ࠦࠢቓ") + str(self.state) + bstack1111_opy_ (u"ࠤࠣࡁࡃࠦࠢቔ") + str(bstack1ll1lll111l_opy_))
        self.previous_state = self.state
        self.state = bstack1ll1lll111l_opy_
        self.bstack1ll1l1lll11_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1lll11l1ll1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lll1111lll_opy_: Dict[str, bstack1ll1ll1l111_opy_] = dict()
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
    def bstack1ll1ll1111l_opy_(self, instance: bstack1ll1ll1l111_opy_, method_name: str, bstack1ll1ll11ll1_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1ll1l1ll1l1_opy_(
        self, method_name, previous_state: bstack1ll1lll1ll1_opy_, *args, **kwargs
    ) -> bstack1ll1lll1ll1_opy_:
        return
    @abc.abstractmethod
    def bstack1ll1lll11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1ll1ll1l111_opy_, str],
        bstack1ll1ll1ll1l_opy_: Tuple[bstack1ll1lll1ll1_opy_, bstack1ll1l1lll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1ll1llll111_opy_(self, bstack1ll1l1l1l1l_opy_: List[str]):
        if not self.classes or len(self.classes) == 0:
            return
        for clazz in self.classes:
            for method_name in bstack1ll1l1l1l1l_opy_:
                bstack1ll1l1l111l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1ll1l1l111l_opy_):
                    self.logger.warning(bstack1111_opy_ (u"ࠥࡹࡳࡶࡡࡵࡥ࡫ࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࡀࠠࠣቕ") + str(method_name) + bstack1111_opy_ (u"ࠦࠧቖ"))
                    continue
                bstack1ll1l11llll_opy_ = self.bstack1ll1l1ll1l1_opy_(
                    method_name, previous_state=bstack1ll1lll1ll1_opy_.NONE
                )
                bstack1ll1ll1llll_opy_ = self.bstack1ll1ll11l1l_opy_(
                    method_name,
                    (bstack1ll1l11llll_opy_ if bstack1ll1l11llll_opy_ else bstack1ll1lll1ll1_opy_.NONE),
                    bstack1ll1l1l111l_opy_,
                )
                if not callable(bstack1ll1ll1llll_opy_):
                    self.logger.warning(bstack1111_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠥࡴ࡯ࡵࠢࡳࡥࡹࡩࡨࡦࡦ࠽ࠤࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࠭ࢁࡳࡦ࡮ࡩ࠲࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࢂࡀࠠࠣ቗") + str(self.framework_version) + bstack1111_opy_ (u"ࠨࠩࠣቘ"))
                    continue
                setattr(clazz, method_name, bstack1ll1ll1llll_opy_)
    def bstack1ll1ll11l1l_opy_(
        self,
        method_name: str,
        bstack1ll1l11llll_opy_: bstack1ll1lll1ll1_opy_,
        bstack1ll1l1l111l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1l1llll111_opy_ = datetime.now()
            (bstack1ll1l11llll_opy_,) = wrapped.__vars__
            bstack1ll1l11llll_opy_ = (
                bstack1ll1l11llll_opy_
                if bstack1ll1l11llll_opy_ and bstack1ll1l11llll_opy_ != bstack1ll1lll1ll1_opy_.NONE
                else self.bstack1ll1l1ll1l1_opy_(method_name, previous_state=bstack1ll1l11llll_opy_, *args, **kwargs)
            )
            if bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.bstack1ll1l1l1111_opy_:
                ctx = bstack1ll1llll1l1_opy_.create_context(self.bstack1ll1l1lllll_opy_(target))
                if not self.bstack1ll1ll1ll11_opy_() or ctx.id not in bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_:
                    bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_[ctx.id] = bstack1ll1ll1l111_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1ll1l11llll_opy_
                    )
                    label = BrowserStackHelper.get_driver_label()
                    bstack1ll1l1l11ll_opy_ = None
                    if label:
                        if bstack1111_opy_ (u"ࠢࠤࠤ቙") in label:
                            suffix = label.rsplit(bstack1111_opy_ (u"ࠣࠥࠥቚ"), 1)[-1]
                            if suffix.isdigit():
                                bstack1ll1l1l11ll_opy_ = int(suffix)
                            else:
                                self.logger.debug(
                                    bstack1ll1l1l11l1_opy_ (u"ࠤࡌࡲࡻࡧ࡬ࡪࡦࠣࡨࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭ࠢࡶࡹ࡫࡬ࡩࡹࠢࠪࡿࡸࡻࡦࡧ࡫ࡻࢁࠬࠦࡩ࡯ࠢ࡯ࡥࡧ࡫࡬ࠡࠩࡾࡰࡦࡨࡥ࡭ࡿࠪ࠿ࠥ࡫ࡸࡱࡧࡦࡸࡪࡪࠠ࡯ࡷࡰࡩࡷ࡯ࡣࠡࡴࡤࡲࡰ࠴ࠢቛ")
                                )
                        else:
                            self.logger.debug(
                                bstack1ll1l1l11l1_opy_ (u"ࠥࡈࡷ࡯ࡶࡦࡴࠣࡰࡦࡨࡥ࡭ࠢࠪࡿࡱࡧࡢࡦ࡮ࢀࠫࠥࡪ࡯ࡦࡵࠣࡲࡴࡺࠠࡤࡱࡱࡸࡦ࡯࡮ࠡࠩࠦࠫࡀࠦࡳ࡬࡫ࡳࡴ࡮ࡴࡧࠡࡴࡤࡲࡰࠦࡡࡴࡵ࡬࡫ࡳࡳࡥ࡯ࡶ࠱ࠦቜ")
                            )
                    self.logger.debug(bstack1111_opy_ (u"ࠦࡨࡸࡥࡢࡶࡨࡨࠥࡴࡥࡸࠢࡷࡶࡦࡩ࡫ࡦࡦࠣ࡭ࡳࡹࡴࡢࡰࡦࡩ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡳࡣࡱ࡯ࡂࢁࡲࡢࡰ࡮ࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤቝ") + str(bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.keys()) + bstack1111_opy_ (u"ࠧࠨ቞"))
                    bstack1ll1ll11lll_opy_ = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(self.bstack1ll1l1lllll_opy_(target))
                    bstack1ll1ll11lll_opy_.data[bstack1111_opy_ (u"࠭ࡲࡢࡰ࡮ࠫ቟")] = bstack1ll1l1l11ll_opy_
                self.logger.debug(bstack1111_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡥࡵࡩࡦࡺࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥࡩࡴࡹ࠿ࡾࡧࡹࡾ࠮ࡪࡦࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣበ") + str(bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.keys()) + bstack1111_opy_ (u"ࠣࠤቡ"))
            else:
                self.logger.debug(bstack1111_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣ࡭ࡳࡼ࡯࡬ࡧࡧ࠾ࠥࢁࡴࡢࡴࡪࡩࡹ࠴࡟ࡠࡥ࡯ࡥࡸࡹ࡟ࡠࡿࠣࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥ࠾ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࡀࡿ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦቢ") + str(bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.keys()) + bstack1111_opy_ (u"ࠥࠦባ"))
            instance = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(self.bstack1ll1l1lllll_opy_(target))
            if bstack1ll1l11llll_opy_ == bstack1ll1lll1ll1_opy_.NONE or not instance:
                ctx = bstack1ll1llll1l1_opy_.create_context(self.bstack1ll1l1lllll_opy_(target))
                self.logger.warning(bstack1111_opy_ (u"ࠦࡼࡸࡡࡱࡲࡨࡨࠥࡳࡥࡵࡪࡲࡨࠥࡻ࡮ࡵࡴࡤࡧࡰ࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺࢀࠤ࡮ࡴࡳࡵࡣࡱࡧࡪࡹ࠽ࠣቤ") + str(bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.keys()) + bstack1111_opy_ (u"ࠧࠨብ"))
                return bstack1ll1l1l111l_opy_(target, *args, **kwargs)
            bstack1ll1lll1111_opy_ = self.bstack1ll1lll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1ll1l11llll_opy_, bstack1ll1l1lll1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lll1l11l1l_opy_(bstack1ll1l11llll_opy_):
                self.logger.debug(bstack1111_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡪࡪࠠࡴࡶࡤࡸࡪ࠳ࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࢀ࡯࡮ࡴࡶࡤࡲࡨ࡫࠮ࡱࡴࡨࡺ࡮ࡵࡵࡴࡡࡶࡸࡦࡺࡥࡾࠢࡀࡂࠥࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡵࡷࡥࡹ࡫ࡽࠡࠪࡾࡸࡾࡶࡥࠩࡶࡤࡶ࡬࡫ࡴࠪࡿ࠱ࡿࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦࡿࠣࡿࡦࡸࡧࡴࡿࠬࠤࡠࠨቦ") + str(instance.ref()) + bstack1111_opy_ (u"ࠢ࡞ࠤቧ"))
            result = (
                bstack1ll1lll1111_opy_(target, bstack1ll1l1l111l_opy_, *args, **kwargs)
                if callable(bstack1ll1lll1111_opy_)
                else bstack1ll1l1l111l_opy_(target, *args, **kwargs)
            )
            bstack1ll1l11lll1_opy_ = self.bstack1ll1lll11ll_opy_(
                target,
                (instance, method_name),
                (bstack1ll1l11llll_opy_, bstack1ll1l1lll1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1ll1ll1111l_opy_(instance, method_name, datetime.now() - bstack1l1llll111_opy_, *args, **kwargs)
            return bstack1ll1l11lll1_opy_ if bstack1ll1l11lll1_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1ll1l11llll_opy_,)
        return wrapped
    @staticmethod
    def bstack1ll1l1l1lll_opy_(target: object, strict=True):
        ctx = bstack1ll1llll1l1_opy_.create_context(target)
        instance = bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.get(ctx.id, None)
        if instance and instance.bstack1ll1l1l1l11_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1ll1l1ll11l_opy_(
        ctx: bstack1ll1ll11l11_opy_, state: bstack1ll1lll1ll1_opy_, reverse=True
    ) -> List[bstack1ll1ll1l111_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1lll11l1ll1_opy_.bstack1lll1111lll_opy_.values(),
            ),
            key=lambda t: t.bstack1ll1l1llll1_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1ll1l1l1ll1_opy_(instance: bstack1ll1ll1l111_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll1l11111_opy_(instance: bstack1ll1ll1l111_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll1l11l1l_opy_(instance: bstack1ll1ll1l111_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1lll11l1ll1_opy_.logger.debug(bstack1111_opy_ (u"ࠣࡵࡨࡸࡤࡹࡴࡢࡶࡨ࠾ࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫࠽ࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡶࡪ࡬ࠨࠪࡿࠣ࡯ࡪࡿ࠽ࡼ࡭ࡨࡽࢂࠦࡶࡢ࡮ࡸࡩࡂࠨቨ") + str(value) + bstack1111_opy_ (u"ࠤࠥቩ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(target, strict)
        return bstack1lll11l1ll1_opy_.bstack1lll1l11111_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1lll11l1ll1_opy_.bstack1ll1l1l1lll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1ll1ll1ll11_opy_(self):
        return self.framework_name == bstack1111_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧቪ")
    def bstack1ll1l1lllll_opy_(self, target):
        return target if not self.bstack1ll1ll1ll11_opy_() else self.bstack1ll1l1ll1ll_opy_()
    @staticmethod
    def bstack1ll1l1ll1ll_opy_():
        return str(os.getpid()) + str(threading.get_ident())