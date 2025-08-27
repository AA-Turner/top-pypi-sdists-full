# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import logging
from enum import Enum
from typing import Dict, Tuple, Callable, Type, List, Any
import abc
from datetime import datetime, timezone, timedelta
from browserstack_sdk.sdk_cli.bstack1111111l1l_opy_ import bstack1lllll1l111_opy_, bstack1111111ll1_opy_
import os
import threading
class bstack1llllll1111_opy_(Enum):
    PRE = 0
    POST = 1
    def __repr__(self) -> str:
        return bstack1111lll_opy_ (u"ࠤࡋࡳࡴࡱࡓࡵࡣࡷࡩ࠳ࢁࡽࠣ႔").format(self.name)
class bstack1lllll1lll1_opy_(Enum):
    NONE = 0
    bstack1lllll1l11l_opy_ = 1
    bstack1llllll11l1_opy_ = 3
    bstack1llll1llll1_opy_ = 4
    bstack1lllllll1ll_opy_ = 5
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
        return bstack1111lll_opy_ (u"ࠥࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡕࡷࡥࡹ࡫࠮ࡼࡿࠥ႕").format(self.name)
class bstack1lllll1ll11_opy_(bstack1lllll1l111_opy_):
    framework_name: str
    framework_version: str
    state: bstack1lllll1lll1_opy_
    previous_state: bstack1lllll1lll1_opy_
    bstack1llllllll1l_opy_: datetime
    bstack1llll1lll1l_opy_: datetime
    def __init__(
        self,
        context: bstack1111111ll1_opy_,
        framework_name: str,
        framework_version: str,
        state=bstack1lllll1lll1_opy_.NONE,
    ):
        super().__init__(context)
        self.framework_name = framework_name
        self.framework_version = framework_version
        self.state = state
        self.previous_state = bstack1lllll1lll1_opy_.NONE
        self.bstack1llllllll1l_opy_ = datetime.now(tz=timezone.utc)
        self.bstack1llll1lll1l_opy_ = datetime.now(tz=timezone.utc)
    def bstack1llllll1l1l_opy_(self, bstack1lllll11l1l_opy_: bstack1lllll1lll1_opy_):
        bstack1llllllll11_opy_ = bstack1lllll1lll1_opy_(bstack1lllll11l1l_opy_).name
        if not bstack1llllllll11_opy_:
            return False
        if bstack1lllll11l1l_opy_ == self.state:
            return False
        if self.state == bstack1lllll1lll1_opy_.bstack1llllll11l1_opy_: # bstack1111111l11_opy_ bstack1lllll111ll_opy_ for bstack1llll1ll1ll_opy_ in bstack1llll1ll1l1_opy_, it bstack1lllll111l1_opy_ bstack1lllllll1l1_opy_ bstack1lllllllll1_opy_ times bstack1lllll1ll1l_opy_ a new state
            return True
        if (
            bstack1lllll11l1l_opy_ == bstack1lllll1lll1_opy_.NONE
            or (self.state != bstack1lllll1lll1_opy_.NONE and bstack1lllll11l1l_opy_ == bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_)
            or (self.state < bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_ and bstack1lllll11l1l_opy_ == bstack1lllll1lll1_opy_.bstack1llll1llll1_opy_)
            or (self.state < bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_ and bstack1lllll11l1l_opy_ == bstack1lllll1lll1_opy_.QUIT)
        ):
            raise ValueError(bstack1111lll_opy_ (u"ࠦ࡮ࡴࡶࡢ࡮࡬ࡨࠥࡹࡴࡢࡶࡨࠤࡹࡸࡡ࡯ࡵ࡬ࡸ࡮ࡵ࡮࠻ࠢࠥ႖") + str(self.state) + bstack1111lll_opy_ (u"ࠧࠦ࠽࠿ࠢࠥ႗") + str(bstack1lllll11l1l_opy_))
        self.previous_state = self.state
        self.state = bstack1lllll11l1l_opy_
        self.bstack1llll1lll1l_opy_ = datetime.now(tz=timezone.utc)
        return True
