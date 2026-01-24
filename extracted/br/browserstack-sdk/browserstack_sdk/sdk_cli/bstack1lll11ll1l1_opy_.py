# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1lll1lll11l_opy_ import bstack1lll1l1llll_opy_, bstack1lll11lll11_opy_
import os
import threading
class bstack1lll1l1ll1l_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1l1111_opy_ (u"ࠦࡍࡵ࡯࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥᄷ").format(self.name)
class bstack1lll111lll1_opy_(Enum):
    NONE = 0
    bstack1lll1l1l1l1_opy_ = 1
    bstack1lll1l111ll_opy_ = 3
    bstack1lll11l11l1_opy_ = 4
    bstack1lll1ll1111_opy_ = 5
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
        return bstack1l1111_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡗࡹࡧࡴࡦ࠰ࡾࢁࠧᄸ").format(self.name)
class bstack1lll1l1111l_opy_(bstack1lll1l1llll_opy_):
    framework_name: str
    framework_version: str
    state: bstack1lll111lll1_opy_
    previous_state: bstack1lll111lll1_opy_
    bstack1lll1lll111_opy_: datetime
    bstack1lll11l1111_opy_: datetime
    def __init__(
        self,
        context: bstack1lll11lll11_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1lll111lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1lll111lll1_opy_.NONE
        self.bstack1lll1lll111_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1lll11l1111_opy_ = datetime.now(tz=timezone.utc)
    def bstack1lll11l1ll1_opy_(self, bstack1lll11l111l_opy_: bstack1lll111lll1_opy_):
        bstack1lll1l1l111_opy_ = bstack1lll111lll1_opy_(bstack1lll11l111l_opy_).name
        if not bstack1lll1l1l111_opy_:
            return False
        if bstack1lll11l111l_opy_ == self.state:
            return False
        if self.state == bstack1lll111lll1_opy_.bstack1lll1l111ll_opy_: # bstack1lll1ll11ll_opy_ bstack1lll1l1ll11_opy_ for bstack1lll1l11ll1_opy_ in bstack1lll1l111l1_opy_, it bstack1lll1l11l1l_opy_ bstack1lll1l1l11l_opy_ bstack1lll1l11l11_opy_ times bstack1lll11ll11l_opy_ a new state
            return True
        if (
            bstack1lll11l111l_opy_ == bstack1lll111lll1_opy_.NONE
            or (self.state != bstack1lll111lll1_opy_.NONE and bstack1lll11l111l_opy_ == bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_)
            or (self.state < bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_ and bstack1lll11l111l_opy_ == bstack1lll111lll1_opy_.bstack1lll11l11l1_opy_)
            or (self.state < bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_ and bstack1lll11l111l_opy_ == bstack1lll111lll1_opy_.QUIT)
        ):
            raise ValueError(bstack1l1111_opy_ (u"ࠨࡩ࡯ࡸࡤࡰ࡮ࡪࠠࡴࡶࡤࡸࡪࠦࡴࡳࡣࡱࡷ࡮ࡺࡩࡰࡰ࠽ࠤࠧᄹ") + str(self.state) + bstack1l1111_opy_ (u"ࠢࠡ࠿ࡁࠤࠧᄺ") + str(bstack1lll11l111l_opy_))
        self.previous_state = self.state
        self.state = bstack1lll11l111l_opy_
        self.bstack1lll11l1111_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack1lll1ll1l1l_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lll11ll1ll_opy_: Dict[str, bstack1lll1l1111l_opy_] = dict()
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
    def bstack1lll1ll111l_opy_(self, instance: bstack1lll1l1111l_opy_, method_name: str, bstack1lll11ll111_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1lll1l1lll1_opy_(
        self, method_name, previous_state: bstack1lll111lll1_opy_, *args, **kwargs
    ) -> bstack1lll111lll1_opy_:
        return
    @abc.abstractmethod
    def bstack1lll11l11ll_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lll1l1111l_opy_, str],
        bstack1lll111llll_opy_: Tuple[bstack1lll111lll1_opy_, bstack1lll1l1ll1l_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lll1ll1lll_opy_(self, bstack1lll11l1l1l_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1lll11l1l1l_opy_:
                bstack1lll111ll1l_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1lll111ll1l_opy_):
                    self.logger.warning(bstack1l1111_opy_ (u"ࠣࡷࡱࡴࡦࡺࡣࡩࡧࡧࠤࡲ࡫ࡴࡩࡱࡧ࠾ࠥࠨᄻ") + str(method_name) + bstack1l1111_opy_ (u"ࠤࠥᄼ"))
                    continue
                bstack1lll1lll1ll_opy_ = self.bstack1lll1l1lll1_opy_(
                    method_name, previous_state=bstack1lll111lll1_opy_.NONE
                )
                bstack1lll1ll1ll1_opy_ = self.bstack1lll11lllll_opy_(
                    method_name,
                    (bstack1lll1lll1ll_opy_ if bstack1lll1lll1ll_opy_ else bstack1lll111lll1_opy_.NONE),
                    bstack1lll111ll1l_opy_,
                )
                if not callable(bstack1lll1ll1ll1_opy_):
                    self.logger.warning(bstack1l1111_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠣࡲࡴࡺࠠࡱࡣࡷࡧ࡭࡫ࡤ࠻ࠢࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࠫࡿࡸ࡫࡬ࡧ࠰ࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࢀ࠾ࠥࠨᄽ") + str(self.framework_version) + bstack1l1111_opy_ (u"ࠦ࠮ࠨᄾ"))
                    continue
                setattr(clazz, method_name, bstack1lll1ll1ll1_opy_)
    def bstack1lll11lllll_opy_(
        self,
        method_name: str,
        bstack1lll1lll1ll_opy_: bstack1lll111lll1_opy_,
        bstack1lll111ll1l_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack1ll1lll11l_opy_ = datetime.now()
            (bstack1lll1lll1ll_opy_,) = wrapped.__vars__
            bstack1lll1lll1ll_opy_ = (
                bstack1lll1lll1ll_opy_
                if bstack1lll1lll1ll_opy_ and bstack1lll1lll1ll_opy_ != bstack1lll111lll1_opy_.NONE
                else self.bstack1lll1l1lll1_opy_(method_name, previous_state=bstack1lll1lll1ll_opy_, *args, **kwargs)
            )
            if bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.bstack1lll1l1l1l1_opy_:
                ctx = bstack1lll1l1llll_opy_.create_context(self.bstack1lll11llll1_opy_(target))
                if not self.bstack1lll1ll1l11_opy_() or ctx.id not in bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_:
                    bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_[ctx.id] = bstack1lll1l1111l_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1lll1lll1ll_opy_
                    )
                self.logger.debug(bstack1l1111_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡣࡳࡧࡤࡸࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣࡧࡹࡾ࠽ࡼࡥࡷࡼ࠳࡯ࡤࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᄿ") + str(bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_.keys()) + bstack1l1111_opy_ (u"ࠨࠢᅀ"))
            else:
                self.logger.debug(bstack1l1111_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡ࡫ࡱࡺࡴࡱࡥࡥ࠼ࠣࡿࡹࡧࡲࡨࡧࡷ࠲ࡤࡥࡣ࡭ࡣࡶࡷࡤࡥࡽࠡ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࡃࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡶࡸࡦࡺࡥ࠾ࡽࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࢁࠥ࡯࡮ࡴࡶࡤࡲࡨ࡫ࡳ࠾ࠤᅁ") + str(bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_.keys()) + bstack1l1111_opy_ (u"ࠣࠤᅂ"))
            instance = bstack1lll1ll1l1l_opy_.bstack1lll11l1lll_opy_(self.bstack1lll11llll1_opy_(target))
            if bstack1lll1lll1ll_opy_ == bstack1lll111lll1_opy_.NONE or not instance:
                ctx = bstack1lll1l1llll_opy_.create_context(self.bstack1lll11llll1_opy_(target))
                self.logger.warning(bstack1l1111_opy_ (u"ࠤࡺࡶࡦࡶࡰࡦࡦࠣࡱࡪࡺࡨࡰࡦࠣࡹࡳࡺࡲࡢࡥ࡮ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦ࠿ࡾࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡳࡵࡣࡷࡩࢂࠦࡣࡵࡺࡀࡿࡨࡺࡸࡾࠢ࡬ࡲࡸࡺࡡ࡯ࡥࡨࡷࡂࠨᅃ") + str(bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_.keys()) + bstack1l1111_opy_ (u"ࠥࠦᅄ"))
                return bstack1lll111ll1l_opy_(target, *args, **kwargs)
            bstack1lll1ll11l1_opy_ = self.bstack1lll11l11ll_opy_(
                target,
                (instance, method_name),
                (bstack1lll1lll1ll_opy_, bstack1lll1l1ll1l_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1lll11l1ll1_opy_(bstack1lll1lll1ll_opy_):
                self.logger.debug(bstack1l1111_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡨࡨࠥࡹࡴࡢࡶࡨ࠱ࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࡾ࡭ࡳࡹࡴࡢࡰࡦࡩ࠳ࡶࡲࡦࡸ࡬ࡳࡺࡹ࡟ࡴࡶࡤࡸࡪࢃࠠ࠾ࡀࠣࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡳࡵࡣࡷࡩࢂࠦࠨࡼࡶࡼࡴࡪ࠮ࡴࡢࡴࡪࡩࡹ࠯ࡽ࠯ࡽࡰࡩࡹ࡮࡯ࡥࡡࡱࡥࡲ࡫ࡽࠡࡽࡤࡶ࡬ࡹࡽࠪࠢ࡞ࠦᅅ") + str(instance.ref()) + bstack1l1111_opy_ (u"ࠧࡣࠢᅆ"))
            result = (
                bstack1lll1ll11l1_opy_(target, bstack1lll111ll1l_opy_, *args, **kwargs)
                if callable(bstack1lll1ll11l1_opy_)
                else bstack1lll111ll1l_opy_(target, *args, **kwargs)
            )
            bstack1lll11lll1l_opy_ = self.bstack1lll11l11ll_opy_(
                target,
                (instance, method_name),
                (bstack1lll1lll1ll_opy_, bstack1lll1l1ll1l_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1lll1ll111l_opy_(instance, method_name, datetime.now() - bstack1ll1lll11l_opy_, *args, **kwargs)
            return bstack1lll11lll1l_opy_ if bstack1lll11lll1l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1lll1lll1ll_opy_,)
        return wrapped
    @staticmethod
    def bstack1lll11l1lll_opy_(target: object, strict=True):
        ctx = bstack1lll1l1llll_opy_.create_context(target)
        instance = bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_.get(ctx.id, None)
        if instance and instance.bstack1lll1l1l1ll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1lll11l1l11_opy_(
        ctx: bstack1lll11lll11_opy_, state: bstack1lll111lll1_opy_, reverse=True
    ) -> List[bstack1lll1l1111l_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack1lll1ll1l1l_opy_.bstack1lll11ll1ll_opy_.values(),
            ),
            key=lambda t: t.bstack1lll1lll111_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lll1l11111_opy_(instance: bstack1lll1l1111l_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1lll1l11lll_opy_(instance: bstack1lll1l1111l_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1lll11l1ll1_opy_(instance: bstack1lll1l1111l_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack1lll1ll1l1l_opy_.logger.debug(bstack1l1111_opy_ (u"ࠨࡳࡦࡶࡢࡷࡹࡧࡴࡦ࠼ࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡂࢁࡩ࡯ࡵࡷࡥࡳࡩࡥ࠯ࡴࡨࡪ࠭࠯ࡽࠡ࡭ࡨࡽࡂࢁ࡫ࡦࡻࢀࠤࡻࡧ࡬ࡶࡧࡀࠦᅇ") + str(value) + bstack1l1111_opy_ (u"ࠢࠣᅈ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack1lll1ll1l1l_opy_.bstack1lll11l1lll_opy_(target, strict)
        return bstack1lll1ll1l1l_opy_.bstack1lll1l11lll_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack1lll1ll1l1l_opy_.bstack1lll11l1lll_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1lll1ll1l11_opy_(self):
        return self.framework_name == bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠬᅉ")
    def bstack1lll11llll1_opy_(self, target):
        return target if not self.bstack1lll1ll1l11_opy_() else self.bstack1lll1lll1l1_opy_()
    @staticmethod
    def bstack1lll1lll1l1_opy_():
        return str(os.getpid()) + str(threading.get_ident())