class bstack11111111l1_opy_(abc.ABC):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    bstack1lllllll11l_opy_: Dict[str, bstack1lllll1ll11_opy_] = dict()
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
    def bstack1111111111_opy_(self, instance: bstack1lllll1ll11_opy_, method_name: str, bstack1llll1lllll_opy_: timedelta, *args, **kwargs):
        return
    @abc.abstractmethod
    def bstack1llllllllll_opy_(
        self, method_name, previous_state: bstack1lllll1lll1_opy_, *args, **kwargs
    ) -> bstack1lllll1lll1_opy_:
        return
    @abc.abstractmethod
    def bstack1llllll111l_opy_(
        self,
        target: object,
        exec: Tuple[bstack1lllll1ll11_opy_, str],
        bstack1llllll11ll_opy_: Tuple[bstack1lllll1lll1_opy_, bstack1llllll1111_opy_],
        result: Any,
        *args,
        **kwargs,
    ) -> Callable:
        return
    def bstack1lllll1l1l1_opy_(self, bstack1lllll11l11_opy_: List[str]):
        for clazz in self.classes:
            for method_name in bstack1lllll11l11_opy_:
                bstack1llllll1ll1_opy_ = getattr(clazz, method_name, None)
                if not callable(bstack1llllll1ll1_opy_):
                    self.logger.warning(bstack1111lll_opy_ (u"ࠨࡵ࡯ࡲࡤࡸࡨ࡮ࡥࡥࠢࡰࡩࡹ࡮࡯ࡥ࠼ࠣࠦ႘") + str(method_name) + bstack1111lll_opy_ (u"ࠢࠣ႙"))
                    continue
                bstack1llll1ll111_opy_ = self.bstack1llllllllll_opy_(
                    method_name, previous_state=bstack1lllll1lll1_opy_.NONE
                )
                bstack1lllll1l1ll_opy_ = self.bstack1lllllll111_opy_(
                    method_name,
                    (bstack1llll1ll111_opy_ if bstack1llll1ll111_opy_ else bstack1lllll1lll1_opy_.NONE),
                    bstack1llllll1ll1_opy_,
                )
                if not callable(bstack1lllll1l1ll_opy_):
                    self.logger.warning(bstack1111lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠡࡰࡲࡸࠥࡶࡡࡵࡥ࡫ࡩࡩࡀࠠࡼ࡯ࡨࡸ࡭ࡵࡤࡠࡰࡤࡱࡪࢃࠠࠩࡽࡶࡩࡱ࡬࠮ࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࡾ࠼ࠣࠦႚ") + str(self.framework_version) + bstack1111lll_opy_ (u"ࠤࠬࠦႛ"))
                    continue
                setattr(clazz, method_name, bstack1lllll1l1ll_opy_)
    def bstack1lllllll111_opy_(
        self,
        method_name: str,
        bstack1llll1ll111_opy_: bstack1lllll1lll1_opy_,
        bstack1llllll1ll1_opy_: Callable,
    ):
        def wrapped(target, *args, **kwargs):
            bstack11l1l1ll1l_opy_ = datetime.now()
            (bstack1llll1ll111_opy_,) = wrapped.__vars__
            bstack1llll1ll111_opy_ = (
                bstack1llll1ll111_opy_
                if bstack1llll1ll111_opy_ and bstack1llll1ll111_opy_ != bstack1lllll1lll1_opy_.NONE
                else self.bstack1llllllllll_opy_(method_name, previous_state=bstack1llll1ll111_opy_, *args, **kwargs)
            )
            if bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.bstack1lllll1l11l_opy_:
                ctx = bstack1lllll1l111_opy_.create_context(self.bstack11111111ll_opy_(target))
                if not self.bstack1llll1lll11_opy_() or ctx.id not in bstack11111111l1_opy_.bstack1lllllll11l_opy_:
                    bstack11111111l1_opy_.bstack1lllllll11l_opy_[ctx.id] = bstack1lllll1ll11_opy_(
                        ctx, self.framework_name, self.framework_version, bstack1llll1ll111_opy_
                    )
                self.logger.debug(bstack1111lll_opy_ (u"ࠥࡻࡷࡧࡰࡱࡧࡧࠤࡲ࡫ࡴࡩࡱࡧࠤࡨࡸࡥࡢࡶࡨࡨ࠿ࠦࡻࡵࡣࡵ࡫ࡪࡺ࠮ࡠࡡࡦࡰࡦࡹࡳࡠࡡࢀࠤࡲ࡫ࡴࡩࡱࡧࡣࡳࡧ࡭ࡦ࠿ࡾࡱࡪࡺࡨࡰࡦࡢࡲࡦࡳࡥࡾࠢࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡹࡴࡢࡶࡨࡁࢀ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫ࡽࠡࡥࡷࡼࡂࢁࡣࡵࡺ࠱࡭ࡩࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦႜ") + str(bstack11111111l1_opy_.bstack1lllllll11l_opy_.keys()) + bstack1111lll_opy_ (u"ࠦࠧႝ"))
            else:
                self.logger.debug(bstack1111lll_opy_ (u"ࠧࡽࡲࡢࡲࡳࡩࡩࠦ࡭ࡦࡶ࡫ࡳࡩࠦࡩ࡯ࡸࡲ࡯ࡪࡪ࠺ࠡࡽࡷࡥࡷ࡭ࡥࡵ࠰ࡢࡣࡨࡲࡡࡴࡵࡢࡣࢂࠦ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࡁࢀࡳࡥࡵࡪࡲࡨࡤࡴࡡ࡮ࡧࢀࠤ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡴࡶࡤࡸࡪࡃࡻࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡷࡹࡧࡴࡦࡿࠣ࡭ࡳࡹࡴࡢࡰࡦࡩࡸࡃࠢ႞") + str(bstack11111111l1_opy_.bstack1lllllll11l_opy_.keys()) + bstack1111lll_opy_ (u"ࠨࠢ႟"))
            instance = bstack11111111l1_opy_.bstack1lllll1111l_opy_(self.bstack11111111ll_opy_(target))
            if bstack1llll1ll111_opy_ == bstack1lllll1lll1_opy_.NONE or not instance:
                ctx = bstack1lllll1l111_opy_.create_context(self.bstack11111111ll_opy_(target))
                self.logger.warning(bstack1111lll_opy_ (u"ࠢࡸࡴࡤࡴࡵ࡫ࡤࠡ࡯ࡨࡸ࡭ࡵࡤࠡࡷࡱࡸࡷࡧࡣ࡬ࡧࡧ࠾ࠥࢁ࡭ࡦࡶ࡫ࡳࡩࡥ࡮ࡢ࡯ࡨࢁࠥ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡵࡷࡥࡹ࡫࠽ࡼࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡸࡺࡡࡵࡧࢀࠤࡨࡺࡸ࠾ࡽࡦࡸࡽࢃࠠࡪࡰࡶࡸࡦࡴࡣࡦࡵࡀࠦႠ") + str(bstack11111111l1_opy_.bstack1lllllll11l_opy_.keys()) + bstack1111lll_opy_ (u"ࠣࠤႡ"))
                return bstack1llllll1ll1_opy_(target, *args, **kwargs)
            bstack1lllll1llll_opy_ = self.bstack1llllll111l_opy_(
                target,
                (instance, method_name),
                (bstack1llll1ll111_opy_, bstack1llllll1111_opy_.PRE),
                None,
                *args,
                **kwargs,
            )
            if instance.bstack1llllll1l1l_opy_(bstack1llll1ll111_opy_):
                self.logger.debug(bstack1111lll_opy_ (u"ࠤࡤࡴࡵࡲࡩࡦࡦࠣࡷࡹࡧࡴࡦ࠯ࡷࡶࡦࡴࡳࡪࡶ࡬ࡳࡳࡀࠠࡼ࡫ࡱࡷࡹࡧ࡮ࡤࡧ࠱ࡴࡷ࡫ࡶࡪࡱࡸࡷࡤࡹࡴࡢࡶࡨࢁࠥࡃ࠾ࠡࡽ࡬ࡲࡸࡺࡡ࡯ࡥࡨ࠲ࡸࡺࡡࡵࡧࢀࠤ࠭ࢁࡴࡺࡲࡨࠬࡹࡧࡲࡨࡧࡷ࠭ࢂ࠴ࡻ࡮ࡧࡷ࡬ࡴࡪ࡟࡯ࡣࡰࡩࢂࠦࡻࡢࡴࡪࡷࢂ࠯ࠠ࡜ࠤႢ") + str(instance.ref()) + bstack1111lll_opy_ (u"ࠥࡡࠧႣ"))
            result = (
                bstack1lllll1llll_opy_(target, bstack1llllll1ll1_opy_, *args, **kwargs)
                if callable(bstack1lllll1llll_opy_)
                else bstack1llllll1ll1_opy_(target, *args, **kwargs)
            )
            bstack1llll1ll11l_opy_ = self.bstack1llllll111l_opy_(
                target,
                (instance, method_name),
                (bstack1llll1ll111_opy_, bstack1llllll1111_opy_.POST),
                result,
                *args,
                **kwargs,
            )
            self.bstack1111111111_opy_(instance, method_name, datetime.now() - bstack11l1l1ll1l_opy_, *args, **kwargs)
            return bstack1llll1ll11l_opy_ if bstack1llll1ll11l_opy_ else result
        wrapped.__name__ = method_name
        wrapped.__vars__ = (bstack1llll1ll111_opy_,)
        return wrapped
    @staticmethod
    def bstack1lllll1111l_opy_(target: object, strict=True):
        ctx = bstack1lllll1l111_opy_.create_context(target)
        instance = bstack11111111l1_opy_.bstack1lllllll11l_opy_.get(ctx.id, None)
        if instance and instance.bstack1lllll11lll_opy_(target):
            return instance
        return instance if instance and not strict else None
    @staticmethod
    def bstack1lllll11111_opy_(
        ctx: bstack1111111ll1_opy_, state: bstack1lllll1lll1_opy_, reverse=True
    ) -> List[bstack1lllll1ll11_opy_]:
        return sorted(
            filter(
                lambda t: t.state == state
                and t.context.thread_id == ctx.thread_id
                and t.context.process_id == ctx.process_id,
                bstack11111111l1_opy_.bstack1lllllll11l_opy_.values(),
            ),
            key=lambda t: t.bstack1llllllll1l_opy_,
            reverse=reverse,
        )
    @staticmethod
    def bstack1lllll11ll1_opy_(instance: bstack1lllll1ll11_opy_, key: str):
        return instance and key in instance.data
    @staticmethod
    def bstack1llllll1l11_opy_(instance: bstack1lllll1ll11_opy_, key: str, default_value=None):
        return instance.data.get(key, default_value) if instance else default_value
    @staticmethod
    def bstack1llllll1l1l_opy_(instance: bstack1lllll1ll11_opy_, key: str, value: Any) -> bool:
        instance.data[key] = value
        bstack11111111l1_opy_.logger.debug(bstack1111lll_opy_ (u"ࠦࡸ࡫ࡴࡠࡵࡷࡥࡹ࡫࠺ࠡ࡫ࡱࡷࡹࡧ࡮ࡤࡧࡀࡿ࡮ࡴࡳࡵࡣࡱࡧࡪ࠴ࡲࡦࡨࠫ࠭ࢂࠦ࡫ࡦࡻࡀࡿࡰ࡫ࡹࡾࠢࡹࡥࡱࡻࡥ࠾ࠤႤ") + str(value) + bstack1111lll_opy_ (u"ࠧࠨႥ"))
        return True
    @staticmethod
    def get_data(key: str, target: object, strict=True, default_value=None):
        instance = bstack11111111l1_opy_.bstack1lllll1111l_opy_(target, strict)
        return bstack11111111l1_opy_.bstack1llllll1l11_opy_(instance, key, default_value)
    @staticmethod
    def set_data(key: str, value: Any, target: object, strict=True):
        instance = bstack11111111l1_opy_.bstack1lllll1111l_opy_(target, strict)
        if not instance:
            return False
        instance.data[key] = value
        return True
    def bstack1llll1lll11_opy_(self):
        return self.framework_name == bstack1111lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠪႦ")
    def bstack11111111ll_opy_(self, target):
        return target if not self.bstack1llll1lll11_opy_() else self.bstack111111111l_opy_()
    @staticmethod
    def bstack111111111l_opy_():
        return str(os.getpid()) + str(threading.get_ident())